import numpy as np
from manim import (
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    ManimColor,
    MoveAlongPath,
    Rectangle,
    RIGHT,
    Square,
    Text,
    UP,
    VGroup,
    VMobject,
    interpolate_color,
)

from aiqri_palette import ACCENT, BG, INK, MUTED, RULE, BaseScene


def signal_y(x, electrode=0):
    slow = 0.34 * np.sin(1.55 * x + electrode * 0.3)
    detail = 0.1 * np.sin(5.4 * x + electrode * 0.7) + 0.035 * np.sin(17.1 * x)
    envelope = np.exp(-((x - 0.35) / 0.6) ** 2)
    ripple = 0.31 * envelope * np.sin(34 * x + electrode * 0.9)
    return slow + detail + ripple


def make_trace(x_min=-5.9, x_max=5.9, y_shift=0, scale_y=1, electrode=0):
    xs = np.linspace(x_min, x_max, 460)
    trace = VMobject(color=INK, stroke_width=2.4)
    trace.set_points_as_corners(
        [np.array([x, y_shift + scale_y * signal_y(x, electrode), 0]) for x in xs]
    )
    return trace


class LfpTools(BaseScene):
    def construct(self):
        title = Text("One signal, two open-source lenses", color=INK, font_size=34, weight="BOLD")
        title.to_edge(UP, buff=0.25)
        baseline = Line(LEFT * 6, RIGHT * 6, color=RULE, stroke_width=2)
        trace = make_trace()
        trace_label = Text("local field potential", color=MUTED, font_size=22)
        trace_label.next_to(baseline, DOWN, buff=0.65).align_to(baseline, LEFT)
        cursor = Dot(trace.get_start(), radius=0.07, color=ACCENT)

        self.play(FadeIn(title), FadeIn(baseline), FadeIn(trace_label), run_time=0.7)
        self.play(Create(trace), MoveAlongPath(cursor, trace), run_time=2.2)

        ripple_box = Rectangle(width=1.65, height=1.45, color=ACCENT, stroke_width=3)
        ripple_box.move_to(RIGHT * 0.35)
        time_label = Text("hfoGUI: ripples, time", color=ACCENT, font_size=27, weight="BOLD")
        time_label.next_to(ripple_box, UP, buff=0.2)
        self.play(Create(ripple_box), FadeIn(time_label), run_time=0.9)
        self.wait(0.7)

        left_panel = Rectangle(width=5.8, height=3.75, color=RULE, stroke_width=2)
        right_panel = left_panel.copy()
        left_panel.move_to(LEFT * 3.2 + DOWN * 0.35)
        right_panel.move_to(RIGHT * 3.2 + DOWN * 0.35)
        time_head = Text("hfoGUI", color=ACCENT, font_size=27, weight="BOLD")
        time_sub = Text("detect events across time", color=MUTED, font_size=20)
        time_heading = VGroup(time_head, time_sub).arrange(DOWN, buff=0.08)
        time_heading.move_to(left_panel.get_top() + DOWN * 0.48)
        mini_trace = trace.copy().scale(0.43).move_to(left_panel.get_center() + DOWN * 0.2)
        mini_box = Rectangle(width=0.78, height=0.72, color=ACCENT, stroke_width=2)
        mini_box.move_to(mini_trace.get_center() + RIGHT * 0.18)

        space_head = Text("SSM", color=ACCENT, font_size=27, weight="BOLD")
        space_sub = Text("power across space", color=MUTED, font_size=20)
        space_heading = VGroup(space_head, space_sub).arrange(DOWN, buff=0.08)
        space_heading.move_to(right_panel.get_top() + DOWN * 0.48)

        stacked = VGroup()
        for index in range(4):
            small = make_trace(-2.1, 2.1, electrode=index, scale_y=0.27)
            small.scale(0.42).move_to(
                right_panel.get_center() + LEFT * 1.45 + UP * (0.55 - index * 0.38)
            )
            stacked.add(small)

        heatmap = VGroup()
        bg_color = ManimColor(BG)
        accent_color = ManimColor(ACCENT)
        for row in range(5):
            for column in range(6):
                hotspot = np.exp(-((row - 2.8) ** 2 / 2.4 + (column - 3.1) ** 2 / 3.2))
                color = interpolate_color(bg_color, accent_color, 0.12 + 0.88 * hotspot)
                cell = Square(side_length=0.31, stroke_color=RULE, stroke_width=0.8)
                cell.set_fill(color, opacity=1)
                cell.move_to(RIGHT * column * 0.31 + DOWN * row * 0.31)
                heatmap.add(cell)
        heatmap.move_to(right_panel.get_center() + RIGHT * 1.35 + DOWN * 0.25)
        axes_labels = VGroup(
            Text("frequency", color=MUTED, font_size=16).next_to(heatmap, UP, buff=0.08),
            Text("space", color=MUTED, font_size=16).next_to(heatmap, LEFT, buff=0.08),
        )

        self.play(
            FadeOut(baseline),
            FadeOut(trace),
            FadeOut(trace_label),
            FadeOut(cursor),
            FadeOut(ripple_box),
            FadeOut(time_label),
            FadeIn(left_panel),
            FadeIn(right_panel),
            FadeIn(time_heading),
            FadeIn(space_heading),
            FadeIn(mini_trace),
            FadeIn(mini_box),
            run_time=1.2,
        )
        self.play(Create(stacked), FadeIn(heatmap, lag_ratio=0.025), FadeIn(axes_labels), run_time=1.6)

        punchline = Text(
            "Time and space, both open source.",
            color=INK,
            font_size=29,
            weight="BOLD",
        )
        punchline.to_edge(DOWN, buff=0.18)
        self.play(FadeIn(punchline), run_time=0.7)
        self.wait(1.8)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=1.25)
