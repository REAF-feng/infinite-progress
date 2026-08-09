/** 英语学习页面逻辑 */
(function() {
  'use strict';

  let currentWords = [];
  let currentIndex = 0;

  const wordCard = document.getElementById('word-card');
  const wordFront = document.getElementById('word-front');
  const wordBack = document.getElementById('word-back');
  const prevBtn = document.getElementById('prev-word');
  const nextBtn = document.getElementById('next-word');
  const masteredBtn = document.getElementById('mark-mastered');
  const reviewBtn = document.getElementById('mark-review');
  const reloadBtn = document.getElementById('reload-words');
  const progressEl = document.getElementById('word-progress');
  const statsEl = document.getElementById('vocab-stats');

  function updateCard() {
    if (!currentWords.length || !wordCard || !wordFront || !wordBack) return;

    const w = currentWords[currentIndex];
    wordFront.querySelector('.word').textContent = w.word;
    wordBack.querySelector('.meaning').textContent = w.meaning;
    wordBack.querySelector('.word-reminder').textContent = w.word;

    wordCard.classList.remove('flipped');

    if (progressEl) {
      progressEl.textContent = `${currentIndex + 1} / ${currentWords.length}`;
    }

    // 按钮状态
    if (masteredBtn) masteredBtn.style.display = w.mastered ? 'none' : 'inline-flex';
  }

  async function loadWords() {
    try {
      const data = await api.get('/api/vocabulary/random?count=15');
      currentWords = data.words || [];
      currentIndex = 0;

      if (statsEl) {
        const s = data.stats;
        statsEl.innerHTML = `
          已掌握 <span style="color:var(--green);font-weight:700;">${s.mastered}</span> / ${s.total} 词
          | 今日复习 <span style="color:var(--accent2);font-weight:700;">${s.today_reviewed}</span> 词
        `;
      }

      if (currentWords.length === 0) {
        if (wordCard) {
          wordFront.querySelector('.word').textContent = '🎉';
          wordBack.querySelector('.meaning').textContent = '全部掌握！';
        }
        return;
      }
      updateCard();
    } catch (e) {
      console.error('Failed to load words:', e);
    }
  }

  // 翻转卡片
  if (wordCard) {
    wordCard.addEventListener('click', () => {
      wordCard.classList.toggle('flipped');
    });
  }

  // 上一词
  if (prevBtn) {
    prevBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (currentIndex > 0) {
        currentIndex--;
        updateCard();
      }
    });
  }

  // 下一词
  if (nextBtn) {
    nextBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      if (currentIndex < currentWords.length - 1) {
        currentIndex++;
        updateCard();
      }
    });
  }

  // 标记已掌握
  if (masteredBtn) {
    masteredBtn.addEventListener('click', async (e) => {
      e.stopPropagation();
      if (!currentWords.length) return;
      const w = currentWords[currentIndex];
      try {
        await api.post('/api/vocabulary/review', { word_id: w.id, mastered: true });
        w.mastered = 1;
        showToast(`✅ 已掌握: ${w.word}`);
        updateCard();

        // 更新统计
        const data = await api.get('/api/vocabulary/random?count=1');
        if (statsEl) {
          const s = data.stats;
          statsEl.innerHTML = `
            已掌握 <span style="color:var(--green);font-weight:700;">${s.mastered}</span> / ${s.total} 词
            | 今日复习 <span style="color:var(--accent2);font-weight:700;">${s.today_reviewed}</span> 词
          `;
        }
      } catch (e) {
        showToast('操作失败', true);
      }
    });
  }

  // 再复习
  if (reviewBtn) {
    reviewBtn.addEventListener('click', async (e) => {
      e.stopPropagation();
      if (!currentWords.length) return;
      const w = currentWords[currentIndex];
      try {
        await api.post('/api/vocabulary/review', { word_id: w.id, mastered: false });
        showToast(`🔄 需要再复习: ${w.word}`);
      } catch (e) {
        showToast('操作失败', true);
      }
    });
  }

  // 换一批
  if (reloadBtn) {
    reloadBtn.addEventListener('click', () => loadWords());
  }

  // 键盘快捷键
  document.addEventListener('keydown', (e) => {
    if (!currentWords.length) return;
    if (e.key === 'ArrowLeft' && currentIndex > 0) {
      currentIndex--;
      updateCard();
    } else if (e.key === 'ArrowRight' && currentIndex < currentWords.length - 1) {
      currentIndex++;
      updateCard();
    } else if (e.key === ' ' || e.key === 'Spacebar') {
      e.preventDefault();
      if (wordCard) wordCard.classList.toggle('flipped');
    }
  });

  // 初始化
  if (wordCard) {
    loadWords();
  }
})();
