"""History page - past test records."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from storage.json_storage import JSONStorage
from gui.styles import theme, tk_color, tk_font

class HistoryPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=tk_color("content_bg"))
        self.app = app
        self.storage = JSONStorage()
        self.records = []
        self._build()

    def _build(self):
        self.title_label = tk.Label(self, text="Test History", font=tk_font("heading"),
                                    fg=tk_color("primary"), bg=tk_color("content_bg"))
        self.title_label.pack(pady=(25, 15))
        tree_frame = tk.Frame(self, bg=tk_color("card_bg"),
                              highlightbackground=tk_color("card_border"),
                              highlightthickness=1)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 10))
        columns = ("date", "type", "nickname", "consistency", "duration")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=12)
        self.tree.heading("date", text="Date")
        self.tree.heading("type", text="Type")
        self.tree.heading("nickname", text="Nickname")
        self.tree.heading("consistency", text="Consistency")
        self.tree.heading("duration", text="Duration")
        self.tree.column("date", width=180, anchor="center")
        self.tree.column("type", width=100, anchor="center")
        self.tree.column("nickname", width=140, anchor="center")
        self.tree.column("consistency", width=100, anchor="center")
        self.tree.column("duration", width=80, anchor="center")
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.bind("<Double-1>", self._on_view)
        btn_frame = tk.Frame(self, bg=tk_color("content_bg"))
        btn_frame.pack(fill=tk.X, padx=30, pady=(0, 20))
        tk.Button(btn_frame, text="View", font=tk_font("button"), fg="#FFFFFF",
                  bg=tk_color("primary"), bd=0, cursor="hand2", padx=18, pady=6,
                  command=self._view_selected).pack(side=tk.LEFT, padx=(0, 10))
        tk.Button(btn_frame, text="Delete", font=tk_font("button"),
                  fg=tk_color("text_secondary"), bg=tk_color("card_bg"), bd=1,
                  cursor="hand2", padx=18, pady=6,
                  command=self._delete_selected).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="Refresh", font=tk_font("button"),
                  fg=tk_color("text_secondary"), bg=tk_color("card_bg"), bd=1,
                  cursor="hand2", padx=18, pady=6,
                  command=self._refresh).pack(side=tk.RIGHT)

    def on_enter(self):
        self._refresh()

    def _refresh(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.records = self.storage.load_all()
        for rec in self.records:
            ts = (rec.timestamp or "")[:16]
            result = rec.result or {}
            tc = result.get("type_code", "?")
            nn = result.get("type_nickname", "")
            cs = result.get("consistency_score", 0)
            dur = rec.test_duration_seconds or 0
            dur_d = f"{dur//60}m{dur%60}s" if dur else "?"
            self.tree.insert("", tk.END, iid=rec.id or "",
                             values=(ts, tc, nn, f"{cs:.2f}", dur_d))
        if not self.records:
            self.tree.insert("", tk.END, values=("No records yet", "", "", "", ""))

    def _get_selected(self):
        sel = self.tree.selection()
        return sel[0] if sel else ""

    def _view_selected(self):
        rid = self._get_selected()
        if not rid:
            return messagebox.showinfo("Info", "Select a record first.")
        self._on_view(None)

    def _on_view(self, event):
        rid = self._get_selected()
        if not rid:
            return
        rec = self.storage.get_by_id(rid)
        if rec and rec.result:
            r = rec.result
            from models.mbti_result import MBTIResult
            result = MBTIResult(
                type_code=r.get("type_code", ""),
                type_nickname=r.get("type_nickname", ""),
                dimension_scores=r.get("dimension_scores", {}),
                dimension_percentages=r.get("dimension_percentages", {}),
                function_scores=r.get("function_scores", {}),
                function_stack=r.get("function_stack", []),
                function_labels=r.get("function_labels", {}),
                validation_passed=r.get("validation_passed", True),
                consistency_score=r.get("consistency_score", 0),
                report_sections=r.get("report_sections", {}),
            )
            self.app.display_results(result, r.get("report_sections", {}))
            messagebox.showinfo("Loaded", f"Loaded {result.type_code}. Switch to Results tab.")

    def _delete_selected(self):
        rid = self._get_selected()
        if not rid:
            return
        if messagebox.askyesno("Delete", "Delete this record?"):
            self.storage.delete(rid)
            self._refresh()

    def refresh_theme(self):
        self.config(bg=tk_color("content_bg"))
        self.title_label.config(fg=tk_color("primary"), bg=tk_color("content_bg"))
