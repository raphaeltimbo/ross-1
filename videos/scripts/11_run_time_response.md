# Video 11 — `run_time_response`: Time-Domain Integration

> **Goal:** explain the two integrator paths inside `run_time_response`
> (LTI shortcut via `scipy.signal.lsim` and the Newmark-β solver in
> `ross/utils.py`) and visualise the predictor / corrector update.

**Estimated length:** 4 min · **Code:** `ross/rotor_assembly.py:3447-3509`,
`ross/utils.py:718-884`

---

## Scene 1 — When time-domain? (15 s)

Use frequency response when the rotor is operating in steady state. Use
time-domain when:

- Rotor speed is **changing** (run-up, coast-down).
- Forcing is non-harmonic (impulse, transient blade-loss).
- Faults (rubbing, misalignment, crack) introduce non-linearity.

## Scene 2 — The equation again (15 s)

$$
\mathbf{M}\ddot{\mathbf{q}} + (\mathbf{C} + \Omega(t)\,\mathbf{G})\dot{\mathbf{q}} + \mathbf{K}\mathbf{q} = \mathbf{F}(t)
$$

If $\Omega$ is constant and $\mathbf{F}$ is a known time series, the
system is linear time-invariant.

## Scene 3 — Two paths (30 s)

```python
# ross/rotor_assembly.py:2829-2835
if isinstance(speed, Iterable) or method.lower() == "newmark":
    t_, yout = self.integrate_system(speed, F, t, **kwargs)
else:
    lti = self._lti(speed)
    return signal.lsim(lti, F, t, X0=ic)
```

- **LTI shortcut**: `scipy.signal.lsim` handles constant-speed cases
  efficiently using the state-space representation.
- **Newmark-β**: required when the speed (and therefore $\mathbf{G}$ in
  the EOM) varies with time.

## Scene 4 — Newmark-β predictor / corrector (90 s)

For step $t_n \to t_{n+1}$ with $\Delta t = t_{n+1} - t_n$:

**Predictor** (advance state with current acceleration):

$$
\dot{\mathbf{q}}^{p} = \dot{\mathbf{q}}_n + (1-\gamma)\,\Delta t\,\ddot{\mathbf{q}}_n
$$

$$
\mathbf{q}^{p} = \mathbf{q}_n + \Delta t\,\dot{\mathbf{q}}_n + \big(\tfrac{1}{2} - \beta\big)\,\Delta t^{2}\,\ddot{\mathbf{q}}_n
$$

**Corrector** (Newton-Raphson loop on residual):

$$
\Delta\ddot{\mathbf{q}} = \big[\mathbf{M} + \gamma\,\Delta t\,\mathbf{C} + \beta\,\Delta t^{2}\,\mathbf{K}\big]^{-1}\,\mathbf{r}
$$

$$
\ddot{\mathbf{q}} \mathrel{+}= \Delta\ddot{\mathbf{q}}, \quad
\dot{\mathbf{q}} \mathrel{+}= \gamma\,\Delta t\,\Delta\ddot{\mathbf{q}}, \quad
\mathbf{q} \mathrel{+}= \beta\,\Delta t^{2}\,\Delta\ddot{\mathbf{q}}
$$

Default coefficients: $\beta = 1/4$, $\gamma = 1/2$ (constant-average
acceleration → unconditionally stable).

```python
# ross/utils.py:718-817 (paraphrased)
ydot = ydot0 + y2dot0 * (1 - gamma) * dt
y    = y0 + ydot0 * dt + y2dot0 * (0.5 - beta) * dt**2

# inside Newton-Raphson loop:
dy2dot = la.solve(M + C * gamma * dt + K * beta * dt**2, residual)
y2dot += dy2dot
ydot  += dy2dot * gamma * dt
y     += dy2dot * beta * dt**2
```

The "effective stiffness" matrix $\mathbf{M} + \gamma\Delta t\,\mathbf{C} + \beta\Delta t^{2}\mathbf{K}$ is factorised once per step (or, for
constant $\Delta t$ and linear systems, even once per simulation).

## Scene 5 — Visualise the update (30 s)

Plot the displacement at one node over a few time steps:

- Start with $\mathbf{q}_n, \dot{\mathbf{q}}_n, \ddot{\mathbf{q}}_n$.
- Draw the predictor (a single jump).
- Draw the correction back to the true trajectory.
- Highlight that bigger $\Delta t$ → more correction work but the same
  stability for $\beta = 1/4, \gamma = 1/2$.

## Scene 6 — Code & outputs (15 s)

```python
t = np.linspace(0, 1, 5000)
F = np.zeros((len(t), rotor.ndof))
F[:, 4] = 100 * np.sin(2*np.pi*60*t)
res = rotor.run_time_response(speed=Q_(3000,"RPM").to("rad/s").m, F=F, t=t)
res.plot_1d(probe=(2, 1))
res.plot_dfft(probe=(2, 1))
```

## Scene 7 — Outro (10 s)

- One last family: stability sweeps with `run_ucs` and `run_level1`.

---

## Visual / Manim notes

- The Newmark animation can re-use a simple SDOF mass-spring as a
  surrogate for the matrix update, then expand to the matrix form.
- DFFT is a frequency analysis of the time signal — could spawn a
  short side panel showing the FFT magnitude.
