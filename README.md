# Hermes Agent Docs — Russian Translation 🇷🇺

[![Status](https://img.shields.io/badge/status-100%25%20translated-brightgreen)](https://hermes-agent.nousresearch.com/docs)

Full Russian translation of the [Hermes Agent](https://hermes-agent.nousresearch.com) documentation — an open-source CLI AI agent by Nous Research.

## What's Inside

- **293 pages** of documentation fully translated from English to Russian
- All original markdown files preserved in `originals/`
- All translations in `translated/` with identical directory structure
- `translation_state.json` — tracks translation progress
- `update_check.py` — checks for upstream doc changes and syncs new pages
- `scrape.py` — initial download tool (for fresh setups)

## Project Structure

```
~/hermes-docs-ru/
├── originals/              # Original .md files (downloaded from docs site)
│   └── docs/...
├── translated/             # Russian translations (same structure)
│   └── docs/...
├── small_batches/
│   └── _batches.json       # Translation batch definitions
├── scrape.py               # Download tool
├── update_check.py         # Incremental update checker
└── translation_state.json  # Translation progress state
```

## How Translation Works

The translation is done via AI subagents (`delegate_task` in Hermes Agent), processing 1-2 pages per batch with 3 batches in parallel. Key methodology:

1. **Phase A (subagents)** — each reads an original, translates it, saves to `translated/`
2. **Phase B (parent)** — after all subagents finish, syncs `translated/` with `translation_state.json`
3. **Split strategy** — files >60KB are split into parts, translated separately, then merged

## Keeping Up to Date

When the upstream Hermes Agent documentation gains new pages:

```bash
cd ~/hermes-docs-ru
python3 update_check.py           # check what's new
python3 update_check.py --apply   # download new pages, prepare for translation
```

Then run the translate workflow for only the new/changed pages.

## License

The translated content is provided under the same terms as the original Hermes Agent documentation.
