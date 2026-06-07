# Design System — Implementation Reference

> **للمحادثات القادمة:** نفّذ المكوّن الموجود في مجلده بالاعتماد على هذا الملف كمرجع كامل للبنية والاتفاقيات.

---

## هيكل المجلدات

```
design-system/
├── REFERENCE.md                          ← هذا الملف
├── token.css                             ← design tokens مشتركة لكل المكونات
└── components/
    └── [component-name]/
        ├── reference.json                ← مرجع المكوّن (axes + variants + properties)
        ├── [component-name].css          ← CSS نظيف (كلاسات المكوّن فقط)
        └── _figma/
            └── [shape]/
                ├── [shape]--[state]-details.json
                └── states/
                    └── [state].png
```

---

## token.css

ملف واحد مشترك يحتوي على كل القيم. **لا تُكتب أي قيمة ثابتة في CSS المكوّنات** — كل شيء يرجع لـ token.

### أهم مجموعات التوكنز

| المجموعة | البادئة | مثال |
|---|---|---|
| Spacing | `--space-*`, `--spacing-*` | `--space-16`, `--spacing-lg` |
| Typography | `--fs-*`, `--lh-*`, `--font-weight-*` | `--fs-text-md`, `--lh-text-md` |
| Radius | `--radius-*` | `--radius-sm`, `--radius-md` |
| Colors (Brand) | `--sa-*`, `--gray-*` | `--sa-600`, `--gray-200` |
| Icons | `--icon-size-*` | `--icon-size-md` |
| Shadows | `--shadow-*` | `--shadow-sm` |
| Motion | `--transition-*`, `--ease-*` | `--transition-fast`, `--ease-in-out` |

### توكنز المكوّنات (مخصصة لكل مكوّن)

تُعرَّف في `token.css` تحت قسم خاص بالمكوّن، مثال للـ Button:

```css
--button-lg-height: var(--space-40);
--button-lg-padding-inline: var(--space-16);
--button-lg-gap: var(--space-4);
--button-radius: var(--radius-sm);
--button-label-font-size: var(--fs-text-md);
--button-primary-bg-default: var(--sa-600);
--button-primary-bg-hover: var(--sa-500);
--button-primary-bg-pressed: var(--sa-900);
--button-primary-bg-selected: var(--sa-800);
--button-primary-text: var(--white);
--button-disabled-bg: var(--gray-200);
--button-disabled-text: var(--gray-400);
--button-focus-border-width: var(--space-2);
--button-focus-ring-inner-color: var(--white);
--button-focus-ring-outer-color: var(--black);
```

---

## reference.json — المخطط الكامل

### المستوى الأعلى

```json
{
  "schema_version": "2.0.0",
  "component": {
    "name": "component-name",
    "description": "وصف المكوّن"
  },
  "axes": ["shape", "state", "size", ...],
  "axis_values": {
    "shape": ["primary", "secondary", "ghost"],
    "state": ["default", "hovered", "focused", "pressed", "disabled", "selected"],
    "size":  ["sm", "md", "lg"]
  },
  "variants": [ ... ]
}
```

### axes — المحاور

كل مكوّن يعرّف محاوره الخاصة. الأمثلة الشائعة:

| المحور | القيم المعتادة | نوع التطبيق في CSS |
|---|---|---|
| `state` | default, hovered, focused, pressed, disabled, selected | pseudo-classes |
| `shape` | primary, secondary, ghost, danger | modifier class |
| `size` | sm, md, lg | modifier class |
| `expanded` | true, false | data attribute |
| `flush` | true, false | data attribute |
| `icon_align` | leading, trailing | modifier class أو data attribute |
| `rtl` | true, false | `[dir="rtl"]` |

### variant — كل حالة

```json
{
  "id": "primary-default",
  "axes": { "shape": "primary", "state": "default" },
  "status": "available",
  "files": {
    "details_json": "_figma/btn-primary/btn-primary--default-details.json",
    "state_image":  "_figma/btn-primary/states/default.png"
  },
  "properties": {
    "root_css_props": { ... },
    "text_css":       { ... },
    "icon_css":       { ... },
    "focus_outline_css": null
  }
}
```

