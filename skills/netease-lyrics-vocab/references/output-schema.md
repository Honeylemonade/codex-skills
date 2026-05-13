# Output Schema

Use this schema for vocabulary study tables generated from NetEase playlist lyrics.

| Column | Meaning |
| --- | --- |
| `word` | Normalized lowercase English token. |
| `count` | Total occurrences across processed lyrics. |
| `meaning_zh` | Concise Chinese meaning, filled by Codex or the user after extraction. |
| `definition_en` | Optional short English definition fetched by the script. |
| `source_indexes` | Semicolon-separated source locations in `songNumber:lineNumber` form. |
| `source_examples` | Short lyric snippets showing representative uses. Do not store full lyrics. |
| `songs` | Semicolon-separated song titles where the word appears. |

Source index rules:

- `songNumber` is 1-based by playlist order after applying any `--max-songs` limit.
- `lineNumber` is 1-based within the cleaned lyric lines for that song.
- When a word appears many times, keep the first several indexes and examples. Counts remain complete.

Recommended sorting:

1. `count` descending.
2. `word` ascending for ties.
