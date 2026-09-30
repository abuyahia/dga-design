# خطة بناء منتج موقع هيئة — V1

الحالة: خطة تنفيذ قابلة للتطبيق بعد اعتماد البحث والمخطط. تُنفذ حزمة واحدة في
كل مرة، مع اختبار مركز ومعيار خروج قبل الانتقال.

## 1. استراتيجية البناء

الأولوية للبنية والبيانات والتفاصيل قبل القوائم والرئيسية:

```text
حد المنتج
  ↓
الصفحات المؤسسية المعاد استخدامها
  ↓
العقود المشتركة الجديدة
  ↓
الخدمات والتحرير والمحفظة والموارد
  ↓
التنظيمات الخاصة بالهيئة
  ↓
الرئيسية
  ↓
التكامل والفحص النهائي
```

كل حزمة تحافظ على بناء legacy ومنتج الوزارة. لا يبدأ renderer جديد قبل اكتمال
عقد بياناته وسجلات demo الآمنة.

### Page Specification Gate

Before starting any page implementation package, read the corresponding
complete Page Specification in `authority-blueprint.md`.

The Page Specification is the authoritative source for page purpose, content,
structure, presentation, UX, responsive behavior, RTL, accessibility, SEO,
components, and ownership.

Package labels such as REUSE, ADAPT, and NEW define implementation strategy
only and must never reduce the approved page experience.

If the approved specification cannot be satisfied by the planned implementation,
stop and report the gap before changing or omitting the requirement.

## 2. ملخص الحزم

| ID  | الحزمة                        | التصنيف        | التعقيد | تعتمد على |
| --- | ----------------------------- | -------------- | ------- | --------- |
| A01 | Product Boundary and Overlay  | Infrastructure | HIGH    | —         |
| A02 | About Registration            | REUSE          | LOW     | A01       |
| A03 | Mandate Registration          | REUSE          | LOW     | A01       |
| A04 | Strategy Registration         | REUSE          | LOW     | A01       |
| A05 | Executive Leader Profile      | NEW            | MEDIUM  | A01       |
| A06 | Shared Organization Structure | NEW shared     | HIGH    | A01       |
| A07 | Contact Registration          | REUSE          | LOW     | A01       |
| A08 | FAQ Registration              | REUSE          | LOW     | A07       |
| A09 | Shared Search Results         | NEW shared     | HIGH    | A01       |
| A10 | Authority Search Adapter      | Integration    | MEDIUM  | A09       |
| A11 | Service Records               | Data           | LOW     | A01       |
| A12 | Services Catalogue            | REUSE          | LOW     | A11       |
| A13 | Service Details               | REUSE          | LOW     | A11–A12   |
| A14 | Shared Editorial Contract     | Shared data    | MEDIUM  | A01       |
| A15 | News Details                  | ADAPT shared   | MEDIUM  | A14       |
| A16 | News Listing                  | NEW shared     | MEDIUM  | A15       |
| A17 | Shared Portfolio Contract     | Shared data    | MEDIUM  | A01       |
| A18 | Portfolio Details             | ADAPT shared   | MEDIUM  | A17       |
| A19 | Portfolio Listing             | NEW shared     | MEDIUM  | A18       |
| A20 | Shared Resource Contract      | Shared data    | MEDIUM  | A01       |
| A21 | Knowledge Resource Details    | ADAPT shared   | MEDIUM  | A20       |
| A22 | Knowledge Library             | NEW shared     | HIGH    | A21       |
| A23 | Regulatory Record Contract    | Authority data | HIGH    | A01       |
| A24 | Regulatory Document Details   | NEW            | HIGH    | A23       |
| A25 | Regulations Library           | NEW            | HIGH    | A24       |
| A26 | Authority Home Composition    | ADAPT          | HIGH    | A12–A25   |
| A27 | Product Integration           | Integration    | MEDIUM  | A02–A26   |
| A28 | Final QA and Packaging        | Validation     | HIGH    | A27       |

الحزم الموصى بها 20–29 من المخطط (الاستشارات والمشاريع والاستثمار وغيرها)
تبدأ بعد اكتمال A28 ولا تدخل بوابة V1 الأساسية.

