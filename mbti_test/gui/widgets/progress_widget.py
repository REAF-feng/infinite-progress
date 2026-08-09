"""Custom progress bar widget using Canvas."""
import tkinter as tk
from gui.styles import tk_color

class ProgressWidget(tk.Canvas):
    def __init__(self, parent, height=28, **kwargs):
        super().__init__(parent, height=height, bg=tk_color("content_bg"),
                         highlightthickness=0, **kwargs)
        self._height = height
        self._value = 0
        self._max_value = 100
        self.bind("<Configure>", self._on_resize)

    def set_progress(self, current, total):
        self._value = current
        self._max_value = total
        self._draw()

    def _on_resize(self, event=None):
        self._draw()

    def _draw(self):
        self.delete("all")
        w = self.winfo_width()
        h = self._height
        if w < 10:
            return
        ratio = min(self._value / max(self._max_value, 1), 1.0)
        fill_w = int((w - 4) * ratio) if ratio > 0 else 0
        r = h // 2 - 2
        # Background track
        self.create_rectangle(2, 2, w - 2, h - 2, fill=tk_color("progress_bg"),
                              outline="", tags="bg")
        # Fill bar
        if fill_w > 4:
            self.create_rectangle(2, 2, 2 + fill_w, h - 2, fill=tk_color("progress_fill"),
                                  outline="", tags="fill")
        # Percentage text
        pct_text = f"{self._value}/{self._max_value} ({int(ratio * 100)}%)"
        self.create_text(w // 2, h // 2, text=pct_text,
                         fill=tk_color("text_primary"),
                         font=("Microsoft YaHei", 10, "bold"))
