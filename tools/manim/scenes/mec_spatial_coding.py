import numpy as np
from manim import (
    Arrow,
    Circle,
    Create,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    Line,
    MathTex,
    MoveAlongPath,
    Rectangle,
    RIGHT,
    Square,
    Text,
    Transform,
    UP,
    VGroup,
    VMobject,
)

from aiqri_palette import ACCENT, BG, INK, MUTED, RULE, BaseScene


STABLE = "#2E7D5B"
DISORDERED = "#A6321E"


def arena(center):
    box = Rectangle(width=5.65, height=4.25, color=RULE, stroke_width=2)
    return box.set_fill(BG, opacity=0.45).move_to(center)


def trajectory(center):
    points = [
        (-2.15, -1.45),
        (-1.45, -0.75),
        (-1.9, 0.35),
        (-0.9, 1.35),
        (0.15, 0.65),
        (1.35, 1.35),
        (2.05, 0.25),
        (1.1, -0.45),
        (1.75, -1.4),
        (0.3, -1.05),
        (-0.45, -0.25),
        (-1.55, -1.25),
    ]
    path = VMobject(color=MUTED, stroke_width=2.2, stroke_opacity=0.55)
    path.set_points_smoothly([center + np.array([x, y, 0]) for x, y in points])
    return path


def heatmap(center, peaks):
    frame = Square(side_length=2.05, color=RULE, stroke_width=2)
    frame.set_fill(BG, opacity=0.55).move_to(center)
    grid = VGroup(
        *[
            Line(
                center + np.array([offset, -1.02, 0]),
                center + np.array([offset, 1.02, 0]),
                color=RULE,
                stroke_width=1,
            )
            for offset in (-0.51, 0, 0.51)
        ],
        *[
            Line(
                center + np.array([-1.02, offset, 0]),
                center + np.array([1.02, offset, 0]),
                color=RULE,
                stroke_width=1,
            )
            for offset in (-0.51, 0, 0.51)
        ],
    )
    fields = VGroup()
    for x, y in peaks:
        peak = center + np.array([x, y, 0])
        fields.add(
            Circle(radius=0.42, stroke_width=0, fill_color=ACCENT, fill_opacity=0.12).move_to(peak),
            Circle(radius=0.27, stroke_width=0, fill_color=ACCENT, fill_opacity=0.24).move_to(peak),
            Circle(radius=0.12, stroke_width=0, fill_color=ACCENT, fill_opacity=0.68).move_to(peak),
        )
    return VGroup(frame, grid, fields)


def stability_panel(center, title_text, observed_offset, status_text, status_color):
    frame = Rectangle(width=5.95, height=3.55, color=RULE, stroke_width=2)
    frame.set_fill(BG, opacity=0.36).move_to(center)
    title = Text(title_text, color=INK, font_size=24, weight="BOLD")
    title.move_to(center + UP * 1.43)
    null_label = Text(
        "chance: mismatched cells",
        color=MUTED,
        font_size=19,
        weight="BOLD",
    ).move_to(center + UP * 0.93)
    axis_y = center[1] + 0.05
    axis = Line(
        center + np.array([-2.35, 0.05, 0]),
        center + np.array([2.35, 0.05, 0]),
        color=MUTED,
        stroke_width=2,
    )
    axis_label = Text("EMD", color=MUTED, font_size=16).move_to(
        center + np.array([2.58, -0.20, 0])
    )
    null_offsets = [
        (-0.55, 0), (-0.30, 0), (-0.05, 0), (0.20, 0), (0.45, 0),
        (0.70, 0), (0.95, 0), (1.20, 0), (1.45, 0), (1.70, 0),
        (-0.05, 1), (0.20, 1), (0.45, 1), (0.70, 1), (0.95, 1),
        (1.20, 1), (0.20, 2), (0.45, 2), (0.70, 2), (0.95, 2),
    ]
    null_dots = VGroup(
        *[
            Dot(
                np.array([center[0] + x, axis_y + 0.14 + 0.18 * row, 0]),
                radius=0.065,
                color=MUTED,
                fill_opacity=0.72,
            )
            for x, row in null_offsets
        ]
    )
    observed_x = center[0] + observed_offset
    observed_marker = Line(
        np.array([observed_x, axis_y - 0.22, 0]),
        np.array([observed_x, axis_y + 0.70, 0]),
        color=status_color,
        stroke_width=5,
    )
    observed_label = Text(
        "real matched EMD",
        color=status_color,
        font_size=17,
        weight="BOLD",
    ).move_to(np.array([observed_x, axis_y - 0.53, 0]))
    status = Text(status_text, color=status_color, font_size=20, weight="BOLD")
    status.move_to(center + DOWN * 1.35)
    context = VGroup(frame, title, null_label, axis, axis_label)
    observed = VGroup(observed_marker, observed_label)
    return context, null_dots, observed, status