## 3. حزم البنية والصفحات المؤسسية

### A01 — Product Boundary and Overlay

- **الهدف:** إنشاء `products/authority/` كمنتج قابل للبناء بهوية ومحتوى
  مملوكين له دون نسخ `site/government.json` أو استيراد منتج الوزارة.
- **النطاق:** manifest، navigation/footer/page registries، demo content/assets
  roots، وآلية overlay متحققة لأصغر حقول الهوية والرئيسية والخدمات اللازمة.
- **الملفات المتوقعة:** `products/authority/product.json`؛ `navigation.json`؛
  `footer.json`؛ `pages/index.json`؛ سجلات محتوى أولية؛ تعديل صغير في
  `scripts/build_site.py` واختبارات product boundary.
- **إعادة الاستخدام:** product loader والغلاف الحكومي وFoundation paths.
- **غير مطلوب:** نقل Foundation، renderer خاص، Home جديدة، أو generic CMS.
- **التحقق:** منع path escape والحقول التنفيذية؛ build للـlegacy والوزارة
  والهيئة؛ هوية Authority تظهر في الناتج؛ لا أصل من `products/ministry/`.
- **معيار الخروج:** `python3 scripts/build_site.py --product authority` يبني
  baseline مستقلًا في output مؤقت وهوية demo مصدرها المنتج.

### A02 — About Registration

- **الهدف:** تسجيل `about.html` عبر Heavy Content المشترك.
- **الملفات:** page definition و`content/demo/about.json` واختبارات مركزة.
- **إعادة الاستخدام:** Page Intro، Breadcrumb، Heavy Content، TOC، List، Link،
  Feedback.
- **غير مطلوب:** قالب أو CSS خاصان.
- **التحقق:** H1 واحد، نص خيالي، روابط الأجزاء، route مسجل، RTL.
- **معيار الخروج:** الصفحة تبنى دون ملف داخل `templates/` الخاص بالمنتج.

### A03 — Mandate Registration

- **الهدف:** تسجيل `mandate.html` بمصدر التكليف والاختصاصات التجريبية.
- **الملفات:** definition وcontent واختبار metadata/links.
- **إعادة الاستخدام:** Heavy Content، List، Link، Feedback.
- **غير مطلوب:** Regulatory Detail؛ هذه الصفحة تصف اختصاص الجهة نفسها.
- **التحقق:** مصدر وحالة demo ظاهران، والأرقام معزولة الاتجاه، والتنزيل اختياري.
- **معيار الخروج:** كل مسؤولية قابلة للقراءة دون ملف أو صورة.

### A04 — Strategy Registration

- **الهدف:** تسجيل `strategy.html` بمحاور 2027–2030 وعلاقاتها.
- **الملفات:** definition وcontent واختبار عقود Heavy Content.
- **إعادة الاستخدام:** Page Intro، TOC، List، Card/Link عند الحاجة.
- **غير مطلوب:** KPI component أو timeline جديد.
- **التحقق:** العلاقات تشير إلى IDs موجودة عند تفعيلها؛ لا مؤشرات دعائية.
- **معيار الخروج:** الرؤية والرسالة والأهداف والممكنات مكتملة ومتجاوبة.

### A05 — Executive Leader Profile

- **الهدف:** تنفيذ صفحة مسؤول تنفيذي خاصة بالهيئة دون استيراد Minister Profile.
- **الملفات:** `products/authority/templates/executive-profile/`؛ content؛ asset
  خيالي وSOURCES؛ definition؛ registry/tests.
- **إعادة الاستخدام:** Page Intro، Breadcrumb، Avatar، List، Link، Feedback.
- **غير مطلوب:** مكوّن Profile عالمي، شبكة قيادات، روابط اجتماعية افتراضية.
- **التحقق:** role label من allow-list أو نص متحقق؛ portrait/alt pair؛ منع حقول
  الادعاء الرسمي؛ responsive وRTL.
- **معيار الخروج:** `leadership.html` يبنى بقالب Authority scoped فقط.

### A06 — Shared Organization Structure

- **الهدف:** إنشاء عقد شجرة دلالي يصلح للوزارة والهيئة، مع دمج consumer واحد
  على الأقل واختبار consumer الآخر قبل اعتباره مشتركًا.
