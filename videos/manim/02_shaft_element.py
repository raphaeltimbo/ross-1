"""Episode 02 — Shaft element: the Timoshenko beam.

Render with:
    cd videos
    uv run manim render manim/02_shaft_element.py Episode02 -ql -p
"""

import numpy as np

from manim import (
    DEGREES,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    ORIGIN,
    RIGHT,
    Scene,
    UP,
    Write,
    Arrow,
    Brace,
    Circle,
    Create,
    Dot,
    Indicate,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    SurroundingRectangle,
    Tex,
    Text,
    Transform,
    VGroup,
)

from _theme import (
    ROSS_BLUE,
    ROSS_DARK,
    ROSS_GOLD,
    ROSS_GREEN,
    ROSS_GREY,
    ROSS_LIGHT,
    ROSS_RED,
    caption_text,
    matrix_grid,
    subtitle_text,
    title_text,
    use_dark_background,
)

use_dark_background()


# ---------------------------------------------------------------------------
# helpers specific to this episode
# ---------------------------------------------------------------------------


def shaft_with_nodes(length=7.0, radius=0.5, color=ROSS_BLUE, center=ORIGIN):
    """Return a VGroup with a horizontal shaft body and node markers."""
    body = Rectangle(
        width=length,
        height=2 * radius,
        color=color,
        fill_color=color,
        fill_opacity=0.25,
        stroke_width=3,
    ).move_to(center)
    n0 = Dot(body.get_left(), color=ROSS_GOLD, radius=0.13)
    n1 = Dot(body.get_right(), color=ROSS_GOLD, radius=0.13)
    n0_lbl = Text("node 0", font_size=22, color=ROSS_LIGHT).next_to(n0, DOWN, buff=0.35)
    n1_lbl = Text("node 1", font_size=22, color=ROSS_LIGHT).next_to(n1, DOWN, buff=0.35)
    return VGroup(body, n0, n1, n0_lbl, n1_lbl)


def dof_arrows_at(node_pos, plane="left"):
    """Return six small DOF arrows at a node."""
    arrows = VGroup(
        Arrow(node_pos, node_pos + UP * 0.7, color=ROSS_GOLD, buff=0,
              stroke_width=4, max_tip_length_to_length_ratio=0.25),  # x or y
        Arrow(node_pos, node_pos + RIGHT * 0.7, color=ROSS_GREEN, buff=0,
              stroke_width=4, max_tip_length_to_length_ratio=0.25),  # z (axial)
    )
    return arrows


def legend_item(label, color):
    sq = Rectangle(width=0.4, height=0.3, color=color,
                   fill_color=color, fill_opacity=0.7, stroke_width=2)
    txt = caption_text(label, font_size=22, color=ROSS_LIGHT)
    return VGroup(sq, txt).arrange(RIGHT, buff=0.25, aligned_edge=ORIGIN)


def highlight_block(scene, grid, rows, cols, color, eq_text):
    cells = VGroup()
    for r in rows:
        for c in cols:
            cell = grid[r * 12 + c]
            cells.add(
                Rectangle(
                    height=cell.height,
                    width=cell.width,
                    fill_color=color,
                    fill_opacity=0.55,
                    stroke_width=0,
                ).move_to(cell.get_center())
            )
    eq = MathTex(eq_text, font_size=34, color=color)
    eq.to_edge(DOWN, buff=1.5)
    scene.play(FadeIn(cells), Write(eq))
    scene.wait(1.0)
    scene.play(FadeOut(cells), FadeOut(eq))


# ---------------------------------------------------------------------------
# Chapter Scenes
# ---------------------------------------------------------------------------


class TitleAndPipelineScene(Scene):
    def construct(self):
        title = title_text("Episode 02 — Shaft Element", font_size=46).to_edge(UP, buff=1.0)
        sub = subtitle_text(
            "From a Timoshenko beam to a 12 × 12 mass matrix.",
            font_size=28,
            color=ROSS_GOLD,
        ).next_to(title, DOWN, buff=0.4)
        self.play(Write(title))
        self.play(FadeIn(sub, shift=UP * 0.2))
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, sub)))


