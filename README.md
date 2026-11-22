# RA-L · Controller Target Readback

This repository contains the RA-L manuscript page and source files for
**Reconstructing Cartesian Controller Targets from Replay Telemetry**.

The page and asset tree are RA-L-only. RSS has a separate repository and
separate website at
[`rss-cartesian-target-replay`](https://github.com/Shiraikuroko123/rss-cartesian-target-replay).

## Evidence boundary

The manuscript studies which fields and timestamps identify the target at the
receiver. It evaluates a bound on individual command rewrites, tests application
timing in a Franka software harness and examines the meaning of a status flag
in 25 DROID recordings. The Fetch, Sawyer and Panda simulation comparisons
include data also used in the alternative RSS manuscript.
The page does not claim real-robot deployment, hard real-time behavior, or a
universal target-readback schedule.

The complex-tabletop section contains two supplementary clips. They are
exploratory occlusion and movable-clutter stress tests. They are not new RA-L
trials and do not change the paper statistics.

## Media

- `assets/videos/ral-fetch-pick-place-drop-event5-202611204-1080p.mp4` is the
  autoplay hero replay.
- The replay selector offers four native Fetch branches, with a distinct matching poster for each.
- `assets/videos/ral-extension-manifest.json` records the two supplementary
  tabletop clips and their source reports.
- `assets/videos/ral-media-manifest.json` records the frozen RA-L replay render
  provenance.

## Local preview

```powershell
python -m http.server 8787
```

Open `http://127.0.0.1:8787/`.

## Paper files

- [`papers/ral/ral-manuscript.pdf`](papers/ral/ral-manuscript.pdf)
- [`papers/ral/main.tex`](papers/ral/main.tex)
- [Complete LaTeX source and figures](papers/ral/manuscript-source.zip)
- [`papers/ral/figures/`](papers/ral/figures/)