- **الملفات:** قدرة تحت `templates/` أو `sections/` بحسب التركيب؛ validator؛
  contract؛ registry؛ Authority data/definition؛ اختبارات مشتركة ومنتجية.
- **إعادة الاستخدام:** Page Intro، Breadcrumb، List، Card، Link، Button، Feedback.
- **غير مطلوب:** محرر شجرة، drag/drop، canvas، أو صورة فقط.
- **التحقق:** duplicate/cycle/orphan/multiple-root policies؛ DOM نصي كامل؛
  nesting على 320px؛ no-JS.
- **معيار الخروج:** `organization.html` يشرح الهيكل كاملًا نصيًا ويستخدم قدرة
  لا تعتمد على اسم القطاع.

## 4. حزم التفاعل والبحث

### A07 — Contact Registration

- **الهدف:** تسجيل Contact بالقنوات التجريبية وفئات الاستفسار.
- **الملفات:** definition و`content/demo/contact.json` واختبار المنتج.
- **إعادة الاستخدام:** Contact الحالي وكل field components.
- **غير مطلوب:** إرسال أو تخزين أو خريطة حقيقية.
- **التحقق:** labels/errors/privacy، بريد `.invalid`، رقم موصوف بأنه عرض.
- **معيار الخروج:** `contact.html` يعمل عبر renderer المشترك.

### A08 — FAQ Registration

- **الهدف:** تسجيل FAQ وعلاقاتها بـContact والخدمات.
- **الملفات:** definition/content/index واختبار IDs/CTA.
- **إعادة الاستخدام:** FAQ، Accordion، Contact CTA، Feedback.
- **غير مطلوب:** بحث أو تصنيفات FAQ.
- **التحقق:** unique IDs، keyboard، no-JS، CTA target.
- **معيار الخروج:** الأسئلة الستة التجريبية تبنى دون fork.

### A09 — Shared Search Results

- **الهدف:** تنفيذ UI وعقد بحث موقع محايد للقطاع.
- **الملفات:** `sections/search-results/` أو shared template؛ validator/renderer؛
  contract؛ registry؛ focused tests.
- **إعادة الاستخدام:** Page Intro، Label، Text Input، Select، Button، Link، Tag،
  List، Pagination، Feedback.
- **غير مطلوب:** crawler، ranking، stemming، analytics، أو تعديل service search.
- **التحقق:** escaping؛ safe routes؛ empty/results states؛ GET semantics؛
  `noindex` contract؛ keyboard إن وجد JS.
- **معيار الخروج:** القدرة تعرض records عامة ولا تعرف مخطط Authority.

### A10 — Authority Search Adapter

- **الهدف:** اشتقاق فهرس ثابت من السجلات المسجلة وربط Header بـ`search.html`.
- **الملفات:** page definition؛ adapter تحت product templates؛ tests.
- **إعادة الاستخدام:** A09 وNavigation Header.
- **غير مطلوب:** ملف index يدوي مكرر أو محرك إنتاج.
- **التحقق:** كل عائلة مطلوبة قابلة للانضمام؛ الحقول الخاصة غير مفهرسة؛
  type/query filters؛ empty state؛ route آمن.
- **معيار الخروج:** البحث يعمل على المحتوى الحالي ويقبل العائلات اللاحقة دون
  تعديل renderer.

## 5. حزم الخدمات

### A11 — Service Records

- **الهدف:** تحويل S01–S05 إلى collection واحد بعقد الخدمات الحالي.
- **الملفات:** `content/demo/services.json` وسجل/اختبارات البيانات.
- **إعادة الاستخدام:** `validate_services` وservice relationship rules.
- **غير مطلوب:** حقول خدمة جديدة أو معاملات.
- **التحقق:** unique slugs، audiences/categories، steps/requirements، safe
  preview destinations، valid relations.
- **معيار الخروج:** collection يمر بعقد Foundation دون تنازلات.

### A12 — Services Catalogue

- **الهدف:** تسجيل `services.html` من A11.
- **الملفات:** page definition/index واختبار build/filter.
- **إعادة الاستخدام:** Service Catalogue وService Card.
- **غير مطلوب:** category routes أو template fork.
- **التحقق:** count/filter/empty state وكل بطاقة لصفحة مولدة.
- **معيار الخروج:** الكتالوج مصدره A11 وحده.

