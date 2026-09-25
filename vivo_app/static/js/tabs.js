(function () {
  function ready(fn) {
    if (document.readyState !== 'loading') {
      fn();
    } else {
      document.addEventListener('DOMContentLoaded', fn);
    }
  }

  function $(selector, root) {
    return (root || document).querySelector(selector);
  }

  function $all(selector, root) {
    return Array.prototype.slice.call((root || document).querySelectorAll(selector));
  }

  function show(el) {
    if (!el) return;
    el.style.display = '';
    el.removeAttribute('aria-hidden');
  }

  function hide(el) {
    if (!el) return;
    el.style.display = 'none';
    el.setAttribute('aria-hidden', 'true');
  }

  function setActive(btns, activeBtn) {
    btns.forEach(function (b) { b.classList.remove('active'); });
    if (activeBtn) activeBtn.classList.add('active');
  }

  ready(function () {
    var panel = $('#people-right-panel');
    var tabButtons = $('#tabButtons');
    if (!panel || !tabButtons) return; // Only run on people profile pages with tabs

    var sections = $all('#section_overview .tabFinder');
    var btns = $all('#tabButtons a[id^="tab"][id$="Btn"]');

    var mapBtnToSection = function (btnId) {
      if (btnId === 'tabAllBtn') return null; // special case
      return btnId.replace(/Btn$/, ''); // e.g., tabOverviewBtn -> tabOverview
    };

    function showOnly(sectionId) {
      sections.forEach(function (s) { hide(s); });
      var target = $('#' + sectionId);
      if (target) show(target);
    }

    function showAll() {
      sections.forEach(function (s) { show(s); });
    }

    // Initialize: if a button has .active, reflect it; else default to Overview
    var activeBtn = btns.find(function (b) { return b.classList.contains('active'); });
    if (activeBtn && activeBtn.id !== 'tabAllBtn') {
      var sid = mapBtnToSection(activeBtn.id);
      if (sid) showOnly(sid);
    } else {
      // default to Overview
      showOnly('tabOverview');
      var overviewBtn = $('#tabOverviewBtn');
      if (overviewBtn) setActive(btns, overviewBtn);
    }

    // Wire clicks
    btns.forEach(function (btn) {
      btn.addEventListener('click', function (ev) {
        ev.preventDefault();
        if (btn.id === 'tabAllBtn') {
          showAll();
          setActive(btns, btn);
          return false;
        }
        var sectionId = mapBtnToSection(btn.id);
        if (!sectionId) return false;
        showOnly(sectionId);
        setActive(btns, btn);
        return false;
      });
    });
  });
})();
