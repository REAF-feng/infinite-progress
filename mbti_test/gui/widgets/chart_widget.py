"""Matplotlib chart widget embedded in Tkinter."""
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from gui.styles import theme

def _setup_font():
    try:
        plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
        plt.rcParams["axes.unicode_minus"] = False
    except Exception:
        pass

_setup_font()

class ChartWidget(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg=theme.get("card_bg", "#FFFFFF"), **kwargs)
        self.fig = None
        self.canvas = None

    def plot_function_bar(self, function_scores, function_stack, function_labels):
        self._clear()
        colors = theme.colors
        self.fig = Figure(figsize=(8, 4.5), dpi=100, facecolor=colors["card_bg"])
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(colors["card_bg"])
        funcs = function_stack
        scores = [function_scores.get(f, 0) for f in funcs]
        bar_colors = []
        for f in funcs:
            label = function_labels.get(f, "")
            if "Dominant" in label or "主导" in label:
                bar_colors.append(colors["function_dominant"])
            elif "Auxiliary" in label or "辅助" in label:
                bar_colors.append(colors["function_auxiliary"])
            elif "Tertiary" in label or "第三" in label:
                bar_colors.append(colors["function_tertiary"])
            elif "Inferior" in label or "劣势" in label:
                bar_colors.append(colors["function_inferior"])
            else:
                bar_colors.append(colors["function_shadow"])
        ax.barh(range(len(funcs)), scores, height=0.6, color=bar_colors)
        ax.set_yticks(range(len(funcs)))
        ax.set_yticklabels(funcs, fontsize=11)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel("Score (0-100)", fontsize=10, color=colors["text_secondary"])
        ax.tick_params(colors=colors["text_secondary"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_color(colors["text_muted"])
        ax.spines["bottom"].set_color(colors["text_muted"])
        ax.set_title("Cognitive Functions", fontsize=14, fontweight="bold",
                     color=colors["text_primary"], pad=15)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def plot_dimension_comparison(self, dim_percentages):
        self._clear()
        colors = theme.colors
        self.fig = Figure(figsize=(7, 3.5), dpi=100, facecolor=colors["card_bg"])
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(colors["card_bg"])
        dims = ["EI", "SN", "TF", "JP"]
        labels = ["E/I", "S/N", "T/F", "J/P"]
        x = range(len(dims))
        width = 0.35
        first_vals = []
        for d in dims:
            pcts = dim_percentages.get(d, {})
            if pcts:
                first_vals.append(list(pcts.values())[0])
            else:
                first_vals.append(50)
        second_vals = [100 - v for v in first_vals]
        ax.bar([i - width/2 for i in x], first_vals, width, color=colors["function_auxiliary"], label="First")
        ax.bar([i + width/2 for i in x], second_vals, width, color=colors["function_inferior"], label="Second")
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=9)
        ax.set_ylim(0, 100)
        ax.set_ylabel("%", fontsize=10, color=colors["text_secondary"])
        ax.tick_params(colors=colors["text_secondary"])
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.set_title("Dimension Comparison", fontsize=13, fontweight="bold",
                     color=colors["text_primary"], pad=12)
        ax.legend(fontsize=8)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def plot_radar(self, function_scores):
        self._clear()
        colors = theme.colors
        self.fig = Figure(figsize=(6, 6), dpi=100, facecolor=colors["card_bg"])
        ax = self.fig.add_subplot(111, polar=True)
        ax.set_facecolor(colors["card_bg"])
        funcs = ["Ne", "Ni", "Se", "Si", "Te", "Ti", "Fe", "Fi"]
        labels = ["Ne", "Ni", "Se", "Si", "Te", "Ti", "Fe", "Fi"]
        values = [function_scores.get(f, 0) for f in funcs]
        angles = [n / float(len(funcs)) * 2 * 3.14159 for n in range(len(funcs))]
        values += values[:1]
        angles += angles[:1]
        ax.fill(angles, values, alpha=0.25, color=colors["radar_fill"])
        ax.plot(angles, values, color=colors["radar_line"], linewidth=2)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=8, color=colors["text_primary"])
        ax.set_ylim(0, 100)
        ax.set_yticks([20, 40, 60, 80, 100])
        ax.set_yticklabels(["20", "40", "60", "80", "100"], fontsize=7,
                           color=colors["text_muted"])
        ax.set_title("Radar Chart", fontsize=13, fontweight="bold",
                     color=colors["text_primary"], pad=20)
        ax.grid(True, color=colors["text_muted"], alpha=0.3)
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        self.canvas.draw()

    def _clear(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        if self.fig:
            plt.close(self.fig)
            self.fig = None

    def refresh_theme(self):
        pass
