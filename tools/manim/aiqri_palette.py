from manim import Scene


INK = "#1C1A17"
MUTED = "#5C564C"
ACCENT = "#B0502F"
BG = "#FAF6EF"
RULE = "#E2D9C8"


class BaseScene(Scene):
    """Shared warm canvas for the publication schematics."""

    def setup(self):
        super().setup()
        self.camera.background_color = BG
