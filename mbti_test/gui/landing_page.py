"""Landing/welcome page."""
import tkinter as tk
from gui.styles import theme, tk_color, tk_font

class LandingPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=tk_color("content_bg"))
        self.app = app
        self._build()

    def _build(self):
        tk.Frame(self, height=60, bg=tk_color("content_bg")).pack()
        tk.Label(self, text="MBTI Personality Test", font=tk_font("title_large"),
                 fg=tk_color("primary"), bg=tk_color("content_bg")).pack(pady=(0, 10))
        tk.Label(self, text="60 Professional Questions | Jungian 8 Functions | Expert Report",
                 font=tk_font("subheading"), fg=tk_color("text_secondary"),
                 bg=tk_color("content_bg")).pack(pady=(0, 30))

        card = tk.Frame(self, bg=tk_color("card_bg"), bd=0,
                        highlightbackground=tk_color("card_border"),
                        highlightthickness=1, padx=40, pady=30)
        card.pack(ipadx=60, ipady=20)

        features = [
            ("60 Standard Items", "Based on MBTI official scale with Jungian theory"),
            ("8 Function Analysis", "Radar chart + bar chart of cognitive functions"),
            ("Expert Report", "7 sections covering traits, career, relationships, growth"),
            ("Local Storage", "All data stored locally, no network upload"),
            ("PDF Export", "Export full report as PDF file"),
        ]
        for title, desc in features:
            row = tk.Frame(card, bg=tk_color("card_bg"))
            row.pack(fill=tk.X, pady=8)
            tk.Label(row, text=title, font=tk_font("body_bold"),
                     fg=tk_color("text_primary"), bg=tk_color("card_bg")).pack(side=tk.LEFT)
            tk.Label(row, text=f"  - {desc}", font=tk_font("body"),
                     fg=tk_color("text_secondary"), bg=tk_color("card_bg")).pack(side=tk.LEFT)

        tk.Frame(self, height=25, bg=tk_color("content_bg")).pack()
        start_btn = tk.Button(self, text="Start Test", font=tk_font("subheading"),
                              fg="#FFFFFF", bg=tk_color("accent"),
                              activeforeground="#FFFFFF", activebackground=tk_color("primary"),
                              bd=0, cursor="hand2", padx=60, pady=14,
                              command=self._start_test)
        start_btn.pack(pady=(10, 8))
        tk.Label(self, text="10-15 min | Save progress mid-test",
                 font=tk_font("small"), fg=tk_color("text_muted"),
                 bg=tk_color("content_bg")).pack()
        tk.Frame(self, height=30, bg=tk_color("content_bg")).pack(side=tk.BOTTOM)
        tk.Label(self, text="v2.0.0 | Professional Assessment | Offline Only",
                 font=tk_font("small"), fg=tk_color("text_muted"),
                 bg=tk_color("content_bg")).pack(side=tk.BOTTOM, pady=15)

    def _start_test(self):
        self.app.start_new_quiz()

    def refresh_theme(self):
        self.config(bg=tk_color("content_bg"))
