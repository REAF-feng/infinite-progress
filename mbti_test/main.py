#!/usr/bin/env python3
"""
MBTI Personality Test v2.0 - Entry Point
Python + Tkinter + Matplotlib, fully offline.

Run:  python main.py
Build: pyinstaller --onedir --noconsole --name MBTI_Test main.py
"""

import sys
import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

import matplotlib
matplotlib.use("TkAgg")

import matplotlib.pyplot as plt
try:
    plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "sans-serif"]
    plt.rcParams["axes.unicode_minus"] = False
except Exception:
    pass

from gui.app import MBTIApp

def main():
    app = MBTIApp()
    app.mainloop()

if __name__ == "__main__":
    main()
