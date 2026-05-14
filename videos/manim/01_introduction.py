"""Episode 01 — Introduction: the ROSS pipeline.

Render with:
    cd videos
    uv run manim render manim/01_introduction.py -ql -p

The file exposes one ``Episode01`` Scene that plays the full storyboard,
plus individual Scenes for each chapter so they can be rendered in
isolation while iterating.
"""

from manim import (
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
    MathTex,
    Paragraph,
    Tex,
    Text,
    VGroup,
)

from _theme import (
    ROSS_BLUE,
    ROSS_DARK,
    ROSS_GOLD,
    ROSS_GREEN,
    ROSS_GREY,
    ROSS_LIGHT,
    caption_text,
    pipeline_box,
    subtitle_text,
    title_text,
    use_dark_background,
)

use_dark_background()


# ---------------------------------------------------------------------------
# Chapter Scenes
# ---------------------------------------------------------------------------


class TitleScene(Scene):
    """Scene 1 — Title card."""

    def construct(self):
        title = title_text("How ROSS Works", font_size=64).to_edge(UP, buff=1.5)
        episode = subtitle_text("Episode 01 — The Pipeline", font_size=36)
        episode.next_to(title, DOWN, buff=0.4)
        tagline = caption_text(
            "From geometry to rotordynamic answers.",
            font_size=26,
            color=ROSS_GOLD,
        )
        tagline.next_to(episode, DOWN, buff=0.8)

        self.play(Write(title))
        self.play(FadeIn(episode, shift=UP * 0.2))
        self.play(FadeIn(tagline, shift=UP * 0.2))
        self.wait(1.5)
        self.play(FadeOut(VGroup(title, episode, tagline)))