### A13 — Service Details

- **الهدف:** توليد صفحة لكل خدمة وربط التنظيم/الدليل/FAQ.
- **الملفات:** collection registration/adapter واختبارات routes/relations.
- **إعادة الاستخدام:** Service Detail الكامل.
- **غير مطلوب:** تسجيل دخول أو backend أو تغيير Tabs.
- **التحقق:** route collision؛ Breadcrumb؛ CTA preview؛ relations؛ H1 واحد.
- **معيار الخروج:** S01–S05 تملك routes ثابتة والكتالوج لا يرتبط بغيرها.

## 6. حزم التحرير

### A14 — Shared Editorial Contract

- **الهدف:** عقد News record واحد صالح للوزارة والهيئة.
- **الملفات:** shared contract/validator؛ `content/demo/news.json`؛ tests.
- **إعادة الاستخدام:** slug/date/safe-link/block conventions.
- **غير مطلوب:** renderer أو Announcements أو media expansion.
- **التحقق:** unique IDs/routes، ISO dates، image-alt pairing، safe blocks.
- **معيار الخروج:** السجل الواحد يخدم list/detail دون نسخ.

### A15 — News Details

- **الهدف:** shared Editorial Detail مبني حول Heavy Content.
- **الملفات:** shared template/renderer/CSS scoped؛ Authority definitions/tests.
- **إعادة الاستخدام:** shell، Page Intro، Breadcrumb، Heavy Content، Tag، Feedback.
- **غير مطلوب:** share widgets أو video gallery.
- **التحقق:** `<article>`، `<time>`، canonical، optional omissions، RTL/mobile.
- **معيار الخروج:** كل خبر demo يولد صفحة ثابتة.

### A16 — News Listing

- **الهدف:** shared Editorial Listing وربط `news.html`.
- **الملفات:** shared listing template/renderer/CSS؛ Authority definition/tests.
- **إعادة الاستخدام:** Card، Link، Tag، Pagination.
- **غير مطلوب:** قسم Home جديد؛ A26 يستهلك نفس السجلات.
- **التحقق:** chronological order، empty state، routes، alt، 320/768/1280.
- **معيار الخروج:** القائمة والتفاصيل تستخدم collection A14 وحده.

## 7. حزم البرامج والمبادرات

### A17 — Shared Portfolio Contract

- **الهدف:** عقد kind/status/relations للبرامج والمبادرات.
- **الملفات:** shared contract/validator؛ `content/demo/portfolio.json`؛ tests.
- **إعادة الاستخدام:** ID/date/safe relation utilities.
- **غير مطلوب:** Project-specific fields أو progress calculations.
- **التحقق:** controlled kind/status، valid dates، no cycles، verified metrics shape.
- **معيار الخروج:** P01–P04 صالحان للقائمة والتفاصيل.

### A18 — Portfolio Details

- **الهدف:** shared detail للأهداف والمخرجات والعلاقات.
- **الملفات:** shared template/renderer/CSS؛ definitions/tests.
- **إعادة الاستخدام:** Page Intro، Heavy Content، Card، Tag، List، Feedback.
- **غير مطلوب:** dashboard أو live progress.
- **التحقق:** status text، relationship targets، metric source/date، no empty wrappers.
- **معيار الخروج:** صفحة لكل سجل P01–P04.

### A19 — Portfolio Listing

- **الهدف:** shared list لـkind/status دون قالبين.
- **الملفات:** shared listing template/renderer؛ `programs.html` definition/tests.
- **إعادة الاستخدام:** Card، Tag، Select، Pagination.
- **غير مطلوب:** routes منفصلة لكل kind.
- **التحقق:** filter/sort/empty state، route coverage، RTL keyboard إذا وجد JS.
- **معيار الخروج:** قائمة واحدة تخدم برامج ومبادرات Authority.

## 8. حزم المعرفة والموارد

### A20 — Shared Resource Contract

