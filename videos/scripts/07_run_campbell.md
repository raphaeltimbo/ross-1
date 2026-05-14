# Video 07 — `run_campbell`: The Campbell Diagram

> **Goal:** show how repeated modal analyses across a speed range — combined
> with **MAC-based mode tracking** — produce the Campbell diagram, and how
> intersections with $n\,\Omega$ lines reveal critical speeds.

**Estimated length:** 4 min · **Code:** `ross/rotor_assembly.py:3038-3157`

---

## Scene 1 — Why a sweep? (20 s)

- Natural frequencies depend on $\Omega$ because of $\mathbf{G}$ and any
  speed-dependent bearing data.
- Whirl modes split forward/backward → the diagram becomes the central
  visualisation in turbomachinery design.

## Scene 2 — The recipe (30 s)

```python
# ross/rotor_assembly.py:3095-3136 (paraphrased)
for i, w in enumerate(speed_range):
    modal = self.run_modal(speed=w, num_modes=num_modes)
    evec_v = modal.evectors[:, :evec_size]
    if i > 0:
        macs = compute_MAC(evec_u, evec_v)
        order = match_modes(macs, threshold=0.9)
        reorder(eigenvalues_at_w, order)
    evec_u = evec_v
```

Two ideas combined:
1. Loop `run_modal` at each speed.
2. **Match modes across speeds** so that "mode 2 at 1000 rpm" really is
   the same mode as "mode 2 at 1500 rpm" — the eigensolver doesn't keep
   that order for free.

## Scene 3 — MAC: Mode Assurance Criterion (45 s)

Two modes are "the same" if their shapes are well-aligned:

$$
\text{MAC}(\boldsymbol\phi_u, \boldsymbol\phi_v) =
\frac{|\boldsymbol\phi_u^{H}\boldsymbol\phi_v|^{2}}
{(\boldsymbol\phi_u^{H}\boldsymbol\phi_u)\,(\boldsymbol\phi_v^{H}\boldsymbol\phi_v)}
\in [0,1]
$$

- 1 → identical shape (up to a complex scalar)
- 0 → orthogonal

ROSS builds a MAC matrix at each step and matches modes greedily where
MAC > 0.9 (`rotor_assembly.py:3095-3136`).

Animation: a 4 × 4 colour grid showing MAC values; arrows draw the
matched permutation.

## Scene 4 — The diagram itself (45 s)

- $x$-axis: rotor speed $\Omega$.
- $y$-axis: natural frequency $\omega_n$.
- One curve per tracked mode; forward (rising) and backward (falling)
  branches diverge as speed grows.
- Add lines $\omega = n\Omega$ for $n = 1$ (synchronous), $n = 2$
  (twice-per-rev), etc.
- **Critical speeds** are where the natural-frequency curves cross those
  lines.

## Scene 5 — Code in one line (10 s)

```python
camp = rotor.run_campbell(np.linspace(0, 4000, 50) * 2*np.pi/60)
camp.plot()
```

## Scene 6 — Outro (10 s)

- Mode tracking is the "magic" inside.
- Up next: solving for those crossings exactly with Newton's method.

---

## Visual / Manim notes

- Build the diagram by precomputing the data in a Python helper file
  (`videos/manim/_data.py`) so the Scene only needs to render the points.
- Use `Axes.plot_line_graph(x_values=..., y_values=...)` per mode and
  `ReplacementTransform` to add the $n\Omega$ lines.
- Highlight one crossing with `Indicate` and a label "critical speed
  candidate".