### properties — الخصائص

| الحقل | يُطبَّق على | ملاحظة |
|---|---|---|
| `root_css_props` | العنصر الجذر `.component` | layout, background, border, radius |
| `text_css` | `.component__text` | color, font-family, font-size, font-weight, line-height |
| `icon_css` | `.component__icon` | width, height فقط |
| `focus_outline_css` | `::after` pseudo-element | `null` إذا لم تكن حالة focused |

---

## اتفاقية تسمية CSS

### BEM المبسّط

```
.component              ← base
.component--shape       ← shape modifier
.component--size        ← size modifier
.component__icon        ← icon child
.component__text        ← text child
```

### تطبيق المحاور على CSS

```css
/* shape → modifier class */
.btn--primary { background: var(--button-primary-bg-default); }
.btn--secondary { ... }

/* size → modifier class */
.accordion--sm { height: var(--accordion-sm-height); }
.accordion--lg { height: var(--accordion-lg-height); }

/* state → pseudo-classes */
.component:hover:not(:disabled) { ... }
.component:focus,
.component:focus-visible { ... }
.component:active:not(:disabled) { ... }
.component:disabled { ... }
.component[aria-pressed="true"] { ... }   /* selected */

/* expanded / flush / variant → data attribute */
.accordion[data-expanded="true"] { ... }
.accordion[data-flush="true"] { ... }

/* RTL → dir attribute (يرث من html[dir="rtl"]) */
[dir="rtl"] .component { ... }
```

---

## قواعد حالة focused

حالة focused دائماً تتكوّن من **طبقتين**:

```css
/* 1. إطار خارجي على العنصر نفسه */
.component:focus,
.component:focus-visible,
.component.is-focused {
  border: var(--[component]-focus-border-width) solid var(--[component]-focus-ring-outer-color);
}

/* 2. حلقة داخلية عبر ::after */
.component:focus::after,
.component:focus-visible::after,
.component.is-focused::after {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  border: 3px solid var(--[component]-focus-ring-inner-color);
  pointer-events: none;
}
```

> العنصر الجذر يجب أن يكون `position: relative` دائماً.

---

## قاعدة حالة pressed

pressed **تلغي** تأثير focused كاملاً:

```css
.component:active:not(:disabled),
.component.is-pressed {
  background: var(--[component]-bg-pressed);
  border: none;
}

.component:active:not(:disabled)::after,
.component.is-pressed::after {
  display: none;
}
```

---

## قواعد disabled

```css
.component:disabled,
.component[aria-disabled="true"] {
  background: var(--[component]-disabled-bg);
  color: var(--[component]-disabled-text);
  cursor: not-allowed;
  pointer-events: none;
}
```

---

## هيكل HTML المعياري للمكوّن

```html
<[tag] class="component component--[shape] component--[size]"
       type="button"
       aria-pressed="false"
       data-expanded="false"
       data-flush="false">

  <!-- Icon (إذا وُجد) -->
  <span class="component__icon" aria-hidden="true">
    <svg>...</svg>
  </span>

  <!-- Text -->
  <span class="component__text">Label</span>

</[tag]>
```

### HTML Attributes للحالات

| الحالة | الـ attribute |
|---|---|
| disabled | `disabled` (أو `aria-disabled="true"`) |
| selected | `aria-pressed="true"` |
| expanded | `data-expanded="true"` |
| flush | `data-flush="true"` |
| focused (static) | class `is-focused` (للـ showcase فقط) |
| pressed (static) | class `is-pressed` (للـ showcase فقط) |

---

## ملف CSS المكوّن — ما يحتويه وما لا يحتويه

### يحتوي فقط على
- `.component` base styles
- `.component--[variant]` modifier styles
- `.component__[child]` child styles
- كل الحالات التفاعلية للمكوّن

### لا يحتوي على
- reset (`*`, `body`, `html`)
- page layout (`.page`, `.showcase`, `.interactive`)
- أي قيمة ثابتة بدون `var(--token)`

---

