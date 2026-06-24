# Quote — Component Contract

```
contract_version: 1.0.0
component_id:     quote
status:           stable
category:         content / editorial
last_reviewed:    2026-06-13
```

---

## 1. Component Type

**Primitive**

---

## 2. Dependencies

- None

---

## 3. Purpose

The Quote component highlights an attributed quotation. It presents a block of quoted text with an optional heading title and author attribution. It is a purely presentational component — no interactive states.

Use Quote when you need to:
- Feature a notable quotation on a page
- Attribute a statement to a named individual or source
- Create visual emphasis for editorial content

Do NOT use Quote for:
- Inline citations within body text (use `<cite>` inline)
- Decorative text blocks without attribution (use a styled `<p>` instead)
- Interactive testimonial carousels (add a carousel wrapper component)

---

## 4. Anatomy

```
.quote                         ← <blockquote> root, position: relative
  ::before                     ← opening " decorative mark (CSS pseudo-element)
  ::after                      ← closing " decorative mark (CSS pseudo-element)
  .quote__body                 ← <div> content inset area (64px horizontal padding)
    .quote__title              ← <p> optional heading text (display font, 500 weight)
    .quote__text               ← <p> main quote body text (text font, 400 weight)
  .quote__author-details       ← <footer> author attribution container
    .quote__author-info        ← <div> column stack
      .quote__author-name      ← <cite> author name (500 weight, right-aligned)
      .quote__author-description ← <span> author brief / role (400 weight)
```

**Slot rules:**

| Slot | Required | Notes |
|---|---|---|
| `.quote__text` | Always | The main quoted content |
| `.quote__title` | Optional | Heading text above the quote body |
| `.quote__author-name` | Recommended | Author or source attribution |
| `.quote__author-description` | Optional | Author role, title, or brief description |

---

## 5. CSS Modifiers

| Modifier | Description | Required? |
|---|---|---|
| `.quote--sm` | Small size — 640px width | Default is Large (846px) |
| `.quote--white-bg` | White surface background (`#F9FAFB`) | Default is transparent |

**Direction** is not a CSS modifier class. Set `dir="rtl"` or `dir="ltr"` on the `.quote` root element or an ancestor element.

---

## 6. HTML Contract

### Standard quote (LTR, Large, No Background)
```html
<blockquote class="quote" dir="ltr">
  <div class="quote__body">
    <p class="quote__title">Title of quote</p>
    <p class="quote__text">The quote is placed here to highlight a specific saying or to present a brief quote that expresses an important idea or concept.</p>
  </div>
  <footer class="quote__author-details">
    <div class="quote__author-info">
      <cite class="quote__author-name">Author's name</cite>
      <span class="quote__author-description">Brief or description</span>
    </div>
  </footer>
</blockquote>
```

### White background surface
```html
<blockquote class="quote quote--white-bg" dir="ltr">
  ...
</blockquote>
```

### Small size
```html
<blockquote class="quote quote--sm" dir="ltr">
  ...
</blockquote>
```

### Small size with white background
```html
<blockquote class="quote quote--sm quote--white-bg" dir="ltr">
  ...
</blockquote>
```

### RTL (Arabic)
```html
<blockquote class="quote" dir="rtl">
  <div class="quote__body">
    <p class="quote__title">عنوان الاقتباس</p>
    <p class="quote__text">تُوضع هنا عبارة الاقتباس لتسليط الضوء على مقولة معينة أو تقديم اقتباس مختصر يعبر عن فكرة أو مفهوم مهم.</p>
  </div>
  <footer class="quote__author-details">
    <div class="quote__author-info">
      <cite class="quote__author-name">اسم المؤلف</cite>
      <span class="quote__author-description">نبذة أو وصف</span>
    </div>
  </footer>
</blockquote>
```

### Quote without title
```html
<blockquote class="quote quote--white-bg" dir="ltr">
  <div class="quote__body">
    <p class="quote__text">The quote text goes here expressing an important idea or concept.</p>
  </div>
  <footer class="quote__author-details">
    <div class="quote__author-info">
      <cite class="quote__author-name">Author's name</cite>
      <span class="quote__author-description">Role or description</span>
    </div>
  </footer>
</blockquote>
```

