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
  function setLanguage(lang) {
    root.lang = lang === 'en' ? 'en' : 'zh-CN';
    document.title = translations[language()].title;
    languageButton.querySelector('.language-text').textContent = translations[language()].toggle;
    languageButton.setAttribute('aria-label', translations[language()].label);
    var accountButton = document.querySelector('.copy-account');
    if (accountButton) accountButton.setAttribute('aria-label', language() === 'en' ? 'Copy Xiaohongshu ID' : '复制小红书号');
    document.querySelector('meta[name="description"]').content = language() === 'en' ? 'Xiang Zhang, master\'s student in Computer Science at Shanghai Jiao Tong University. Research in LLM Agents, Agentic Memory, and Data-Centric AI.' : '张翔，上海交通大学计算机专业硕士研究生。研究兴趣：LLM Agents、Agentic Memory、Data-Centric AI。';
    updateVisitor();
  }
  // Each page load starts in English; switching applies only to this open page.
  try {
    var currentURL = new URL(location.href);
    if (currentURL.searchParams.has('lang')) {
      currentURL.searchParams.delete('lang');
      history.replaceState(null, '', currentURL);
    }
  } catch (_) {}
  setLanguage('en');
  languageButton.addEventListener('click', function () { setLanguage(language() === 'en' ? 'zh' : 'en'); });
  // Keep paper figures on this page; the native dialog handles focus and Escape.
  var imagePreview = document.getElementById('image-preview');
  if (imagePreview && typeof imagePreview.showModal === 'function') {
    var previewImage = imagePreview.querySelector('.image-preview-image');
    var previewTitle = document.getElementById('image-preview-title');
    document.querySelectorAll('.paper-figure').forEach(function (link) {
      link.setAttribute('aria-haspopup', 'dialog');
      link.setAttribute('aria-controls', 'image-preview');
      link.addEventListener('click', function (event) {
        event.preventDefault();
        var thumbnail = link.querySelector('img');
        previewImage.src = link.href;
        previewImage.alt = thumbnail.alt;
        previewTitle.textContent = thumbnail.alt;
        imagePreview.showModal();
        root.classList.add('image-preview-open');
      });
    });
    imagePreview.querySelector('.image-preview-close').addEventListener('click', function () {
      imagePreview.close();
    });
    function outsidePreview(event) {
      var bounds = imagePreview.getBoundingClientRect();
      return event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom;
    }
    var backdropPress = false;
    imagePreview.addEventListener('pointerdown', function (event) {
      backdropPress = event.target === imagePreview && outsidePreview(event);
    });
    imagePreview.addEventListener('click', function (event) {
      if (backdropPress && event.target === imagePreview && outsidePreview(event)) imagePreview.close();
      backdropPress = false;
    });
    imagePreview.addEventListener('close', function () {
      root.classList.remove('image-preview-open');
      previewImage.removeAttribute('src');
    });
  }
  // Shorten only when needed, keeping the owner and the original author order.
  function fitAuthors(element) {
    var names = JSON.parse(element.getAttribute('data-authors'));
    function render(indices) {
      element.replaceChildren();
      var previous = -1;
      indices.slice().sort(function (a, b) { return a - b; }).forEach(function (index) {
        if (previous >= 0) element.appendChild(document.createTextNode(', '));
        if (index > previous + 1) element.appendChild(document.createTextNode('…, '));
        var name = document.createElement(names[index] === 'Xiang Zhang' ? 'strong' : 'span');
        name.textContent = names[index]; element.appendChild(name); previous = index;
      });
      if (previous < names.length - 1) element.appendChild(document.createTextNode(', …'));
    }
    var all = names.map(function (_, index) { return index; });
    render(all);
    if (element.scrollWidth <= element.clientWidth) return;
    var owner = names.indexOf('Xiang Zhang');
    var selected = [owner >= 0 ? owner : 0];
    var priorities = [0, names.length - 1, 1, names.length - 2].concat(all);
    priorities.forEach(function (index) {
      if (index < 0 || index >= names.length || selected.indexOf(index) >= 0) return;
      render(selected.concat(index));
      if (element.scrollWidth <= element.clientWidth) selected.push(index);
    });
    render(selected);
  }
  var authorRows = Array.from(document.querySelectorAll('[data-authors]'));
  function fitAllAuthors() { authorRows.forEach(fitAuthors); }
  fitAllAuthors();
  if ('ResizeObserver' in window) {
    var authorObserver = new ResizeObserver(fitAllAuthors);
    authorRows.forEach(function (row) { authorObserver.observe(row); });
  } else window.addEventListener('resize', fitAllAuthors);
  if (document.fonts) document.fonts.ready.then(fitAllAuthors);
  var copyAccount = document.querySelector('.copy-account');
  if (copyAccount) {
    copyAccount.hidden = false;
    copyAccount.addEventListener('click', function () {
      var id = copyAccount.getAttribute('data-copy');
      var status = document.querySelector('.copy-status');
      function show(message) {
        status.textContent = message;
        clearTimeout(copyAccount.statusTimer);
        copyAccount.statusTimer = setTimeout(function () { status.textContent = ''; }, 4000);
      }
      if (!navigator.clipboard) { show(id); return; }
      navigator.clipboard.writeText(id).then(function () {
        show(language() === 'en' ? 'ID copied' : '号码已复制');
      }).catch(function () { show(id); });
    });
  }
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
