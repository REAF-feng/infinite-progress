"""Quiz page - question-by-question with Likert scale."""
import tkinter as tk
from tkinter import messagebox
from models.answer import Answer
from data.question_bank import QUESTIONS
from storage.json_storage import save_progress, load_progress, clear_progress
from gui.styles import theme, tk_color, tk_font
from gui.widgets.progress_widget import ProgressWidget
from gui.widgets.likert_widget import LikertWidget
import time

class QuizPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=tk_color("content_bg"))
        self.app = app
        self.questions = QUESTIONS
        self.total = len(self.questions)
        self.current_idx = 0
        self.answers = {}
        self.question_start = 0
        self._build()

    def _build(self):
        self.columnconfigure(0, weight=1)
        self.progress = ProgressWidget(self, height=28)
        self.progress.grid(row=0, column=0, sticky="ew", padx=40, pady=(20, 10))

        self.card = tk.Frame(self, bg=tk_color("card_bg"), bd=0,
                             highlightbackground=tk_color("card_border"),
                             highlightthickness=1)
        self.card.grid(row=1, column=0, sticky="nsew", padx=40, pady=10)
        self.card.columnconfigure(0, weight=1)

        self.qnum_label = tk.Label(self.card, text="", font=tk_font("subheading"),
                                   fg=tk_color("text_muted"), bg=tk_color("card_bg"))
        self.qnum_label.grid(row=0, column=0, sticky="w", padx=30, pady=(25, 5))

        self.qtext_label = tk.Label(self.card, text="", font=("Microsoft YaHei", 16),
                                    fg=tk_color("text_primary"), bg=tk_color("card_bg"),
                                    wraplength=700, justify="left")
        self.qtext_label.grid(row=1, column=0, sticky="w", padx=30, pady=(10, 5))

        self.dim_label = tk.Label(self.card, text="", font=tk_font("small"),
                                  fg=tk_color("accent"), bg=tk_color("card_bg"))
        self.dim_label.grid(row=2, column=0, sticky="w", padx=30, pady=(0, 15))

        sep = tk.Frame(self.card, height=1, bg=tk_color("card_border"))
        sep.grid(row=3, column=0, sticky="ew", padx=30)

        self.likert = LikertWidget(self.card, on_select=self._on_answer)
        self.likert.grid(row=4, column=0, sticky="ew", padx=30, pady=20)

        nav_frame = tk.Frame(self, bg=tk_color("content_bg"))
        nav_frame.grid(row=2, column=0, sticky="ew", padx=40, pady=(5, 20))
        nav_frame.columnconfigure(0, weight=1)
        nav_frame.columnconfigure(1, weight=1)

        self.prev_btn = tk.Button(nav_frame, text="Previous", font=tk_font("button"),
                                  fg=tk_color("text_primary"), bg=tk_color("card_bg"),
                                  activeforeground=tk_color("accent"),
                                  activebackground=tk_color("card_bg"),
                                  bd=1, cursor="hand2", padx=20, pady=8,
                                  command=self._prev_question)
        self.prev_btn.grid(row=0, column=0, sticky="w")

        btn_frame = tk.Frame(nav_frame, bg=tk_color("content_bg"))
        btn_frame.grid(row=0, column=1, sticky="e")

        self.save_btn = tk.Button(btn_frame, text="Save", font=tk_font("small"),
                                  fg=tk_color("text_secondary"), bg=tk_color("content_bg"),
                                  activeforeground=tk_color("accent"),
                                  bd=0, cursor="hand2", padx=12, pady=6,
                                  command=self._save_progress)
        self.save_btn.pack(side=tk.LEFT, padx=(0, 15))

        self.next_btn = tk.Button(btn_frame, text="Next", font=tk_font("button"),
                                  fg="#FFFFFF", bg=tk_color("primary"),
                                  activeforeground="#FFFFFF", activebackground=tk_color("accent"),
                                  bd=0, cursor="hand2", padx=24, pady=8,
                                  command=self._next_question)
        self.next_btn.pack(side=tk.LEFT)
        self.rowconfigure(1, weight=1)

    def on_enter(self):
        saved = load_progress()
        if saved and saved.get("answers"):
            resume = messagebox.askyesno("Resume", f"Found saved progress ({len(saved['answers'])}/60). Resume?")
            if resume:
                self.current_idx = saved.get("current_index", 0)
                self.answers = {}
                for item in saved.get("answers", []):
                    self.answers[item["question_id"]] = Answer(
                        question_id=item["question_id"], value=item["value"],
                        timestamp_ms=item.get("timestamp_ms", 0))
                self._show_current()
                return
        self.current_idx = 0
        self.answers = {}
        clear_progress()
        self._show_current()

    def _make_progress_dict(self):
        return {
            "current_index": self.current_idx,
            "answers": [{"question_id": a.question_id, "value": a.value,
                         "timestamp_ms": a.timestamp_ms}
                        for a in self.answers.values()],
        }

    def on_leave(self):
        if self.answers and len(self.answers) < self.total:
            save_progress(self._make_progress_dict())

    def _show_current(self):
        if 0 <= self.current_idx < self.total:
            q = self.questions[self.current_idx]
            self.qnum_label.config(text=f"Question {self.current_idx + 1} / {self.total}")
            self.qtext_label.config(text=q.text)
            dim_names = {"EI": "Energy", "SN": "Information", "TF": "Decision", "JP": "Lifestyle"}
            self.dim_label.config(text=f"Dimension: {q.dichotomy} - {dim_names.get(q.dichotomy, '')}")
            self.progress.set_progress(self.current_idx + 1, self.total)
            if q.id in self.answers:
                self.likert.set_value(self.answers[q.id].value)
            else:
                self.likert.clear()
            self.question_start = time.time()
            self._update_nav()

    def _update_nav(self):
        self.prev_btn.config(state=tk.NORMAL if self.current_idx > 0 else tk.DISABLED)
        if self.current_idx >= self.total - 1:
            self.next_btn.config(text="Submit", bg=tk_color("accent"))
        else:
            self.next_btn.config(text="Next", bg=tk_color("primary"))

    def _on_answer(self, value):
        if 0 <= self.current_idx < self.total:
            q = self.questions[self.current_idx]
            elapsed = (time.time() - self.question_start) * 1000
            self.answers[q.id] = Answer(question_id=q.id, value=value, timestamp_ms=elapsed)

    def _next_question(self):
        if self.current_idx >= self.total - 1:
            self._finish_quiz()
            return
        q = self.questions[self.current_idx]
        if q.id not in self.answers:
            if not messagebox.askokcancel("Skip", "Not answered yet. Skip?"):
                return
        self.current_idx += 1
        self._show_current()

    def _prev_question(self):
        if self.current_idx > 0:
            self.current_idx -= 1
            self._show_current()

    def _save_progress(self):
        if self.answers:
            save_progress(self._make_progress_dict())
            messagebox.showinfo("Saved", f"Progress saved ({len(self.answers)}/60).")

    def _finish_quiz(self):
        answered = len(self.answers)
        if answered < self.total:
            if not messagebox.askyesno("Confirm", f"Only {answered}/{self.total} answered. Unanswered items get neutral score. Submit?"):
                return
        for q in self.questions:
            if q.id not in self.answers:
                self.answers[q.id] = Answer(question_id=q.id, value=2, timestamp_ms=0)
        clear_progress()
        self.app.on_quiz_complete(list(self.answers.values()))

    def refresh_theme(self):
        self.config(bg=tk_color("content_bg"))
        self.card.config(bg=tk_color("card_bg"), highlightbackground=tk_color("card_border"))
        self.qnum_label.config(fg=tk_color("text_muted"), bg=tk_color("card_bg"))
        self.qtext_label.config(fg=tk_color("text_primary"), bg=tk_color("card_bg"))
        self.dim_label.config(fg=tk_color("accent"), bg=tk_color("card_bg"))
        self.likert.refresh_theme()
