"""Shared colours and helpers for the ROSS video series."""

from manim import (
    BLACK,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Arrow,
    Circle,
    DashedLine,
    Line,
    Polygon,
    Rectangle,
    RoundedRectangle,
    Text,
    VGroup,
    config,
)

ROSS_BLUE = "#005BBB"
ROSS_GREEN = "#00A859"
ROSS_GOLD = "#F1C40F"
ROSS_RED = "#E74C3C"
ROSS_GREY = "#7F8C8D"
ROSS_LIGHT = "#ECF0F1"
ROSS_DARK = "#1B1B1B"

DEFAULT_BG = ROSS_DARK


def use_dark_background():
    config.background_color = DEFAULT_BG


def title_text(text, font_size=44, color=ROSS_LIGHT):
    return Text(text, font_size=font_size, color=color, weight="BOLD")


def subtitle_text(text, font_size=28, color=ROSS_GREY):
    return Text(text, font_size=font_size, color=color)


def caption_text(text, font_size=22, color=ROSS_LIGHT):
    return Text(text, font_size=font_size, color=color)


def pipeline_box(label, color=ROSS_BLUE, width=2.6, height=1.3):
    """Rounded box used in the pipeline diagrams."""
    box = RoundedRectangle(
        corner_radius=0.18,
        height=height,
        width=width,
        stroke_color=color,
        stroke_width=3,
        fill_color=color,
        fill_opacity=0.18,
    )
    text = Text(label, font_size=22, color=ROSS_LIGHT, weight="BOLD")
    text.move_to(box.get_center())
    return VGroup(box, text)


def dof_arrow(start, direction, color=ROSS_GOLD, length=0.6):
    end = start + direction * length
    return Arrow(
        start=start,
        end=end,
        buff=0,
        color=color,
        stroke_width=4,
        max_tip_length_to_length_ratio=0.25,
    )


def shaft_outline(left=LEFT * 5, right=RIGHT * 5, radius=0.55, color=ROSS_BLUE):
    """Simple rectangular shaft body between two x-positions."""
    p0 = left + UP * radius
    p1 = right + UP * radius
    p2 = right + DOWN * radius
    p3 = left + DOWN * radius
    body = Polygon(p0, p1, p2, p3, color=color, stroke_width=3, fill_opacity=0.15)
    body.set_fill(color)
    return body


def support_triangle(top, color=ROSS_GREEN, size=0.5):
    p0 = top
    p1 = top + DOWN * size + LEFT * size * 0.7
    p2 = top + DOWN * size + RIGHT * size * 0.7
    return Polygon(p0, p1, p2, color=color, fill_color=color, fill_opacity=0.7)


def disk_shape(center, radius=1.0, thickness=0.25, color=ROSS_GREEN):
    """A simple disk drawn as a thick rectangle (axial profile)."""
    return Rectangle(
        height=2 * radius,
        width=thickness,
        color=color,
        fill_color=color,
        fill_opacity=0.35,
        stroke_width=2,
    ).move_to(center)


def matrix_grid(rows, cols, side=0.32, color=ROSS_GREY):
    """A blank n x n grid of squares used to illustrate matrices."""
    grid = VGroup()
    for r in range(rows):
        for c in range(cols):
            cell = Rectangle(
                height=side,
                width=side,
                stroke_color=color,
                stroke_width=1,
                fill_opacity=0,
            )
            cell.move_to(RIGHT * (c - (cols - 1) / 2) * side
                         + DOWN * (r - (rows - 1) / 2) * side)
            grid.add(cell)
    return grid
