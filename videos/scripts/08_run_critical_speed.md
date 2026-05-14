# Video 08 — `run_critical_speed`: Newton's Method on the Campbell Diagram

> **Goal:** show that critical speeds are roots of $\Omega - \omega_n(\Omega) = 0$
> and that ROSS uses `scipy.optimize.newton` initialised from a baseline
> modal analysis to find them precisely.

**Estimated length:** 2–3 min · **Code:** `ross/rotor_assembly.py:893-993`

---

## Scene 1 — Definition (20 s)

A **critical speed** $\Omega^{*}$ is a spin rate at which the synchronous
excitation matches a natural frequency:

$$
\Omega^{*} = \omega_n(\Omega^{*})
$$

Visually: where the synchronous line $\omega = \Omega$ on the Campbell
diagram intersects a mode curve.

## Scene 2 — Reformulate as a root-finding problem (20 s)

Define

$$
f_i(\Omega) = \Omega - \omega_{n,i}(\Omega)
$$

so each critical speed is a root $f_i(\Omega^{*}) = 0$.

## Scene 3 — Newton's method (45 s)

$$
\Omega_{k+1} = \Omega_k - \frac{f_i(\Omega_k)}{f_i'(\Omega_k)}
$$

In ROSS the derivative is approximated numerically by SciPy because each
function evaluation requires a fresh modal analysis — symbolic
differentiation through the eigensolver isn't available.

```python
# ross/rotor_assembly.py:967-972
for i in range(len(wn)):
    wn_func = lambda s: s - self.run_modal(s, num_modes).wn[i]
    wn[i] = newton(func=wn_func, x0=_wn[i], rtol=rtol)
for i in range(len(wd)):
    wd_func = lambda s: s - self.run_modal(s, num_modes).wd[i]
    wd[i] = newton(func=wd_func, x0=_wd[i], rtol=rtol)
```

Two passes:

- $\omega_n$ critical speeds (undamped reference).
- $\omega_d$ critical speeds (damped — slightly different in real machines).

Initial guesses come from a single `run_modal(speed=0)`.

## Scene 4 — Animate Newton on a curve (40 s)

- Draw $f_i(\Omega) = \Omega - \omega_n(\Omega)$.
- Start from $\Omega_0 = \omega_n(0)$.
- Drop a tangent line, intersect the $x$-axis to get $\Omega_1$.
- Repeat 2-3 times until visually converged.

## Scene 5 — Output and pitfalls (20 s)

```python
crit = rotor.run_critical_speed(num_modes=12)
crit.wn, crit.wd, crit.log_dec
```

- Watch out for: poor initial guess if a mode disappears (e.g. heavily
  damped); Newton may converge to the wrong root.

## Scene 6 — Outro (10 s)

- Up next: static analysis — gravity sag and reaction loads.

---

## Visual / Manim notes

- For the Newton animation, use `Axes` with a sample function such as
  $f(\Omega) = \Omega - 200\sqrt{1 + 10^{-6}\Omega^{2}}$ that mimics
  the gentle non-linearity of $\omega_n(\Omega)$.
- Use `Line` for the tangent and `DashedLine` to drop the iterate down
  to the $x$-axis.
