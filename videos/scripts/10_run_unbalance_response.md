# Video 10 — `run_freq_response` and `run_unbalance_response`

> **Goal:** explain the frequency-response transfer matrix
> $\mathbf{H}(\omega) = (-\omega^{2}\mathbf{M} + j\omega\mathbf{C} + \mathbf{K})^{-1}$,
> show how ROSS computes it via LU factorisation, and how an unbalance is
> turned into a centrifugal forcing $\mathbf{F}(\omega) = \omega^{2}\mathbf{b}_0$.

**Estimated length:** 5 min · **Code:** `ross/rotor_assembly.py:1599-1761`, `2064-2269`

---

## Scene 1 — From EOM to $\mathbf{H}(\omega)$ (45 s)

Steady harmonic motion: $\mathbf{q}(t) = \mathbf{Q}(\omega)\,e^{j\omega t}$,
$\mathbf{f}(t) = \mathbf{F}(\omega)\,e^{j\omega t}$.

Substitute into the EOM:

$$
\big[-\omega^{2}\mathbf{M} + j\omega(\mathbf{C} + \Omega\mathbf{G}) + \mathbf{K}\big]\,\mathbf{Q}(\omega) = \mathbf{F}(\omega)
$$

Define the **dynamic stiffness**:

$$
\mathbf{Z}(\omega, \Omega) = -\omega^{2}\mathbf{M} + j\omega(\mathbf{C} + \Omega\mathbf{G}) + \mathbf{K}
$$

The transfer matrix is its inverse:

$$
\mathbf{H}(\omega, \Omega) = \mathbf{Z}(\omega, \Omega)^{-1}
$$

## Scene 2 — Implementation: LU factorise, don't invert (45 s)

ROSS never explicitly inverts. It LU-factorises and back-substitutes
against the identity matrix:

```python
# ross/rotor_assembly.py:1599-1606 (paraphrased)
I = np.eye(self.M().shape[0])
lu, piv = lu_factor(
    -(omega**2) * self.M(frequency=speed)
    + 1j * omega * (self.C(frequency=speed) + speed * self.G())
    + self.K(frequency=speed)
)
H = lu_solve((lu, piv), I)
```

Why? Solving $\mathbf{Z}\mathbf{x} = \mathbf{F}$ for many right-hand
sides (one per excited DOF, all collected as columns of $\mathbf{I}$) is
much cheaper and more accurate than computing $\mathbf{Z}^{-1}$ outright.

## Scene 3 — Sweeping over $\omega$ (30 s)

```python
# ross/rotor_assembly.py:1743-1751
for i, omega in enumerate(speed_range):
    H = transfer_matrix(omega)
    freq_resp[..., i] = H
    velc_resp[..., i] = 1j * omega * H
    accl_resp[..., i] = -(omega ** 2) * H
```

Output is a 3D array of shape `(ndof, ndof, n_freq)`.

Visualise: animate a 2D `Axes` of `|H_{ij}(ω)|` vs $\omega$ for one
chosen pair of DOFs; mark the resonance peaks where eigenvalues lie.

## Scene 4 — Unbalance as a force (60 s)

A residual mass $m$ at radius $\varepsilon$ on the spinning rotor produces
a rotating centrifugal force whose components in stationary $x, y$ are

$$
F_x(t) = m\,\varepsilon\,\Omega^{2}\cos(\Omega t + \varphi),\quad
F_y(t) = m\,\varepsilon\,\Omega^{2}\sin(\Omega t + \varphi)
$$

In complex form on the $x, y$ DOFs of the unbalance node $n$:

$$
\mathbf{b}_0 = m\,\varepsilon\,e^{j\varphi}\begin{bmatrix} 1 \\ -j \end{bmatrix},
\qquad
\mathbf{F}_n(\omega) = \omega^{2}\,\mathbf{b}_0
$$

Code:

```python
# ross/rotor_assembly.py:2064-2076 (paraphrased)
b0 = np.zeros(number_dof, dtype=complex)
b0[0] = magnitude * np.exp(1j * phase)        # x component
b0[1] = -1j * magnitude * np.exp(1j * phase)  # y component
n0, n1 = number_dof * node, number_dof * node + number_dof
for i, w in enumerate(omega):
    F0[n0:n1, i] += w**2 * b0
```

`magnitude` here is $m\,\varepsilon$ in **kg·m**.

## Scene 5 — Putting it together (30 s)

```python
# ross/rotor_assembly.py:2249-2257
force = sum(self._unbalance_force(n, m, p, omega)
            for n, m, p in zip(node, magnitude, phase))
forced = self.run_forced_response(force=force, speed_range=omega, ...)
```

`run_unbalance_response` is `run_freq_response` + the unbalance force
construction.

## Scene 6 — Bode plot tour (30 s)

Show the four standard plots from `ForcedResponseResults`:

- Magnitude $|Q_i(\omega)|$
- Phase $\angle Q_i(\omega)$
- Bode (combined)
- Deflected shape at one $\omega$

Resonance peaks line up with critical speeds from Episode 8 — that's the
physical confirmation of the modal analysis.

## Scene 7 — Outro (10 s)

- Frequency-domain story is complete.
- Up next: time-domain integration with Newmark-β.

---

## Visual / Manim notes

- Use `MathTex` with `set_color_by_tex` for $\omega$ vs $\Omega$ — they
  are visually similar but mean different things.
- For the Bode plot, generate a (frequency, magnitude) array offline
  from `rotor_example().run_unbalance_response(...)` and plot via
  `Axes.plot_line_graph`.