- **الهدف:** عقد للأدلة والتقارير والقوالب والبيانات مع تنزيل آمن.
- **الملفات:** shared contract/validator؛ `content/demo/resources.json`؛ tests.
- **إعادة الاستخدام:** safe URL/path utilities وHeavy Content blocks.
- **غير مطلوب:** regulatory status أو document number.
- **التحقق:** format/size/language، cover-alt pairing، local/HTTPS destination،
  unique routes.
- **معيار الخروج:** R01–R05 يمرون بعقد واحد.

### A21 — Knowledge Resource Details

- **الهدف:** shared Resource Detail وDownload Item الصغير إن ثبتت حاجته.
- **الملفات:** shared template/renderer/CSS/component contract عند الحاجة؛ tests.
- **إعادة الاستخدام:** Page Intro، Heavy Content، Link/Button، Feedback.
- **غير مطلوب:** PDF viewer أو preview generator.
- **التحقق:** اسم التنزيل/الصيغة/الحجم، safe destination، canonical، mobile.
- **معيار الخروج:** صفحة لكل مورد وسلوك آمن دون JS.

### A22 — Knowledge Library

- **الهدف:** shared searchable Resource Library وربط `knowledge.html`.
- **الملفات:** shared template/renderer/CSS؛ definition/tests؛ registry.
- **إعادة الاستخدام:** Text Input، Select، List/Card، Tag، Pagination.
- **غير مطلوب:** faceted-search framework أو Regulatory records.
- **التحقق:** filters، order، empty state، metadata wrapping، routes.
- **معيار الخروج:** المكتبة تستهلك A20 فقط، ولا تنسخ summary في ملف آخر.

## 9. حزم التنظيمات الخاصة بالهيئة

### A23 — Regulatory Record Contract

- **الهدف:** عقد صارم لـG01–G03 وحالة النسخ والاستبدال.
- **الملفات:** `products/authority/templates/regulatory/` contract/validator؛
  `content/demo/regulations.json`؛ tests.
- **إعادة الاستخدام:** generic validation utilities فقط.
- **غير مطلوب:** دمج Resource contract أو ادعاء قانوني.
- **التحقق:** types/status allow-lists، number/version/date، file safety،
  supersedes graph، mandatory demo disclaimer.
- **معيار الخروج:** السجلات تميز المسودة والساري في المعاينة والملغى نصيًا.

### A24 — Regulatory Document Details

- **الهدف:** صفحة دلالية لكل وثيقة مع alert وmetadata وعلاقات النسخ.
- **الملفات:** product template/renderer/CSS؛ definitions/tests.
- **إعادة الاستخدام:** Page Intro، Inline Alert، Heavy Content، Link/Button،
  Feedback، Metadata List إن أُهل.
- **غير مطلوب:** legal structured data أو viewer.
- **التحقق:** status alert، `bdi` للأرقام، download label، previous/next links،
  no-JS/mobile/RTL.
- **معيار الخروج:** G01–G03 تملك صفحات، ولا يمكن إخفاء حالة demo.

### A25 — Regulations Library

- **الهدف:** كتالوج التنظيمات المستقل وربط `regulations.html`.
- **الملفات:** product listing template/renderer/CSS؛ definition/tests.
- **إعادة الاستخدام:** Page Intro، Text Input، Select، Tag، List/Card، Alert،
  Pagination.
- **غير مطلوب:** generic library switch أو Public Consultations.
- **التحقق:** type/status/topic filters، adoption sort، obsolete visibility،
  routes وempty state.
- **معيار الخروج:** المكتبة تعتمد A23 فقط وتربط A24.

## 10. Home والتكامل

### A26 — Authority Home Composition

- **الهدف:** تركيب Home من السجلات المنشورة، مع profile policy موثقة.
- **الملفات:** product home configuration/mapper؛ scoped composition CSS/JS عند
  الضرورة؛ asset sources؛ tests.
- **إعادة الاستخدام:** shared shell، Hero، Service Card، Editorial/Portfolio/
  Resource/Regulatory cards أو renderers الجزئية، About، Contact CTA، Feedback.
- **غير مطلوب:** slider تلقائي، أرقام إنجاز، أو قالب Home لكل profile.
- **التحقق:** section order لكل profile؛ no duplicate records/IDs؛ كل CTA route؛
  one H1؛ no-JS؛ reduced motion؛ 320/768/1280 RTL/LTR.
