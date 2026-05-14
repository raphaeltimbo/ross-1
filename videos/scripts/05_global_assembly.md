# Video 05 — Global Matrix Assembly

> **Goal:** show how `Rotor.__init__` and the global `M(), K(speed), C(speed),
> G()` methods stamp every element matrix into the global system using
> `dof_global_index`, and how the **state-space** matrix `A(speed)` is built
> from them.

**Estimated length:** 4–5 min · **Code:** `ross/rotor_assembly.py`

---

## Scene 1 — The bookkeeping problem (20 s)

- Each element produces a small dense matrix (12 × 12, 6 × 6, 3 × 3).
- Globally we have $N_\text{nodes} \times \text{dof}_\text{node}$ DOFs.
- Question: *"How does ROSS know which rows/columns each element touches?"*

## Scene 2 — Node and DOF numbering (40 s)

In `Rotor.__init__`:

```python
# ross/rotor_assembly.py:182-186 (paraphrased)
for i, sh in enumerate(shaft_elements):
    sh.n = i
self.shaft_elements = sorted(shaft_elements, key=lambda el: el.n)
```

Number of DOFs:

```python
# ross/rotor_assembly.py:379-383
half_ndof = self.number_dof / 2
self.ndof = int(self.number_dof * len(self.nodes)
                + half_ndof * len(self.point_mass_elements))
```

For the standard 6-DOF shaft + $N$ nodes:

$$
N_\text{dof} = 6\,N_\text{nodes} \;+\; 3\,N_\text{pointmasses}
$$

(point masses only add lateral DOFs).

Animate: a horizontal beam with 7 nodes, each labelled with a 6-tuple of
DOF indices that count up.

## Scene 3 — `dof_global_index` (45 s)

Built in `__init__`:

```python
# ross/rotor_assembly.py:388-403
for k, v in elm.dof_mapping().items():
    global_dof_mapping[k] = int(self.number_dof * elm.n + v)
elm.dof_global_index = global_dof_mapping
```

So a shaft element on nodes $n$ and $n+1$ touches DOFs
$\{6n, 6n+1, \ldots, 6n+5,\; 6(n+1), \ldots, 6(n+1)+5\}$.

A disk on node $n$ touches $\{6n, \ldots, 6n+5\}$.

## Scene 4 — Stamping with `np.ix_` (60 s)

The heart of assembly:

```python
# ross/rotor_assembly.py:543-557
M0 = np.zeros((self.ndof, self.ndof))
C0 = np.zeros((self.ndof, self.ndof))
K0 = np.zeros((self.ndof, self.ndof))
G0 = np.zeros((self.ndof, self.ndof))
for elm in elements:
    dofs = list(elm.dof_global_index.values())
    M0[np.ix_(dofs, dofs)] += elm.M()
    C0[np.ix_(dofs, dofs)] += elm.C()
    K0[np.ix_(dofs, dofs)] += elm.K()
    G0[np.ix_(dofs, dofs)] += elm.G()
```

Animation: small element matrix slides up to the big global matrix, the
`dofs` indices light up as a row/column "stencil", and the entries are
**added** (with a small `+=` annotation) into the global block.

Repeat for two adjacent shaft elements that **share** the middle node —
their middle-node blocks overlap and the contributions superpose.

## Scene 5 — Sparsity pattern (20 s)

Show the resulting global $\mathbf{K}$ as a heatmap. Block-banded shape:
non-zeros along the diagonal, with disks reinforcing diagonal blocks and
bearings adding sparse "spikes" at their nodes.

## Scene 6 — Equation of motion (15 s)

Putting it together:

$$
\mathbf{M}(\omega)\,\ddot{\mathbf{q}} \;+\;
\big[\mathbf{C}(\omega) + \Omega\,\mathbf{G}\big]\,\dot{\mathbf{q}} \;+\;
\mathbf{K}(\omega)\,\mathbf{q} \;=\; \mathbf{f}(t)
$$

Note the two distinct frequencies:

- $\Omega$ — the **rotor spin speed** (multiplies $\mathbf{G}$).
- $\omega$ — the **excitation frequency** at which bearings are evaluated.

## Scene 7 — State-space form $\mathbf{A}(\Omega)$ (40 s)

Many ROSS analyses (`run_modal`, `run_campbell`, `run_critical_speed`)
use the **first-order** form:

$$
\dot{\mathbf{x}} = \mathbf{A}(\Omega)\,\mathbf{x},\qquad
\mathbf{x} = \begin{bmatrix}\mathbf{q}\\ \dot{\mathbf{q}}\end{bmatrix}
$$

with

$$
\mathbf{A}(\Omega) = \begin{bmatrix}
\mathbf{0} & \mathbf{I} \\
-\mathbf{M}^{-1}\mathbf{K} & -\mathbf{M}^{-1}\big(\mathbf{C} + \Omega\,\mathbf{G}\big)
\end{bmatrix}
$$

Code:

```python
# ross/rotor_assembly.py:1333-1336
A = np.vstack([
    np.hstack([Z, I]),
    np.hstack([la.solve(-M, self.K(frequency)),
               la.solve(-M, self.C(frequency) + self.G() * speed)]),
])
```

Highlight: the $\Omega\,\mathbf{G}$ term is what makes $\mathbf{A}$
**speed-dependent**.

## Scene 8 — Recap (15 s)

- Element matrices = bricks.
- `dof_global_index` = the address each brick goes to.
- `np.ix_` adds them in.
- $\mathbf{A}(\Omega)$ packages everything for eigenvalue analysis.

---

## Visual / Manim notes

- The "small matrix slides into big matrix" animation is the centrepiece
  — use `MoveAlongPath` / `Transform` and a 2D coloured `Square` grid.
- For the heatmap, generate it offline from `rs.rotor_example().K(0)` and
  `imshow` to a PNG, then load with `ImageMobject`.
- For the state-space matrix, use a 2 × 2 `Matrix` of block matrices.
