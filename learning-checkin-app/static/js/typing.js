/** 打字训练引擎 */
(function() {
  'use strict';

  let state = {
    text: '',
    textName: '',
    category: 'python',
    pos: 0,
    errors: 0,
    started: false,
    startTime: null,
    finished: false,
    totalKeystrokes: 0
  };

  const textDisplay = document.getElementById('text-display');
  const typingInput = document.getElementById('typing-input');
  const wpmEl = document.getElementById('wpm-value');
  const accEl = document.getElementById('acc-value');
  const timerEl = document.getElementById('timer-value');
  const catButtons = document.querySelectorAll('.cat-btn');
  const textSelect = document.getElementById('text-select');
  const restartBtn = document.getElementById('restart-btn');
  const containerEl = document.getElementById('text-display-container');

  function loadTexts() {
    return api.get('/api/typing/texts');
  }

  function renderText() {
    if (!textDisplay) return;
    textDisplay.innerHTML = state.text.split('\n').map(line => {
      return '<div class="line">' + [...line].map(ch => {
        let cls = 'char pending';
        if (ch === ' ') cls += ' space-pending';
        return `<span class="${cls}">${ch === ' ' ? ' ' : ch}</span>`;
      }).join('') + '<span class="char newline pending"></span></div>';
    }).join('');
  }

  function updateDisplay() {
    if (!textDisplay) return;
    const chars = textDisplay.querySelectorAll('.char:not(.newline)');
    const newlines = textDisplay.querySelectorAll('.char.newline');
    const text = state.text;

    for (let i = 0; i < chars.length; i++) {
      chars[i].className = 'char';
      if (i < state.pos) {
        chars[i].classList.add('correct');
      } else if (i === state.pos) {
        chars[i].classList.add('current');
      } else {
        chars[i].classList.add('pending');
      }
    }

    // 更新换行符
    let nlIdx = 0;
    for (let i = 0; i < text.length; i++) {
      if (text[i] === '\n' && nlIdx < newlines.length) {
        if (i < state.pos) {
          newlines[nlIdx].className = 'char newline correct';
        } else if (i === state.pos) {
          newlines[nlIdx].className = 'char newline current';
        } else {
          newlines[nlIdx].className = 'char newline pending';
        }
        nlIdx++;
      }
    }
  }

  function updateStats() {
    if (!state.started) return;
    const elapsed = (Date.now() - state.startTime) / 1000 / 60; // 分钟
    const words = state.pos / 5; // 标准：每5字符=1词
    const wpm = elapsed > 0 ? Math.round(words / elapsed) : 0;
    const accuracy = state.totalKeystrokes > 0
      ? Math.round((state.totalKeystrokes - state.errors) / state.totalKeystrokes * 100)
      : 100;

    if (wpmEl) wpmEl.textContent = wpm;
    if (accEl) accEl.textContent = accuracy + '%';
    if (timerEl) {
      const secs = Math.floor((Date.now() - state.startTime) / 1000);
      timerEl.textContent = Math.floor(secs / 60) + ':' + String(secs % 60).padStart(2, '0');
    }

    if (state.finished) {
      return { wpm, accuracy, duration: Math.floor((Date.now() - state.startTime) / 1000) };
    }
    return null;
  }

  function finish() {
    state.finished = true;
    if (containerEl) containerEl.classList.add('finished');
    if (typingInput) typingInput.disabled = true;

    const result = updateStats();
    if (result) {
      // 保存成绩
      api.post('/api/typing/save', {
        wpm: result.wpm,
        accuracy: result.accuracy,
        duration_sec: result.duration,
        text_category: state.category,
        text_name: state.textName
      }).then(() => {
        showToast(`🎯 完成！WPM: ${result.wpm} 准确率: ${result.accuracy}%`);
        loadHistory();
      }).catch(() => {});
    }
  }

  async function loadHistory() {
    const container = document.getElementById('typing-history');
    if (!container) return;
    try {
      const data = await api.get('/api/typing/history');
      const history = data.history || [];
      if (history.length === 0) {
        container.innerHTML = '<div class="text-muted text-sm text-center">暂无记录，开始你的第一次打字练习吧！</div>';
        return;
      }
      container.innerHTML = history.slice(0, 20).map((h, i) => `
        <div class="knowledge-item" style="cursor:default">
          <div class="day-num" style="background:var(--surface2);font-size:16px;">${i + 1}</div>
          <div class="day-info">
            <div class="day-topic">${h.text_name || h.text_category || '练习'} — WPM: <span style="color:var(--accent2)">${h.wpm}</span> | 准确率: <span style="color:var(--green)">${h.accuracy}%</span></div>
            <div class="day-points">${h.created_at ? new Date(h.created_at).toLocaleString('zh-CN') : ''}</div>
          </div>
          <div style="text-align:right">
            <span class="tag accent">${h.wpm} WPM</span>
          </div>
        </div>
      `).join('');
    } catch (e) {
      console.error('Failed to load history:', e);
    }
  }

  function reset() {
    state.pos = 0;
    state.errors = 0;
    state.started = false;
    state.startTime = null;
    state.finished = false;
    state.totalKeystrokes = 0;
    if (wpmEl) wpmEl.textContent = '0';
    if (accEl) accEl.textContent = '100%';
    if (timerEl) timerEl.textContent = '0:00';
    if (typingInput) {
      typingInput.value = '';
      typingInput.disabled = false;
      typingInput.focus();
    }
    if (containerEl) {
      containerEl.classList.remove('finished', 'focused');
    }
    renderText();
  }

  function selectText(texts, category, name) {
    state.category = category;
    const items = texts[category] || [];
    const item = name ? items.find(t => t.name === name) : items[0];
    if (item) {
      state.text = item.text;
      state.textName = item.name;
    }
    reset();
  }

  // 初始化
  async function init() {
    if (!typingInput || !textDisplay) return;

    const texts = await loadTexts();

    // 分类按钮
    if (catButtons) {
      catButtons.forEach(btn => {
        btn.addEventListener('click', () => {
          catButtons.forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
          const cat = btn.dataset.cat;
          selectText(texts, cat);
          updateTextSelect(texts, cat);
        });
      });
    }

    // 素材选择
    if (textSelect) {
      textSelect.addEventListener('change', () => {
        const cat = document.querySelector('.cat-btn.active')?.dataset?.cat || 'python';
        selectText(texts, cat, textSelect.value);
      });
    }

    function updateTextSelect(textsData, cat) {
      if (!textSelect) return;
      const items = textsData[cat] || [];
      textSelect.innerHTML = items.map(t => `<option value="${t.name}">${t.name}</option>`).join('');
    }

    // 打字输入处理
    typingInput.addEventListener('input', () => {
      if (state.finished) return;

      if (!state.started) {
        state.started = true;
        state.startTime = Date.now();
        if (containerEl) containerEl.classList.add('focused');
      }

      const typed = typingInput.value;
      const text = state.text;
      let pos = 0;
      let errors = 0;
      let keystrokes = typed.length;

      for (let i = 0; i < typed.length && i < text.length; i++) {
        if (typed[i] === text[i]) {
          pos = i + 1;
        } else {
          errors++;
          pos = i;
          break;
        }
      }

      // 如果完全匹配
      if (typed.length > text.length) {
        pos = text.length;
      }

      state.pos = pos;
      state.totalKeystrokes = keystrokes;
      updateDisplay();
      const result = updateStats();

      // 检查是否完成
      if (pos >= text.length && !state.finished) {
        finish();
      }
    });

    // 防止粘贴
    typingInput.addEventListener('paste', (e) => {
      e.preventDefault();
      showToast('请手动输入，不要粘贴！', true);
    });

    if (restartBtn) {
      restartBtn.addEventListener('click', () => {
        const cat = document.querySelector('.cat-btn.active')?.dataset?.cat || 'python';
        const name = textSelect ? textSelect.value : null;
        loadTexts().then(t => {
          selectText(t, cat, name);
        });
      });
    }

    // 初始加载
    selectText(texts, 'python');
    updateTextSelect(texts, 'python');
    loadHistory();

    // 定时更新计时器
    setInterval(() => {
      if (state.started && !state.finished) updateStats();
    }, 500);
  }

  if (typingInput && textDisplay) {
    init();
  }
})();
