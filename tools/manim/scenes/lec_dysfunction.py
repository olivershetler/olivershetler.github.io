import numpy as np
from manim import (
    Circle,
    Create,
    CubicBezier,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MoveAlongPath,
    Rectangle,
    RIGHT,
    Square,
    Text,
    UP,
    VGroup,
)

from aiqri_palette import ACCENT, INK, MUTED, RULE, BaseScene


def object_icon(position):
    body = Square(side_length=0.42, color=INK, stroke_width=2)
    body.set_fill(RULE, opacity=0.9).move_to(position)
    top = Circle(radius=0.11, color=ACCENT, stroke_width=2).set_fill(ACCENT, opacity=0.8)
    top.next_to(body, UP, buff=0.02)
    return VGroup(body, top)


class LecDysfunction(BaseScene):
    def construct(self):
        rng = np.random.default_rng(13)
        left_center = LEFT * 3.35 + DOWN * 0.05
        right_center = RIGHT * 3.35 + DOWN * 0.05
        object_offset = RIGHT * 1.15 + UP * 0.45
        left_object_position = left_center + object_offset
        right_object_position = right_center + object_offset

        title = Text("How the brain tags what was here", color=INK, font_size=34, weight="BOLD")
        title.to_edge(UP, buff=0.22)
        healthy_title = Text("Healthy LEC", color=INK, font_size=27, weight="BOLD")
        disease_title = Text("Disease LEC", color=ACCENT, font_size=27, weight="BOLD")
        healthy_title.move_to(left_center + UP * 2.55)
        disease_title.move_to(right_center + UP * 2.55)

        arenas = VGroup(
            Rectangle(width=5.65, height=4.25, color=RULE, stroke_width=2).move_to(left_center),
            Rectangle(width=5.65, height=4.25, color=RULE, stroke_width=2).move_to(right_center),
        )
        divider = Line(UP * 2.75, DOWN * 2.85, color=RULE, stroke_width=2)
        objects = VGroup(object_icon(left_object_position), object_icon(right_object_position))
        object_labels = VGroup(
            Text("object", color=INK, font_size=19).next_to(objects[0], DOWN, buff=0.08),
            Text("object", color=INK, font_size=19).next_to(objects[1], DOWN, buff=0.08),
        )

        left_path = CubicBezier(
            left_center + LEFT * 2 + DOWN * 1.25,
            left_center + LEFT * 0.8 + UP * 1.2,
            left_center + RIGHT * 0.2 + DOWN * 0.3,
            left_object_position + LEFT * 0.3,
        ).set_stroke(MUTED, width=2, opacity=0.45)
        right_path = left_path.copy().shift(RIGHT * 6.7)
        mice = VGroup(
            Dot(left_path.get_start(), radius=0.11, color=INK),
            Dot(right_path.get_start(), radius=0.11, color=INK),
        )

        tight_points = [
            left_object_position
            + np.array([rng.normal(0, 0.22), rng.normal(0, 0.22), 0])
            for _ in range(20)
        ]
        tight_cluster = VGroup(
            *[Dot(point, radius=0.065, color=ACCENT, fill_opacity=0.9) for point in tight_points]
        )

        diffuse_points = [
            right_center + np.array([rng.uniform(-2.4, 2.4), rng.uniform(-1.7, 1.7), 0])
            for _ in range(50)
        ]
        diffuse_cloud = VGroup(
            *[Dot(point, radius=0.055, color=ACCENT, fill_opacity=0.68) for point in diffuse_points]
        )

        precise_label = Text("object cell, precise", color=INK, font_size=21, weight="BOLD")
        diffuse_label = Text("diffuse + hyperactive", color=ACCENT, font_size=21, weight="BOLD")
        precise_label.move_to(left_center + DOWN * 1.8)
        diffuse_label.move_to(right_center + DOWN * 1.8)

        self.play(
            FadeIn(title),
            FadeIn(healthy_title),
            FadeIn(disease_title),
            FadeIn(arenas),
            FadeIn(divider),
            FadeIn(objects),
            FadeIn(object_labels),
            run_time=0.9,
        )
        self.play(
            Create(left_path),
            Create(right_path),
            MoveAlongPath(mice[0], left_path),
            MoveAlongPath(mice[1], right_path),
            run_time=1.8,
        )
        self.play(FadeIn(tight_cluster, lag_ratio=0.045), FadeIn(precise_label), run_time=1.4)
        self.play(FadeIn(diffuse_cloud, lag_ratio=0.02), FadeIn(diffuse_label), run_time=1.7)

        trace_cluster = tight_cluster.copy().set_opacity(0.20)
        trace_label = Text("memory trace remains", color=MUTED, font_size=22, weight="BOLD")
        no_trace_label = Text("memory trace absent", color=MUTED, font_size=22)
        trace_label.move_to(left_center + DOWN * 2.52)
        no_trace_label.move_to(right_center + DOWN * 2.52)
        self.play(
            FadeOut(objects),
            FadeOut(object_labels),
            FadeOut(tight_cluster),
            FadeOut(diffuse_cloud),
            FadeOut(precise_label),
            FadeOut(diffuse_label),
            FadeIn(trace_cluster),
            FadeIn(trace_label),
            FadeIn(no_trace_label),
            run_time=1.1,
        )

        punchline = Text(
            "LEC tags objects and traces. In disease, the tag blurs.",
            color=INK,
            font_size=27,
            weight="BOLD",
        )
        punchline.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(punchline), run_time=0.8)
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=1.25)
