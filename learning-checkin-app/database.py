"""数据库初始化与操作层"""
import sqlite3
import os
from datetime import date, datetime, timedelta

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'learning.db')


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript('''
        CREATE TABLE IF NOT EXISTS checkins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            subject TEXT NOT NULL,
            date DATE NOT NULL,
            study_time_min INTEGER DEFAULT 0,
            self_score INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(subject, date)
        );

        CREATE TABLE IF NOT EXISTS typing_sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            wpm REAL NOT NULL,
            accuracy REAL NOT NULL,
            duration_sec INTEGER DEFAULT 0,
            text_category TEXT DEFAULT '',
            text_name TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS vocabulary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word TEXT NOT NULL UNIQUE,
            meaning TEXT NOT NULL,
            level TEXT DEFAULT 'cet4',
            mastered INTEGER DEFAULT 0,
            review_count INTEGER DEFAULT 0,
            last_review_date DATE
        );
    ''')

    conn.commit()
    conn.close()


# ==================== 打卡相关 ====================

def get_today_checkins():
    """获取今日所有科目的打卡状态"""
    today = date.today().isoformat()
    conn = get_db()
    rows = conn.execute(
        "SELECT subject, study_time_min, self_score, notes FROM checkins WHERE date = ?", (today,)
    ).fetchall()
    conn.close()
    result = {}
    for r in rows:
        result[r['subject']] = {
            'study_time_min': r['study_time_min'],
            'self_score': r['self_score'],
            'notes': r['notes']
        }
    return result


def do_checkin(subject, study_time_min=0, self_score=0, notes=''):
    """执行打卡（同科同日不可重复）"""
    today = date.today().isoformat()
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO checkins (subject, date, study_time_min, self_score, notes) VALUES (?, ?, ?, ?, ?)",
            (subject, today, study_time_min, self_score, notes)
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # 今天已经打过卡，更新
        conn.execute(
            "UPDATE checkins SET study_time_min=?, self_score=?, notes=? WHERE subject=? AND date=?",
            (study_time_min, self_score, notes, subject, today)
        )
        conn.commit()
        return True
    finally:
        conn.close()


