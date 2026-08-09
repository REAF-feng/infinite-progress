"""GUI theme manager - dark/light dual theme."""
from config import LIGHT_THEME, DARK_THEME, DEFAULT_THEME

class ThemeManager:
    def __init__(self):
        self._current = DEFAULT_THEME
        self._themes = {"light": LIGHT_THEME, "dark": DARK_THEME}

    @property
    def current(self) -> str:
        return self._current

    @property
    def colors(self) -> dict:
        return self._themes[self._current]

    def get(self, key: str, default=None):
        return self._themes[self._current].get(key, default)

    def toggle(self):
        self._current = "light" if self._current == "dark" else "dark"
        return self._current

    def set_theme(self, name: str):
        if name in self._themes:
            self._current = name

theme = ThemeManager()

FONT_FAMILY = "Microsoft YaHei"
FONTS = {
    "title_large": (FONT_FAMILY, 36, "bold"),
    "heading": (FONT_FAMILY, 24, "bold"),
    "subheading": (FONT_FAMILY, 16, "normal"),
    "body": (FONT_FAMILY, 12, "normal"),
    "body_bold": (FONT_FAMILY, 12, "bold"),
    "small": (FONT_FAMILY, 10, "normal"),
    "nav": (FONT_FAMILY, 13, "normal"),
    "button": (FONT_FAMILY, 12, "normal"),
    "mono": ("Consolas", 11, "normal"),
}

PADDING = {"page": 40, "card": 24, "element": 12, "compact": 6}

def tk_color(key: str) -> str:
    return theme.get(key, "#000000")

def tk_font(key: str) -> tuple:
    return FONTS.get(key, (FONT_FAMILY, 12, "normal"))
