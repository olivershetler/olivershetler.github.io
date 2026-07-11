from manim import (
    Arrow,
    Circle,
    Create,
    DOWN,
    FadeIn,
    FadeOut,
    LEFT,
    MathTex,
    Rectangle,
    RIGHT,
    Text,
    UP,
    ValueTracker,
    VGroup,
    always_redraw,
    linear,
)

from aiqri_palette import ACCENT, BG, INK, MUTED, RULE, BaseScene


def firing_blob(color):
    return VGroup(
        Circle(radius=0.92, stroke_width=0, fill_color=color, fill_opacity=0.10),
        Circle(radius=0.68, stroke_width=0, fill_color=color, fill_opacity=0.16),
        Circle(radius=0.45, stroke_width=0, fill_color=color, fill_opacity=0.24),
        Circle(radius=0.23, stroke_width=0, fill_color=color, fill_opacity=0.46),
    )


class BeyondCorrelation(BaseScene):
    def construct(self):
        title = Text("When spatial fields separate", color=INK, font_size=34, weight="BOLD")
        title.to_edge(UP, buff=0.28)

        arena = Rectangle(width=6.1, height=4.45, color=RULE, stroke_width=3)
        arena.set_fill(BG, opacity=0.55).move_to(LEFT * 3.45 + DOWN * 0.05)
        arena_label = Text("ratemap, where a place cell fires", color=MUTED, font_size=22)
        arena_label.next_to(arena, UP, buff=0.12)

        start = arena.get_center() + LEFT * 1.75
        separation = ValueTracker(0)
        field_a = firing_blob(MUTED).move_to(start)
        field_b = firing_blob(ACCENT).move_to(start)
        field_b.add_updater(lambda mob: mob.move_to(start + RIGHT * separation.get_value()))

        label_a = Text("field A", color=MUTED, font_size=20).next_to(start, DOWN, buff=1.02)
        label_b = Text("field B", color=ACCENT, font_size=20)
        label_b.add_updater(
            lambda mob: mob.next_to(start + RIGHT * separation.get_value(), DOWN, buff=1.02)
        )

        pearson_label = Text("Pearson r", color=INK, font_size=24)
        pearson_label.move_to(RIGHT * 3.60 + UP * 1.08)
        pearson_math = MathTex(r"\rho(P,Q)", color=INK, font_size=26)
        pearson_math.next_to(pearson_label, RIGHT, buff=0.18)
        pearson_value = always_redraw(
            lambda: Text(
                f"{max(0, 1 - separation.get_value() / 1.65) ** 2:.2f}",
                color=MUTED if separation.get_value() >= 1.65 else INK,
                font_size=28,
            ).move_to(RIGHT * 5.95 + UP * 1.08)
        )

        emd_label = Text("EMD", color=INK, font_size=24)
        emd_label.move_to(RIGHT * 3.55 + UP * 0.38)
        emd_value = always_redraw(
            lambda: Text(
                f"{separation.get_value():.2f}",
                color=ACCENT,
                font_size=28,
            ).move_to(RIGHT * 5.95 + UP * 0.38)
        )
        emd_math = MathTex(
            r"W_1(P,Q)=\int \lvert F_P(x)-F_Q(x)\rvert\,dx",
            color=INK,
            font_size=20,
        ).move_to(RIGHT * 4.55 + DOWN * 0.24)

        metrics = VGroup(
            pearson_label,
            pearson_math,
            pearson_value,
            emd_label,
            emd_value,
            emd_math,
        )
        metric_rule = Rectangle(width=4.05, height=2.30, color=RULE, stroke_width=2)
        metric_rule.set_fill(BG, opacity=0).move_to(RIGHT * 4.48 + UP * 0.55)

        blind = Text("correlation is blind here", color=MUTED, font_size=22)
        blind.next_to(metric_rule, DOWN, buff=0.22)

        self.play(FadeIn(title), FadeIn(arena), FadeIn(arena_label), FadeIn(field_a), run_time=0.8)
        self.play(
            FadeIn(field_b),
            FadeIn(label_a),
            FadeIn(label_b),
            FadeIn(metric_rule),
            FadeIn(metrics),
            run_time=0.7,
        )
        self.play(separation.animate.set_value(3.45), run_time=3.0, rate_func=linear)
        self.play(FadeIn(blind), run_time=0.4)

        arrow_offsets = [-0.55, -0.27, 0, 0.27, 0.55]
        arrows = VGroup(
            *[
                Arrow(
                    start + UP * offset + RIGHT * 0.3,
                    start + RIGHT * 3.15 + UP * offset,
                    color=ACCENT,
                    stroke_width=3,
                    buff=0,
                    max_tip_length_to_length_ratio=0.08,
                )
                for offset in arrow_offsets
            ]
        )
        cost = Text("cost = mass x distance", color=ACCENT, font_size=23)
        cost.next_to(arrows, UP, buff=0.2)
        self.play(Create(arrows), FadeIn(cost), run_time=1.0)

        punchline = Text(
            "Correlation stops. Optimal transport keeps measuring.",
            color=INK,
            font_size=29,
            weight="BOLD",
        )
        punchline.to_edge(DOWN, buff=0.22)
        self.play(FadeIn(punchline), run_time=0.7)
        self.wait(1.4)

        self.play(FadeOut(arrows), FadeOut(cost), FadeOut(blind), FadeOut(punchline), run_time=0.6)
        self.play(separation.animate.set_value(0), run_time=2.1, rate_func=linear)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=1.0)
