# {{component_name}} - Component Contract

```
contract_version: {{contract_version}}
component_id:     {{component_id}}
status:           {{status}}
category:         {{category}}
last_reviewed:    {{last_reviewed}}
```

---

## 1. Purpose

Describe what `{{component_name}}` is for, the user intent it supports, and what
it must not be used for.

> AI Rule: Add a concise rule that helps choose this component correctly.

---

## 2. When to Use / When NOT to Use

| Situation | Use {{component_name}}? |
|---|---|
| {{recommended_situation}} | Yes |
| {{unsupported_situation}} | No - use {{alternative_component}} |

---

## 3. Anatomy

```html
<{{root_element}} class="{{selector_root_without_dot}}">
  <span class="{{selector_root_without_dot}}__text">{{label_example}}</span>
</{{root_element}}>
```

| Slot | Required | Notes |
|---|---|---|
| `{{selector_root}}__text` | {{required}} | {{slot_notes}} |

---

## 4. HTML Contract

```html
<{{root_element}} class="{{selector_root_without_dot}}" {{root_attributes}}>
  <span class="{{selector_root_without_dot}}__text">{{label_example}}</span>
</{{root_element}}>
```

---

## 5. Variants

| Variant | CSS Modifier | Use when |
|---|---|---|
| {{variant_name}} | `{{selector_root}}--{{variant_modifier}}` | {{variant_usage}} |

---

## 6. Sizes

| Size | CSS Modifier | Min touch target | Use when |
|---|---|---|---|
| {{size_name}} | `{{size_modifier}}` | {{touch_target}} | {{size_usage}} |

---

## 7. Content Rules

- {{content_rule_1}}
- {{content_rule_2}}
- {{content_rule_3}}

---

## 8. CSS Class Contract

| Class | Purpose | Required |
|---|---|---|
| `{{selector_root}}` | Root element | Yes |
| `{{selector_root}}--{{variant_modifier}}` | Variant modifier | {{variant_required}} |
| `{{selector_root}}__text` | Text slot | {{text_required}} |

---

## 9. State Management

| State | How to apply |
|---|---|
| `hovered` | CSS `:hover` |
| `focused` | CSS `:focus-visible` |
| `disabled` | {{disabled_rule}} |

---

## 10. Accessibility Contract

| Requirement | Rule |
|---|---|
| Accessible name | {{accessible_name_rule}} |
| Role | {{role_rule}} |
| Keyboard | {{keyboard_rule}} |

---

## 11. Token Contract

| Token | Purpose |
|---|---|
| `--{{component_id}}-{{token_name}}` | {{token_purpose}} |
