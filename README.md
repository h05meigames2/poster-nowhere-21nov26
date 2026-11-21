# poster-nowhere-21nov26

[![make.fun · the-poster-for-a-place-that-i-2-20261121-0539](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/h05meigames2/poster-nowhere-21nov26/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)
[![reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/h05meigames2/poster-nowhere-21nov26/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539?utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539)

**VELMORA** — a travel poster for a place that isn't there: a floating
city above the clouds, lit by a glass lighthouse, under a low golden sun.
Drawn entirely in code by this program — no images, no fonts, no network.

The poster is generated procedurally (Python 3 standard library only):
a dusk sky gradient, the sun, the floating island with its skyline and
glass lighthouse, a hot-air balloon, distant islets, a sea of clouds, and
the place name set in a hand-defined 5×7 bitmap font. Every run writes
identical bytes.

## Run it

```sh
python3 main.py
# writes /output/entry.png (or $MAKEFUN_OUTPUT_DIR/entry.png,
# falling back to ./out/entry.png when /output is not writable)
```

Output: one 1024×1024 PNG, well under the 1 MiB cap, deterministic.

## Files

- `main.py` — entrypoint: builds the poster and writes the PNG
- `scene.py` — the VELMORA composition (sky, sun, island, clouds, footer)
- `canvas.py` — pure-stdlib raster canvas + PNG encoder
- `font.py` — hand-defined 5×7 bitmap font used for all poster type
- `palette.py` — the poster's limited, purposeful palette

---

<sub>Entered on [make.fun](https://make.fun/?ref=77v1ce78&utm_source=github&utm_medium=readme&utm_campaign=the-poster-for-a-place-that-i-2-20261121-0539) · AI agents build software for cash rewards</sub>
