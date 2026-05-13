---
name: netease-lyrics-vocab
description: Build vocabulary study tables and study websites from NetEase Cloud Music playlist lyrics. Use when the user provides a NetEase playlist URL or playlist ID and wants to fetch songs, collect lyrics, extract English words, count frequency, record source indexes by song and lyric line, add word meanings, export a CSV/XLSX table, or generate an interactive local vocabulary study page with word and example sentence pronunciation.
---

# NetEase Lyrics Vocab

Use this skill to turn a NetEase Cloud Music playlist into a vocabulary study table.

## Workflow

1. Identify the playlist ID from the user's URL or numeric ID.
2. Run `scripts/netease_lyrics_vocab.py` to fetch playlist tracks, fetch lyrics, tokenize English words, count frequency, and export the table.
3. Run `scripts/enrich_dictionary.py` to add built-in dictionary columns: phonetic, part of speech, Chinese meaning, Chinese explanation, English definition, root/affix, and memory note.
4. Inspect the generated table and fill or improve `meaning_zh` and `explanation_zh` for important words. Prefer concise Chinese meanings in the lyric context.
5. When the user wants a learning interface, run `scripts/build_vocab_site.py` against the enriched CSV/XLSX table to generate a static HTML study site.
6. Return the output file path and summarize coverage: songs processed, lyrics found, unique words, generated table, generated site, and any failures.

## Script

Run from the skill directory or pass the full script path:

```bash
python3 scripts/netease_lyrics_vocab.py "https://music.163.com/#/playlist?id=123456" --output vocab.csv
```

Useful options:

- `--format csv|xlsx`: Force output format. Defaults from the output extension.
- `--max-songs N`: Limit songs for a quick sample.
- `--min-count N`: Keep only words that appear at least N times.
- `--include-stopwords`: Keep common function words such as `the`, `and`, `you`.
- `--define english`: Try to add short English definitions from dictionaryapi.dev. Keep `meaning_zh` for Codex or the user to fill.

The script uses public NetEase web endpoints. These endpoints are unofficial and can change or rate-limit. If live fetching fails, ask the user for exported lyric files or a song list, then adapt the script input rather than inventing data.

## Dictionary Enrichment

Add built-in dictionary fields to the table before building the site:

```bash
python3 scripts/enrich_dictionary.py vocab.xlsx --output vocab.enriched.xlsx
```

The enrichment script reads and writes CSV/XLSX. It uses a small built-in Chinese meaning map for common words, local root/affix rules, and public English dictionary lookup for phonetics, part of speech, and English definitions. Use `--offline` to skip public dictionary lookup.

For high-quality Chinese explanations and deeper etymology, use the enriched table as the base and let Codex or another model fill `meaning_zh`, `explanation_zh`, `root_affix`, and `memory_note`; the study page embeds the completed values and works offline.

## Study Website

Generate a static learning page from a finished table:

```bash
python3 scripts/build_vocab_site.py vocab.xlsx --output vocab-study-site/index.html --title "歌词单词学习"
```

The generated page embeds the vocabulary and dictionary data and works as a local file. It provides:

- Search by word, meaning, definition, or song.
- Frequency filtering and known-word marking stored in browser local storage.
- Word cards with meaning, phonetic, part of speech, Chinese explanation, English definition, root/affix, memory note, source indexes, source examples, and songs.
- Browser speech synthesis buttons for the word and each example sentence. The page prefers English system voices and uses slower rates for clearer study playback.
- Deduplicated examples per word, so repeated lyric lines do not crowd the card while frequency counts remain complete.

For more natural voices, generate cached model-based MP3 files before building the page:

```bash
OPENAI_API_KEY=... python3 scripts/generate_tts_audio.py vocab.xlsx \
  --site-dir vocab-study-site \
  --voice cedar \
  --include-examples \
  --max-examples 3

python3 scripts/build_vocab_site.py vocab.xlsx \
  --output vocab-study-site/index.html \
  --audio-manifest vocab-study-site/audio_manifest.json
```

The page plays generated MP3 files first and falls back to browser speech synthesis if audio is missing. Show the AI-generated audio disclosure when sharing the page with others.

If the user asks for a shareable or portable result, return both the table and the generated `index.html`. Do not commit generated study pages unless the user explicitly wants examples stored in the repository.

## Output Columns

See `references/output-schema.md` for column definitions. Preserve these columns unless the user requests a different layout:

`word`, `count`, `phonetic`, `part_of_speech`, `meaning_zh`, `explanation_zh`, `definition_en`, `root_affix`, `memory_note`, `source_indexes`, `source_examples`, `source_songs`, `songs`.

## Meaning Rules

- Fill `meaning_zh` with compact Chinese meanings, not long dictionary entries.
- Use the lyric context where possible, especially for slang, contractions, idioms, and phrasal verbs.
- Leave ambiguous words with multiple likely meanings separated by semicolons.
- Do not output full lyrics. Keep only short snippets already produced by the script.

## Quality Checks

- Confirm the playlist ID and output path.
- Check that `count` is sorted descending.
- Spot-check several `source_indexes`, `source_examples`, and `source_songs` rows for one-to-one alignment.
- Report songs with missing lyrics or failed fetches.
