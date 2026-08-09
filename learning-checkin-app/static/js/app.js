/** 通用交互逻辑 */
(function() {
  'use strict';

  // 激活当前页面导航
  const path = window.location.pathname;
  const pageMap = {
    '/': 'index',
    '/english': 'english',
    '/typing': 'typing',
    '/c-lang': 'c_lang',
    '/python': 'python'
  };
  const currentPage = pageMap[path] || 'index';
  document.querySelectorAll('.nav-btn').forEach(btn => {
    if (btn.dataset.page === currentPage) btn.classList.add('active');
  });

  // 显示今日日期
  const dateEl = document.getElementById('today-date');
  if (dateEl) {
    const now = new Date();
    const weekdays = ['日', '一', '二', '三', '四', '五', '六'];
    dateEl.textContent = `${now.getFullYear()}年${now.getMonth()+1}月${now.getDate()}日 星期${weekdays[now.getDay()]}`;
  }

  // Toast 提示
  window.showToast = function(msg, isError) {
    const toast = document.createElement('div');
    toast.className = 'toast' + (isError ? ' error' : '');
    toast.textContent = msg;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 2500);
  };

  // API 封装
  window.api = {
    get: async function(url) {
      const res = await fetch(url);
      if (!res.ok) throw new Error('Network error');
      return res.json();
    },
    post: async function(url, data) {
      const res = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });
      if (!res.ok) throw new Error('Network error');
      return res.json();
    }
  };

  // 打卡弹窗
  window.showCheckinModal = function(subject, subjectName, onSuccess) {
    const overlay = document.createElement('div');
    overlay.className = 'modal-overlay';
    overlay.innerHTML = `
      <div class="modal">
        <h3>📝 ${subjectName} 打卡</h3>
        <div class="form-group">
          <label class="form-label">学习时长（分钟）</label>
          <input type="number" class="form-input" id="modal-time" value="60" min="1" max="600">
        </div>
        <div class="form-group">
          <label class="form-label">自我评分</label>
          <div class="range-group">
            <input type="range" id="modal-score" value="7" min="1" max="10" step="1">
            <span class="range-value" id="modal-score-val">7/10</span>
          </div>
        </div>
        <div class="form-group">
          <label class="form-label">学习笔记 / 难点记录</label>
          <textarea class="form-textarea" id="modal-notes" placeholder="今天学了什么？遇到了什么问题？"></textarea>
        </div>
        <div class="modal-actions">
          <button class="btn" id="modal-cancel">取消</button>
          <button class="btn btn-primary" id="modal-submit">✅ 确认打卡</button>
        </div>
      </div>
    `;
    document.body.appendChild(overlay);

    const scoreInput = overlay.querySelector('#modal-score');
    const scoreVal = overlay.querySelector('#modal-score-val');
    scoreInput.addEventListener('input', () => {
      scoreVal.textContent = scoreInput.value + '/10';
    });

    overlay.querySelector('#modal-cancel').addEventListener('click', () => overlay.remove());
    overlay.addEventListener('click', (e) => { if (e.target === overlay) overlay.remove(); });

    overlay.querySelector('#modal-submit').addEventListener('click', async () => {
      const time = parseInt(overlay.querySelector('#modal-time').value) || 0;
      const score = parseInt(overlay.querySelector('#modal-score').value) || 0;
      const notes = overlay.querySelector('#modal-notes').value.trim();

      try {
        const res = await api.post('/api/checkin', {
          subject, study_time_min: time, self_score: score, notes
        });
        if (res.success) {
          overlay.remove();
          showToast(`🔥 ${subjectName}打卡成功！连续打卡 ${res.streak} 天`);
          if (onSuccess) onSuccess(res);
        }
      } catch (e) {
        showToast('打卡失败，请重试', true);
      }
    });
  };

})();
