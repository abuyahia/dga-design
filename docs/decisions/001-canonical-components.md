# 001 — اختيار مسارات Link وAccordion

الحالة: قرار للعمل القادم في الدفعة الأولى. لا حذف، لا rename، ولا تعديل CSS أوHTML للنسخ المقارنة.

## Link

| المقارنة | dga-links | link |
|---|---|---|
| styles | primary/neutral/on-color | نفسها |
| sizes | small/medium | نفسها |
| states | default/hover/focus/pressed/visited/disabled | نفسها |
| inline | موجود | موجود |
| CSS namespace | `.link` | `.link` |
| عقد وaudit وcompliance | لا | نعم |
| tokens | fallbacks وأسماء غير مركزية | fallbacks وأسماء غير مركزية |

القرار: `components/link/` المسار المعتمد للعمل القادم؛ `dga-links/` legacy source محفوظ. تغطية المحاور متكافئة على مستوى المرجع، لكن التكافؤ البصري لم يُختبر. بيانات `_figma` الموجودة في dga-links تظل مصدرًا متاحًا؛ لا تنسخ المكتبة ولا تفقد المصدر.

لا تحميل لملفَي `link.css` معًا. أي نقل مستقبلي لمستهلك يتطلب مقارنة شكل focus وتعطيل الرابط وأسماء modifiers. الاختيار لا يثبت المطابقة.

## Accordion

| المقارنة | accordion | accordion-new |
|---|---|---|
| sizes | large/medium/small | large/medium/small |
| presentation | normal/flush/leading/leading-flush | icon_alignment + flush، ويمكن تركيبهما |
| trigger/panel | `__header` / `__content` | `__trigger` / `__panel` |
| expanded | `.is-expanded` مع ARIA في المثال | CSS يعتمد على `aria-expanded` |
| size modifiers | `--medium` / `--small` | `--md` / `--sm` |
| disabled | class على root وnative في المثال | native disabled على trigger |
| reduced motion | لا | موجود |
| عقد وaudit وcompliance | لا | نعم |
| tokens | أقرب إلى الملف المركزي | bridge محلي يحتاج تسوية |

القرار: `components/accordion-new/` المسار المختار للتأهيل والعمل الجديد، بمعرف دلالي `accordion`. السبب اتساق عقد الحالة المعتمدة على ARIA واكتمال الوثائق وتغطية التركيبات، وليس كلمة new في الاسم.

القديم يبقى legacy. الاثنان يستخدمان `.accordion`، ولذلك لا يجوز تحميلهما معًا. لا استبدال href وحده: HTML وmodifiers وإدارة expanded مختلفة. المقارنة كشفت أن flush القديم يضبط `padding-inline: 16px` رغم وصفه بأنه بلا padding، ولا توجد قاعدة مستقلة لـleading-flush في CSS القديم. لا نعتمد مطابقة بصرية لأي منهما قبل المرحلة الخاصة بالمكونات.

## بوابة التأهيل القادمة

1. تسوية tokens لكل variant دون إنشاء أسماء متوازية.
2. تشغيل الاتجاهين مع النص العربي الطويل والمحتوى المختلط.
3. تنفيذ keyboard/expanded/disabled behavior، والتحقق من focus والـpanel وprogressive enhancement.
4. مقارنة التغطية بمصادر Figma؛ نقل المستهلكين لاحقًا فقط بعد اجتيازها.

`card-bk/` بيانات مصدر فقط؛ لا نسخة Card إنتاجية ثانية. لا حذف لأي مصدر في هذه الدفعة.
