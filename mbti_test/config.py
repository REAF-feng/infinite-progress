"""
MBTI - Global Config
"""
import os

APP_NAME = "MBTI Personality Test v2.0"
APP_VERSION = "2.0.0"
SCHEMA_VERSION = 2

DATA_DIR = os.path.join(os.path.expanduser("~"), ".mbti_test_pro")
RECORDS_FILE = os.path.join(DATA_DIR, "test_records.json")
PROGRESS_FILE = os.path.join(DATA_DIR, "quiz_progress.json")

LIKERT_MIN = 0
LIKERT_MAX = 4
LIKERT_LABELS = ["Very Disagree", "Disagree", "Neutral", "Agree", "Very Agree"]
# Chinese labels used in GUI
LIKERT_CN = ["非常不同意", "不同意", "中立", "同意", "非常同意"]
LIKERT_SHORT = ["极不同意", "不同意", "中立", "同意", "非常同意"]

TOTAL_QUESTIONS = 60
QUESTIONS_PER_DICHOTOMY = 15
DICHOTOMIES = ["EI", "SN", "TF", "JP"]

MIN_RESPONSE_TIME_MS = 1000
RUSHED_THRESHOLD_PCT = 50
CONSISTENCY_PASS_THRESHOLD = 0.75
MAX_CONSECUTIVE_SAME = 8

FUNCTION_BASE_SCORES = {
    "dominant": 85.0, "auxiliary": 70.0,
    "tertiary": 50.0, "inferior": 30.0,
    "shadow_dominant": 22.0, "shadow_auxiliary": 18.0,
    "shadow_tertiary": 13.0, "shadow_inferior": 8.0,
}
FUNCTION_ACTIVATION_RANGE = 25.0
PREFERENCE_SLIGHT = 5.0
PREFERENCE_MODERATE = 15.0

REPORT_TARGET_CHARS = 12000
EXPORT_DEFAULT_DIR = os.path.join(os.path.expanduser("~"), "Desktop")

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 840
WINDOW_MIN_WIDTH = 1024
WINDOW_MIN_HEIGHT = 680
NAV_WIDTH = 200

MATPLOTLIB_CHINESE_FONT = "Microsoft YaHei"
MATPLOTLIB_FALLBACK_FONTS = ["Microsoft YaHei", "SimHei", "sans-serif"]

LIGHT_THEME = {
    "nav_bg": "#1A1A2E", "nav_active": "#E94560", "nav_text": "#E0E0E0",
    "nav_hover": "#16213E", "content_bg": "#F0F2F5", "card_bg": "#FFFFFF",
    "card_border": "#DEE2E6", "primary": "#0F3460", "accent": "#E94560",
    "success": "#20A39E", "warning": "#F39C12", "danger": "#E74C3C",
    "text_primary": "#2D3436", "text_secondary": "#636E72",
    "text_muted": "#ADB5BD", "progress_bg": "#E9ECEF",
    "progress_fill": "#0F3460",
    "function_dominant": "#E94560", "function_auxiliary": "#0F3460",
    "function_tertiary": "#20A39E", "function_inferior": "#F39C12",
    "function_shadow": "#ADB5BD",
    "radar_fill": "#E9456080", "radar_line": "#E94560",
}

DARK_THEME = {
    "nav_bg": "#0D1117", "nav_active": "#58A6FF", "nav_text": "#C9D1D9",
    "nav_hover": "#161B22", "content_bg": "#161B22", "card_bg": "#21262D",
    "card_border": "#30363D", "primary": "#58A6FF", "accent": "#F78166",
    "success": "#3FB950", "warning": "#D29922", "danger": "#F85149",
    "text_primary": "#C9D1D9", "text_secondary": "#8B949E",
    "text_muted": "#484F58", "progress_bg": "#30363D",
    "progress_fill": "#58A6FF",
    "function_dominant": "#F78166", "function_auxiliary": "#58A6FF",
    "function_tertiary": "#3FB950", "function_inferior": "#D29922",
    "function_shadow": "#484F58",
    "radar_fill": "#F7816680", "radar_line": "#58A6FF",
}

DEFAULT_THEME = "dark"
