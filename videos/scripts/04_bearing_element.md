# Video 04 — Bearing Element: Frequency-Dependent Coefficients

> **Goal:** explain what the eight bearing coefficients $k_{ij}, c_{ij}$ mean
> physically, how ROSS interpolates them as functions of speed, and how the
> resulting 3 × 3 (or 6 × 6 with `n_link`) matrix slots into the rotor.

**Estimated length:** 3–4 min · **Code:** `ross/bearing_seal_element.py`

---

## Scene 1 — Picture of a journal bearing (20 s)

- Cross-section: shaft inside a sleeve, oil film in the gap.
- The film acts like 4 springs and 4 dashpots arranged between the shaft
  and the housing.

## Scene 2 — The 8 coefficients (30 s)

Linearised film force around the static equilibrium:

$$
\begin{bmatrix} F_x \\ F_y \end{bmatrix}
= -
\begin{bmatrix} k_{xx} & k_{xy} \\ k_{yx} & k_{yy} \end{bmatrix}
\begin{bmatrix} x \\ y \end{bmatrix}
-
\begin{bmatrix} c_{xx} & c_{xy} \\ c_{yx} & c_{yy} \end{bmatrix}
\begin{bmatrix} \dot x \\ \dot y \end{bmatrix}
$$

- **Direct terms** $k_{xx}, k_{yy}, c_{xx}, c_{yy}$ — restore in the same direction.
- **Cross-coupled terms** $k_{xy}, k_{yx}, c_{xy}, c_{yx}$ — couple the two
  lateral planes; responsible for fluid-film instability.

## Scene 3 — Local matrices (30 s)

Bearing acts on a single node, lateral DOFs only:

$$
\mathbf{K}(\omega) = \begin{bmatrix}
k_{xx}(\omega) & k_{xy}(\omega) & 0 \\
k_{yx}(\omega) & k_{yy}(\omega) & 0 \\
0 & 0 & k_{zz}(\omega)
\end{bmatrix},
\quad
\mathbf{C}(\omega) = \begin{bmatrix}
c_{xx}(\omega) & c_{xy}(\omega) & 0 \\
c_{yx}(\omega) & c_{yy}(\omega) & 0 \\
0 & 0 & c_{zz}(\omega)
\end{bmatrix}
$$

`dof_mapping()` is `{"x_0": 0, "y_0": 1, "z_0": 2}`
(`bearing_seal_element.py:660-685`).

Note: $\mathbf{M} = \mathbf{0}$ for typical fluid-film bearings, but the
class accepts $m_{ij}$ for AMB / fluid-mass models.

## Scene 4 — Frequency dependence (45 s)

Stiffness and damping change with operating speed. ROSS supports two
input forms:

- **Scalar** — constant.
- **Array indexed by frequency** — passed alongside a `frequency` array;
  ROSS builds a `scipy.interpolate.UnivariateSpline` per coefficient.

```python
# ross/bearing_seal_element.py:235-289 (paraphrased)
self.kxx_interpolated = UnivariateSpline(frequency, kxx, s=0)
# K(speed) then evaluates the spline at the requested speed
```

Visualisation: a 2D plot of $k_{xx}(\omega)$ from `bearing_example()`,
with a vertical bar that sweeps from low to high speed; the matrix entry
on the right updates as the bar moves.

## Scene 5 — Cross-coupling and stability (45 s)

- Pure direct stiffness → orbits decay.
- Add positive $k_{xy} = -k_{yx}$ → orbit can grow → **whirl instability**.
- Animate two journal orbits side by side: one stable (decaying), one
  unstable (growing).
- Foreshadow Episode 12 (`run_level1`): we sweep $Q$ as cross-coupling and
  check the log decrement.

## Scene 6 — `n_link` and floating bearings (20 s)

When the housing itself can move (squeeze-film damper, support
flexibility), pass `n_link=n_other`. The matrix expands to 6 × 6:

$$
\mathbf{K}_{\text{ext}} = \begin{bmatrix}
\mathbf{K} & -\mathbf{K} \\
-\mathbf{K} & \mathbf{K}
\end{bmatrix}
$$

so that forces act between the rotor node $n$ and the support node $n_l$.

## Scene 7 — Recap (10 s)

- 8 coefficients → 3 × 3 stiffness/damping matrices.
- Frequency dependence handled by splines.
- Cross-coupling is the seed of whirl instability.

---

## Visual / Manim notes

- Use a 2D bearing cross-section (two circles, oil-film fill colour).
- Spring/dashpot icons can be drawn with `VGroup` of zig-zag lines and
  a `Rectangle`+`Line` dashpot.
- For the spline interpolation, plot a smooth curve through 4-5 marker
  points and animate a `Dot` riding along it.
