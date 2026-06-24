# Avatar Contract

## Component Type

Primitive

---

## Dependencies

None.

---

## Anatomy

```
.avatar                     — Root container (surface + shape + size)
  ├── .avatar__icon         — Icon slot (icon type only)
  │     └── <svg>           — User SVG icon, aria-hidden
  ├── .avatar__initials     — Initials slot (initials type only), aria-hidden
  └── <img>.avatar__image   — Image element (image type only)

.avatar-group               — Group layout wrapper
  ├── .avatar               — Avatar instance × N
  └── .avatar.avatar--overflow — Overflow counter avatar (optional)
        └── .avatar__initials — "+99" text, aria-hidden
```

---

## CSS Modifiers

### Shape

| Modifier        | Effect                              |
|-----------------|-------------------------------------|
| _(none)_        | Circle — `border-radius: 9999px`    |
| `.avatar--square` | Square — `border-radius: 4px`     |

> At size 120px, `.avatar--square` uses `border-radius: 8px`.

### Size

| Modifier       | Dimensions |
|----------------|------------|
| `.avatar--24`  | 24×24 px   |
| `.avatar--32`  | 32×32 px   |
| `.avatar--40`  | 40×40 px   |
| `.avatar--48`  | 48×48 px   |
| `.avatar--64`  | 64×64 px   |
| `.avatar--80`  | 80×80 px   |
| `.avatar--120` | 120×120 px |

### Type

| Modifier         | Effect                                  |
|------------------|-----------------------------------------|
| _(none)_         | Icon or Initials (default fill + text)  |
| `.avatar--image` | Photo mode — white background for `<img>` |
| `.avatar--overflow` | Overflow counter — same fill as default |

### Group

| Modifier               | Effect                               |
|------------------------|--------------------------------------|
| `.avatar-group--stacked` | Overlapping avatars (negative gap) |
| `.avatar-group--flat`    | Side-by-side avatars (4px gap)    |

---

## HTML Patterns

### Icon type

```html
<div class="avatar avatar--32" role="img" aria-label="Ahmed Al-Rashidi">
  <span class="avatar__icon" aria-hidden="true">
    <!-- SVG user icon -->
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
      <path d="M12 12C14.761 12 17 9.761 17 7C17 4.239 14.761 2 12 2C9.239 2 7 4.239 7 7C7 9.761 9.239 12 12 12Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
      <path d="M20.59 22C20.59 18.13 16.74 15 12 15C7.26 15 3.41 18.13 3.41 22" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </span>
</div>
```

### Initials type

```html
<div class="avatar avatar--40" role="img" aria-label="Sara Mohammed">
  <span class="avatar__initials" aria-hidden="true">SM</span>
</div>
```

### Image type

```html
<div class="avatar avatar--48 avatar--image">
  <img class="avatar__image" src="/path/to/photo.jpg" alt="Nasser Al-Otaibi" />
</div>
```

### Square shape

```html
<div class="avatar avatar--40 avatar--square" role="img" aria-label="Khalid Ibrahim">
  <span class="avatar__initials" aria-hidden="true">KI</span>
</div>
```

### Avatar Group — Stacked

```html
<div class="avatar-group avatar-group--stacked" role="group" aria-label="5 team members and 99 more">
  <div class="avatar avatar--32 avatar--image">
    <img class="avatar__image" src="/users/1.jpg" alt="User 1" />
  </div>
  <div class="avatar avatar--32 avatar--image">
    <img class="avatar__image" src="/users/2.jpg" alt="User 2" />
  </div>
  <div class="avatar avatar--32 avatar--overflow" aria-hidden="true">
    <span class="avatar__initials">+99</span>
  </div>
</div>
```

### Avatar Group — Flat

```html
<div class="avatar-group avatar-group--flat" role="group" aria-label="3 team members">
  <div class="avatar avatar--32 avatar--image">
    <img class="avatar__image" src="/users/1.jpg" alt="User 1" />
  </div>
  <div class="avatar avatar--32 avatar--image">
    <img class="avatar__image" src="/users/2.jpg" alt="User 2" />
  </div>
  <div class="avatar avatar--32 avatar--image">
    <img class="avatar__image" src="/users/3.jpg" alt="User 3" />
  </div>
</div>
```

---

## Accessibility Contract

| Requirement | Rule |
|---|---|
| Root `role="img"` | Required on Icon and Initials types when conveying identity |
| `aria-label` on root | Required — must contain the person's name |
| `aria-hidden` on `.avatar__icon` | Required — icon is decorative |
| `aria-hidden` on `.avatar__initials` | Required — label is on root |
| `alt` on `<img>` | Required — must be person's name (replaces `role`/`aria-label` on root) |
| `.avatar--overflow` | Must be `aria-hidden="true"` |
| `.avatar-group` | Must have `role="group"` and descriptive `aria-label` |

---

## Token Contract

The component currently uses Figma-exported token names as fallback references. Component-level tokens are pending definition.

### Pending tokens (to be added to token.css)

| Token | Proposed value |
|---|---|
| `--avatar-bg-default` | `var(--Button-button-background-neutral-default, #F3F4F6)` |
| `--avatar-border-color` | `var(--Border-border-white, #FFF)` |
| `--avatar-text-color` | `var(--Text-text-default, #161616)` |
| `--avatar-bg-image` | `var(--Background-background-white, #FFF)` |
| `--avatar-radius-circle` | `var(--radius-round, 9999px)` |
| `--avatar-radius-square-sm` | `var(--radius-4, 4px)` |
| `--avatar-radius-square-lg` | `var(--radius-8, 8px)` |
| `--avatar-group-gap` | `var(--Global-spacing-xs, 4px)` |

---

## Size Contract

| Size | Dimensions | Border | Icon slot | Font scale             | Font weight |
|------|-----------|--------|-----------|------------------------|-------------|
| 24px | 24×24     | 2px    | 16×16     | text-2xs (10px)        | 700         |
| 32px | 32×32     | 2px    | 24×24     | text-xs (12px)         | 600         |
| 40px | 40×40     | 2px    | 32×32     | text-sm (14px)         | 600         |
| 48px | 48×48     | 2px    | 32×32     | text-md (16px)         | 500         |
| 64px | 64×64     | 2px    | 40×40     | text-xl (20px)         | 500         |
| 80px | 80×80     | 2px    | 56×56     | display-sm (30px)      | 500         |
| 120px | 120×120  | 4px    | 80×80     | display-md (36px)      | 500         |

> Square shape at 120px uses `border-radius: 8px`. All other square sizes use `border-radius: 4px`.

---

## Constraints

- Initials should be 1–2 characters maximum.
- Overflow counter text should follow "+N" pattern (e.g. "+5", "+99").
- Do not apply `.avatar--image` without a valid `<img>` inside.
- Avatar does not define its own focus ring — focus belongs to the interactive wrapper if avatar is used inside a link or button.
- Do not nest `.avatar-group` inside another `.avatar-group`.

---

## Assembly Notes

Avatar is a leaf primitive and participates in:

- `avatar-group` — layout grouping of multiple avatars
- `card` — profile cards, content cards (future)
- `comment` — author attribution (future)
- `list-item` — user lists (future)

Avatar boundaries must remain independent. Parent assemblies must not override `.avatar` internal styles.