## showcase page — ملف HTML

عند إنشاء صفحة عرض المكوّن:

```html
<head>
  <!-- 1. Token أولاً -->
  <link rel="stylesheet" href="../../token.css" />
  <!-- 2. CSS المكوّن -->
  <link rel="stylesheet" href="../[component].css" />
  <!-- 3. Page styles داخل style tag (ليس ملف خارجي) -->
  <style>
    /* reset + page layout + showcase styles هنا */
  </style>
</head>
```

### ترتيب الصفوف في showcase

```
Default → Hovered → Focused → Pressed → Disabled → Selected
```

### عرض خصائص Figma — سياسة إلزامية

كل صف `.showcase__row` يجب أن يحمل الـ `data-props` المقابل له من ملف JSON في `_figma/`.

**قاعدة الـ attribute:**
```html
<div class="showcase__row"
     data-props="RTL=False, Size=Large, State=Default, Style=Primary, ...">
```

القيمة هي **حرفياً** قيمة الحقل `name` الموجودة في ملف JSON المقابل لهذه الحالة.

**آلية العرض:** يقرأ JavaScript في نهاية الصفحة هذا الـ attribute ويُنشئ `.prop-tags` تلقائياً أسفل المكوّن — لا تكتب HTML للشارات يدوياً.

**CSS + JS المطلوبان في كل showcase page:**

```css
/* أضف هذا داخل <style> في <head> */
.prop-tags {
  display: flex; flex-wrap: wrap; gap: 4px;
  direction: ltr; margin-top: 8px;
  padding-top: 8px; border-top: 1px dashed var(--gray-150, #eaecf0);
}
.prop-tag {
  display: inline-flex; align-items: center;
  padding: 2px 7px; background: var(--gray-50);
  border: 1px solid var(--gray-200); border-radius: 3px;
  font-size: 11px; font-family: "ui-monospace", monospace;
  line-height: 1.5; white-space: nowrap;
}
.prop-tag__key { color: var(--gray-400); }
.prop-tag__eq  { color: var(--gray-300); margin: 0 2px; }
.prop-tag__val { color: var(--gray-700); font-weight: 500; }
```

```html
<!-- أضف هذا قبل </body> -->
<script>
  (function () {
    document.querySelectorAll('.showcase__row[data-props]').forEach(function(row) {
      var label = row.querySelector('.showcase__label');
      var others = Array.from(row.children).filter(function(c){ return c !== label; });
      if (!others.length) return;
      var first = others[0];
      var item = first.classList.contains('showcase__item') ? first : (function(){
        var w = document.createElement('div');
        w.className = 'showcase__item';
        first.replaceWith(w); w.appendChild(first); return w;
      })();
      row.style.alignItems = 'flex-start';
      var tags = document.createElement('div');
      tags.className = 'prop-tags';
      row.getAttribute('data-props').split(',').forEach(function(part) {
        part = part.trim();
        var eq = part.indexOf('='); if (eq < 0) return;
        var t = document.createElement('span'); t.className = 'prop-tag';
        t.innerHTML = '<span class="prop-tag__key">' + part.slice(0,eq).trim() + '</span>'
                    + '<span class="prop-tag__eq">=</span>'
                    + '<span class="prop-tag__val">' + part.slice(eq+1).trim() + '</span>';
        tags.appendChild(t);
      });
      item.appendChild(tags);
    });
  }());
</script>
```

---

## سير العمل — إضافة مكوّن جديد

```
1. أنشئ مجلد: components/[name]/
2. أضف بيانات Figma في _figma/
3. حدد المحاور في reference.json  →  axes + axis_values
4. وثّق كل variant في variants[]  →  properties مرتبطة بـ tokens
5. أنشئ [name].css بالاتفاقيات أعلاه
6. أضف توكنز المكوّن في token.css
```

---

## مثال مرجعي — Button

المكوّن المكتمل كنموذج:

- [reference.json](components/button/reference.json) — axes: shape + state
- [button.css](components/button/button.css) — implementation
- [_figma/btn-primary/](components/button/_figma/btn-primary/) — Figma source data
