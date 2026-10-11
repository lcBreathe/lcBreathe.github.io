(function () {
  'use strict';
  var root = document.documentElement;
  var languageButton = document.getElementById('language-toggle');
  var visitorValue = document.getElementById('visitor-value');
  var visitorCount = null;
  var visitorState = 'loading';
  var fallbackTimer;
  var translations = {
    zh: { title: '张翔 · Xiang Zhang | 学术主页', toggle: 'English', label: 'Switch to English', loading: '加载中…', unavailable: '暂不可用', preview: '上线后统计' },
    en: { title: 'Xiang Zhang | Academic Homepage', toggle: '中文', label: '切换到中文', loading: 'Loading…', unavailable: 'Unavailable', preview: 'Available when live' }
  };
  function language() { return root.lang === 'en' ? 'en' : 'zh'; }
  function updateVisitor() {
    visitorValue.textContent = visitorCount === null ? translations[language()][visitorState] : new Intl.NumberFormat(language() === 'en' ? 'en-US' : 'zh-CN').format(visitorCount);
  }
  function setLanguage(lang, updateURL) {
    root.lang = lang === 'en' ? 'en' : 'zh-CN';
    document.title = translations[language()].title;
    languageButton.querySelector('.language-text').textContent = translations[language()].toggle;
    languageButton.setAttribute('aria-label', translations[language()].label);
    document.querySelector('meta[name="description"]').content = language() === 'en' ? 'Xiang Zhang, master\'s student in Computer Science at Shanghai Jiao Tong University. Research in LLM Agents, Agentic Memory, and Data-Centric AI.' : '张翔，上海交通大学计算机专业硕士研究生。研究兴趣：LLM Agents、Agentic Memory、Data-Centric AI。';
    try { localStorage.setItem('academic-language', language()); } catch (_) {}
    if (updateURL) {
      try { var url = new URL(location.href); url.searchParams.set('lang', language()); history.replaceState(null, '', url); } catch (_) {}
    }
    updateVisitor();
  }
  var selected = new URLSearchParams(location.search).get('lang');
  if (selected !== 'en' && selected !== 'zh') {
    try { selected = localStorage.getItem('academic-language'); } catch (_) {}
  }
  setLanguage(selected === 'en' ? 'en' : 'zh', false);
  languageButton.addEventListener('click', function () { setLanguage(language() === 'en' ? 'zh' : 'en', true); });
  if ('IntersectionObserver' in window) {
    var links = Array.from(document.querySelectorAll('.nav a'));
    var sections = links.map(function (link) { return document.querySelector(link.getAttribute('href')); }).filter(Boolean);
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) links.forEach(function (link) {
          var active = link.getAttribute('href') === '#' + entry.target.id;
          link.classList.toggle('active', active);
          if (active) link.setAttribute('aria-current', 'location'); else link.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
    sections.forEach(function (section) { observer.observe(section); });
  }
  // The external service supplies site UV. Never manufacture a count in localStorage.
  var localPreview = location.protocol === 'file:' || /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$/.test(location.hostname);
  if (localPreview) { visitorState = 'preview'; updateVisitor(); return; }
  var sourceValue = document.getElementById('busuanzi_value_site_uv');
  var counterObserver = new MutationObserver(function () {
    var raw = sourceValue.textContent.trim();
    if (/^\d+$/.test(raw) && Number.isSafeInteger(Number(raw))) {
      visitorCount = Number(raw); clearTimeout(fallbackTimer); updateVisitor();
    }
  });
  counterObserver.observe(sourceValue, { childList: true, subtree: true, characterData: true });
  var counterScript = document.createElement('script');
  counterScript.src = 'https://busuanzi.ibruce.info/busuanzi/2.3/busuanzi.pure.mini.js';
  counterScript.async = true;
  counterScript.onerror = function () { visitorState = 'unavailable'; updateVisitor(); };
  fallbackTimer = setTimeout(function () { if (visitorCount === null) { visitorState = 'unavailable'; updateVisitor(); } }, 10000);
  document.head.appendChild(counterScript);
}());
