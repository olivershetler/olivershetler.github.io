import numpy as np
from manim import (
    Arrow, Create, DashedLine, Dot, DOWN, Ellipse, FadeIn, FadeOut,
    LEFT, Line, MathTex, Polygon, RIGHT, Text, UP, VGroup, linear,
)

from aiqri_palette import ACCENT, INK, MUTED, RULE, BaseScene


VIOLATION = "#A6321E"
BOUNDARY_SLOPE = 0.14
BOUNDARY_INTERCEPT = 1.08
ELLIPSE_WIDTH = 2.65
ELLIPSE_HEIGHT = 1.45
ELLIPSE_ANGLE = 0.28


def point_on_boundary(x):
    return np.array([x, BOUNDARY_SLOPE * x + BOUNDARY_INTERCEPT, 0.0])


def ellipse_support_radius(normal):
    """Half-extent of the rotated confidence ellipse along a unit normal."""
    major = np.array([np.cos(ELLIPSE_ANGLE), np.sin(ELLIPSE_ANGLE), 0.0])
    minor = np.array([-np.sin(ELLIPSE_ANGLE), np.cos(ELLIPSE_ANGLE), 0.0])
    return np.sqrt(
        ((ELLIPSE_WIDTH / 2) * np.dot(normal, major)) ** 2
        + ((ELLIPSE_HEIGHT / 2) * np.dot(normal, minor)) ** 2
    )


def unsafe_half_ellipse(center, normal):
    """Return the half of a centered ellipse lying beyond the boundary."""
    major = np.array([np.cos(ELLIPSE_ANGLE), np.sin(ELLIPSE_ANGLE), 0.0])
    minor = np.array([-np.sin(ELLIPSE_ANGLE), np.cos(ELLIPSE_ANGLE), 0.0])
    major_term = (ELLIPSE_WIDTH / 2) * np.dot(normal, major)
    minor_term = (ELLIPSE_HEIGHT / 2) * np.dot(normal, minor)
    peak_angle = np.arctan2(minor_term, major_term)
    angles = np.linspace(peak_angle - np.pi / 2, peak_angle + np.pi / 2, 64)
    points = [
        center
        + (ELLIPSE_WIDTH / 2) * np.cos(angle) * major
        + (ELLIPSE_HEIGHT / 2) * np.sin(angle) * minor
        for angle in angles
    ]
    return Polygon(
        *points, stroke_width=0, fill_color=VIOLATION, fill_opacity=0.58
    )


def gaussian_ellipse(center):
    density_outer = Ellipse(
        width=ELLIPSE_WIDTH * 1.38,
        height=ELLIPSE_HEIGHT * 1.38,
        color=MUTED,
        stroke_width=1.5,
        stroke_opacity=0.20,
    ).rotate(ELLIPSE_ANGLE)
    density_inner = Ellipse(
        width=ELLIPSE_WIDTH * 0.57,
        height=ELLIPSE_HEIGHT * 0.57,
        color=MUTED,
        stroke_width=1.5,
        stroke_opacity=0.28,
    ).rotate(ELLIPSE_ANGLE)
    confidence = Ellipse(
        width=ELLIPSE_WIDTH,
        height=ELLIPSE_HEIGHT,
        color=ACCENT,
        stroke_width=6,
    ).rotate(ELLIPSE_ANGLE)
    mean = Dot(radius=0.095, color=INK)
    return VGroup(density_outer, density_inner, confidence, mean).move_to(center)


