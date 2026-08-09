"""Side navigation bar widget."""
import tkinter as tk
from gui.styles import theme, tk_color, tk_font

class NavigationBar(tk.Frame):
    def __init__(self, parent, app, width=200):
        super().__init__(parent, width=width, bg=tk_color("nav_bg"))
        self.app = app
        self._buttons = {}
        self._active_key = None
        self.pack_propagate(False)
        self._build()

    def _build(self):
        title_frame = tk.Frame(self, bg=tk_color("nav_bg"))
        title_frame.pack(fill=tk.X, pady=(30, 40))
        tk.Label(title_frame, text="MBTI", font=tk_font("heading"),
                 fg=tk_color("accent"), bg=tk_color("nav_bg")).pack()
        tk.Label(title_frame, text="Personality Test", font=tk_font("small"),
                 fg=tk_color("nav_text"), bg=tk_color("nav_bg")).pack()

        sep = tk.Frame(self, height=1, bg=tk_color("nav_hover"))
        sep.pack(fill=tk.X, padx=20, pady=(0, 20))

        nav_items = [
            ("home", "Home", "landing"),
            ("quiz", "Start Test", "quiz"),
            ("results", "Results", "results"),
            ("history", "History", "history"),
        ]
        for key, label, page_name in nav_items:
            btn = tk.Button(self, text=label, font=tk_font("nav"),
                            fg=tk_color("nav_text"), bg=tk_color("nav_bg"),
                            activeforeground=tk_color("accent"),
                            activebackground=tk_color("nav_hover"),
                            bd=0, cursor="hand2", anchor="w", padx=30, pady=12,
                            command=lambda p=page_name, k=key: self._on_click(p, k))
            btn.pack(fill=tk.X)
            self._buttons[key] = btn

        bottom_frame = tk.Frame(self, bg=tk_color("nav_bg"))
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        self.theme_btn = tk.Button(bottom_frame, text="Toggle Theme", font=tk_font("small"),
                                   fg=tk_color("nav_text"), bg=tk_color("nav_bg"),
                                   activeforeground=tk_color("accent"),
                                   activebackground=tk_color("nav_hover"),
                                   bd=0, cursor="hand2", padx=20, pady=8,
                                   command=self._toggle_theme)
        self.theme_btn.pack(fill=tk.X)

        tk.Label(bottom_frame, text="v2.0.0", font=("Consolas", 9),
                 fg=tk_color("text_muted"), bg=tk_color("nav_bg")).pack()

    def _on_click(self, page_name, key):
        self.set_active(key)
        self.app.show_page(page_name)

    def _toggle_theme(self):
        new = theme.toggle()
        label = "Light Mode" if new == "dark" else "Dark Mode"
        self.theme_btn.config(text=label)
        self.app.apply_theme()

    def set_active(self, key):
        if self._active_key and self._active_key in self._buttons:
            self._buttons[self._active_key].config(bg=tk_color("nav_bg"), fg=tk_color("nav_text"))
        if key in self._buttons:
            self._buttons[key].config(bg=tk_color("nav_hover"), fg=tk_color("accent"))
            self._active_key = key

    def refresh_theme(self):
        self.config(bg=tk_color("nav_bg"))
        for key, btn in self._buttons.items():
            is_active = key == self._active_key
            btn.config(fg=tk_color("accent") if is_active else tk_color("nav_text"),
                       bg=tk_color("nav_hover") if is_active else tk_color("nav_bg"),
                       activeforeground=tk_color("accent"),
                       activebackground=tk_color("nav_hover"))
        self.theme_btn.config(fg=tk_color("nav_text"), bg=tk_color("nav_bg"),
                              activeforeground=tk_color("accent"),
                              activebackground=tk_color("nav_hover"))
