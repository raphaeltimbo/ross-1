# Video 06 — `run_modal`: Modal Analysis

> **Goal:** explain how ROSS turns the assembled matrices into natural
> frequencies, damping ratios, mode shapes, and a forward/backward whirl
> classification — by solving an eigenvalue problem on $\mathbf{A}(\Omega)$.

**Estimated length:** 4–5 min · **Code:** `ross/rotor_assembly.py:805-890`

---

## Scene 1 — The question (15 s)

> *"At what frequencies does the rotor want to vibrate, and how is it
> shaped when it does?"*

Modal analysis answers both — for any chosen spin speed $\Omega$.

## Scene 2 — From M, K, C, G to an eigenvalue problem (45 s)

Free vibration EOM:

$$
\mathbf{M}\ddot{\mathbf{q}} + (\mathbf{C} + \Omega\mathbf{G})\dot{\mathbf{q}} + \mathbf{K}\mathbf{q} = \mathbf{0}
$$

Try $\mathbf{q}(t) = \boldsymbol{\phi}\,e^{\lambda t}$. The system becomes
quadratic in $\lambda$, and is linearised to first order via the
state-space form from Episode 5:

$$
\dot{\mathbf{x}} = \mathbf{A}(\Omega)\,\mathbf{x},\qquad
\mathbf{A}(\Omega)\,\boldsymbol{\psi} = \lambda\,\boldsymbol{\psi}
$$

## Scene 3 — Solving the eigenvalue problem (40 s)

```python
# ross/rotor_assembly.py:863-874 (paraphrased)
evalues, evectors = self._eigen(speed, num_modes=num_modes,
                                sparse=sparse, synchronous=synchronous)
wn = np.absolute(evalues)[:wn_len]
wd = np.imag(evalues)[:wn_len]
damping_ratio = (-np.real(evalues) / np.absolute(evalues))[:wn_len]
log_dec = 2 * np.pi * damping_ratio / np.sqrt(1 - damping_ratio**2)
```

- **Sparse path**: `scipy.sparse.linalg.eigs` (ARPACK), $k = 2 \cdot \text{num\_modes}$.
- **Dense path**: `scipy.linalg.eig`.

## Scene 4 — Reading the eigenvalues (45 s)

Each eigenvalue $\lambda = \sigma + j\omega_d$ encodes one oscillation:

$$
\omega_n = |\lambda|, \qquad
\omega_d = \mathrm{Im}(\lambda), \qquad
\zeta = \frac{-\mathrm{Re}(\lambda)}{|\lambda|}, \qquad
\delta = \frac{2\pi\zeta}{\sqrt{1-\zeta^2}}
$$

- $\omega_n$ — undamped natural frequency
- $\omega_d$ — damped natural frequency
- $\zeta$ — damping ratio (positive = decaying, negative = unstable)
- $\delta$ — log decrement (favourite stability metric in API standards)

Animate a 2D oscilloscope trace for three cases: $\zeta>0$, $\zeta=0$,
$\zeta<0$.

## Scene 5 — Mode shapes & whirl direction (45 s)

The eigenvector $\boldsymbol{\psi}$ contains complex displacements at
every node. ROSS reshapes it into 3D coordinates and animates the orbit.

Whirl direction is decided by the **rotation sense** of the orbit at the
node of maximum amplitude:

- Same sense as $\Omega$ → **forward whirl** (typically destabilised by
  cross-coupled stiffness).
- Opposite sense → **backward whirl** (often heavily damped).

Show three modes from `rotor_example().run_modal(speed=0)`:

- Mode 1 (1st bending) — symmetric.
- Mode 2 (1st bending, antisymmetric / S-shape).
- Mode 3 (2nd bending).

## Scene 6 — Code recap (20 s)

```python
modal = rotor.run_modal(speed=Q_(4000, "RPM").to("rad/s").m)
print(modal.wn[:6])       # [rad/s]
modal.plot_mode_2d(0)
modal.plot_mode_3d(2)
```

## Scene 7 — What's next (10 s)

A modal analysis is **one snapshot** at one speed. Episode 7: sweep over
a range of speeds → the **Campbell diagram**.

---

## Visual / Manim notes

- For Scene 4, draw three damped sinusoids on a single `Axes`.
- For Scene 5, render mode shapes from a precomputed
  `rotor_example().run_modal(0).evectors` — extract $x, y$ at each node,
  plot deformed beam vs undeformed, animate orbit at one node.
