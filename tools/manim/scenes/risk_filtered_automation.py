import numpy as np
from manim import (
    Axes,
    Create,
    DashedLine,
    Dot,
    DOWN,
    FadeIn,
    FadeOut,
    GrowFromEdge,
    LaggedStart,
    LEFT,
    Line,
    ManimColor,
    MoveToTarget,
    Rectangle,
    RIGHT,
    SurroundingRectangle,
    Text,
    Transform,
    UP,
    ValueTracker,
    VGroup,
    always_redraw,
    interpolate_color,
    linear,
)

from aiqri_palette import ACCENT, BG, INK, MUTED, RULE, BaseScene


LOW_RISK = "#2E7D5B"
HIGH_RISK = "#A6321E"


def risk_color(score):
    return interpolate_color(ManimColor(LOW_RISK), ManimColor(HIGH_RISK), score)


def readout(label, value, color=INK, decimals=0):
    label_mob = Text(label, color=MUTED, font_size=20, weight="BOLD")
    number = Text(
        f"{value:.{decimals}f}%",
        color=color,
        font_size=22,
        weight="BOLD",
    )
    return VGroup(label_mob, number).arrange(RIGHT, buff=0.12), number, label_mob


class RiskFilteredAutomation(BaseScene):
    def construct(self):
        scores = np.array(
            [
                0.04, 0.06, 0.08, 0.09, 0.11, 0.12, 0.14, 0.15,
                0.17, 0.18, 0.19, 0.21, 0.22, 0.23, 0.25, 0.26,
                0.28, 0.29, 0.31, 0.32, 0.34, 0.35, 0.37, 0.39,
                0.41, 0.43, 0.46, 0.49, 0.52, 0.55, 0.58, 0.62,
                0.66, 0.70, 0.74, 0.79, 0.84, 0.89, 0.94, 0.98,
            ]
        )

        # Beat 1: score a low-risk majority with a high-risk tail.
        title = Text(
            "Score every claim by denial risk",
            color=INK,
            font_size=36,
            weight="BOLD",
        ).to_edge(UP, buff=0.24)

        axis_y = 0.50
        axis_left, axis_right = -5.25, 5.25

        def score_x(score):
            return axis_left + score * (axis_right - axis_left)

        risk_axis = Line(
            np.array([axis_left, axis_y, 0.0]),
            np.array([axis_right, axis_y, 0.0]),
            color=MUTED,
            stroke_width=3,
        )
        ticks = VGroup(
            *[
                Line(
                    np.array([score_x(tick), axis_y - 0.09, 0.0]),
                    np.array([score_x(tick), axis_y + 0.09, 0.0]),
                    color=MUTED,
                    stroke_width=2,
                )
                for tick in np.linspace(0, 1, 6)
            ]
        )
        axis_label = Text(
            "denial risk score",
            color=INK,
            font_size=22,
            weight="BOLD",
        ).next_to(risk_axis, DOWN, buff=0.28)
        low_label = Text("low risk", color=LOW_RISK, font_size=21, weight="BOLD").move_to(
            np.array([axis_left + 0.50, axis_y - 0.65, 0.0])
        )
        high_label = Text("high risk", color=HIGH_RISK, font_size=21, weight="BOLD").move_to(
            np.array([axis_right - 0.58, axis_y - 0.65, 0.0])
        )
        axis_group = VGroup(risk_axis, ticks, axis_label, low_label, high_label)

        rows = np.zeros(8, dtype=int)
        dots = VGroup()
        for score in scores:
            bin_index = min(int(score * 8), 7)
            row = rows[bin_index]
            rows[bin_index] += 1
            y = axis_y + 0.28 + 0.27 * row
            jitter = 0.05 * np.sin(37 * score)
            dots.add(
                Dot(
                    np.array([score_x(score) + jitter, y, 0.0]),
                    radius=0.085,
                    color=risk_color(score),
                ).set_stroke(BG, width=1)
            )

        self.play(FadeIn(title), FadeIn(axis_group), run_time=0.75)
        self.play(
            LaggedStart(*[FadeIn(dot, shift=UP * 0.12) for dot in dots], lag_ratio=0.025),
            run_time=1.35,
        )
        self.wait(0.55)

        # Beat 2: route each claim at the cutoff.
        cutoff = 0.68
        threshold_x = score_x(cutoff)
        threshold = Line(
            np.array([threshold_x, axis_y - 0.15, 0.0]),
            np.array([threshold_x, 2.16, 0.0]),
            color=ACCENT,
            stroke_width=5,
        )
        threshold_label = Text(
            "risk threshold",
            color=ACCENT,
            font_size=20,
            weight="BOLD",
        ).next_to(threshold, UP, buff=0.08)
        routing_rule = Text(
            "Claims above the threshold go to people; below, to AI.",
            color=MUTED,
            font_size=21,
            weight="BOLD",
        ).move_to(np.array([0.0, -3.42, 0.0]))
        self.play(
            Create(threshold),
            FadeIn(threshold_label),
            FadeIn(routing_rule),
            run_time=0.55,
        )

        automate_label = Text(
            "Automate (AI, $0.10)",
            color=LOW_RISK,
            font_size=22,
            weight="BOLD",
        ).move_to(np.array([-3.20, -0.94, 0.0]))
        review_label = Text(
            "Human review ($5.00)",
            color=HIGH_RISK,
            font_size=22,
            weight="BOLD",
        ).move_to(np.array([3.20, -0.94, 0.0]))

        low_dots = []
        high_dots = []
        for dot, score in zip(dots, scores):
            dot.generate_target()
            if score < cutoff:
                index = len(low_dots)
                column = index % 9
                row = index // 9
                target_x = -4.80 + 0.40 * column
                target_y = -1.34 - 0.25 * row
                low_dots.append(dot)
            else:
                index = len(high_dots)
                column = index % 4
                row = index // 4
                target_x = 2.60 + 0.40 * column
                target_y = -1.43 - 0.30 * row
                high_dots.append(dot)
            dot.target.move_to(np.array([target_x, target_y, 0.0])).scale(0.88)

        # Size each lane from the completed target grid, then add ample inner padding.
        low_target_grid = VGroup(*[dot.target for dot in low_dots])
        high_target_grid = VGroup(*[dot.target for dot in high_dots])
        automate_box = SurroundingRectangle(
            VGroup(automate_label, low_target_grid),
            buff=0.28,
            corner_radius=0.14,
            color=LOW_RISK,
            stroke_width=2.5,
            fill_color=LOW_RISK,
            fill_opacity=0.08,
        )
        review_box = SurroundingRectangle(
            VGroup(review_label, high_target_grid),
            buff=0.28,
            corner_radius=0.14,
            color=HIGH_RISK,
            stroke_width=2.5,
            fill_color=HIGH_RISK,
            fill_opacity=0.06,
        )
        lanes = VGroup(automate_box, review_box, automate_label, review_label)
        self.play(FadeIn(lanes), run_time=0.50)

        self.play(
            LaggedStart(*[MoveToTarget(dot) for dot in dots], lag_ratio=0.018),
            run_time=1.45,
        )

        automation_display, _, _ = readout("automation rate", 68, LOW_RISK)
        missed_display, _, _ = readout("missed errors", 2.1, HIGH_RISK, decimals=1)
        automation_display.next_to(automate_box, DOWN, buff=0.18)
        missed_display.next_to(review_box, DOWN, buff=0.18)
        route_readouts = VGroup(automation_display, missed_display)
        self.play(FadeIn(route_readouts), run_time=0.40)
        self.wait(0.65)

        # Beat 3: sweep the cutoff and find the lowest total cost.
        optimize_title = Text(
            "Find the lowest total cost",
            color=INK,
            font_size=36,
            weight="BOLD",
        ).to_edge(UP, buff=0.24)
        self.play(
            Transform(title, optimize_title),
            FadeOut(axis_group),
            FadeOut(dots),
            FadeOut(threshold),
            FadeOut(threshold_label),
            FadeOut(routing_rule),
            FadeOut(lanes),
            FadeOut(route_readouts),
            run_time=0.65,
        )

        tracker = ValueTracker(0.20)
        sweep_rule = Text(
            "Claims above the threshold go to people; below, to AI.",
            color=MUTED,
            font_size=20,
            weight="BOLD",
        ).move_to(np.array([0.0, 2.63, 0.0]))
        compact_axis = Line(LEFT * 4.80, RIGHT * 4.80, color=MUTED, stroke_width=3).shift(UP * 1.86)
        compact_low = Text("fewer automated", color=MUTED, font_size=18).next_to(
            compact_axis, DOWN, buff=0.10
        ).align_to(compact_axis, LEFT)
        compact_high = Text("more automated", color=MUTED, font_size=18).next_to(
            compact_axis, DOWN, buff=0.10
        ).align_to(compact_axis, RIGHT)
        moving_threshold = always_redraw(
            lambda: Line(
                np.array([-4.80 + 9.60 * tracker.get_value(), 1.62, 0.0]),
                np.array([-4.80 + 9.60 * tracker.get_value(), 2.08, 0.0]),
                color=ACCENT,
                stroke_width=5,
            )
        )
        moving_threshold_label = always_redraw(
            lambda: Text(
                "risk threshold",
                color=ACCENT,
                font_size=18,
                weight="BOLD",
            ).move_to(
                np.array(
                    [
                        np.clip(-4.80 + 9.60 * tracker.get_value(), -4.10, 4.10),
                        2.25,
                        0.0,
                    ]
                )
            )
        )

        def moving_tradeoff_readout():
            automation = Text(
                f"automation {100 * tracker.get_value():.0f}%",
                color=LOW_RISK,
                font_size=19,
                weight="BOLD",
            )
            missed = Text(
                f"missed errors {0.4 + 10.5 * tracker.get_value() ** 3:.1f}%",
                color=HIGH_RISK,
                font_size=19,
                weight="BOLD",
            )
            group = VGroup(automation, missed).arrange(RIGHT, buff=0.38)
            group.move_to(
                np.array(
                    [
                        np.clip(-4.80 + 9.60 * tracker.get_value(), -3.30, 3.30),
                        1.08,
                        0.0,
                    ]
                )
            )
            return group

        sweep_tradeoff = always_redraw(moving_tradeoff_readout)

        cost_axes = Axes(
            x_range=[0, 1, 0.2],
            y_range=[0, 6, 2],
            x_length=8.30,
            y_length=2.70,
            tips=False,
            axis_config={"color": MUTED, "stroke_width": 2, "include_numbers": False},
        ).move_to(np.array([0.20, -1.10, 0.0]))
        x_caption = Text("risk threshold", color=MUTED, font_size=18, weight="BOLD").next_to(
            cost_axes, DOWN, buff=0.10
        )
        dollar_ticks = VGroup(
            *[
                Text(f"${value}", color=MUTED, font_size=17).next_to(
                    cost_axes.c2p(0, value), LEFT, buff=0.13
                )
                for value in (0, 2, 4, 6)
            ]
        )
        y_caption = Text(
            "cost per claim ($)", color=MUTED, font_size=18, weight="BOLD"
        ).rotate(np.pi / 2).next_to(
            dollar_ticks, LEFT, buff=0.18
        )

        def cost_value(x):
            optimum = 0.62
            if x <= optimum:
                return 2.55 + (5.00 - 2.55) * ((optimum - x) / optimum) ** 2
            return 2.55 + (5.80 - 2.55) * ((x - optimum) / (1 - optimum)) ** 2

        curve = cost_axes.plot(cost_value, x_range=[0.02, 0.98], color=INK, stroke_width=5)
        cost_endpoints = VGroup(
            Text(
                "$5.00 all human", color=MUTED, font_size=17, weight="BOLD"
            ).next_to(
                cost_axes.c2p(0.02, cost_value(0.02)), RIGHT, buff=0.20
            ).shift(UP * 0.20),
            Text(
                "$0.10 AI + rework", color=MUTED, font_size=17, weight="BOLD"
            ).next_to(
                cost_axes.c2p(0.98, cost_value(0.98)), UP, buff=0.08
            ).shift(LEFT * 0.54),
        )
        curve_marker = always_redraw(
            lambda: Dot(
                cost_axes.c2p(tracker.get_value(), cost_value(tracker.get_value())),
                radius=0.105,
                color=ACCENT,
            ).set_stroke(BG, width=2)
        )
        graph_threshold = always_redraw(
            lambda: DashedLine(
                cost_axes.c2p(tracker.get_value(), 0),
                cost_axes.c2p(
                    tracker.get_value(), cost_value(tracker.get_value())
                ),
                color=ACCENT,
                stroke_width=2,
                dash_length=0.08,
            )
        )
        optimize_context = VGroup(
            sweep_rule,
            compact_axis,
            compact_low,
            compact_high,
            moving_threshold,
            moving_threshold_label,
            sweep_tradeoff,
            cost_axes,
            x_caption,
            dollar_ticks,
            y_caption,
        )
        self.play(
            FadeIn(optimize_context),
            FadeIn(graph_threshold),
            FadeIn(curve_marker),
            run_time=0.80,
        )
        self.play(
            Create(curve),
            FadeIn(cost_endpoints),
            tracker.animate.set_value(0.90),
            run_time=2.00,
            rate_func=linear,
        )
        self.play(tracker.animate.set_value(0.62), run_time=0.70)
        optimum_label = VGroup(
            Text("$2.55", color=ACCENT, font_size=24, weight="BOLD"),
            Text(
                "lowest cost per claim",
                color=ACCENT,
                font_size=20,
                weight="BOLD",
            ),
        ).arrange(DOWN, buff=0.03).next_to(
            cost_axes.c2p(0.62, cost_value(0.62)), DOWN, buff=0.18
        )
        optimum_line = DashedLine(
            optimum_label.get_top(),
            cost_axes.c2p(0.62, cost_value(0.62)) + DOWN * 0.10,
            color=ACCENT,
            stroke_width=2,
            dash_length=0.07,
        )
        self.play(FadeIn(optimum_label), Create(optimum_line), run_time=0.45)
        self.wait(0.60)
        bridge = Text(
            "Risk-stratified routing = split at the cost-optimal threshold.",
            color=INK,
            font_size=23,
            weight="BOLD",
        ).to_edge(DOWN, buff=0.16)
        self.play(FadeIn(bridge), run_time=0.40)
        self.wait(0.45)

        # Beat 4: compare cost bars and failure markers.
        payoff_title = Text(
            "Lower cost without more failures",
            color=INK,
            font_size=36,
            weight="BOLD",
        ).to_edge(UP, buff=0.24)
        self.play(
            Transform(title, payoff_title),
            FadeOut(optimize_context),
            FadeOut(curve),
            FadeOut(cost_endpoints),
            FadeOut(curve_marker),
            FadeOut(graph_threshold),
            FadeOut(optimum_label),
            FadeOut(optimum_line),
            FadeOut(bridge),
            run_time=0.65,
        )

        baseline_y = -2.28
        category_x = [-3.75, 0.0, 3.75]
        cost_heights = [3.25, 0.82, 1.65]
        failure_heights = [0.48, 2.85, 0.48]
        names = ["All human", "All AI", "Risk-stratified"]
        bar_colors = [MUTED, RULE, ACCENT]

        legend_bar = Rectangle(
            width=0.30,
            height=0.18,
            stroke_width=0,
            fill_color=MUTED,
            fill_opacity=0.75,
        )
        legend_cost = VGroup(
            legend_bar,
            Text("cost", color=MUTED, font_size=19, weight="BOLD"),
        ).arrange(RIGHT, buff=0.10)
        legend_failure = VGroup(
            Dot(radius=0.075, color=HIGH_RISK),
            Text("failure rate", color=MUTED, font_size=19, weight="BOLD"),
        ).arrange(RIGHT, buff=0.10)
        payoff_legend = VGroup(legend_cost, legend_failure).arrange(RIGHT, buff=0.48)
        payoff_legend.move_to(np.array([0.0, 1.70, 0.0]))

        bars = VGroup()
        guides = VGroup()
        failure_dots = VGroup()
        for x, height, failure_height, name, color in zip(
            category_x, cost_heights, failure_heights, names, bar_colors
        ):
            bar = Rectangle(
                width=1.05,
                height=height,
                stroke_color=color,
                stroke_width=2,
                fill_color=color,
                fill_opacity=0.72 if color != RULE else 0.92,
            ).move_to(np.array([x - 0.38, baseline_y + height / 2, 0.0]))
            guide = Line(
                np.array([x + 0.55, baseline_y, 0.0]),
                np.array([x + 0.55, baseline_y + 3.30, 0.0]),
                color=RULE,
                stroke_width=3,
            )
            failure_dot = Dot(
                np.array([x + 0.55, baseline_y + failure_height, 0.0]),
                radius=0.11,
                color=HIGH_RISK,
            ).set_stroke(BG, width=2)
            bars.add(bar)
            guides.add(guide)
            failure_dots.add(failure_dot)

        half_cost = Text(
            "~half the cost",
            color=ACCENT,
            font_size=22,
            weight="BOLD",
        ).next_to(bars[2], UP, buff=0.13)
        same_rate_line = Line(
            failure_dots[0].get_center(),
            failure_dots[2].get_center(),
            color=LOW_RISK,
            stroke_width=3,
        )
        same_rate = Text(
            "same failure rate",
            color=LOW_RISK,
            font_size=19,
            weight="BOLD",
        ).move_to(np.array([1.82, baseline_y + 0.88, 0.0]))
        winner_content = VGroup(
            bars[2],
            guides[2],
            failure_dots[2],
            half_cost,
        )
        winner_outline = SurroundingRectangle(
            winner_content,
            buff=0.30,
            corner_radius=0.18,
            color=ACCENT,
            stroke_width=3,
            fill_color=ACCENT,
            fill_opacity=0.035,
        )
        labels = VGroup(
            Text("All human", color=INK, font_size=21, weight="BOLD").move_to(
                np.array([category_x[0], baseline_y - 0.43, 0.0])
            ),
            Text("All AI", color=INK, font_size=21, weight="BOLD").move_to(
                np.array([category_x[1], baseline_y - 0.43, 0.0])
            ),
            Text(
                "Risk-stratified",
                color=ACCENT,
                font_size=21,
                weight="BOLD",
            ).next_to(winner_outline, DOWN, buff=0.18),
        )

        self.play(FadeIn(payoff_legend), FadeIn(guides), FadeIn(labels), run_time=0.60)
        self.play(
            LaggedStart(*[GrowFromEdge(bar, DOWN) for bar in bars], lag_ratio=0.16),
            LaggedStart(*[FadeIn(dot) for dot in failure_dots], lag_ratio=0.16),
            FadeIn(winner_outline),
            run_time=1.20,
        )

        callouts = VGroup(half_cost, same_rate_line, same_rate)
        self.play(FadeIn(half_cost), Create(same_rate_line), FadeIn(same_rate), run_time=0.65)
        self.wait(1.35)

        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.70)
        self.wait(0.15)
