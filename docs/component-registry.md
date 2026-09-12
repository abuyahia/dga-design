# سجل المكوّنات القابلة لإعادة الاستخدام

سجل تدريجي للمكوّنات التي تمت مراجعتها أثناء بناء القوالب. مسارات CSS هي مصدر التنسيق؛ لا تُنسخ إلى القوالب.

| المكوّن / القسم | المصدر | CSS / السلوك | الاستخدام والملاحظات |
|---|---|---|---|
| Digital Stamp | `components/digital-stamp/template.html`؛ `scripts/digital_stamp_markup.py` | `components/digital-stamp/digital-stamp.css` و`.js` | جميع الصفحات؛ preview/registered من الإعدادات |
| Navigation Header | `partials/site-header/template.html`؛ `components/navigation-header/` | `components/navigation-header/navigation-header.css` و`.js` | جميع الصفحات؛ روابط وقوائم فرعية من navigation |
| Footer | `partials/site-footer/template.html`؛ `scripts/footer_markup.py` | `components/footer/footer.css` | جميع الصفحات؛ النسخة الداكنة، الروابط من footer_groups |
| Breadcrumb | `components/breadcrumb/two-level.html`؛ أمثلة `showcases/index.html` | `components/breadcrumb/breadcrumb.css` | الخدمات والمحتوى الثقيل؛ أضيف تركيب مستويين قابل لإعادة الاستخدام |
| Divider | `components/divider/template.html` | `components/divider/divider.css` | المحتوى الثقيل؛ النسخة الأفقية المحايدة |
| List | `components/list/template.html` | `components/list/list.css` | المحتوى الثقيل؛ ordered وunordered من بيانات مهربة، ودعم RTL منطقي |
| Page Intro | `sections/page-intro/template.html`؛ `scripts/page_intro_markup.py` | `templates/government/composition.css` | جميع رؤوس الصفحات الداخلية؛ يركّب Breadcrumb الحالي عبر `breadcrumb_markup`، وتبقى `eyebrow_markup` و`description_markup` و`extra_content_markup` اختيارية. `default` يستخدم `page-intro` فقط للعنوان القياسي؛ `compact` للصفحات الكثيفة مثل FAQ؛ `description` للصفحات المعلوماتية؛ `featured` للبطاقة أو CTA أو كتلة مرتبطة؛ `decorative` لخلفية زخرفية مقصودة دون أصول إضافية |
| Accordion | `components/accordion-new/item.html`؛ أمثلة `template.html` | `components/accordion-new/accordion-new.css`؛ `scripts/core/index.js` | FAQ؛ ملف item تركيب معرّف وسؤال وإجابة مهربة؛ large، trailing icon؛ محتوى ظاهر دون JS |
| Card | `components/card/template.html` | `components/card/card.css` | الرئيسية والأخبار ودعوة التواصل؛ content/title/body/actions |
| Button / Link | `components/button/template.html`؛ `components/link/template.html` | CSS داخل المجلدين | جميع القوالب؛ CTA يستخدم رابطًا بتنسيق btn--primary btn--lg |
| Page Feedback | `sections/feedback/template.html`؛ `scripts/feedback_markup.py` | `components/page-feedback/page-feedback.css`؛ `styles/composites/feedback.css` و`.js` | الصفحات العامة ومنها FAQ؛ الإحصاءات اختيارية، تقييم محلي تجريبي |
| FAQ section | `sections/faq/template.html`؛ فرع faq في `scripts/build_site.py` | `templates/faq/faq.css`؛ core يُركب أثناء البناء | FAQ؛ قائمة questions من إعدادات الصفحة، دون حد ثابت لعدد الأسئلة |
| Contact CTA section | `sections/contact-cta/template.html` | `templates/faq/faq.css` | FAQ؛ يركب Card وButton؛ title/description/href/label قابلة للتخصيص |
| Table of Contents | `components/table-of-contents/template.html`؛ `item.html` | `components/table-of-contents/table-of-contents.css`؛ `templates/content/content.js` | المحتوى الثقيل؛ عناصر عادية وفرعية، aria-current نشط، روابط fragment تعمل دون JS |
| Heavy Content section | `sections/heavy-content/`؛ `scripts/content_markup.py` | `templates/content/content.css` | content.html؛ فقرات وقوائم وروابط ووسائط وعناوين فرعية من إعدادات منظمة |
| Text Input / Input Affix | `components/text-input/template.html`؛ `components/input-affix/template.html` | CSS داخل المجلدين؛ `scripts/form_markup.py` يركّب الحالات | contact.html وform.html؛ افتراضي وأيقونة وبادئة ولاحقة ومساعد وخطأ وتعطيل، مع معرّفات وسمات وصول أصلية |
| Progress Indicator | `components/progress-indicator/template.html`؛ `item.html` | `components/progress-indicator/progress-indicator.css`؛ `templates/form/form.js` | form.html؛ خطوات عمودية للحاسوب وملخص دائري للجوال، aria-current واحد، ويعمل مبدئيًا دون JS |
| Form Template section | `sections/form/template.html`؛ `scripts/form_markup.py` | `templates/form/form.css` و`.js` | form.html؛ نموذج الحالات من إعدادات variants، أزواج مطلوبة/اختيارية، وتنقل خطوات محلي بلا إرسال |
| Error State / Error Template | `sections/error-state/template.html`؛ `templates/error/template.html`؛ `scripts/error_state_markup.py` | `templates/error/error.css`؛ الأيقونات الأصلية في `templates/error/assets/` | error.html؛ قالب صفحة يركّب حالة خطأ قابلة لإعادة الاستخدام لرمز ورسالة ووصف وإجراء رئيسي، ومتجاوب حسب مرجع Figma. صفحة نظام مستقلة لا تستخدم Page Intro لأن المرجع يعرّف حالة الخطأ نفسها كمحتوى الصفحة |
| Container / Stack | `styles/base/layout.css` | نفس الملف؛ `token.css` | جميع القوالب؛ مقاسات واتجاهات مشتركة |
