# Notification Toast — Component Contract

```
contract_version: 1.0.0
component_id:     notification-toast
status:           stable
category:         feedback
last_reviewed:    2026-06-26
```

---

## Component Type

Composite

---

## Dependencies

Required:

- `button` — used for action buttons in the Actions slot and for the dismiss button in the Title header

Optional:

- None

---

## 1. Purpose

A Notification Toast surfaces a brief, contextual message to the user — a status update, alert, or informational notice — with an optional dismiss action and up to two CTA buttons.

It is NOT a persistent banner. Use it for transient feedback that appears in response to a user action or system event. It dismisses either automatically (timed) or via the close button.

---

## 2. When to Use / When NOT to Use

| Situation | Use Toast? |
|---|---|
| Confirm a background action completed (save, send, upload) | Yes |
| Surface a critical error that blocks a user workflow | Yes — type=critical-error |
| Warn the user about an impending issue | Yes — type=warning |
| Provide a persistent navigation notice | No — use Banner or Alert |
| Display form validation errors inline | No — use inline-alert |
| Show a blocking confirmation dialog | No — use Dialog |

---

## 3. Anatomy

```
.notification-toast                    ← root container (white card, drop shadow)
  .notification-toast__title           ← header row (desktop: flex-row; mobile: flex-col)
    .notification-toast__icon-wrap     ← 40×40 full-radius circle, type-specific background
      <svg aria-hidden="true">         ← type-specific icon (decorative)
    .notification-toast__text          ← text content column
      .notification-toast__lead        ← title (font-weight 600, text-md)
      .notification-toast__helper      ← description (font-weight 400, text-sm)
    .notification-toast__close         ← dismiss button (icon-only, delegated to .btn)
  .notification-toast__actions         ← CTA button slot
    .btn (slot)                        ← primary action — consumer-provided
    .btn (slot)                        ← secondary/dismiss — consumer-provided
```

---

## 4. HTML Contract

### Standard toast (neutral, desktop)
```html
<div class="notification-toast notification-toast--neutral" role="alert">
  <div class="notification-toast__title">
    <div class="notification-toast__icon-wrap">
      <svg aria-hidden="true" width="20" height="20"><!-- information-circle --></svg>
    </div>
    <div class="notification-toast__text">
      <p class="notification-toast__lead">عنوان الإشعار</p>
      <p class="notification-toast__helper">تفاصيل الإشعار تظهر هنا عند الحاجة إلى شرح إضافي.</p>
    </div>
    <button type="button" class="notification-toast__close btn btn--subtle btn--icon-only btn--md" aria-label="إغلاق الإشعار">
      <span class="btn__icon" aria-hidden="true">
        <svg width="20" height="20"><!-- multiplication-sign --></svg>
      </span>
    </button>
  </div>
  <div class="notification-toast__actions">
    <button type="button" class="btn btn--secondary-solid btn--md">
      <span class="btn__text">إجراء</span>
    </button>
    <button type="button" class="btn btn--subtle btn--md">
      <span class="btn__text">تجاهل</span>
    </button>
  </div>
</div>
```

### Success toast
```html
<div class="notification-toast notification-toast--success" role="status">
  <div class="notification-toast__title">
    <div class="notification-toast__icon-wrap">
      <svg aria-hidden="true" width="20" height="20"><!-- checkmark-circle-02 --></svg>
    </div>
    <div class="notification-toast__text">
      <p class="notification-toast__lead">تم الحفظ بنجاح</p>
      <p class="notification-toast__helper">تم حفظ التغييرات.</p>
    </div>
    <button type="button" class="notification-toast__close btn btn--subtle btn--icon-only btn--md" aria-label="إغلاق الإشعار">
      <span class="btn__icon" aria-hidden="true"><svg width="20" height="20"><!-- multiplication-sign --></svg></span>
    </button>
  </div>
  <div class="notification-toast__actions">
    <button type="button" class="btn btn--secondary-solid btn--md"><span class="btn__text">عرض التفاصيل</span></button>
    <button type="button" class="btn btn--subtle btn--md"><span class="btn__text">تجاهل</span></button>
  </div>
</div>
```

