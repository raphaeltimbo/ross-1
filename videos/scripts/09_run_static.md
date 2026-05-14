# Video 09 — `run_static`: Gravity Sag and Reaction Loads

> **Goal:** show how ROSS solves $\mathbf{K}\mathbf{u} = \mathbf{F}_g$ to find
> the static deformation under gravity, and how it derives bending moments,
> shear forces, and bearing reactions from the result.

**Estimated length:** 3 min · **Code:** `ross/rotor_assembly.py:4124-4262`

---

## Scene 1 — Why bother? (15 s)

- A horizontal rotor sags under its own weight.
- The static deformation tells us:
  - Bearing reactions (must stay positive!).
  - Bending moments (limit the shaft size).
  - Initial shape used as the equilibrium for dynamic linearisation.

## Scene 2 — The linear system (45 s)

Free-body equation, all velocities and accelerations zero:

$$
\mathbf{K}\,\mathbf{u} = \mathbf{F}_g
$$

with the gravity load assembled as

$$
\mathbf{F}_g = \mathbf{M}\,\mathbf{g}
$$

where $\mathbf{g}$ has $-9.8065\;\text{m/s}^{2}$ on every $y$ DOF and zero
elsewhere.

```python
# ross/rotor_assembly.py:4225-4232 (paraphrased)
g = -9.8065
weight = self.gravitational_force(g=g, M=aux_M, num_dof=num_dof)
displacement = la.solve(aux_K, weight).flatten()
displacement_y = displacement[1::num_dof]   # vertical DOFs
nodal_forces = aux1_K @ displacement
```

To make the system solvable, bearings are temporarily **stiffened** to
$10^{20}\,\text{N/m}$ so they act like fixed supports, and the auxiliary
stiffness `aux1_K` (with bearings removed) is used to compute reactions.

## Scene 3 — Visualising the deflection (40 s)

- Draw the rotor centerline.
- Solve for $\mathbf{u}$ from a small example.
- Plot deformation at every node, with vertical exaggeration ×500.
- Show two bearings as triangle supports; reactions appear as upward
  arrows whose lengths sum to $-\sum m_i g$.

## Scene 4 — Bending moment & shear (30 s)

From the nodal forces, ROSS integrates:

- Shear force $V(x) = \sum_{x_i \le x} F_y$
- Bending moment $M(x) = \int V(x)\,dx$

Show two profiles below the rotor:

- $V(x)$ — piecewise linear / step.
- $M(x)$ — piecewise quadratic, zero at supports.

## Scene 5 — Code in one line (15 s)

```python
static = rotor.run_static()
static.plot_deformation()
static.plot_bending_moment()
static.plot_shearing_force()
static.plot_free_body_diagram()
```

## Scene 6 — Outro (15 s)

- Static is the cheap analysis; everything dynamic builds on top.
- Up next: forced response and the unbalance problem.

---

## Visual / Manim notes

- The deformation plot can be a `ParametricFunction` interpolating the
  node displacements with a cubic spline.
- For arrows, use `Arrow(start, end)` with `stroke_width` proportional to
  reaction magnitude.
