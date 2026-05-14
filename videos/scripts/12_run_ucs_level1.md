# Video 12 — `run_ucs` and `run_level1`: Stability Sweeps

> **Goal:** close the series with the two API-617-flavoured analyses:
> the **undamped critical speed map** (sweep bearing stiffness) and the
> **Level 1 stability** screening (sweep cross-coupled stiffness $Q$ and
> watch the log decrement).

**Estimated length:** 4 min · **Code:** `ross/rotor_assembly.py:3173-3441`

---

## Scene 1 — Undamped Critical Speed Map (UCS) (60 s)

Question: *"How does my critical speed change if my bearing stiffness
changes?"*

Procedure:

```python
# ross/rotor_assembly.py:3217-3268 (paraphrased)
stiffness_log = np.logspace(*stiffness_range, num=num)
for i, k in enumerate(stiffness_log):
    bearings = [BearingElement(b.n, kxx=k, cxx=0) for b in self.bearing_elements]
    rotor = Rotor(self.shaft_elements, self.disk_elements, bearings)
    modal = rotor.run_modal(speed=0, num_modes=num_modes)
    rotor_wn[:, i] = modal.wn[::2]   # forward modes
```

- Log-sweep $k$ from soft (e.g. $10^{5}$) to stiff (e.g. $10^{10}$ N/m).
- Plot $\omega_n$ vs $k$ (log-log axes).
- Overlay the actual bearing dynamic stiffness $k(\omega)$ as a separate
  curve — intersections with each mode line give critical speeds.

Animation: slide the curve $k(\omega)$ left/right; the intersections
mark on the rotor where the critical speeds will fall.

## Scene 2 — Level 1 Stability Screening (90 s)

API-617 / API-684 ask: *"How much extra cross-coupled stiffness can the
machine tolerate before the first forward mode goes unstable?"*

Procedure:

```python
# ross/rotor_assembly.py:3424-3440 (paraphrased)
stiffness = np.linspace(*stiffness_range, num)
for i, Q in enumerate(stiffness):
    bearings = [copy(b) for b in self.bearing_elements]
    cc = bearings[0].__class__(n=n, kxx=0, cxx=0, kxy=Q, kyx=-Q)
    bearings.append(cc)
    rotor = self.__class__(self.shaft_elements, self.disk_elements, bearings)
    modal = rotor.run_modal(speed=speed)
    non_backward = modal.whirl_direction() != "Backward"
    log_dec[i] = modal.log_dec[non_backward][0]
```

- Add a virtual cross-coupled bearing at node $n$ with
  $k_{xy} = Q,\;k_{yx} = -Q$.
- Sweep $Q$ over a positive range.
- Track the **first non-backward** log decrement $\delta$.
- Where $\delta$ crosses zero, the rotor becomes unstable.

The reported quantity is the cross-coupling $Q_0$ at $\delta = 0$ — the
**stability margin** in N/m.

## Scene 3 — Plotting both (30 s)

- UCS: log-log natural-frequency vs bearing-stiffness plot, with the
  bearing curve overlay.
- Level 1: log decrement vs $Q$, threshold line at $\delta = 0$, marker
  at the crossing.

## Scene 4 — Wrap-up of the series (40 s)

A compact recap:

- Episodes 02–04: building blocks (shaft / disk / bearing matrices).
- Episode 05: assembly into $\mathbf{M}, \mathbf{K}, \mathbf{C}, \mathbf{G}$.
- Episodes 06–08: modal family (modal, Campbell, critical speed).
- Episode 09: static.
- Episodes 10–11: forced response & time integration.
- Episode 12: design-screening tools.

> *"From a few elements with simple matrices, ROSS builds the full
> rotordynamic toolkit by composition."*

## Scene 5 — Outro (10 s)

- Repository, docs, contribution links.
- Thanks for watching.

---

## Visual / Manim notes

- For UCS, plot in **log scale** explicitly via `Axes(scaling=LogBase())`.
- For Level 1, animate the log-decrement curve being drawn left-to-right;
  zero-crossing flashes red.
