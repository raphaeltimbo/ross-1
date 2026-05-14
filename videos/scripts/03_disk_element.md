# Video 03 — Disk Element: Lumped Mass and Gyroscopics

> **Goal:** show that a disk in ROSS is a **6-DOF lumped element** with a
> diagonal mass matrix and a sparse gyroscopic matrix that couples the two
> bending rotations through the polar inertia $I_p$.

**Estimated length:** 3–4 min · **Code:** `ross/disk_element.py`

---

## Scene 1 — Recap & geometry (20 s)

- A short cylindrical disk on the shaft at node $n$, mass $m$, outer
  diameter $d_o$, inner diameter $d_i$, width $w$.
- Properties (`from_geometry`, lines 532-598):

  $$
  m = \rho\,\pi\,w\,\frac{d_o^{2} - d_i^{2}}{4}, \quad
  I_p = m\,\frac{d_o^{2} + d_i^{2}}{8}, \quad
  I_d = \tfrac{1}{2} I_p + \tfrac{1}{12} m w^{2}
  $$

  - $I_p$ — **polar** moment of inertia (about spin axis $z$)
  - $I_d$ — **diametral** moment of inertia (about $x$ or $y$)

## Scene 2 — Six degrees of freedom (15 s)

Disk acts on a **single node**, so DOFs are just:

$$
\mathbf{q} = [x, y, z, \alpha, \beta, \theta]^{T}
$$

`dof_mapping()` returns this exact ordering (`disk_element.py:166-193`).

## Scene 3 — Mass matrix M (30 s)

Diagonal:

$$
\mathbf{M} = \mathrm{diag}(m, m, m, I_d, I_d, I_p)
$$

Code:

```python
# ross/disk_element.py:195-229
M = np.array([
    [m, 0, 0, 0, 0, 0],
    [0, m, 0, 0, 0, 0],
    [0, 0, m, 0, 0, 0],
    [0, 0, 0, I_d, 0, 0],
    [0, 0, 0, 0, I_d, 0],
    [0, 0, 0, 0, 0, I_p],
])
```

Discussion: the disk does not store strain energy → $\mathbf{K} = \mathbf{0}$,
$\mathbf{C} = \mathbf{0}$ (lines 231-316).

## Scene 4 — Gyroscopic matrix G (60 s)

A spinning disk that is tilted by angle $\beta$ generates a moment about
the perpendicular axis equal to $I_p\,\Omega\,\dot\beta$. This is the
gyroscopic coupling.

The element-level matrix is **almost zero** except two entries:

$$
\mathbf{G} = \begin{bmatrix}
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
0 & 0 & 0 & 0 & I_p & 0 \\
0 & 0 & 0 & -I_p & 0 & 0 \\
0 & 0 & 0 & 0 & 0 & 0 \\
\end{bmatrix}
$$

Skew-symmetric block coupling rotations $\alpha$ and $\beta$.
Code: `disk_element.py:318-351`.

### Why it matters (animation)

- Static disk: deflection in $x$ has zero coupling to rotation about $y$.
- Spinning disk: tilt → restoring moment in the **other** plane.
- This is what splits a single bending mode into a **forward whirl** and
  **backward whirl** pair as soon as $\Omega > 0$. We will use this fact
  again in Episode 06.

## Scene 5 — Recap (15 s)

- Mass matrix: simple lumping.
- Gyroscopic matrix: the entire physics of whirl-splitting lives in two
  numbers $\pm I_p$.
- Up next: bearings, the only element with frequency-dependent matrices.

---

## Visual / Manim notes

- Use a `Cylinder` (3D) for the disk; rotate slowly so $I_p$ is intuitive.
- Show the 6 × 6 matrix as a grid; only the four non-trivial cells (mass
  diagonal, plus the two ±$I_p$ entries) are coloured.
- For the "why it matters" beat, animate two arrows: an applied tilt
  $\beta$ in the $x$-$z$ plane, and the resulting moment in the $y$-$z$
  plane.