class QuantileRisk(BaseScene):
    def construct(self):
        normal = np.array([-BOUNDARY_SLOPE, 1.0, 0.0])
        normal /= np.linalg.norm(normal)
        tangent = np.array([1.0, BOUNDARY_SLOPE, 0.0])
        tangent /= np.linalg.norm(tangent)
        margin = ellipse_support_radius(normal)

        boundary_anchor = point_on_boundary(-0.75)
        naive_mean = boundary_anchor
        tangent_mean = boundary_anchor - margin * normal
        best_mean = tangent_mean + 2.3 * tangent
        start_mean = tangent_mean - 1.05 * normal - 1.0 * tangent

        title = Text(
            "Chance-constrained optimization",
            color=INK,
            font_size=34,
            weight="BOLD",
        ).to_edge(UP, buff=0.20)
        probability = MathTex(
            r"\Pr(a^\top X \le b)\ge 1-\alpha",
            color=INK,
            font_size=27,
        ).next_to(title, DOWN, buff=0.08)

        x_left, x_right = -5.45, 5.45
        boundary = Line(
            point_on_boundary(x_left),
            point_on_boundary(x_right),
            color=ACCENT,
            stroke_width=5,
        )
        safe_region = Polygon(
            np.array([x_left, -2.55, 0.0]),
            np.array([x_right, -2.55, 0.0]),
            point_on_boundary(x_right),
            point_on_boundary(x_left),
            stroke_width=0,
            fill_color=RULE,
            fill_opacity=0.40,
        )
        boundary_label = Text(
            "operating limit",
            color=ACCENT,
            font_size=21,
            weight="BOLD",
        ).move_to(point_on_boundary(3.92) + UP * 0.34)
        safe_label = Text(
            "safe region",
            color=MUTED,
            font_size=22,
            weight="BOLD",
        ).move_to(np.array([-4.15, -1.95, 0.0]))

        axes = VGroup(
            Arrow(
                np.array([-5.55, -2.45, 0.0]),
                np.array([-3.95, -2.45, 0.0]),
                color=MUTED,
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            ),
            Arrow(
                np.array([-5.55, -2.45, 0.0]),
                np.array([-5.55, -0.85, 0.0]),
                color=MUTED,
                stroke_width=2,
                buff=0,
                max_tip_length_to_length_ratio=0.08,
            ),
            Text("outcome (2D)", color=MUTED, font_size=18).move_to(
                np.array([-4.70, -2.72, 0.0])
            ),
        )

        objective_arrow = Arrow(
            np.array([3.75, -1.62, 0.0]),
            np.array([3.42, 0.65, 0.0]),
            color=INK,
            stroke_width=4,
            buff=0,
            max_tip_length_to_length_ratio=0.12,
        )
        objective_label = Text(
            "objective", color=INK, font_size=21, weight="BOLD"
        ).next_to(objective_arrow, RIGHT, buff=0.12)

        distribution = gaussian_ellipse(start_mean)
        ellipse_label = VGroup(
            Text("confidence ellipse", color=INK, font_size=21, weight="BOLD"),
            Text("holds 1 - alpha of outcomes", color=MUTED, font_size=18),
        ).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
        ellipse_label.move_to(np.array([-1.95, -2.30, 0.0]))
        label_leader = DashedLine(
            ellipse_label.get_top() + UP * 0.02,
            distribution[2].get_bottom() + DOWN * 0.02,
            color=MUTED,
            stroke_width=1.5,
            dash_length=0.08,
        )

        context = VGroup(
            safe_region,
            axes,
            safe_label,
            boundary,
            boundary_label,
            objective_arrow,
            objective_label,
        )
        self.play(
            FadeIn(title),
            FadeIn(probability),
            FadeIn(context),
            FadeIn(distribution),
            FadeIn(ellipse_label),
            Create(label_leader),
            run_time=1.0,
        )
        self.wait(0.25)

        beat_a = Text(
            "A. Ignore the noise",
            color=MUTED,
            font_size=25,
            weight="BOLD",
        ).move_to(np.array([-3.90, 2.45, 0.0]))
        self.play(
            FadeOut(ellipse_label),
            FadeOut(label_leader),
            FadeIn(beat_a),
            run_time=0.45,
        )
        self.play(distribution.animate.move_to(naive_mean), run_time=1.65, rate_func=linear)

        overhang = unsafe_half_ellipse(naive_mean, normal)
        unsafe_label = Text(
            "P(unsafe) ~ 50%, over risk budget alpha",
            color=VIOLATION,
            font_size=22,
            weight="BOLD",
        ).move_to(np.array([-2.50, 2.02, 0.0]))
        infeasible = Text(
            "INFEASIBLE",
            color=VIOLATION,
            font_size=27,
            weight="BOLD",
        ).move_to(np.array([0.75, -1.55, 0.0]))
        cross = VGroup(
            Line(LEFT * 0.18 + UP * 0.18, RIGHT * 0.18 + DOWN * 0.18),
            Line(LEFT * 0.18 + DOWN * 0.18, RIGHT * 0.18 + UP * 0.18),
        ).set_color(VIOLATION).set_stroke(width=6)
        cross.next_to(infeasible, LEFT, buff=0.18)
        self.play(
            FadeIn(overhang),
            FadeIn(unsafe_label),
            FadeIn(infeasible),
            Create(cross),
            run_time=0.75,
        )
        self.wait(0.65)

        self.play(
            distribution.animate.move_to(start_mean),
            FadeOut(overhang),
            FadeOut(unsafe_label),
            FadeOut(infeasible),
            FadeOut(cross),
            FadeOut(beat_a),
            run_time=0.9,
        )

        beat_b = Text(
            "B. Quantile constraint",
            color=INK,
            font_size=25,
            weight="BOLD",
        ).move_to(np.array([-3.75, 2.45, 0.0]))
        self.play(FadeIn(beat_b), run_time=0.35)
        self.play(distribution.animate.move_to(tangent_mean), run_time=1.45, rate_func=linear)

        contact = tangent_mean + margin * normal
        margin_line = DashedLine(
            tangent_mean,
            contact,
            color=ACCENT,
            stroke_width=3,
            dash_length=0.09,
        )
        margin_label = Text(
            "quantile margin",
            color=ACCENT,
            font_size=18,
            weight="BOLD",
        ).next_to(margin_line, RIGHT, buff=0.10)
        contact_dot = Dot(contact, radius=0.075, color=ACCENT)
        margin_group = VGroup(margin_line, margin_label, contact_dot)
        feasible_label = Text(
            "P(unsafe) = alpha, feasible",
            color=INK,
            font_size=23,
            weight="BOLD",
        ).move_to(np.array([-2.35, 2.02, 0.0]))
        gaussian_quantile = MathTex(
            r"a^\top\mu + z_{1-\alpha}\sqrt{a^\top\Sigma a}\le b",
            color=INK,
            font_size=27,
        ).to_edge(DOWN, buff=0.18)
        self.play(
            Create(margin_line),
            FadeIn(margin_label),
            FadeIn(contact_dot),
            FadeIn(feasible_label),
            FadeIn(gaussian_quantile),
            run_time=0.70,
        )

        self.play(
            distribution.animate.move_to(best_mean),
            margin_group.animate.shift(2.3 * tangent),
            run_time=1.55,
            rate_func=linear,
        )
        optimum = Text(
            "best objective point",
            color=INK,
            font_size=20,
            weight="BOLD",
        ).next_to(distribution, DOWN, buff=0.18)
        self.play(FadeIn(optimum), run_time=0.35)

        punchline = VGroup(
            Text(
                "The risk constraint is a probability.",
                color=INK,
                font_size=25,
                weight="BOLD",
            ),
            Text(
                "Optimize by keeping the confidence ellipse inside the safe region.",
                color=INK,
                font_size=23,
            ),
        ).arrange(DOWN, buff=0.06)
        punchline.to_edge(DOWN, buff=0.12)
        self.play(
            FadeOut(beat_b),
            FadeOut(feasible_label),
            FadeOut(optimum),
            FadeOut(gaussian_quantile),
            FadeIn(punchline),
            run_time=0.55,
        )
        self.wait(0.85)

        self.play(
            distribution.animate.move_to(start_mean),
            FadeOut(margin_group),
            FadeOut(punchline),
            run_time=1.15,
            rate_func=linear,
        )
        self.wait(0.15)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=0.65)