class GeometryAndDOFsScene(Scene):
    def construct(self):
        title = title_text("Geometry and 12 degrees of freedom", font_size=34)
        title.to_edge(UP, buff=0.5)
        self.play(Write(title))

        shaft_group = shaft_with_nodes(length=8.0, radius=0.55).move_to(DOWN * 0.5)
        self.play(FadeIn(shaft_group))

        # Length brace below
        brace = Brace(shaft_group[0], DOWN, buff=0.5)
        L_label = MathTex("L", font_size=36, color=ROSS_LIGHT).next_to(brace, DOWN, buff=0.15)
        self.play(Create(brace), Write(L_label))

        # DOF arrows on node 0
        n0 = shaft_group[1].get_center()
        arrows0 = VGroup(
            Arrow(n0, n0 + UP * 1.0, color=ROSS_GOLD, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18),  # y
            Arrow(n0, n0 + LEFT * 1.0, color="#FF6B9D", buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18),  # x (out of page proxy)
            Arrow(n0, n0 + RIGHT * 0.9, color=ROSS_GREEN, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18),  # z axial
        )
        labels0 = VGroup(
            MathTex("y_0", color=ROSS_GOLD, font_size=30).next_to(arrows0[0], UP, buff=0.05),
            MathTex("x_0", color="#FF6B9D", font_size=30).next_to(arrows0[1], LEFT, buff=0.05),
            MathTex("z_0", color=ROSS_GREEN, font_size=30).next_to(arrows0[2], DOWN, buff=0.05),
        )

        n1 = shaft_group[2].get_center()
        arrows1 = VGroup(
            Arrow(n1, n1 + UP * 1.0, color=ROSS_GOLD, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18),
            Arrow(n1, n1 + RIGHT * 1.0, color="#FF6B9D", buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18),
            Arrow(n1, n1 + LEFT * 0.9, color=ROSS_GREEN, buff=0, stroke_width=4,
                  max_tip_length_to_length_ratio=0.18),
        )
        labels1 = VGroup(
            MathTex("y_1", color=ROSS_GOLD, font_size=30).next_to(arrows1[0], UP, buff=0.05),
            MathTex("x_1", color="#FF6B9D", font_size=30).next_to(arrows1[1], RIGHT, buff=0.05),
            MathTex("z_1", color=ROSS_GREEN, font_size=30).next_to(arrows1[2], DOWN, buff=0.05),
        )

        self.play(FadeIn(arrows0), FadeIn(labels0))
        self.play(FadeIn(arrows1), FadeIn(labels1))
        self.wait(0.8)

        # DOF vector
        vec = MathTex(
            r"\mathbf{q}_n = \begin{bmatrix}",
            r"x_n & y_n & z_n & \alpha_n & \beta_n & \theta_n",
            r"\end{bmatrix}^{T}",
            font_size=34,
        ).to_edge(UP, buff=1.4)
        vec.shift(DOWN * 0.4)

        explain = caption_text(
            "x, y lateral · z axial · α, β bending rotations · θ torsion",
            font_size=22,
            color=ROSS_GREY,
        ).next_to(vec, DOWN, buff=0.3)

        self.play(
            FadeOut(VGroup(title, brace, L_label, arrows0, labels0,
                           arrows1, labels1, shaft_group)),
            run_time=0.6,
        )
        title2 = title_text("12 DOFs per element  =  6 per node × 2 nodes",
                            font_size=30).to_edge(UP, buff=0.5)
        self.play(Write(title2))
        self.play(Write(vec))
        self.play(FadeIn(explain, shift=UP * 0.2))

        # ROSS dof_mapping snippet
        snippet = (
            "ross/shaft_element.py:510  dof_mapping():\n"
            "  {x_0: 0, y_0: 1, z_0: 2, alpha_0: 3, beta_0: 4, theta_0: 5,\n"
            "   x_1: 6, y_1: 7, z_1: 8, alpha_1: 9, beta_1:10, theta_1:11}"
        )
        snip = caption_text(snippet, font_size=22, color=ROSS_GREEN)
        snip.next_to(explain, DOWN, buff=0.6)
        self.play(FadeIn(snip))
        self.wait(2.0)

        self.play(FadeOut(VGroup(title2, vec, explain, snip)))


