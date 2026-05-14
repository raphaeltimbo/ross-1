# Video 02 — Shaft Element: The Timoshenko Beam

> **Goal:** build, layer by layer, the 12×12 mass, stiffness and gyroscopic
> matrices of a single ROSS shaft element. By the end the viewer should know
> what each block of the matrix represents and what the parameter φ means.

**Estimated length:** 5–6 min · **Code:** `ross/shaft_element.py`

---

## Scene 1 — Where we are in the pipeline (10 s)

- Reuse the pipeline graphic from Episode 1, highlight **"Elements"**,
  zoom into **shaft element**.

## Scene 2 — Geometry and DOFs (30 s)

- Draw a single tapered cylinder between **node 0** (left) and **node 1**
  (right), length **L**, inner / outer diameters at each end.
- Pop up the **6 DOFs per node**:

  $$
  \mathbf{q}_n = \begin{bmatrix} x_n & y_n & z_n & \alpha_n & \beta_n & \theta_n \end{bmatrix}^{T}
  $$

  - $x, y$ — lateral translations (perpendicular to shaft axis)
  - $z$ — axial translation
  - $\alpha, \beta$ — bending rotations about $x, y$
  - $\theta$ — torsion about $z$

- Total: **12 DOFs** per element → matrices are **12 × 12**.

Code reference (DOF mapping):

```python
# ross/shaft_element.py:510-523
def dof_mapping(self):
    return {"x_0": 0, "y_0": 1, "z_0": 2,
            "alpha_0": 3, "beta_0": 4, "theta_0": 5,
            "x_1": 6, "y_1": 7, "z_1": 8,
            "alpha_1": 9, "beta_1": 10, "theta_1": 11}
```

## Scene 3 — Euler–Bernoulli vs Timoshenko (45 s)

- Two beams side by side under transverse load:
  - **Euler–Bernoulli** — sections stay perpendicular to the neutral axis.
  - **Timoshenko** — sections rotate independently (shear deformation
    + rotary inertia).

- Show the **shear factor**:

  $$
  \varphi = \frac{12\,E\,I}{G_s\,\kappa\,A\,L^{2}}
  $$

  - $E$ Young's modulus, $G_s$ shear modulus
  - $I$ second moment of area, $A$ cross-section area
  - $\kappa$ Cowper / Hutchinson shear coefficient
  - $L$ element length

- Limits:
  - thin / long: $\varphi \to 0$ → Euler–Bernoulli
  - thick / short: $\varphi$ large → shear matters

Code reference:

```python
# ross/shaft_element.py:302
phi = 12 * E * I / (G_s * kappa * A * L**2)
```

## Scene 4 — Mass matrix M (60 s)

- Empty 12 × 12 grid appears, DOFs labelled along rows/columns.
- Build it in three layers, each fading in:

### 4.1 Bending mass (cross-coupled translation/rotation)

Coefficient prefactor:

$$
\frac{\rho\,A\,L}{1260\,(1+\varphi)^{2}}
$$

Highlight the lateral DOFs $\{x_0, y_0, \alpha_0, \beta_0, x_1, y_1, \alpha_1, \beta_1\}$.

### 4.2 Rotary inertia correction

$$
\frac{\rho\,I_e}{210\,L\,(1+\varphi)^{2}}
$$

Adds to the rotational DOFs $\{\alpha, \beta\}$.

### 4.3 Axial + torsional blocks

$$
M_{ax} = \frac{\rho A_e L}{6}\!
\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}\!,\quad
M_{ts} = \frac{\rho J_e L}{6}\!
\begin{bmatrix} 2 & 1 \\ 1 & 2 \end{bmatrix}
$$

at the $\{z_0, z_1\}$ and $\{\theta_0, \theta_1\}$ DOF pairs.

Code reference:

```python
# ross/shaft_element.py:525-722
M = (rho * A_l * L / (1260 * (1 + phi)**2)) * M_bending
M += (rho * I_e_l / (210 * L * (1 + phi)**2)) * M_rotary
M[[2,8]][:, [2,8]] += rho * A_e * L / 6 * np.array([[2,1],[1,2]])
M[[5,11]][:,[5,11]] += rho * J_e * L / 6 * np.array([[2,1],[1,2]])
```

## Scene 5 — Stiffness matrix K (60 s)

Same 12 × 12 grid, but built from four contributions:

- **Bending stiffness** $K_1$ ∝ $E I / L^{3}$
- **Shear correction** $K_2$ ∝ $\varphi E I / L^{3}$, vanishes for $\varphi = 0$
- **Axial stiffness**: $\dfrac{E A}{L}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}$ at $\{z_0, z_1\}$
- **Torsional stiffness**: $\dfrac{G_s J}{L}\begin{bmatrix} 1 & -1 \\ -1 & 1 \end{bmatrix}$ at $\{\theta_0, \theta_1\}$

Code reference: `ross/shaft_element.py:724-915`.

## Scene 6 — Gyroscopic matrix G (45 s)

- Animate a spinning element: when it precesses, an out-of-plane moment
  appears.
- Show the antisymmetric structure that couples the two bending planes:

  $$
  \mathbf{G} = \frac{\rho I_e \cdot 2}{210\,L\,(1+\varphi)^{2}}\,\mathbf{G}_0
  $$

  where $\mathbf{G}_0$ is **skew-symmetric** and links $(y_n, \alpha_n)$ to
  $(x_n, \beta_n)$.

- Key identity: $\mathbf{G}^T = -\mathbf{G}$ — that's what makes whirl
  modes split forward/backward when the rotor spins.

Code reference: `ross/shaft_element.py:987-1085`.

## Scene 7 — Damping matrix C (15 s)

- Proportional damping: $\mathbf{C} = \alpha\mathbf{M} + \beta\mathbf{K}$,
  often zero at the element level.
- File: `ross/shaft_element.py:958-985`.

## Scene 8 — Recap (20 s)

- Stack the four matrices side by side.
- Stress: every shaft element contributes the **same shape** — the only
  things that change are the geometry and material that go into the
  coefficients.

---

## Visual / Manim notes

- Render the 12 × 12 grid with a `Matrix` mobject; populate cells with
  semi-transparent `Square`s coloured by which sub-block they belong to.
- For the bending demo (Scene 3), animate two beams with `Polygon`s; rotate
  cross-section markers to show the shear angle.
- For G (Scene 6), animate a small disk attached to the beam doing forward
  whirl, with a torque arrow that flips sign when the precession reverses.
