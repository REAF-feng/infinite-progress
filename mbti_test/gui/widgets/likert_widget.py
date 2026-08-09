"""5-point Likert scale radio button widget."""
import tkinter as tk
from config import LIKERT_SHORT
from gui.styles import tk_color, tk_font

class LikertWidget(tk.Frame):
    def __init__(self, parent, on_select=None, **kwargs):
        super().__init__(parent, bg=tk_color("card_bg"), **kwargs)
        self._on_select = on_select
        self._var = tk.IntVar(value=-1)
        self._buttons = []
        self._build()

    def _build(self):
        label_frame = tk.Frame(self, bg=tk_color("card_bg"))
        label_frame.pack(fill=tk.X, pady=(0, 8))
        for i, label in enumerate(LIKERT_SHORT):
            lbl = tk.Label(label_frame, text=label, font=tk_font("small"),
                           fg=tk_color("text_secondary"), bg=tk_color("card_bg"),
                           width=10, anchor="center")
            lbl.grid(row=0, column=i, padx=5)

        btn_frame = tk.Frame(self, bg=tk_color("card_bg"))
        btn_frame.pack(fill=tk.X)
        for i in range(5):
            btn = tk.Radiobutton(
                btn_frame, text="", variable=self._var, value=i,
                bg=tk_color("card_bg"), activebackground=tk_color("card_bg"),
                selectcolor=tk_color("accent"), indicatoron=True,
                width=3, height=1,
                command=self._on_select_change if self._on_select else None)
            btn.grid(row=0, column=i, padx=5)
            self._buttons.append(btn)
        for i in range(5):
            label_frame.grid_columnconfigure(i, weight=1)
            btn_frame.grid_columnconfigure(i, weight=1)

    def _on_select_change(self):
        if self._on_select:
            self._on_select(self.get_value())

    def get_value(self):
        return self._var.get()

    def set_value(self, value):
        if 0 <= value <= 4:
            self._var.set(value)

    def has_selection(self):
        return self._var.get() >= 0

    def clear(self):
        self._var.set(-1)

    def refresh_theme(self):
        self.config(bg=tk_color("card_bg"))
        for child in self.winfo_children():
            child.config(bg=tk_color("card_bg"))
            for sub in child.winfo_children():
                try:
                    sub.config(bg=tk_color("card_bg"), fg=tk_color("text_secondary"))
                except Exception:
                    pass
