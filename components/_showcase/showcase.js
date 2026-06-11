/* ==========================================================================
   showcase.js — Shared Showcase Infrastructure
   Platform Code Design System
   --------------------------------------------------------------------------
   Responsibilities:
     1. Build the page shell (sidebar + header) from data attributes
     2. Initialize Preview / Code tabs on .showcase and .interactive
     3. Initialize Copy buttons
     4. Render Figma prop tags from data-props attributes
     5. Initialize indeterminate checkboxes (.showcase-indeterminate)

   Contract (HTML side):
     <body
       data-showcase
       data-current-component="button"
       data-showcase-title="Button Showcase">
       <div data-showcase-shell>
         <main data-showcase-content>
           <!-- component examples only — no shell markup -->
         </main>
       </div>
     </body>

   Required links in <head>:
     <link rel="stylesheet" href="../../token.css" />
     <link rel="stylesheet" href="../../_showcase/showcase.css" />
     <script src="../../_showcase/showcase.js" defer></script>
   ========================================================================== */

(function () {
  'use strict';

  /* ── Component registry ──────────────────────────────────────────────── */
  /*
     Add a new entry here whenever a new component gains a showcase.
     Order determines sidebar order.
  */
  var COMPONENTS = [
    { id: 'accordion', label: 'Accordion' },
    { id: 'avatar', label: 'Avatar' },
    { id: 'breadcrumb', label: 'Breadcrumb' },
    { id: 'button', label: 'Button' },
    { id: 'checkbox', label: 'Checkbox' },
    { id: 'chip', label: 'Chip' },
    { id: 'content-switcher', label: 'Content Switcher' },
    { id: 'input-affix', label: 'Input Affix' },
    { id: 'label', label: 'Label' },
    { id: 'link', label: 'Link' },
    { id: 'list', label: 'List' },
    { id: 'pagination', label: 'Pagination' },
    { id: 'rating', label: 'Rating' },
    { id: 'tab', label: 'Tab' },
    { id: 'tag', label: 'Tag' },
    { id: 'text-input', label: 'Text Input' },
  ];

  /* ── Read body data attributes ───────────────────────────────────────── */

  var body = document.body;
  var currentComponent = body.getAttribute('data-current-component') || '';
  var showcaseTitle = body.getAttribute('data-showcase-title') || '';

  /* ── 1. Shell builder ────────────────────────────────────────────────── */

  function buildShell() {
    var shell = document.querySelector('[data-showcase-shell]');
    if (!shell) return;

    var sidebar = buildSidebar();
    shell.insertBefore(sidebar, shell.firstChild);

    if (showcaseTitle) {
      var content = shell.querySelector('[data-showcase-content]');
      if (content) buildHeader(content);
    }
  }

  /* ── 2. Sidebar ──────────────────────────────────────────────────────── */

  function buildSidebar() {
    var aside = document.createElement('aside');
    aside.setAttribute('data-showcase-sidebar', '');

    var nav = document.createElement('nav');
    nav.className = 'showcase-sidebar__nav';
    nav.setAttribute('aria-label', 'Component showcases');

    COMPONENTS.forEach(function (comp) {
      var a = document.createElement('a');
      a.href = '../../' + comp.id + '/showcases/index.html';
      a.className = 'showcase-sidebar__link';
      a.textContent = comp.label;

      if (comp.id === currentComponent) {
        a.classList.add('is-active');
        a.setAttribute('aria-current', 'page');
      }

      nav.appendChild(a);
    });

    aside.appendChild(nav);
    return aside;
  }

  /* ── 3. Page header ──────────────────────────────────────────────────── */

  function buildHeader(content) {
    var componentName = showcaseTitle.replace(/\s*Showcase\s*$/i, '').trim();

    var header = document.createElement('header');
    header.className = 'page__header';

    var meta = document.createElement('p');
    meta.className = 'page__meta';
    meta.textContent = 'Design System / Components / ' + componentName;

    var h1 = document.createElement('h1');
    h1.className = 'page__title';
    h1.textContent = showcaseTitle;

    header.appendChild(meta);
    header.appendChild(h1);
    content.insertBefore(header, content.firstChild);
  }

  /* ── 4. Preview / Code tabs ──────────────────────────────────────────── */

  function extractComponentCode(el) {
    if (el.classList.contains('showcase')) {
      var parts = [];

      el.querySelectorAll('.showcase__row').forEach(function (row) {
        var labelEl = row.querySelector('.showcase__label');
        var labelText = labelEl ? labelEl.textContent.trim() : '';
        var itemEl = row.querySelector('.showcase__item');
        var code;

        if (itemEl) {
          /* Strip prop-tags from code output — they are showcase-only markup */
          var clone = itemEl.cloneNode(true);
          var propTags = clone.querySelector('.prop-tags');
          if (propTags) propTags.parentNode.removeChild(propTags);
          code = clone.innerHTML.trim();
        } else {
          var siblings = Array.from(row.children).filter(function (c) {
            return c !== labelEl;
          });
          code = siblings.map(function (c) { return c.outerHTML; }).join('\n').trim();
        }

        if (labelText) parts.push('<!-- ' + labelText + ' -->');
        if (code) parts.push(code);
        parts.push('');
      });

      return parts.join('\n').trim();
    }

    if (el.classList.contains('interactive')) {
      var items = Array.from(el.children).filter(function (c) {
        return !c.classList.contains('interactive__title');
      });
      return items.map(function (c) { return c.outerHTML; }).join('\n\n').trim();
    }

    return el.innerHTML.trim();
  }

  function initTabs() {
    document.querySelectorAll('.showcase, .interactive').forEach(function (el) {
      var sourceHTML = extractComponentCode(el);

      /* Wrapper block */
      var block = document.createElement('div');
      block.className = 'preview-block';

      /* Tab bar */
      var tabBar = document.createElement('div');
      tabBar.className = 'preview-tabs';
      tabBar.setAttribute('role', 'tablist');

      var btnPreview = document.createElement('button');
      btnPreview.type = 'button';
      btnPreview.className = 'preview-tab is-active';
      btnPreview.textContent = 'Preview';
      btnPreview.setAttribute('role', 'tab');
      btnPreview.setAttribute('aria-selected', 'true');

      var btnCode = document.createElement('button');
      btnCode.type = 'button';
      btnCode.className = 'preview-tab';
      btnCode.textContent = 'Code';
      btnCode.setAttribute('role', 'tab');
      btnCode.setAttribute('aria-selected', 'false');

      tabBar.appendChild(btnPreview);
      tabBar.appendChild(btnCode);

      /* Preview pane */
      var previewPane = document.createElement('div');
      previewPane.className = 'preview-pane';
      previewPane.setAttribute('role', 'tabpanel');

      /* Code pane */
      var codePane = document.createElement('div');
      codePane.className = 'code-pane';
      codePane.hidden = true;
      codePane.setAttribute('role', 'tabpanel');

      var toolbar = document.createElement('div');
      toolbar.className = 'code-pane__toolbar';

      var copyBtn = document.createElement('button');
      copyBtn.type = 'button';
      copyBtn.className = 'code-copy-btn';
      copyBtn.textContent = 'Copy';
      toolbar.appendChild(copyBtn);

      var pre = document.createElement('pre');
      var code = document.createElement('code');
      code.textContent = sourceHTML;
      pre.appendChild(code);

      codePane.appendChild(toolbar);
      codePane.appendChild(pre);

      /* Assemble */
      el.parentNode.insertBefore(block, el);
      previewPane.appendChild(el);
      block.appendChild(tabBar);
      block.appendChild(previewPane);
      block.appendChild(codePane);

      /* Tab activation */
      function activate(showCode) {
        btnPreview.classList.toggle('is-active', !showCode);
        btnPreview.setAttribute('aria-selected', showCode ? 'false' : 'true');
        btnCode.classList.toggle('is-active', showCode);
        btnCode.setAttribute('aria-selected', showCode ? 'true' : 'false');
        previewPane.hidden = showCode;
        codePane.hidden = !showCode;
      }

      btnPreview.addEventListener('click', function () { activate(false); });
      btnCode.addEventListener('click', function () { activate(true); });

      /* Copy button */
      copyBtn.addEventListener('click', function () {
        if (navigator.clipboard && navigator.clipboard.writeText) {
          navigator.clipboard.writeText(sourceHTML).then(function () {
            copyBtn.textContent = 'Copied!';
            setTimeout(function () { copyBtn.textContent = 'Copy'; }, 2000);
          }).catch(function () {
            fallbackCopy(sourceHTML, copyBtn);
          });
        } else {
          fallbackCopy(sourceHTML, copyBtn);
        }
      });
    });
  }

  function fallbackCopy(text, btn) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.cssText = 'position:fixed;top:-9999px;left:-9999px;opacity:0';
    document.body.appendChild(ta);
    ta.select();
    try {
      document.execCommand('copy');
      btn.textContent = 'Copied!';
      setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
    } catch (e) {
      btn.textContent = 'Error';
      setTimeout(function () { btn.textContent = 'Copy'; }, 2000);
    }
    document.body.removeChild(ta);
  }

  /* ── 5. Figma prop tags ──────────────────────────────────────────────── */

  function initPropTags() {
    document.querySelectorAll('.showcase__row[data-props]').forEach(function (row) {
      var labelEl = row.querySelector('.showcase__label');
      var others = Array.from(row.children).filter(function (c) { return c !== labelEl; });
      if (!others.length) return;

      var first = others[0];
      var item;

      if (first.classList.contains('showcase__item')) {
        item = first;
      } else {
        item = document.createElement('div');
        item.className = 'showcase__item';
        first.replaceWith(item);
        item.appendChild(first);
      }

      row.style.alignItems = 'flex-start';

      var tags = document.createElement('div');
      tags.className = 'prop-tags';

      row.getAttribute('data-props').split(',').forEach(function (part) {
        part = part.trim();
        var eq = part.indexOf('=');
        if (eq < 0) return;
        var k = part.slice(0, eq).trim();
        var v = part.slice(eq + 1).trim();
        var t = document.createElement('span');
        t.className = 'prop-tag';
        t.innerHTML =
          '<span class="prop-tag__key">' + escapeHtml(k) + '</span>' +
          '<span class="prop-tag__eq">=</span>' +
          '<span class="prop-tag__val">' + escapeHtml(v) + '</span>';
        tags.appendChild(t);
      });

      item.appendChild(tags);
    });
  }

  function escapeHtml(str) {
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  /* ── 6. Indeterminate checkboxes ─────────────────────────────────────── */

  function initIndeterminate() {
    document.querySelectorAll('.showcase-indeterminate').forEach(function (input) {
      input.indeterminate = true;
    });
  }

  /* ── Bootstrap ───────────────────────────────────────────────────────── */

  document.addEventListener('DOMContentLoaded', function () {
    buildShell();
    initTabs();
    initPropTags();
    initIndeterminate();
  });

}());
