# Video 01 — Introduction: The ROSS Pipeline

> **Goal:** establish the mental model that every ROSS analysis follows the
> same pipeline — **Elements → Rotor → `run_*` analysis → Results object**
> — and motivate the rest of the series.

**Estimated length:** 2–3 min

---

## Scene 1 — Title (10 s)

- Title card: **"How ROSS Works — Episode 1"**.
- Subtitle: *"The pipeline that turns geometry into rotordynamic answers."*
- Animated logo: a stylised shaft (cylinder) with two disks rotating, flanked by springs/dashpots.

## Scene 2 — Why rotordynamics? (25 s)

- Show a real industrial rotor (sketch / icon: turbine, compressor).
- Introduce the central question:

  > *"Will this machine vibrate dangerously when it spins?"*

- Three things engineers need to know:
  1. **Natural frequencies** (modes) — and their **whirl direction**.
  2. **Critical speeds** — where rotation excites a mode.
  3. **Forced response** — how big is the vibration in operation?

## Scene 3 — Discretisation (25 s)

- Morph the smooth rotor into a chain of **finite elements**:
  - cylinders → **shaft elements**
  - thick blades / wheels → **disk elements**
  - supports → **bearing / seal elements**
- Caption: *"Finite element method: replace the continuous rotor with a chain of small elements with known matrices."*

Math overlay (the master equation we'll build):

$$
\mathbf{M}\,\ddot{\mathbf{q}}(t) + \big(\mathbf{C} + \Omega\,\mathbf{G}\big)\,\dot{\mathbf{q}}(t) + \mathbf{K}\,\mathbf{q}(t) = \mathbf{f}(t)
$$

Label each matrix:
- **M** — mass
- **C** — damping
- **G** — gyroscopic (multiplied by spin speed Ω)
- **K** — stiffness
- **f** — applied force vector

## Scene 4 — The pipeline (40 s)

A horizontal flow chart, revealed step by step:

```
 ┌────────────┐    ┌─────────┐    ┌──────────────┐    ┌──────────┐
 │  Elements  │ →  │  Rotor  │ →  │  run_*()     │ →  │  Results │
 │  (M,K,C,G) │    │ (global │    │ (algorithm)  │    │ (.plot_*)│
 └────────────┘    │  M,K,C,G│    └──────────────┘    └──────────┘
                   └─────────┘
```

Highlight each box in turn while showing a code snippet from the project:

```python
import ross as rs

steel = rs.Material(name="steel", rho=7810, E=211e9, G_s=81.2e9)
shaft = [rs.ShaftElement(L=0.05, idl=0, odl=0.05, material=steel)
         for _ in range(6)]
disks = [rs.DiskElement.from_geometry(n=2, material=steel,
                                      width=0.07, i_d=0.05, o_d=0.28)]
bearings = [rs.BearingElement(n=0, kxx=1e6, cxx=0),
            rs.BearingElement(n=6, kxx=1e6, cxx=0)]

rotor = rs.Rotor(shaft, disks, bearings)
modal = rotor.run_modal(speed=0)
modal.plot_mode_2d(0)
```

(this is the `rs.rotor_example()` code from `ross/rotor_assembly.py`).

## Scene 5 — Series outline (30 s)

A vertical roadmap:

| # | Topic |
|---|-------|
| 02 | **Shaft element** — Timoshenko beam matrices |
| 03 | **Disk element** — lumped mass and gyroscopic effects |
| 04 | **Bearing element** — stiffness/damping coefficients |
| 05 | **Global assembly** — putting it all together |
| 06 | `run_modal` |
| 07 | `run_campbell` |
| 08 | `run_critical_speed` |
| 09 | `run_static` |
| 10 | `run_unbalance_response` / `run_freq_response` |
| 11 | `run_time_response` |
| 12 | `run_ucs` / `run_level1` |

## Scene 6 — Outro (10 s)

- "Next: how a single shaft element becomes a 12×12 mass matrix."
- Fade to title card.

---

## Visual / Manim notes

- Use ROSS-blue `#005BBB` and Petrobras-green `#00A859` accents.
- Pipeline boxes: `Rectangle(height=1.2, width=2.4)` with rounded corners,
  fade in left-to-right with `FadeIn(box, shift=RIGHT*0.3)`.
- The matrix equation should be a single `MathTex` so we can colour each
  symbol independently with `set_color_by_tex`.
- For the discretisation morph, use a `ParametricFunction` for the smooth
  rotor outline and `Transform` it into a sequence of `Rectangle`s.

## References (code in this episode)

- `rs.rotor_example()` → `ross/rotor_assembly.py`
- The four element ABCs → `ross/element.py:126-214`