def get_checkin_history(subject, days=30):
    """获取某科最近N天的打卡记录"""
    conn = get_db()
    rows = conn.execute(
        "SELECT date, study_time_min, self_score, notes FROM checkins WHERE subject=? ORDER BY date DESC LIMIT ?",
        (subject, days)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_streak(subject):
    """计算某科的连续打卡天数"""
    conn = get_db()
    rows = conn.execute(
        "SELECT date FROM checkins WHERE subject=? ORDER BY date DESC LIMIT 366",
        (subject,)
    ).fetchall()
    conn.close()

    if not rows:
        return 0

    dates = [row['date'] for row in rows]
    today = date.today()
    yesterday = today - timedelta(days=1)

    # 检查最近一次打卡是否是今天或昨天（中断则streak=0）
    latest = datetime.strptime(dates[0], '%Y-%m-%d').date()
    if latest < yesterday:
        return 0

    streak = 1
    for i in range(1, len(dates)):
        d1 = datetime.strptime(dates[i - 1], '%Y-%m-%d').date()
        d2 = datetime.strptime(dates[i], '%Y-%m-%d').date()
        if (d1 - d2).days == 1:
            streak += 1
        else:
            break
    return streak


def get_weekly_heatmap():
    """获取本周热力图数据（最近7天 × 4科）"""
    today = date.today()
    result = {}
    for i in range(6, -1, -1):
        d = today - timedelta(days=i)
        day_name = ['周一', '周二', '周三', '周四', '周五', '周六', '周日'][d.weekday()]
        result[d.isoformat()] = {'label': f"{d.month}/{d.day} {day_name}", 'subjects': {}}

    conn = get_db()
    week_start = (today - timedelta(days=6)).isoformat()
    rows = conn.execute(
        "SELECT subject, date FROM checkins WHERE date >= ? AND date <= ?",
        (week_start, today.isoformat())
    ).fetchall()
    conn.close()

    for r in rows:
        if r['date'] in result:
            result[r['date']]['subjects'][r['subject']] = True

    return result


def get_stats():
    """获取综合统计数据"""
    conn = get_db()
    stats = {}

    # 各科总打卡天数
    for subj in ['english', 'typing', 'c_lang', 'python']:
        row = conn.execute(
            "SELECT COUNT(*) as cnt, COALESCE(SUM(study_time_min), 0) as total_min FROM checkins WHERE subject=?",
            (subj,)
        ).fetchone()
        stats[subj] = {'total_days': row['cnt'], 'total_minutes': row['total_min']}

    # 各科连续打卡
    for subj in ['english', 'typing', 'c_lang', 'python']:
        stats[f'{subj}_streak'] = get_streak(subj)

    # 打字统计
    typing = conn.execute(
        "SELECT COUNT(*) as sessions, COALESCE(ROUND(AVG(wpm), 1), 0) as avg_wpm, COALESCE(MAX(wpm), 0) as best_wpm, COALESCE(ROUND(AVG(accuracy), 1), 0) as avg_acc FROM typing_sessions"
    ).fetchone()
    stats['typing_sessions'] = typing['sessions']
    stats['typing_avg_wpm'] = typing['avg_wpm']
    stats['typing_best_wpm'] = typing['best_wpm']
    stats['typing_avg_acc'] = typing['avg_acc']

    # 英语词汇统计
    vocab = conn.execute(
        "SELECT COUNT(*) as total, COALESCE(SUM(CASE WHEN mastered=1 THEN 1 ELSE 0 END), 0) as mastered FROM vocabulary"
    ).fetchone()
    stats['vocab_total'] = vocab['total']
    stats['vocab_mastered'] = vocab['mastered']

    conn.close()
    return stats


# ==================== 打字相关 ====================

def save_typing_session(wpm, accuracy, duration_sec, text_category='', text_name=''):
    """保存打字训练成绩"""
    conn = get_db()
    conn.execute(
        "INSERT INTO typing_sessions (wpm, accuracy, duration_sec, text_category, text_name) VALUES (?, ?, ?, ?, ?)",
        (wpm, accuracy, duration_sec, text_category, text_name)
    )
    conn.commit()
    conn.close()


def get_typing_history(days=30):
    """获取打字历史记录"""
    conn = get_db()
    rows = conn.execute(
        "SELECT wpm, accuracy, duration_sec, text_category, text_name, created_at FROM typing_sessions ORDER BY created_at DESC LIMIT ?",
        (days * 10,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_typing_trend(days=30):
    """获取打字趋势数据（用于图表）"""
    conn = get_db()
    cutoff = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    rows = conn.execute(
        "SELECT DATE(created_at) as date, ROUND(AVG(wpm), 1) as avg_wpm, ROUND(AVG(accuracy), 1) as avg_acc FROM typing_sessions WHERE created_at >= ? GROUP BY DATE(created_at) ORDER BY date",
        (cutoff,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ==================== 英语词汇相关 ====================

def get_random_words(count=10):
    """随机获取未掌握的单词"""
    conn = get_db()
    rows = conn.execute(
        "SELECT id, word, meaning, mastered, review_count FROM vocabulary WHERE mastered=0 ORDER BY RANDOM() LIMIT ?",
        (count,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def mark_word_reviewed(word_id, mastered):
    """标记单词复习状态"""
    conn = get_db()
    conn.execute(
        "UPDATE vocabulary SET review_count=review_count+1, mastered=?, last_review_date=? WHERE id=?",
        (1 if mastered else 0, date.today().isoformat(), word_id)
    )
    conn.commit()
    conn.close()


def get_vocab_stats():
    """获取词汇学习统计"""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as cnt FROM vocabulary").fetchone()['cnt']
    mastered = conn.execute("SELECT COUNT(*) as cnt FROM vocabulary WHERE mastered=1").fetchone()['cnt']
    today_reviewed = conn.execute(
        "SELECT COUNT(*) as cnt FROM vocabulary WHERE last_review_date=?", (date.today().isoformat(),)
    ).fetchone()['cnt']
    conn.close()
    return {'total': total, 'mastered': mastered, 'today_reviewed': today_reviewed}


def import_vocabulary(words):
    """批量导入词汇（如已存在则忽略）"""
    conn = get_db()
    for w in words:
        try:
            conn.execute(
                "INSERT INTO vocabulary (word, meaning, level) VALUES (?, ?, ?)",
                (w['word'], w['meaning'], w.get('level', 'cet4'))
            )
        except sqlite3.IntegrityError:
            pass
    conn.commit()
    conn.close()