### Quote without author description
```html
<blockquote class="quote" dir="ltr">
  <div class="quote__body">
    <p class="quote__title">Title of quote</p>
    <p class="quote__text">The quote text goes here.</p>
  </div>
  <footer class="quote__author-details">
    <div class="quote__author-info">
      <cite class="quote__author-name">Author's name</cite>
    </div>
  </footer>
</blockquote>
```

---

## 7. States

This component has no interactive states. It is purely presentational.

| Axis | Values | CSS mechanism |
|---|---|---|
| Direction | LTR, RTL | `[dir="rtl"] .quote` selector |
| Size | Large (default), Small | `.quote--sm` modifier |
| Background | None (default), White | `.quote--white-bg` modifier |

---

## 8. Typography Reference

| Element | Font family | Size | Weight | Line height |
|---|---|---|---|---|
| `.quote__title` | Display (`--Font-Family-font-family-display`) | 24px | 500 | 32px |
| `.quote__text` | Text (`--Font-Family-font-family-text`) | 20px | 400 | 30px |
| `.quote__author-name` | Text (`--Font-Family-font-family-text`) | 20px | 500 | 30px |
| `.quote__author-description` | Text (`--Font-Family-font-family-text`) | 18px | 400 | 28px |
| Decorative marks (`::before`, `::after`) | Text font | 128px | 400 | 32px |

---

## 9. Decorative Quotation Marks

The opening `"` (U+201C) and closing `"` (U+201D) marks are **decorative** and rendered via CSS `::before`/`::after` pseudo-elements. They are not part of the HTML markup.

CSS positions by variant:

| Variant | Opening mark | Closing mark |
|---|---|---|
| LTR Large | `left: 14px; top: 20px` | `right: 19px; bottom: 23px` |
| LTR Small | `left: 13px; top: 20px` | `right: 13px; bottom: 36px` |
| RTL Large | `right: 7px; top: 20px` | `left: 23px; bottom: 23px` |
| RTL Small | `right: 7px; top: 20px` | `left: 23px; bottom: 23px` |

Mark color: `--Text-text-primary-sa-flag` (#14573A — Saudi green)

---

## 10. Quote Title Element

`.quote__title` defaults to `<p>`. If the quote block functions as a section heading within the document hierarchy, the implementer may substitute an appropriate heading element:

```html
<h2 class="quote__title">Title of quote</h2>
```

The visual presentation is identical. The element choice depends on the document outline.

---

## 11. Accessibility Requirements

| Requirement | Rule ID |
|---|---|
| Root must be `<blockquote>` | QUOTE-A11Y-001 |
| Author name must use `<cite>` | QUOTE-A11Y-002 |
| Author attribution section must use `<footer>` | QUOTE-A11Y-003 |
| `dir` attribute must match content language direction | QUOTE-A11Y-004 |
| Decorative marks must not generate meaningful accessible names | QUOTE-A11Y-005 |

---

## 12. What NOT to Do

```html
<!-- WRONG: not using <blockquote> as root -->
<div class="quote" dir="ltr">...</div>

<!-- WRONG: using <span> for author name instead of <cite> -->
<span class="quote__author-name">Author Name</span>

<!-- WRONG: adding decorative marks to HTML (they are in CSS ::before/::after) -->
<blockquote class="quote">
  <span aria-hidden="true">"</span>
  ...
</blockquote>

<!-- WRONG: hardcoded color or font size -->
<blockquote class="quote" style="background: #F9FAFB; font-size: 20px;">...</blockquote>

<!-- WRONG: using .quote--rtl modifier class (RTL is set via dir attribute) -->
<blockquote class="quote quote--rtl">...</blockquote>
```

---

## 13. Assembly Awareness

The Quote component may participate in the following assemblies:

| Assembly | Role |
|---|---|
| Editorial article page | Pull quote or featured quotation |
| Landing page | Hero testimonial block |
| Profile section | Featured statement from a person |
| Content carousel | Testimonial slide (wrap with carousel component) |

The Quote component does not define any slot API for other components. It is a leaf component in the composition tree.