class MecSpatialCoding(BaseScene):
    def construct(self):
        rng = np.random.default_rng(21)
        left_center = LEFT * 3.35 + DOWN * 0.1
        right_center = RIGHT * 3.35 + DOWN * 0.1

        title = Text("One path, two neural maps", color=INK, font_size=34, weight="BOLD")
        title.to_edge(UP, buff=0.22)
        healthy_title = Text("Healthy", color=INK, font_size=27, weight="BOLD")
        disease_title = Text("Alzheimer's model, App KI", color=ACCENT, font_size=25, weight="BOLD")
        healthy_title.move_to(left_center + UP * 2.55)
        disease_title.move_to(right_center + UP * 2.55)
        divider = Line(UP * 2.75, DOWN * 2.8, color=RULE, stroke_width=2)
        arenas = VGroup(arena(left_center), arena(right_center))

        left_path = trajectory(left_center)
        right_path = trajectory(right_center)
        mice = VGroup(
            Dot(left_path.get_start(), radius=0.11, color=INK),
            Dot(right_path.get_start(), radius=0.11, color=INK),
        )

        grid_points = []
        for row, y in enumerate(np.linspace(-1.35, 1.35, 4)):
            offset = 0.42 if row % 2 else 0
            for x in np.linspace(-1.65, 1.65, 4):
                grid_points.append(left_center + np.array([x + offset, y, 0]))
        healthy_dots = VGroup(
            *[Dot(point, radius=0.09, color=ACCENT, fill_opacity=0.92) for point in grid_points]
        )

        disease_points = [
            right_center + np.array([rng.uniform(-2.4, 2.4), rng.uniform(-1.75, 1.75), 0])
            for _ in range(42)
        ]
        disease_dots = VGroup(
            *[Dot(point, radius=0.065, color=ACCENT, fill_opacity=0.76) for point in disease_points]
        )

        healthy_tag = Text("crisp grid", color=INK, font_size=21)
        disease_tag = Text("scattered + hyperactive", color=ACCENT, font_size=21)
        healthy_tag.move_to(left_center + DOWN * 1.85)
        disease_tag.move_to(right_center + DOWN * 1.85)

        healthy_info = Text("spatial info  HIGH", color=INK, font_size=22, weight="BOLD")
        disease_info = Text("spatial info  LOW", color=MUTED, font_size=22, weight="BOLD")
        healthy_rate = Text("firing rate  normal", color=MUTED, font_size=19)
        disease_rate = Text("firing rate  HIGH", color=ACCENT, font_size=19, weight="BOLD")
        healthy_scores = VGroup(healthy_info, healthy_rate).arrange(DOWN, buff=0.12)
        disease_scores = VGroup(disease_info, disease_rate).arrange(DOWN, buff=0.12)
        healthy_scores.move_to(left_center + DOWN * 2.55)
        disease_scores.move_to(right_center + DOWN * 2.55)

        self.play(
            FadeIn(title),
            FadeIn(healthy_title),
            FadeIn(disease_title),
            FadeIn(divider),
            FadeIn(arenas),
            run_time=0.8,
        )
        self.play(
            Create(left_path),
            Create(right_path),
            MoveAlongPath(mice[0], left_path),
            MoveAlongPath(mice[1], right_path),
            run_time=2.2,
        )
        self.play(FadeIn(healthy_dots, lag_ratio=0.06), run_time=1.25)
        self.play(FadeIn(disease_dots, lag_ratio=0.025), run_time=1.45)
        self.play(
            FadeIn(healthy_tag),
            FadeIn(disease_tag),
            FadeIn(healthy_scores),
            FadeIn(disease_scores),
            run_time=0.65,
        )

        punchline = Text(
            "The map degrades as the noise floor rises.",
            color=INK,
            font_size=29,
            weight="BOLD",
        )
        punchline.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(punchline), run_time=0.65)
        self.wait(1.1)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.8)

        bridge = Text("Quantify the disorder", color=INK, font_size=36, weight="BOLD")
        self.play(FadeIn(bridge), run_time=0.6)
        self.wait(0.35)

        map_title = Text("One cell, two sessions", color=INK, font_size=34, weight="BOLD")
        map_title.to_edge(UP, buff=0.22)
        self.play(Transform(bridge, map_title), run_time=0.5)

        map_a_center = np.array([-3.65, -0.15, 0])
        map_b_center = np.array([-0.85, -0.15, 0])
        map_a = heatmap(map_a_center, [(-0.44, 0.43), (0.48, -0.38)])
        map_b = heatmap(map_b_center, [(-0.30, 0.36), (0.58, -0.30)])
        session_labels = VGroup(
            Text("session A", color=MUTED, font_size=21, weight="BOLD").next_to(
                map_a, UP, buff=0.16
            ),
            Text("session B", color=MUTED, font_size=21, weight="BOLD").next_to(
                map_b, UP, buff=0.16
            ),
        )
        metric_arrow = Arrow(
            map_a.get_right() + RIGHT * 0.08,
            map_b.get_left() + LEFT * 0.08,
            color=ACCENT,
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.17,
        )
        metric_label = Text("EMD", color=ACCENT, font_size=21, weight="BOLD")
        metric_label.next_to(metric_arrow, UP, buff=0.08)
        emd_formula = MathTex(
            r"W_1(P,Q)=\int \lvert F_P(x)-F_Q(x)\rvert\,dx",
            color=INK,
            font_size=25,
        ).move_to(np.array([3.35, 0.30, 0]))
        distance_caption = Text(
            "distance between a cell's two maps",
            color=MUTED,
            font_size=20,
        ).next_to(emd_formula, DOWN, buff=0.24)
        map_context = VGroup(
            map_a,
            map_b,
            session_labels,
            metric_arrow,
            metric_label,
            emd_formula,
            distance_caption,
        )
        self.play(FadeIn(map_a), FadeIn(map_b), FadeIn(session_labels), run_time=0.75)
        self.play(Create(metric_arrow), FadeIn(metric_label), FadeIn(emd_formula), run_time=0.75)
        self.play(FadeIn(distance_caption), run_time=0.35)
        self.wait(1.1)

        quantile_title = Text(
            "Real stability against a chance reference",
            color=INK,
            font_size=32,
            weight="BOLD",
        ).to_edge(UP, buff=0.20)
        self.play(Transform(bridge, quantile_title), FadeOut(map_context), run_time=0.65)

        q_formula = MathTex(
            r"q=\Pr(\mathrm{EMD}_{\mathrm{null}}<\mathrm{EMD}_{\mathrm{obs}})=\frac{n}{N}",
            color=INK,
            font_size=25,
        ).move_to(UP * 2.55)
        control = stability_panel(
            LEFT * 3.25 + DOWN * 0.52,
            "Control",
            -1.78,
            "q near 0  |  stable, below chance",
            STABLE,
        )
        app_ki = stability_panel(
            RIGHT * 3.25 + DOWN * 0.52,
            "App KI",
            0.92,
            "q near 1  |  at chance, disordered",
            DISORDERED,
        )
        panel_context = VGroup(control[0], app_ki[0])
        nulls = VGroup(control[1], app_ki[1])
        observed = VGroup(control[2], app_ki[2])
        statuses = VGroup(control[3], app_ki[3])
        self.play(FadeIn(q_formula), FadeIn(panel_context), run_time=0.75)
        self.play(FadeIn(nulls, lag_ratio=0.035), run_time=0.85)
        self.play(
            Create(control[2][0]),
            Create(app_ki[2][0]),
            FadeIn(control[2][1]),
            FadeIn(app_ki[2][1]),
            run_time=0.65,
        )
        self.play(FadeIn(statuses), run_time=0.65)
        self.wait(1.1)

        result_title = Text("Group result", color=INK, font_size=36, weight="BOLD")
        result_title.to_edge(UP, buff=0.22)
        quantile_screen = VGroup(q_formula, panel_context, nulls, observed, statuses)
        self.play(Transform(bridge, result_title), FadeOut(quantile_screen), run_time=0.65)

        method = Text(
            "Mixed-effects beta regression on stability quantiles",
            color=MUTED,
            font_size=23,
        ).move_to(UP * 1.75)
        finding = Text(
            "App KI spatial cells: about 7.5x more likely unstable",
            color=DISORDERED,
            font_size=31,
            weight="BOLD",
        ).move_to(UP * 0.62)
        odds_ratio = MathTex(r"\mathrm{OR}\approx 7.9", color=INK, font_size=40)
        odds_ratio.move_to(DOWN * 0.28)
        evidence = Text(
            "Quantiles are larger in App KI on familiar re-exposure.",
            color=MUTED,
            font_size=21,
        ).move_to(DOWN * 1.28)
        result = VGroup(method, finding, odds_ratio, evidence)
        self.play(FadeIn(method), run_time=0.5)
        self.play(FadeIn(finding), FadeIn(odds_ratio), FadeIn(evidence), run_time=0.65)
        self.wait(1.2)

        final = Text(
            "The degraded maps are statistically no different from chance.",
            color=INK,
            font_size=30,
            weight="BOLD",
        )
        self.play(FadeOut(bridge), FadeOut(result), FadeIn(final), run_time=0.6)
        self.wait(1.3)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=1.0)
