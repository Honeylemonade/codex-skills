---
name: netease-lyrics-vocab
description: Build vocabulary study tables from NetEase Cloud Music playlist lyrics. Use when the user provides a NetEase playlist URL or playlist ID and wants to fetch songs, collect lyrics, extract English words, count frequency, record source indexes by song and lyric line, add word meanings, and export a CSV or XLSX table for vocabulary learning.
---

# NetEase Lyrics Vocab

Use this skill to turn a NetEase Cloud Music playlist into a vocabulary study table.

## Workflow

1. Identify the playlist ID from the user's URL or numeric ID.
2. Run `scripts/netease_lyrics_vocab.py` to fetch playlist tracks, fetch lyrics, tokenize English words, count frequency, and export the table.
3. Inspect the generated table and fill or improve `meaning_zh` for important words. Prefer concise Chinese meanings in the lyric context.
4. Return the output file path and summarize coverage: songs processed, lyrics found, unique words, and any failures.

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

## Output Columns

See `references/output-schema.md` for column definitions. Preserve these columns unless the user requests a different layout:

`word`, `count`, `meaning_zh`, `definition_en`, `source_indexes`, `source_examples`, `songs`.

## Meaning Rules

- Fill `meaning_zh` with compact Chinese meanings, not long dictionary entries.
- Use the lyric context where possible, especially for slang, contractions, idioms, and phrasal verbs.
- Leave ambiguous words with multiple likely meanings separated by semicolons.
- Do not output full lyrics. Keep only short snippets already produced by the script.

## Quality Checks

- Confirm the playlist ID and output path.
- Check that `count` is sorted descending.
- Spot-check several `source_indexes` against `source_examples`.
- Report songs with missing lyrics or failed fetches.
