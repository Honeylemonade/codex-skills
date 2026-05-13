# Output Schema

Use this schema for vocabulary study tables generated from NetEase playlist lyrics.

| Column | Meaning |
| --- | --- |
| `word` | Normalized lowercase English token. |
| `count` | Total occurrences across processed lyrics. |
| `phonetic` | IPA or dictionary phonetic form. |
| `part_of_speech` | Primary part of speech, such as noun, verb, adjective, adverb. |
| `meaning_zh` | Concise Chinese meaning, filled by Codex or the user after extraction. |
| `explanation_zh` | Chinese explanation tailored to the lyric context. |
| `definition_en` | Optional short English definition fetched by the script. |
| `root_affix` | Root, prefix, suffix, or morphology note when useful. |
| `memory_note` | Short learning hint or mnemonic. |
| `source_indexes` | Semicolon-separated source locations in `songNumber:lineNumber` form. |
| `source_examples` | Short lyric snippets showing representative uses. Do not store full lyrics. |
| `source_songs` | Pipe-separated song titles aligned one-to-one with `source_examples`. |
| `songs` | Semicolon-separated song titles where the word appears. |

Source index rules:

- `songNumber` is 1-based by playlist order after applying any `--max-songs` limit.
- `lineNumber` is 1-based within the cleaned lyric lines for that song.
- When a word appears many times, keep the first several unique examples, aligned indexes, and aligned song titles. Counts remain complete.

Recommended sorting:

1. `count` descending.
2. `word` ascending for ties.
