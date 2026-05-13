#!/usr/bin/env python3
"""Build a vocabulary table from NetEase Cloud Music playlist lyrics."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


PLAYLIST_ID_RE = re.compile(r"(?:playlist\?id=|[?&]id=|^)(\d{4,})")
LRC_TIME_RE = re.compile(r"\[[0-9]{1,2}:[0-9]{2}(?:\.[0-9]{1,3})?\]")
WORD_RE = re.compile(r"[A-Za-z]+(?:['-][A-Za-z]+)?")
CREDIT_KEYWORDS = (
    "作词", "作曲", "编曲", "制作人", "监制", "出品", "发行", "企划",
    "录音", "混音", "母带", "和声", "和音", "吉他", "贝斯", "鼓",
    "弦乐", "人声", "音频", "工程师", "工作室", "studio",
)

DEFAULT_STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "been", "but", "by", "can",
    "could", "do", "does", "for", "from", "had", "has", "have", "he", "her",
    "him", "his", "i", "if", "in", "is", "it", "its", "me", "my", "no",
    "not", "of", "on", "or", "our", "she", "so", "that", "the", "their",
    "them", "then", "there", "they", "this", "to", "was", "we", "were",
    "what", "when", "where", "who", "will", "with", "you", "your",
}


@dataclass
class Song:
    index: int
    song_id: int
    title: str
    artists: str = ""


@dataclass
class WordEntry:
    count: int = 0
    indexes: list[str] = field(default_factory=list)
    examples: list[str] = field(default_factory=list)
    songs: set[str] = field(default_factory=set)


def http_json(url: str, *, retries: int = 2, delay: float = 0.6) -> dict[str, Any]:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
        ),
        "Referer": "https://music.163.com/",
    }
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt < retries:
                time.sleep(delay * (attempt + 1))
    raise RuntimeError(f"Failed to fetch {url}: {last_error}") from last_error


def parse_playlist_id(value: str) -> str:
    match = PLAYLIST_ID_RE.search(value.strip())
    if not match:
        raise ValueError(f"Could not find a NetEase playlist id in: {value}")
    return match.group(1)


def fetch_playlist(playlist_id: str) -> tuple[str, list[Song]]:
    url = f"https://music.163.com/api/playlist/detail?id={playlist_id}"
    data = http_json(url)
    playlist = data.get("result") or data.get("playlist") or {}
    name = playlist.get("name") or f"playlist-{playlist_id}"
    tracks = playlist.get("tracks") or []
    songs: list[Song] = []
    for i, track in enumerate(tracks, start=1):
        artists = track.get("artists") or track.get("ar") or []
        artist_names = "; ".join(a.get("name", "") for a in artists if isinstance(a, dict))
        songs.append(Song(i, int(track["id"]), track.get("name", ""), artist_names))
    if songs:
        return name, songs

    track_ids = playlist.get("trackIds") or []
    ids = [str(item.get("id")) for item in track_ids if item.get("id")]
    if not ids:
        raise RuntimeError("Playlist did not include tracks or trackIds.")
    return name, fetch_song_details(ids)


def fetch_song_details(ids: list[str], batch_size: int = 200) -> list[Song]:
    songs: list[Song] = []
    for offset in range(0, len(ids), batch_size):
        batch = ids[offset : offset + batch_size]
        encoded = urllib.parse.quote(json.dumps([int(x) for x in batch], separators=(",", ":")))
        url = f"https://music.163.com/api/song/detail?ids={encoded}"
        data = http_json(url)
        for track in data.get("songs", []):
            artists = track.get("artists") or []
            artist_names = "; ".join(a.get("name", "") for a in artists if isinstance(a, dict))
            songs.append(Song(len(songs) + 1, int(track["id"]), track.get("name", ""), artist_names))
    return songs


def fetch_lyrics(song_id: int) -> str:
    url = f"https://music.163.com/api/song/lyric?id={song_id}&lv=1&kv=1&tv=-1"
    data = http_json(url)
    lyric = (data.get("lrc") or {}).get("lyric") or ""
    return lyric


def clean_lyric_lines(raw_lrc: str) -> list[str]:
    lines: list[str] = []
    for raw in raw_lrc.splitlines():
        line = LRC_TIME_RE.sub("", raw).strip()
        if not line:
            continue
        lower = line.lower()
        if lower.startswith(("translation:", "translated by")):
            continue
        if any(keyword in lower for keyword in CREDIT_KEYWORDS):
            continue
        lines.append(line)
    return lines


def normalize_word(token: str) -> str:
    word = token.lower().strip("'-")
    replacements = {
        "i'm": "i",
        "you're": "you",
        "we're": "we",
        "they're": "they",
        "it's": "it",
        "that's": "that",
    }
    return replacements.get(word, word)


def snippet_for(line: str, word: str, max_len: int = 90) -> str:
    compact = " ".join(line.split())
    if len(compact) <= max_len:
        return compact
    match = re.search(re.escape(word), compact, flags=re.IGNORECASE)
    if not match:
        return compact[: max_len - 3] + "..."
    start = max(0, match.start() - max_len // 2)
    end = min(len(compact), start + max_len)
    start = max(0, end - max_len)
    prefix = "..." if start else ""
    suffix = "..." if end < len(compact) else ""
    return prefix + compact[start:end] + suffix


def collect_words(
    songs: list[Song],
    *,
    include_stopwords: bool,
    max_examples: int,
    sleep_seconds: float,
) -> tuple[dict[str, WordEntry], list[str]]:
    entries: dict[str, WordEntry] = defaultdict(WordEntry)
    failures: list[str] = []
    stopwords = set() if include_stopwords else DEFAULT_STOPWORDS

    for song in songs:
        try:
            lyric = fetch_lyrics(song.song_id)
        except RuntimeError as exc:
            failures.append(f"{song.index}. {song.title} ({song.song_id}): {exc}")
            continue
        if not lyric:
            failures.append(f"{song.index}. {song.title} ({song.song_id}): no lyrics")
            continue
        for line_number, line in enumerate(clean_lyric_lines(lyric), start=1):
            seen_in_line: Counter[str] = Counter()
            for token in WORD_RE.findall(line):
                word = normalize_word(token)
                if not word or word in stopwords or len(word) < 2:
                    continue
                seen_in_line[word] += 1
            for word, amount in seen_in_line.items():
                entry = entries[word]
                entry.count += amount
                entry.songs.add(song.title)
                if len(entry.indexes) < max_examples:
                    entry.indexes.append(f"{song.index}:{line_number}")
                if len(entry.examples) < max_examples:
                    entry.examples.append(snippet_for(line, word))
        if sleep_seconds:
            time.sleep(sleep_seconds)
    return entries, failures


def fetch_english_definition(word: str) -> str:
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{urllib.parse.quote(word)}"
    try:
        data = http_json(url, retries=0)
    except RuntimeError:
        return ""
    if not isinstance(data, list) or not data:
        return ""
    meanings = data[0].get("meanings") or []
    for meaning in meanings:
        definitions = meaning.get("definitions") or []
        if definitions:
            return definitions[0].get("definition", "")[:240]
    return ""


def rows_from_entries(
    entries: dict[str, WordEntry],
    *,
    min_count: int,
    define: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for word, entry in sorted(entries.items(), key=lambda item: (-item[1].count, item[0])):
        if entry.count < min_count:
            continue
        definition = fetch_english_definition(word) if define == "english" else ""
        rows.append(
            {
                "word": word,
                "count": entry.count,
                "meaning_zh": "",
                "definition_en": definition,
                "source_indexes": "; ".join(entry.indexes),
                "source_examples": " | ".join(entry.examples),
                "songs": "; ".join(sorted(entry.songs)),
            }
        )
    return rows


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames = ["word", "count", "meaning_zh", "definition_en", "source_indexes", "source_examples", "songs"]
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_xlsx(path: Path, rows: list[dict[str, Any]]) -> None:
    try:
        from openpyxl import Workbook
        from openpyxl.styles import Font
    except ImportError as exc:
        raise RuntimeError("openpyxl is required for xlsx output; use --format csv instead.") from exc

    fieldnames = ["word", "count", "meaning_zh", "definition_en", "source_indexes", "source_examples", "songs"]
    wb = Workbook()
    ws = wb.active
    ws.title = "vocabulary"
    ws.append(fieldnames)
    for cell in ws[1]:
        cell.font = Font(bold=True)
    for row in rows:
        ws.append([row[name] for name in fieldnames])
    widths = {"A": 18, "B": 10, "C": 24, "D": 48, "E": 28, "F": 72, "G": 48}
    for col, width in widths.items():
        ws.column_dimensions[col].width = width
    ws.freeze_panes = "A2"
    wb.save(path)


def infer_format(path: Path, requested: str | None) -> str:
    if requested:
        return requested
    if path.suffix.lower() == ".xlsx":
        return "xlsx"
    return "csv"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("playlist", help="NetEase playlist URL or playlist ID")
    parser.add_argument("--output", default="netease_vocab.csv", help="Output CSV/XLSX path")
    parser.add_argument("--format", choices=["csv", "xlsx"], help="Output format")
    parser.add_argument("--max-songs", type=int, help="Process only the first N songs")
    parser.add_argument("--min-count", type=int, default=1, help="Minimum frequency to include")
    parser.add_argument("--include-stopwords", action="store_true", help="Keep common English stopwords")
    parser.add_argument("--max-examples", type=int, default=8, help="Maximum source indexes/examples per word")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between lyric requests")
    parser.add_argument("--define", choices=["none", "english"], default="none", help="Add optional English definitions")
    args = parser.parse_args(argv)

    playlist_id = parse_playlist_id(args.playlist)
    playlist_name, songs = fetch_playlist(playlist_id)
    if args.max_songs:
        songs = songs[: args.max_songs]
    if not songs:
        raise RuntimeError(f"No songs found for playlist {playlist_id}.")

    entries, failures = collect_words(
        songs,
        include_stopwords=args.include_stopwords,
        max_examples=args.max_examples,
        sleep_seconds=args.sleep,
    )
    rows = rows_from_entries(entries, min_count=args.min_count, define=args.define)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fmt = infer_format(output, args.format)
    if fmt == "xlsx":
        write_xlsx(output, rows)
    else:
        write_csv(output, rows)

    print(f"playlist_id={playlist_id}")
    print(f"playlist_name={playlist_name}")
    print(f"songs_processed={len(songs)}")
    print(f"unique_words={len(rows)}")
    print(f"output={output}")
    if failures:
        print("failures:")
        for item in failures[:20]:
            print(f"- {item}")
        if len(failures) > 20:
            print(f"- ... {len(failures) - 20} more")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
