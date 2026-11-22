# RA-L · Controller Target Readback

This repository contains the independent RA-L manuscript page and
reproducibility artifacts for **When Does Controller Target Readback Help
Cartesian Demonstration Replay?**

The page and asset tree are RA-L-only. RSS has a separate repository and
separate website at
[`rss-robot-replay`](https://github.com/Shiraikuroko123/rss-robot-replay).

## Evidence boundary

The main study separates target-writing error from physical tracking error
across Fetch, Sawyer, and Panda replay conditions. The held-out cohort contains
144 conditions and reports both hand-path error and native terminal outcomes.
The page does not claim real-robot deployment, hard real-time behavior, or a
universal target-readback schedule.

The complex-tabletop section contains two supplementary clips. They are
exploratory occlusion and movable-clutter stress tests. They are not new RA-L
trials and do not change the paper statistics.

## Media

- `assets/videos/ral-fetch-pick-place-drop-event5-202611204-1080p.mp4` is the
  autoplay hero replay.
- The remaining RA-L replay clips have independent poster frames and are shown
  once in the evidence gallery.
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
- [`papers/ral/figures/`](papers/ral/figures/)