class EulerVsTimoshenkoScene(Scene):
    def construct(self):
        title = title_text("Euler-Bernoulli vs Timoshenko", font_size=34).to_edge(UP, buff=0.5)
        self.play(Write(title))

        # Two beams side by side
        eb_origin = LEFT * 3.5 + DOWN * 0.5
        ti_origin = RIGHT * 3.5 + DOWN * 0.5

        def beam(origin, kind):
            color = ROSS_BLUE if kind == "EB" else ROSS_GREEN
            body = Line(origin + LEFT * 1.6, origin + RIGHT * 1.6,
                        color=color, stroke_width=6)
            sections = VGroup()
            for x in np.linspace(-1.4, 1.4, 5):
                s = Line(
                    origin + RIGHT * x + UP * 0.5,
                    origin + RIGHT * x + DOWN * 0.5,
                    color=ROSS_GREY, stroke_width=2,
                )
                if kind == "TI":
                    s.rotate(15 * DEGREES, about_point=origin + RIGHT * x)
                sections.add(s)
            label = caption_text(
                "Euler-Bernoulli" if kind == "EB" else "Timoshenko",
                font_size=24, color=color,
            ).next_to(body, DOWN, buff=0.7)
            return VGroup(body, sections, label)

        eb = beam(eb_origin, "EB")
        ti = beam(ti_origin, "TI")

        self.play(FadeIn(eb), FadeIn(ti))
        self.wait(1.0)

        eb_note = caption_text(
            "sections perpendicular to the neutral axis",
            font_size=20, color=ROSS_GREY,
        ).next_to(eb, DOWN, buff=0.2)
        ti_note = caption_text(
            "sections rotate freely → shear matters",
            font_size=20, color=ROSS_GREY,
        ).next_to(ti, DOWN, buff=0.2)
        self.play(FadeIn(eb_note), FadeIn(ti_note))
        self.wait(1.5)

        # Show phi
        phi_eq = MathTex(
            r"\varphi = \frac{12\,E\,I}{G_s\,\kappa\,A\,L^{2}}",
            font_size=42,
            color=ROSS_GOLD,
        ).to_edge(UP, buff=1.4)
        phi_caption = caption_text(
            "shear factor — bridges Euler-Bernoulli (φ → 0) and Timoshenko (φ large)",
            font_size=22,
            color=ROSS_LIGHT,
        ).next_to(phi_eq, DOWN, buff=0.25)

        self.play(FadeOut(VGroup(eb, ti, eb_note, ti_note, title)))
        self.play(Write(phi_eq))
        self.play(FadeIn(phi_caption, shift=UP * 0.2))
        self.wait(2.0)

        code_ref = caption_text(
            "ross/shaft_element.py:302   phi = 12 * E * I / (G_s * kappa * A * L**2)",
            font_size=22, color=ROSS_GREEN,
        ).next_to(phi_caption, DOWN, buff=0.6)
        self.play(FadeIn(code_ref))
        self.wait(1.5)
        self.play(FadeOut(VGroup(phi_eq, phi_caption, code_ref)))


class MassMatrixScene(Scene):
    def construct(self):
        title = title_text("Mass matrix M  (12 × 12)", font_size=32).to_edge(UP, buff=0.5)
        self.play(Write(title))

        grid = matrix_grid(12, 12, side=0.36).move_to(LEFT * 3.0 + DOWN * 0.3)
        bracket_l = Tex(r"$[$", font_size=120, color=ROSS_LIGHT)
        bracket_r = Tex(r"$]$", font_size=120, color=ROSS_LIGHT)
        bracket_l.next_to(grid, LEFT, buff=0.05)
        bracket_r.next_to(grid, RIGHT, buff=0.05)

        self.play(FadeIn(grid), FadeIn(bracket_l), FadeIn(bracket_r))
        self.wait(0.4)

        legend = VGroup(
            legend_item("bending mass", ROSS_BLUE),
            legend_item("rotary inertia", ROSS_GOLD),
            legend_item("axial / torsion", ROSS_GREEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        legend.to_edge(RIGHT, buff=1.0).shift(DOWN * 0.3)

        self.play(FadeIn(legend))

        bending_idx = [0, 1, 3, 4, 6, 7, 9, 10]   # x,y,alpha,beta @ both nodes
        axial_idx = [2, 8]
        tors_idx = [5, 11]
        rot_idx = [3, 4, 9, 10]

        highlight_block(self, grid, bending_idx, bending_idx, ROSS_BLUE,
                        eq_text=r"\frac{\rho A L}{1260(1+\varphi)^2}")
        self.wait(0.8)
        highlight_block(self, grid, rot_idx, rot_idx, ROSS_GOLD,
                        eq_text=r"\frac{\rho I_e}{210 L (1+\varphi)^2}")
        self.wait(0.8)
        highlight_block(self, grid, axial_idx, axial_idx, ROSS_GREEN,
                        eq_text=r"\frac{\rho A_e L}{6}\!\begin{bmatrix}2&1\\1&2\end{bmatrix}")
        self.wait(0.6)
        highlight_block(self, grid, tors_idx, tors_idx, ROSS_GREEN,
                        eq_text=r"\frac{\rho J_e L}{6}\!\begin{bmatrix}2&1\\1&2\end{bmatrix}")
        self.wait(1.5)

        code_ref = caption_text(
            "implementation: ross/shaft_element.py:525-722",
            font_size=20, color=ROSS_GREY,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(code_ref))
        self.wait(1.0)
        self.play(FadeOut(VGroup(title, grid, bracket_l, bracket_r, legend, code_ref)))


class StiffnessMatrixScene(Scene):
    def construct(self):
        title = title_text("Stiffness matrix K  (12 × 12)", font_size=32).to_edge(UP, buff=0.5)
        self.play(Write(title))

        contributions = VGroup(
            MathTex(r"K_1 = \frac{E I}{105\,L^3}\,K_{\text{bending}}",
                    font_size=32, color=ROSS_BLUE),
            MathTex(r"K_2 = \frac{\varphi\,E I}{L^3 (1+\varphi)^2}\,K_{\text{shear}}",
                    font_size=32, color=ROSS_GOLD),
            MathTex(r"K_{ax} = \frac{E A}{L}\!\begin{bmatrix}1 & -1\\-1 & 1\end{bmatrix}",
                    font_size=32, color=ROSS_GREEN),
            MathTex(r"K_{ts} = \frac{G_s J}{L}\!\begin{bmatrix}1 & -1\\-1 & 1\end{bmatrix}",
                    font_size=32, color="#FF6B9D"),
        ).arrange(DOWN, buff=0.55).move_to(ORIGIN)

        for c in contributions:
            self.play(Write(c), run_time=0.8)
        self.wait(1.0)

        sum_eq = MathTex(
            r"K = K_1 + K_2 + K_{ax} + K_{ts}",
            font_size=40, color=ROSS_LIGHT,
        ).next_to(contributions, DOWN, buff=0.6)
        self.play(Write(sum_eq))
        self.wait(1.2)

        code_ref = caption_text(
            "implementation: ross/shaft_element.py:724-915",
            font_size=20, color=ROSS_GREY,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(code_ref))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, contributions, sum_eq, code_ref)))


