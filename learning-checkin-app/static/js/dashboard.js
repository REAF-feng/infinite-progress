/** 仪表盘页面逻辑 */
(function() {
  'use strict';

  const subjects = [
    { key: 'english', name: '英语', icon: '🇬🇧' },
    { key: 'typing', name: '打字', icon: '⌨️' },
    { key: 'c_lang', name: 'C语言', icon: '🇨' },
    { key: 'python', name: 'Python', icon: '🐍' }
  ];

  async function loadDashboard() {
    try {
      const [todayData, stats] = await Promise.all([
        api.get('/api/checkin/today'),
        api.get('/api/stats')
      ]);
      renderCheckinCards(todayData, stats);
      renderHeatmap(stats.weekly_heatmap);
      renderStatsSummary(stats);
      renderTypingChart();
      renderMilestones(stats);
    } catch (e) {
      console.error('Failed to load dashboard:', e);
    }
  }

  function renderCheckinCards(todayData, stats) {
    const grid = document.getElementById('checkin-grid');
    if (!grid) return;

    grid.innerHTML = subjects.map(s => {
      const checked = todayData[s.key];
      const streak = stats[s.key + '_streak'] || 0;
      return `
        <div class="checkin-card ${checked ? 'checked-in' : ''}" onclick="showCheckinModal('${s.key}', '${s.name}', () => location.reload())">
          ${streak >= 7 ? `<div class="streak-badge">🔥 ${streak}天</div>` : ''}
          <div class="subj-icon">${s.icon}</div>
          <div class="subj-name">${s.name}</div>
          <div class="subj-status ${checked ? 'done' : 'pending'}">
            ${checked ? `✅ 已打卡 · ${checked.study_time_min}分钟 · 自评${checked.self_score}/10` : '⬜ 今日未打卡'}
          </div>
          ${checked && checked.notes ? `<div class="text-sm text-muted mt-2">📝 ${checked.notes.substring(0, 40)}${checked.notes.length > 40 ? '...' : ''}</div>` : ''}
        </div>
      `;
    }).join('');
  }

  function renderHeatmap(heatmapData) {
    const container = document.getElementById('heatmap-container');
    if (!container) return;

    const subjectLabels = { english: '英', typing: '打', c_lang: 'C', python: 'Py' };
    const subjectIcons = { english: '🇬🇧', typing: '⌨️', c_lang: '🇨', python: '🐍' };

    const days = Object.entries(heatmapData);
    container.innerHTML = `
      <div class="heatmap">
        ${days.map(([date, info]) => `
          <div class="heatmap-day">
            <div class="heatmap-label">${info.label}</div>
            <div class="heatmap-cells">
              ${['english', 'typing', 'c_lang', 'python'].map(s => `
                <div class="heatmap-cell ${info.subjects[s] ? 'checked' : ''}" title="${subjectIcons[s]} ${info.label}: ${info.subjects[s] ? '✅' : '❌'}">
                  ${info.subjects[s] ? '✅' : '·'}
                </div>
              `).join('')}
            </div>
          </div>
        `).join('')}
      </div>
      <div class="heatmap-legend">
        <span>图例：</span>
        <span class="legend-dot empty"></span><span>未打卡</span>
        <span class="legend-dot filled"></span><span>已打卡</span>
        <span style="margin-left:auto;font-size:11px;">行: 🇬🇧英 ⌨️打 🇨C 🐍Py</span>
      </div>
    `;
  }

  function renderStatsSummary(stats) {
    const container = document.getElementById('stats-summary');
    if (!container) return;

    const items = [
      { label: '英语词汇', value: `${stats.vocab_mastered}/${stats.vocab_total}`, color: '' },
      { label: '打字平均WPM', value: stats.typing_avg_wpm, color: 'green' },
      { label: '打字最高WPM', value: stats.typing_best_wpm, color: 'purple' },
      { label: '打字平均准确率', value: stats.typing_avg_acc + '%', color: 'orange' },
      { label: 'Python打卡', value: stats.python ? stats.python.total_days + '天' : '0天', color: '' },
      { label: 'C语言打卡', value: stats.c_lang ? stats.c_lang.total_days + '天' : '0天', color: '' },
    ];

    container.innerHTML = `
      <div class="stat-row">
        ${items.map(i => `
          <div class="stat-box">
            <div class="stat-value ${i.color}">${i.value}</div>
            <div class="stat-label">${i.label}</div>
          </div>
        `).join('')}
      </div>
    `;
  }

  let typingChart = null;
  async function renderTypingChart() {
    const canvas = document.getElementById('typing-chart');
    if (!canvas) return;

    try {
      const data = await api.get('/api/typing/history');
      const trend = data.trend || [];

      const labels = trend.map(t => t.date);
      const wpmData = trend.map(t => t.avg_wpm);
      const accData = trend.map(t => t.avg_acc);

      if (typingChart) typingChart.destroy();

      typingChart = new Chart(canvas, {
        type: 'line',
        data: {
          labels,
          datasets: [
            {
              label: 'WPM (字/分钟)',
              data: wpmData,
              borderColor: '#58a6ff',
              backgroundColor: 'rgba(88,166,255,0.1)',
              fill: true,
              tension: 0.3,
              yAxisID: 'y'
            },
            {
              label: '准确率 %',
              data: accData,
              borderColor: '#3fb950',
              backgroundColor: 'rgba(63,185,80,0.1)',
              fill: true,
              tension: 0.3,
              yAxisID: 'y1'
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { intersect: false, mode: 'index' },
          plugins: {
            legend: {
              labels: { color: '#8b949e', usePointStyle: true, pointStyleWidth: 8 }
            }
          },
          scales: {
            x: {
              ticks: { color: '#6e7681', maxTicksLimit: 10 },
              grid: { color: '#21262d' }
            },
            y: {
              type: 'linear',
              display: true,
              position: 'left',
              title: { display: true, text: 'WPM', color: '#58a6ff' },
              ticks: { color: '#6e7681' },
              grid: { color: '#21262d' }
            },
            y1: {
              type: 'linear',
              display: true,
              position: 'right',
              title: { display: true, text: '准确率 %', color: '#3fb950' },
              ticks: { color: '#6e7681', callback: v => v + '%' },
              grid: { drawOnChartArea: false },
              min: 0,
              max: 100
            }
          }
        }
      });
    } catch (e) {
      console.error('Failed to load typing chart:', e);
    }
  }

  function renderMilestones(stats) {
    const container = document.getElementById('milestones');
    if (!container) return;

    const milestones = [
      { days: 7, label: '🌟 坚持7天', icon: '🌟' },
      { days: 15, label: '🔥 坚持15天', icon: '🔥' },
      { days: 21, label: '💪 养成习惯(21天)', icon: '💪' },
      { days: 30, label: '🏆 坚持30天', icon: '🏆' },
      { days: 60, label: '👑 坚持60天', icon: '👑' },
      { days: 100, label: '🎯 坚持100天', icon: '🎯' },
    ];

    const maxStreak = Math.max(
      stats.english_streak || 0,
      stats.typing_streak || 0,
      stats.c_lang_streak || 0,
      stats.python_streak || 0
    );

    container.innerHTML = milestones.map(m => {
      const achieved = maxStreak >= m.days;
      return `
        <div class="stat-box" style="opacity:${achieved ? 1 : 0.4}">
          <div style="font-size:24px;">${m.icon}</div>
          <div style="font-size:12px;font-weight:600;margin-top:4px;color:${achieved ? 'var(--green)' : 'var(--text3)'}">${m.label}</div>
          <div style="font-size:10px;color:var(--text3)">${achieved ? '✅ 已达成' : '🔒 未解锁'}</div>
        </div>
      `;
    }).join('');
  }

  // 启动
  if (document.getElementById('checkin-grid')) {
    loadDashboard();
  }
})();
