"""Main Tkinter application controller."""
import tkinter as tk
from tkinter import messagebox
import time
from config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT
from models.mbti_result import MBTIResult
from models.test_record import TestRecord
from data.question_bank import QUESTIONS
from data.type_profiles import TYPE_PROFILES
from scoring.calculator import run_full_scoring
from scoring.anti_cheat import validate_answers
from storage.json_storage import JSONStorage, clear_progress
from report.generator import generate_full_report
from gui.styles import theme, tk_color
from gui.widgets.navigation_bar import NavigationBar
from gui.landing_page import LandingPage
from gui.quiz_page import QuizPage
from gui.results_page import ResultsPage
from gui.history_page import HistoryPage

class MBTIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MBTI Personality Test v2.0")
        self.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.current_page = None
        self.current_page_name = None
        self.latest_result = None
        self.latest_report = None
        self.quiz_start_time = 0
        self.storage = JSONStorage()
        self.pages = {}
        self._build_nav()
        self._build_content()
        self._init_pages()
        self.show_page("landing")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_nav(self):
        self.nav = NavigationBar(self, self, width=200)
        self.nav.pack(side=tk.LEFT, fill=tk.Y)

    def _build_content(self):
        self.content = tk.Frame(self, bg=tk_color("content_bg"))
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def _init_pages(self):
        self.pages["landing"] = LandingPage(self.content, self)
        self.pages["quiz"] = QuizPage(self.content, self)
        self.pages["results"] = ResultsPage(self.content, self)
        self.pages["history"] = HistoryPage(self.content, self)

    def show_page(self, page_name):
        if self.current_page and hasattr(self.current_page, "on_leave"):
            self.current_page.on_leave()
        if self.current_page:
            self.current_page.pack_forget()
        page = self.pages.get(page_name)
        if page:
            page.pack(fill=tk.BOTH, expand=True)
            self.current_page = page
            self.current_page_name = page_name
            if hasattr(page, "on_enter"):
                page.on_enter()
            nav_map = {"landing": "home", "quiz": "quiz", "results": "results", "history": "history"}
            self.nav.set_active(nav_map.get(page_name, "home"))

    def start_new_quiz(self):
        clear_progress()
        self.quiz_start_time = time.time()
        self.show_page("quiz")

    def on_quiz_complete(self, answers):
        duration = int(time.time() - self.quiz_start_time) if self.quiz_start_time else 0
        validation = validate_answers(answers, QUESTIONS)
        if not validation["passed"]:
            ws = ", ".join(validation.get("warnings", ["unknown"]))
            if not messagebox.askyesno("Warning",
                                       f"Issues detected: {ws}\nConsistency: {validation['consistency_score']:.2f}\n\nView results anyway?"):
                self.show_page("quiz")
                return
        result = run_full_scoring(answers, QUESTIONS, validation)
        profile = TYPE_PROFILES.get(result.type_code, {})
        result.type_nickname = profile.get("nickname", result.type_code)
        report = generate_full_report(result)
        result.report_sections = report
        self._save_record(result, answers, duration)
        self.latest_result = result
        self.latest_report = report
        self.display_results(result, report)

    def display_results(self, result, report):
        self.latest_result = result
        self.latest_report = report
        self.show_page("results")
        self.pages["results"].display_result(result, report)

    def _save_record(self, result, answers, duration):
        rd = {
            "type_code": result.type_code,
            "type_nickname": result.type_nickname,
            "dimension_scores": result.dimension_scores,
            "dimension_percentages": result.dimension_percentages,
            "function_scores": result.function_scores,
            "function_stack": result.function_stack,
            "function_labels": result.function_labels,
            "validation_passed": result.validation_passed,
            "consistency_score": result.consistency_score,
            "report_sections": result.report_sections,
        }
        ad = [{"question_id": a.question_id, "value": a.value, "timestamp_ms": a.timestamp_ms} for a in answers]
        rec = TestRecord.create_new(ad, duration, rd)
        try:
            self.storage.save(rec)
        except Exception:
            pass  # non-critical: don't block results display

    def apply_theme(self):
        self.content.config(bg=tk_color("content_bg"))
        for page in self.pages.values():
            if hasattr(page, "refresh_theme"):
                page.refresh_theme()
        self.nav.refresh_theme()

    def _on_close(self):
        if self.current_page_name == "quiz" and hasattr(self.current_page, "on_leave"):
            self.current_page.on_leave()
        self.destroy()