class GyroscopicMatrixScene(Scene):
    def construct(self):
        title = title_text("Gyroscopic matrix G", font_size=34).to_edge(UP, buff=0.5)
        self.play(Write(title))

        eq = MathTex(
            r"\mathbf{G} = \frac{2\,\rho\,I_e}{210\,L\,(1+\varphi)^2}\,\mathbf{G}_0",
            font_size=40, color=ROSS_GOLD,
        )
        eq.shift(UP * 1.0)
        self.play(Write(eq))
        self.wait(0.6)

        skew = MathTex(r"\mathbf{G}^{T} = -\,\mathbf{G}", font_size=42, color=ROSS_LIGHT)
        skew.next_to(eq, DOWN, buff=0.6)
        self.play(Write(skew))
        self.wait(0.6)

        explain = caption_text(
            "Skew-symmetric — couples the (x, β) and (y, α) bending planes "
            "and splits each mode into forward / backward whirl when Ω > 0.",
            font_size=22, color=ROSS_GREY,
        ).next_to(skew, DOWN, buff=0.5)
        self.play(FadeIn(explain, shift=UP * 0.2))
        self.wait(1.5)

        code_ref = caption_text(
            "implementation: ross/shaft_element.py:987-1085",
            font_size=20, color=ROSS_GREY,
        ).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(code_ref))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, eq, skew, explain, code_ref)))


class RecapScene(Scene):
    def construct(self):
        title = title_text("Recap — the shaft element", font_size=36).to_edge(UP, buff=0.6)
        self.play(Write(title))

        bullets = VGroup(
            caption_text("• 12 DOFs per element (6 per node)"),
            caption_text("• φ controls Euler-Bernoulli ↔ Timoshenko"),
            caption_text("• M, K assembled in three layers (bending / rotary / axial-torsion)"),
            caption_text("• G is skew-symmetric → splits whirl modes"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(title, DOWN, buff=0.6)
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.5)

        outro = subtitle_text(
            "Next: the disk element — and where I_p creates whirl-splitting.",
            font_size=26, color=ROSS_GOLD,
        ).to_edge(DOWN, buff=1.0)
        self.play(FadeIn(outro, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, bullets, outro)))


# ---------------------------------------------------------------------------
# Full episode
# ---------------------------------------------------------------------------


class Episode02(Scene):
    def construct(self):
        for klass in (
            TitleAndPipelineScene,
            GeometryAndDOFsScene,
            EulerVsTimoshenkoScene,
            MassMatrixScene,
            StiffnessMatrixScene,
            GyroscopicMatrixScene,
            RecapScene,
        ):
            klass.construct(self)
