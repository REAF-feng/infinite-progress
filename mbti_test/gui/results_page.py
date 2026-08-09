"""Results page with tabs: overview, charts, report, actions."""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from gui.styles import theme, tk_color, tk_font
from gui.widgets.chart_widget import ChartWidget

class ResultsPage(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg=tk_color("content_bg"))
        self.app = app
        self.result = None
        self.report = None
        self._build()

    def _build(self):
        self.title_label = tk.Label(self, text="Test Results", font=tk_font("heading"),
                                    fg=tk_color("primary"), bg=tk_color("content_bg"))
        self.title_label.pack(pady=(25, 15))
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=30, pady=(0, 20))
        self.tab1 = tk.Frame(self.notebook, bg=tk_color("content_bg"))
        self.tab2 = tk.Frame(self.notebook, bg=tk_color("content_bg"))
        self.tab3 = tk.Frame(self.notebook, bg=tk_color("content_bg"))
        self.tab4 = tk.Frame(self.notebook, bg=tk_color("content_bg"))
        self.notebook.add(self.tab1, text=" Overview ")
        self.notebook.add(self.tab2, text=" Charts ")
        self.notebook.add(self.tab3, text=" Report ")
        self.notebook.add(self.tab4, text=" Actions ")

    def display_result(self, result, report_sections):
        self.result = result
        self.report = report_sections
        self._build_tab1()
        self._build_tab2()
        self._build_tab3()
        self._build_tab4()

    def _build_tab1(self):
        for w in self.tab1.winfo_children():
            w.destroy()
        r = self.result
        c = theme.colors
        tk.Label(self.tab1, text=r.type_code, font=("Microsoft YaHei", 72, "bold"),
                 fg=c["accent"], bg=tk_color("content_bg")).pack(pady=(20, 0))
        tk.Label(self.tab1, text=r.type_nickname, font=tk_font("heading"),
                 fg=c["text_primary"], bg=tk_color("content_bg")).pack(pady=(0, 15))
        card = tk.Frame(self.tab1, bg=tk_color("card_bg"),
                        highlightbackground=tk_color("card_border"),
                        highlightthickness=1, padx=30, pady=20)
        card.pack(fill=tk.X, padx=50, pady=10)
        for dim_key in ["EI", "SN", "TF", "JP"]:
            pcts = r.dimension_percentages.get(dim_key, {})
            if not pcts:
                continue
            k1, k2 = list(pcts.keys())
            v1, v2 = pcts[k1], pcts[k2]
            row = tk.Frame(card, bg=tk_color("card_bg"))
            row.pack(fill=tk.X, pady=8)
            tk.Label(row, text=f"{dim_key}", font=tk_font("body_bold"),
                     fg=c["text_primary"], bg=tk_color("card_bg"), width=8, anchor="w").pack(side=tk.LEFT)
            bar = tk.Canvas(row, height=24, bg=tk_color("card_bg"), highlightthickness=0)
            bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10)
            bar.create_rectangle(2, 2, 2 + int(v1 * 3), 22, fill=c["function_dominant"], outline="")
            bar.create_rectangle(2 + int(v1 * 3), 2, 302, 22, fill=c["function_inferior"], outline="")
            bar.create_text(5, 12, text=f"{k1} {v1}%", anchor="w", font=("Microsoft YaHei", 9), fill="white")
            bar.create_text(297, 12, text=f"{k2} {v2}%", anchor="e", font=("Microsoft YaHei", 9), fill="white")
        status = "PASSED" if r.validation_passed else "WARNING: Low consistency, consider retaking"
        sc = c["success"] if r.validation_passed else c["warning"]
        tk.Label(self.tab1, text=status, font=tk_font("body"), fg=sc, bg=tk_color("content_bg")).pack(pady=10)

    def _build_tab2(self):
        for w in self.tab2.winfo_children():
            w.destroy()
        sub_nb = ttk.Notebook(self.tab2)
        sub_nb.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        bar_frame = tk.Frame(sub_nb, bg=tk_color("card_bg"))
        sub_nb.add(bar_frame, text=" Bar Chart ")
        bc = ChartWidget(bar_frame)
        bc.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        bc.plot_function_bar(self.result.function_scores, self.result.function_stack, self.result.function_labels)
        radar_frame = tk.Frame(sub_nb, bg=tk_color("card_bg"))
        sub_nb.add(radar_frame, text=" Radar ")
        rc = ChartWidget(radar_frame)
        rc.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        rc.plot_radar(self.result.function_scores)
        dim_frame = tk.Frame(sub_nb, bg=tk_color("card_bg"))
        sub_nb.add(dim_frame, text=" Dimensions ")
        dc = ChartWidget(dim_frame)
        dc.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        dc.plot_dimension_comparison(self.result.dimension_percentages)

    def _build_tab3(self):
        for w in self.tab3.winfo_children():
            w.destroy()
        c = theme.colors
        text_frame = tk.Frame(self.tab3, bg=tk_color("card_bg"))
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar = tk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.report_text = tk.Text(text_frame, wrap=tk.WORD, font=("Microsoft YaHei", 11),
                                   fg=c["text_primary"], bg=c["card_bg"],
                                   yscrollcommand=scrollbar.set, bd=0, padx=20, pady=15)
        self.report_text.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.report_text.yview)
        if self.report:
            titles = {"core_traits": "1. Core Traits", "function_analysis": "2. Function Analysis",
                      "strengths": "3. Strengths", "weaknesses": "4. Weaknesses & Stress",
                      "careers": "5. Career Fit", "relationships": "6. Relationships",
                      "growth": "7. Growth Plan"}
            self.report_text.insert(tk.END, f"MBTI Expert Report - {self.result.type_code}\n")
            self.report_text.insert(tk.END, "=" * 56 + "\n\n")
            for key, title in titles.items():
                self.report_text.insert(tk.END, f"\n{title}\n{'-'*40}\n")
                self.report_text.insert(tk.END, self.report.get(key, "") + "\n")
        self.report_text.config(state=tk.DISABLED)

    def _build_tab4(self):
        for w in self.tab4.winfo_children():
            w.destroy()
        c = theme.colors
        card = tk.Frame(self.tab4, bg=tk_color("card_bg"),
                        highlightbackground=tk_color("card_border"),
                        highlightthickness=1, padx=50, pady=40)
        card.pack(expand=True)
        tk.Label(card, text="Export & Actions", font=tk_font("heading"),
                 fg=c["primary"], bg=tk_color("card_bg")).pack(pady=(0, 25))
        tk.Button(card, text="Export TXT", font=tk_font("button"), fg="#FFFFFF", bg=c["primary"],
                  bd=0, cursor="hand2", padx=30, pady=10,
                  command=self._export_txt).pack(fill=tk.X, pady=5)
        tk.Button(card, text="Export PDF", font=tk_font("button"), fg="#FFFFFF", bg=c["accent"],
                  bd=0, cursor="hand2", padx=30, pady=10,
                  command=self._export_pdf).pack(fill=tk.X, pady=5)
        tk.Button(card, text="Retake Test", font=tk_font("button"), fg=c["text_primary"],
                  bg=c["card_bg"], bd=1, cursor="hand2", padx=30, pady=10,
                  command=self._retake).pack(fill=tk.X, pady=5)
        tk.Button(card, text="Home", font=tk_font("button"), fg=c["text_secondary"],
                  bg=c["card_bg"], bd=1, cursor="hand2", padx=30, pady=10,
                  command=lambda: self.app.show_page("landing")).pack(fill=tk.X, pady=5)

    def _export_txt(self):
        from export.txt_exporter import export_txt
        fp = filedialog.asksaveasfilename(defaultextension=".txt",
                                          filetypes=[("Text", "*.txt")],
                                          initialfile=f"MBTI_{self.result.type_code}.txt")
        if fp:
            export_txt(self.result, self.report, fp)
            messagebox.showinfo("Done", f"Saved to {fp}")

    def _export_pdf(self):
        from export.pdf_exporter import export_pdf
        fp = filedialog.asksaveasfilename(defaultextension=".pdf",
                                          filetypes=[("PDF", "*.pdf")],
                                          initialfile=f"MBTI_{self.result.type_code}.pdf")
        if fp:
            export_pdf(self.result, self.report, fp)
            messagebox.showinfo("Done", f"Saved to {fp}")

    def _retake(self):
        if messagebox.askyesno("Retake", "Start a new test? Current result will be replaced."):
            self.app.show_page("quiz")

    def refresh_theme(self):
        self.config(bg=tk_color("content_bg"))
        self.title_label.config(fg=tk_color("primary"), bg=tk_color("content_bg"))