class WhyRotordynamicsScene(Scene):
    """Scene 2 — Why rotordynamics?"""

    def construct(self):
        question = title_text(
            "Will this rotor vibrate dangerously when it spins?",
            font_size=32,
            color=ROSS_GOLD,
        )
        question.to_edge(UP, buff=1.0)

        bullets = VGroup(
            caption_text("• Natural frequencies and whirl direction"),
            caption_text("• Critical speeds (resonances with rotation)"),
            caption_text("• Forced response under unbalance and loads"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        bullets.next_to(question, DOWN, buff=1.0)

        self.play(Write(question))
        for b in bullets:
            self.play(FadeIn(b, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(1.5)
        self.play(FadeOut(VGroup(question, bullets)))


class DiscretizationScene(Scene):
    """Scene 3 — The continuous rotor becomes a chain of finite elements."""

    def construct(self):
        title = title_text("Finite Element Discretisation", font_size=34)
        title.to_edge(UP, buff=0.6)
        self.play(Write(title))

        # Smooth rotor: a single thick rectangle representing the whole shaft.
        from manim import Rectangle, Polygon
        shaft = Rectangle(
            width=8.0,
            height=0.7,
            color=ROSS_BLUE,
            fill_color=ROSS_BLUE,
            fill_opacity=0.25,
            stroke_width=3,
        ).move_to(DOWN * 0.5)

        smooth_label = caption_text("continuous shaft", font_size=22, color=ROSS_GREY)
        smooth_label.next_to(shaft, DOWN, buff=0.4)

        self.play(FadeIn(shaft), FadeIn(smooth_label))
        self.wait(1.0)

        # Discretised: 6 small shaft elements + 2 disks + 2 supports
        self.play(FadeOut(smooth_label))
        n_elements = 6
        elem_w = 8.0 / n_elements
        elements = VGroup()
        for i in range(n_elements):
            cell = Rectangle(
                width=elem_w * 0.94,
                height=0.7,
                color=ROSS_BLUE,
                fill_color=ROSS_BLUE,
                fill_opacity=0.4,
                stroke_width=2,
            )
            cell.move_to(shaft.get_left() + RIGHT * (elem_w * (i + 0.5)))
            elements.add(cell)

        disks = VGroup(
            Rectangle(width=0.3, height=1.6, color=ROSS_GREEN,
                      fill_color=ROSS_GREEN, fill_opacity=0.55,
                      stroke_width=2).move_to(shaft.get_left() + RIGHT * (elem_w * 2)),
            Rectangle(width=0.3, height=1.9, color=ROSS_GREEN,
                      fill_color=ROSS_GREEN, fill_opacity=0.55,
                      stroke_width=2).move_to(shaft.get_left() + RIGHT * (elem_w * 4)),
        )

        supports = VGroup(
            Polygon(
                shaft.get_left() + DOWN * 0.35,
                shaft.get_left() + DOWN * 0.95 + LEFT * 0.4,
                shaft.get_left() + DOWN * 0.95 + RIGHT * 0.4,
                color=ROSS_GOLD, fill_color=ROSS_GOLD, fill_opacity=0.7,
            ),
            Polygon(
                shaft.get_right() + DOWN * 0.35,
                shaft.get_right() + DOWN * 0.95 + LEFT * 0.4,
                shaft.get_right() + DOWN * 0.95 + RIGHT * 0.4,
                color=ROSS_GOLD, fill_color=ROSS_GOLD, fill_opacity=0.7,
            ),
        )

        self.play(FadeOut(shaft), FadeIn(elements), run_time=1.0)
        self.play(FadeIn(disks), FadeIn(supports), run_time=0.8)

        legend = VGroup(
            caption_text("shaft elements", font_size=20, color=ROSS_BLUE),
            caption_text("disk elements", font_size=20, color=ROSS_GREEN),
            caption_text("bearings / supports", font_size=20, color=ROSS_GOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_corner(DOWN + LEFT, buff=0.6)

        self.play(FadeIn(legend))
        self.wait(1.0)

        # Master equation on top half
        eq = MathTex(
            r"\mathbf{M}\,\ddot{\mathbf{q}}",
            r"+",
            r"(\mathbf{C} + \Omega\,\mathbf{G})\,\dot{\mathbf{q}}",
            r"+",
            r"\mathbf{K}\,\mathbf{q}",
            r"=",
            r"\mathbf{f}(t)",
            font_size=42,
        )
        eq.set_color_by_tex(r"\mathbf{M}", ROSS_GREEN)
        eq.set_color_by_tex(r"\mathbf{C}", ROSS_GOLD)
        eq.set_color_by_tex(r"\mathbf{G}", "#FF6B9D")
        eq.set_color_by_tex(r"\mathbf{K}", ROSS_BLUE)
        eq.set_color_by_tex(r"\mathbf{f}", ROSS_LIGHT)
        eq.next_to(title, DOWN, buff=0.6)

        self.play(FadeOut(elements), FadeOut(disks), FadeOut(supports), FadeOut(legend))
        self.play(Write(eq))

        labels = VGroup(
            caption_text("M  mass", font_size=20, color=ROSS_GREEN),
            caption_text("C  damping", font_size=20, color=ROSS_GOLD),
            caption_text("G  gyroscopic (× spin speed Ω)",
                         font_size=20, color="#FF6B9D"),
            caption_text("K  stiffness", font_size=20, color=ROSS_BLUE),
            caption_text("f  applied force", font_size=20, color=ROSS_LIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(eq, DOWN, buff=0.8)

        self.play(FadeIn(labels, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(VGroup(title, eq, labels)))


class PipelineScene(Scene):
    """Scene 4 — The four-box pipeline."""

    def construct(self):
        title = title_text("The ROSS pipeline", font_size=36).to_edge(UP, buff=0.6)
        self.play(Write(title))

        boxes = [
            ("Elements\n(M, K, C, G)", ROSS_BLUE),
            ("Rotor\n(global M, K, C, G)", ROSS_GREEN),
            ("run_*()\nalgorithm", ROSS_GOLD),
            ("Results\n.plot_*()", "#9B59B6"),
        ]

        groups = VGroup()
        gap = 3.4
        for i, (label, color) in enumerate(boxes):
            g = pipeline_box(label, color=color, width=2.7, height=1.6)
            g.move_to(LEFT * (1.5 * gap) + RIGHT * gap * i)
            groups.add(g)

        groups.scale(0.9).move_to(ORIGIN)

        arrows = VGroup()
        for i in range(3):
            a = Arrow(
                start=groups[i].get_right() + RIGHT * 0.05,
                end=groups[i + 1].get_left() + LEFT * 0.05,
                color=ROSS_LIGHT,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.18,
                buff=0.15,
            )
            arrows.add(a)

        for i, group in enumerate(groups):
            self.play(FadeIn(group, shift=RIGHT * 0.3), run_time=0.6)
            if i < len(arrows):
                self.play(FadeIn(arrows[i]), run_time=0.4)
        self.wait(1.0)

        # Code snippet under the pipeline (rendered as a monospace Paragraph
        # to avoid the 0.20.1 Code mobject bug with multiline blocks).
        code_lines = [
            "import ross as rs",
            "",
            "steel    = rs.Material('steel', rho=7810, E=211e9, G_s=81.2e9)",
            "shaft    = [rs.ShaftElement(L=0.05, idl=0, odl=0.05,",
            "                            material=steel) for _ in range(6)]",
            "disks    = [rs.DiskElement.from_geometry(n=2, ...)]",
            "bearings = [rs.BearingElement(n=0, kxx=1e6, cxx=0),",
            "            rs.BearingElement(n=6, kxx=1e6, cxx=0)]",
            "",
            "rotor = rs.Rotor(shaft, disks, bearings)",
            "modal = rotor.run_modal(speed=0)",
            "modal.plot_mode_2d(0)",
        ]
        code = Paragraph(
            *code_lines,
            font="DejaVu Sans Mono",
            font_size=18,
            color=ROSS_LIGHT,
            line_spacing=0.6,
        )
        from manim import Rectangle
        bg = Rectangle(
            width=code.width + 0.6,
            height=code.height + 0.4,
            stroke_color=ROSS_GREY,
            stroke_width=1.5,
            fill_color="#0F0F0F",
            fill_opacity=0.95,
        ).move_to(code.get_center())
        code_group = VGroup(bg, code).next_to(groups, DOWN, buff=0.7)

        self.play(FadeIn(code_group, shift=UP * 0.2))
        self.wait(2.5)
        self.play(FadeOut(VGroup(title, groups, arrows, code)))


class SeriesOutlineScene(Scene):
    """Scene 5 — Roadmap of the rest of the series."""

    def construct(self):
        title = title_text("What's coming up", font_size=38).to_edge(UP, buff=0.6)
        self.play(Write(title))

        rows = [
            ("02", "Shaft element — Timoshenko beam"),
            ("03", "Disk element"),
            ("04", "Bearing element"),
            ("05", "Global matrix assembly"),
            ("06", "run_modal"),
            ("07", "run_campbell"),
            ("08", "run_critical_speed"),
            ("09", "run_static"),
            ("10", "run_unbalance_response / run_freq_response"),
            ("11", "run_time_response"),
            ("12", "run_ucs / run_level1"),
        ]

        items = VGroup()
        for num, label in rows:
            num_t = caption_text(num, font_size=22, color=ROSS_GOLD)
            label_t = caption_text(label, font_size=22, color=ROSS_LIGHT)
            row = VGroup(num_t, label_t).arrange(RIGHT, buff=0.6, aligned_edge=ORIGIN)
            items.add(row)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(title, DOWN, buff=0.6)
        items.scale(0.9)

        for row in items:
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=0.18)

        self.wait(2.0)
        self.play(FadeOut(VGroup(title, items)))


class OutroScene(Scene):
    """Scene 6 — Outro."""

    def construct(self):
        line1 = title_text("Next: the shaft element", font_size=42)
        line2 = subtitle_text(
            "How a single beam becomes a 12 × 12 mass matrix.",
            font_size=28,
            color=ROSS_GOLD,
        )
        line2.next_to(line1, DOWN, buff=0.5)

        self.play(Write(line1))
        self.play(FadeIn(line2, shift=UP * 0.2))
        self.wait(2.0)
        self.play(FadeOut(VGroup(line1, line2)))


# ---------------------------------------------------------------------------
# Full episode that plays everything in order. Render with:
#   uv run manim render manim/01_introduction.py Episode01 -ql
# ---------------------------------------------------------------------------


class Episode01(Scene):
    """Plays all chapter scenes back to back."""

    def construct(self):
        for klass in (
            TitleScene,
            WhyRotordynamicsScene,
            DiscretizationScene,
            PipelineScene,
            SeriesOutlineScene,
            OutroScene,
        ):
            klass.construct(self)