- **معيار الخروج:** Regulatory profile كامل، واختبار composition لكل من
  Enablement وDevelopment دون fork.

### A27 — Product Integration

- **الهدف:** توصيل navigation/footer/search/relations وكل required routes.
- **الملفات:** product registries وnavigation/footer؛ integration tests؛ README.
- **إعادة الاستخدام:** current navigation/footer renderers.
- **غير مطلوب:** صفحات موصى بها أو optional، أو إعادة تصميم التنقل العام.
- **التحقق:** link graph بلا broken routes؛ active states؛ breadcrumbs؛ source
  ownership؛ output لا يحتوي private assets لمنتج آخر.
- **معيار الخروج:** الموقع يتصرف كمنتج واحد وليس صفحات منفصلة.

### A28 — Final QA and Packaging

- **الهدف:** فحص واسع مرة واحدة بعد التكامل.
- **النطاق:** unit/build/audit/browser؛ RTL/LTR؛ mobile/tablet/desktop؛ keyboard؛
  no-JS؛ reduced motion؛ content consistency؛ package contents.
- **الملفات:** نتائج QA ووثائق المنتج/registry فقط إذا لزم؛ لا refactor.
- **غير مطلوب:** إصلاحات خارج نطاق findings المرتبطة بالمنتج.
- **التحقق:** كل معايير الإكمال في `authority-blueprint.md`؛ legacy والوزارة؛
  asset/path/link audits؛ disclaimer demo.
- **معيار الخروج:** كل REQUIRED V1 ناجح، والقضايا المتبقية موثقة أو صفر.

## 11. خطة الحزم الموصى بها بعد V1

| الترتيب | القدرة                           | تعتمد على           | اتجاه التنفيذ                                  |
| ------: | -------------------------------- | ------------------- | ---------------------------------------------- |
|       1 | Public Consultations list/detail | A23–A25             | Authority-specific، مرتبط بالوثيقة             |
|       2 | Areas of Work directory          | A10/A12/A19/A22/A25 | علاقات تجمع المحتوى                            |
|       3 | Leadership Directory             | A05                 | Directory مشترك primitives، بيانات Authority   |
|       4 | Projects list/detail             | A17–A19             | عقد Project مستقل عن Program عند اختلاف الحقول |
|       5 | Investment Opportunities         | Projects + Contact  | Authority development module                   |
|       6 | Open Data / Indicators           | A20–A22             | موارد بمالك/مصدر/تاريخ صارم                    |
|       7 | Procurement Landing              | A20                 | روابط خارجية موثقة، لا نظام مشتريات            |

## 12. ميزانية التحقق أثناء التطوير

- كل حزمة: unit tests للعقد + build للصفحة أو العائلة المتغيرة.
- تغيير Foundation مشترك: اختبار consumer الحالي والوزارة والهيئة.
- صفحة تفاعلية: browser test للحالات المتأثرة فقط.
- shared renderer جديد: RTL/LTR و320/1280 على نموذجين مختلفين.
- لا full browser suite بعد كل حزمة؛ يشغّل مرة في A28.

أوامر متوقعة بحسب ما يتاح في مرحلة التنفيذ:

```sh
python3 -B -m unittest tests.test_authority_<package> -q
python3 scripts/build_site.py --product authority --output /tmp/authority-build
python3 scripts/audit.py --strict
```

## 13. بوابة اكتمال V1

- A01–A28 مكتملة بالترتيب أو بتبعيات مكافئة موثقة.
- الصفحات المطلوبة التسع عشرة ومحتوى demo مترابطان.
- لا قوالب أو CSS أو JS مكررة من Foundation أو Ministry.
- shared capabilities الجديدة مسجلة في `docs/component-registry.md`.
- الروابط والعلاقات والأصول آمنة وموجودة.
- RTL/LTR وresponsive وkeyboard وno-JS ناجحة وفق المخاطر.
- البيانات التنظيمية والخدمية تحمل حدود المعاينة بوضوح.
- build المنتج مستقل، وlegacy ومنتج الوزارة لم يتراجعا.
