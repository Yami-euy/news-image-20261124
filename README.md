# THE TUESDAY GLOBE — Tuesday 24 November 2026

[![news-image-20261124](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/Yami-euy/news-image-20261124/rank.svg)](https://make.fun/bounty/news-image-20261124/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/Yami-euy/news-image-20261124/reward.svg)](https://make.fun/bounty/news-image-20261124?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261124)

A one-page newspaper image summing up the world's news of **Tuesday 24 November 2026** — built for the [news-image-20261124](https://make.fun/bounty/news-image-20261124) bounty on make.fun.

## The day, in brief

- **Wall Street soars** — the Nasdaq posts its best day since April 2025 (+6.51%) as Nvidia surges 31.5% and adds a record $952bn of market value in one session.
- **Russian strike on Zaporizhzhia** kills 2 and wounds 40 overnight.
- **US blacklists Megaspeed and an Alibaba unit** in new export controls.
- Plus 30 more stories across all seven regions, a world map with 12 pinned locations, and a markets strip.

## How it works

`main.py` is a standard-library-only copier (imports only `os`, `shutil`, `sys` and `pathlib`): it copies the pre-rendered `entry.png` sitting beside it to `/output/entry.png` (1024×1024, deterministic — two runs produce byte-identical output), because the grading sandbox runs Python 3.13 with the standard library only and installs nothing. The image itself is rendered locally with `render.py` + Pillow and committed to the repository; `render.py` and `fonts/` stay in the repo as provenance of how the page was drawn. All fonts used are bundled in `fonts/` and were loaded from the repository first, with a system-path and `load_default()` fallback.

## Files

- `main.py` — entry point
- `render.py` — the drawing engine (masthead, lead, chart, map, region grid)
- `stories.py` — the day's verified stories (easy to extend with late news)
- `fonts/` — the five bundled TTFs the renderer uses
