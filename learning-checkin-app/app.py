"""学习打卡软件 — Flask 主应用"""
import json
import os
from flask import Flask, render_template, request, jsonify
from database import (
    init_db, get_today_checkins, do_checkin, get_checkin_history,
    get_streak, get_weekly_heatmap, get_stats,
    save_typing_session, get_typing_history, get_typing_trend,
    get_random_words, mark_word_reviewed, get_vocab_stats, import_vocabulary
)

app = Flask(__name__)
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def load_json(filename):
    """加载JSON数据文件"""
    path = os.path.join(DATA_DIR, filename)
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


# ==================== 页面路由 ====================

@app.route('/')
def index():
    """仪表盘主页"""
    return render_template('index.html')


@app.route('/english')
def english():
    """英语学习页"""
    return render_template('english.html')


@app.route('/typing')
def typing():
    """打字训练页"""
    return render_template('typing.html')


@app.route('/c-lang')
def c_lang():
    """C语言学习页"""
    return render_template('c_lang.html')


@app.route('/python')
def python_page():
    """Python学习页"""
    return render_template('python.html')


# ==================== API路由 ====================

@app.route('/api/checkin/today')
def api_today_checkins():
    """获取今日打卡状态"""
    today_data = get_today_checkins()
    subjects = ['english', 'typing', 'c_lang', 'python']
    result = {}
    for s in subjects:
        result[s] = today_data.get(s, None)
    return jsonify(result)


@app.route('/api/checkin', methods=['POST'])
def api_checkin():
    """提交打卡"""
    data = request.get_json()
    subject = data.get('subject', '')
    if subject not in ['english', 'typing', 'c_lang', 'python']:
        return jsonify({'success': False, 'error': '无效的科目'}), 400
    do_checkin(
        subject,
        data.get('study_time_min', 0),
        data.get('self_score', 0),
        data.get('notes', '')
    )
    return jsonify({'success': True, 'streak': get_streak(subject)})


@app.route('/api/checkin/<subject>')
def api_checkin_history(subject):
    """获取某科打卡历史"""
    days = request.args.get('days', 30, type=int)
    history = get_checkin_history(subject, days)
    streak = get_streak(subject)
    return jsonify({'history': history, 'streak': streak})


@app.route('/api/stats')
def api_stats():
    """获取综合统计数据"""
    stats = get_stats()
    stats['weekly_heatmap'] = get_weekly_heatmap()
    return jsonify(stats)


@app.route('/api/typing/save', methods=['POST'])
def api_save_typing():
    """保存打字成绩"""
    data = request.get_json()
    save_typing_session(
        data.get('wpm', 0),
        data.get('accuracy', 0),
        data.get('duration_sec', 0),
        data.get('text_category', ''),
        data.get('text_name', '')
    )
    return jsonify({'success': True})


@app.route('/api/typing/history')
def api_typing_history():
    """获取打字历史"""
    history = get_typing_history()
    trend = get_typing_trend()
    return jsonify({'history': history, 'trend': trend})


@app.route('/api/typing/texts')
def api_typing_texts():
    """获取打字素材列表"""
    texts = load_json('typing_texts.json')
    return jsonify(texts)


@app.route('/api/vocabulary/random')
def api_random_words():
    """随机获取单词"""
    count = request.args.get('count', 10, type=int)
    words = get_random_words(count)
    stats = get_vocab_stats()
    return jsonify({'words': words, 'stats': stats})


@app.route('/api/vocabulary/review', methods=['POST'])
def api_review_word():
    """标记单词复习"""
    data = request.get_json()
    mark_word_reviewed(data['word_id'], data.get('mastered', False))
    stats = get_vocab_stats()
    return jsonify({'success': True, 'stats': stats})


@app.route('/api/knowledge/<subject>')
def api_knowledge(subject):
    """获取知识点清单"""
    if subject == 'c_lang':
        data = load_json('c_knowledge.json')
    elif subject == 'python':
        data = load_json('python_knowledge.json')
    else:
        return jsonify({'error': '无效的科目'}), 400
    return jsonify(data)


# ==================== 启动 ====================

if __name__ == '__main__':
    # 初始化数据库
    init_db()

    # 导入词汇（首次运行时填充数据库）
    words_data = load_json('words.json')
    import_vocabulary(words_data)

    print("=" * 50)
    print("  [Learning Check-in App] Started!")
    print("  URL: http://127.0.0.1:5000")
    print("  Press Ctrl+C to stop")
    print("=" * 50)

    app.run(debug=True, host='127.0.0.1', port=5000)