### Critical/Error toast
```html
<div class="notification-toast notification-toast--critical-error" role="alert">
  <div class="notification-toast__title">
    <div class="notification-toast__icon-wrap">
      <svg aria-hidden="true" width="20" height="20"><!-- alert-02 --></svg>
    </div>
    <div class="notification-toast__text">
      <p class="notification-toast__lead">خطأ في الاتصال</p>
      <p class="notification-toast__helper">تعذّر الاتصال بالخادم. يُرجى المحاولة مجدداً.</p>
    </div>
    <button type="button" class="notification-toast__close btn btn--subtle btn--icon-only btn--md" aria-label="إغلاق الإشعار">
      <span class="btn__icon" aria-hidden="true"><svg width="20" height="20"><!-- multiplication-sign --></svg></span>
    </button>
  </div>
  <div class="notification-toast__actions">
    <button type="button" class="btn btn--secondary-solid btn--md"><span class="btn__text">إعادة المحاولة</span></button>
    <button type="button" class="btn btn--subtle btn--md"><span class="btn__text">تجاهل</span></button>
  </div>
</div>
```

### RTL toast
```html
<!-- No class change needed — apply dir="rtl" on a parent or on the element -->
<div class="notification-toast notification-toast--info" role="alert" dir="rtl">
  <!-- same inner structure -->
</div>
```

---

## 5. Type Guide

| Type | Modifier Class | Icon | Icon Background Token | ARIA Role |
|------|----------------|------|----------------------|-----------|
| neutral | `.notification-toast--neutral` | `information-circle` | `--notification-toast-icon-bg-neutral` | `alert` or `status` |
| info | `.notification-toast--info` | `information-circle` | `--notification-toast-icon-bg-info` | `status` |
| critical-error | `.notification-toast--critical-error` | `alert-02` | `--notification-toast-icon-bg-critical-error` | `alert` |
| warning | `.notification-toast--warning` | `alert-circle` | `--notification-toast-icon-bg-warning` | `alert` |
| success | `.notification-toast--success` | `checkmark-circle-02` | `--notification-toast-icon-bg-success` | `status` |

---

## 6. CSS Class Contract

| Class | Purpose | Required |
|---|---|---|
| `.notification-toast` | Base styles — always present | Yes |
| `.notification-toast--[type]` | Type modifier (sets icon background) | Yes |
| `.notification-toast--mobile` | Explicit mobile layout (stacked) — use in showcases or forced-narrow contexts | No |
| `.notification-toast__title` | Header row (icon + text + close) | Yes |
| `.notification-toast__icon-wrap` | Icon circle container | Yes |
| `.notification-toast__text` | Text column | Yes |
| `.notification-toast__lead` | Title text | Yes |
| `.notification-toast__helper` | Description text | Recommended |
| `.notification-toast__close` | Dismiss button wrapper | Yes (if dismissable) |
| `.notification-toast__actions` | Actions slot container | Recommended |

---

## 7. State Management

The notification-toast root has no interactive states. State is managed by child buttons per the button contract.

| Child | State | How to apply |
|---|---|---|
| `.notification-toast__close` | All button states | Inherited from `.btn` contract |
| `.notification-toast__actions .btn` | All button states | Inherited from `.btn` contract |

---

## 8. Accessibility Contract

| Requirement | Rule |
|---|---|
| Live region | Use `role="alert"` (assertive) for critical-error and warning. Use `role="status"` (polite) for neutral, info, success. |
| Close button label | `.notification-toast__close` must have `aria-label` (e.g., `"Dismiss notification"` / `"إغلاق الإشعار"`) |
| Icon | SVG inside `.notification-toast__icon-wrap` must carry `aria-hidden="true"` |
| Focus management | On toast appear: do NOT auto-focus the toast. On toast dismiss: return focus to the triggering element if applicable. |
| Keyboard | Close button and action buttons must be operable with keyboard (handled by `.btn` contract) |

