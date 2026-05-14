# ROSS — Animated Series

A series of Manim videos that walk through the internals of
[ROSS](https://ross.readthedocs.io): how each element matrix is built,
how the global system is assembled, and how each `run_*` analysis works.

## Structure

```
videos/
├── pyproject.toml          # self-contained uv project for manim deps
├── scripts/                # written storyboards (.md, with math + code refs)
│   ├── 01_introduction.md
│   ├── 02_shaft_element.md
│   ├── 03_disk_element.md
│   ├── 04_bearing_element.md
│   ├── 05_global_assembly.md
│   ├── 06_run_modal.md
│   ├── 07_run_campbell.md
│   ├── 08_run_critical_speed.md
│   ├── 09_run_static.md
│   ├── 10_run_unbalance_response.md
│   ├── 11_run_time_response.md
│   └── 12_run_ucs_level1.md
├── manim/                  # Manim Scene implementations
│   ├── 01_introduction.py
│   ├── 02_shaft_element.py
│   └── ...
└── media/                  # gitignored render output
```

## Workflow

1. **Edit a script** in `scripts/NN_topic.md` — describe the visual story,
   include the math and any code references.
2. **Edit / write the Manim Scene** in `manim/NN_topic.py` to match.
3. **Render** at low quality first:
   ```bash
   cd videos
   uv run manim render manim/NN_topic.py -ql -p
   ```
4. Once happy, render the deliverable:
   ```bash
   uv run manim render manim/NN_topic.py -qh
   ```

Every Manim file may contain multiple `Scene` subclasses (one per logical
"chapter" of the lesson). Pass the scene name after the file to render
just one, or use `-a` to render all.

## Series outline

| # | Topic | Script |
|---|-------|--------|
| 01 | Introduction & FEM pipeline | [scripts/01_introduction.md](scripts/01_introduction.md) |
| 02 | Shaft element (Timoshenko beam) | [scripts/02_shaft_element.md](scripts/02_shaft_element.md) |
| 03 | Disk element | [scripts/03_disk_element.md](scripts/03_disk_element.md) |
| 04 | Bearing element | [scripts/04_bearing_element.md](scripts/04_bearing_element.md) |
| 05 | Global matrix assembly | [scripts/05_global_assembly.md](scripts/05_global_assembly.md) |
| 06 | `run_modal` | [scripts/06_run_modal.md](scripts/06_run_modal.md) |
| 07 | `run_campbell` | [scripts/07_run_campbell.md](scripts/07_run_campbell.md) |
| 08 | `run_critical_speed` | [scripts/08_run_critical_speed.md](scripts/08_run_critical_speed.md) |
| 09 | `run_static` | [scripts/09_run_static.md](scripts/09_run_static.md) |
| 10 | `run_unbalance_response` / `run_freq_response` | [scripts/10_run_unbalance_response.md](scripts/10_run_unbalance_response.md) |
| 11 | `run_time_response` | [scripts/11_run_time_response.md](scripts/11_run_time_response.md) |
| 12 | `run_ucs` / `run_level1` | [scripts/12_run_ucs_level1.md](scripts/12_run_ucs_level1.md) |