---

## 9. RTL Behavior

Layout mirrors automatically via CSS logical properties when `dir="rtl"` is present on an ancestor or on the root element.

- `padding-inline` reverses automatically
- `inset-inline-end` on mobile close button reverses automatically
- No additional modifier class is required

---

## 10. Responsive Behavior

| Breakpoint | Behavior |
|---|---|
| `> 767px` (Desktop) | Width: 484px. Title: flex row (icon + text + close). Actions: flex row with 40px indent. Buttons: medium (32px). |
| `≤ 767px` (Mobile) | Width: 343px. Title: flex wrap-column (icon first row, text second row, close absolute). Actions: flex column, full-width buttons at 40px. |

---

## 11. Token Surface

These are the tokens this component reads. Override through tokens only — never hardcode values:

```
--notification-toast-bg
--notification-toast-v-padding
--notification-toast-desktop-h-padding
--notification-toast-mobile-h-padding
--notification-toast-gap
--notification-toast-radius
--notification-toast-shadow               (TODO: missing in token.css)
--notification-toast-desktop-width        (TODO: missing in token.css)
--notification-toast-mobile-width         (TODO: missing in token.css)
--notification-toast-title-gap
--notification-toast-icon-size
--notification-toast-icon-radius
--notification-toast-icon-inner-size
--notification-toast-icon-bg-neutral
--notification-toast-icon-bg-info
--notification-toast-icon-bg-critical-error
--notification-toast-icon-bg-warning
--notification-toast-icon-bg-success
--notification-toast-text-gap
--notification-toast-title-color
--notification-toast-title-font-size
--notification-toast-title-font-weight
--notification-toast-title-line-height
--notification-toast-helper-color
--notification-toast-helper-font-size
--notification-toast-helper-font-weight
--notification-toast-helper-line-height
--notification-toast-font-family
--notification-toast-close-size
--notification-toast-close-radius
--notification-toast-close-mobile-offset
--notification-toast-actions-gap
--notification-toast-actions-indent
```

---

## 12. Compliance Mapping

| Standard | Criterion | Status |
|---|---|---|
| WCAG 2.1 AA | 1.1.1 Non-text Content | mapped |
| WCAG 2.1 AA | 1.4.3 Contrast (Minimum) | mapped |
| WCAG 2.1 AA | 2.1.1 Keyboard | mapped (via button contract) |
| WCAG 2.1 AA | 4.1.3 Status Messages | mapped — live region |
| WCAG 2.1 AA | 4.1.2 Name, Role, Value | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-TOAST-001 (tokens) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-TOAST-002 (RTL) | mapped |
| PLATFORM-CODE-DS | PLATFORM-CODE-TOAST-003 (live region) | mapped |
| PLATFORM-CODE-A11Y | PLATFORM-CODE-A11Y-001 (Arabic font) | mapped |

---

## 13. Forbidden Patterns

```html
<!-- WRONG: missing type modifier -->
<div class="notification-toast" role="alert">...</div>

<!-- WRONG: icon not marked aria-hidden -->
<div class="notification-toast__icon-wrap">
  <svg><!-- icon --></svg>
</div>

<!-- WRONG: close button without aria-label -->
<button class="notification-toast__close btn btn--subtle btn--icon-only btn--md">
  <span class="btn__icon"><svg>...</svg></span>
</button>

<!-- WRONG: no role on root -->
<div class="notification-toast notification-toast--warning">...</div>

<!-- WRONG: hardcoded color instead of token -->
<div class="notification-toast" style="background: #FFF;">...</div>
```

---

## 14. Known Limitations

| Limitation | Impact | Workaround |
|---|---|---|
| `--notification-toast-shadow` token missing in `token.css` | Shadow uses hardcoded fallback | Add token to `token.css` |
| Icon SVG source not embedded | Consumer must source SVGs from icon library | Document icon names in `type_icon_map` in `reference.json` |
| Mobile breakpoint (767px) not tokenized | Breakpoint is hardcoded in CSS | Confirm design system breakpoint token and update |
