# موقع هيئة V1 — خريطة الموجود والجديد

الحالة: تدقيق ما قبل التنفيذ للأنواع المطلوبة التسعة عشر. يعتمد على
`docs/component-registry.md` وعلى عقود المنتج في `authority-blueprint.md`.

## 1. خلاصة القرار

لا يحتاج تصنيف «هيئة» إلى Header أو Footer أو Breadcrumb أو Page Intro أو
نظام خدمات جديد. سبعة أنواع صفحات تُنجز بالتهيئة وإعادة الاستخدام، وأربعة
تحتاج تركيبًا فوق قدرات قائمة، وثمانية تحتاج قدرات صفحة جديدة.

ظهور المنتج الثاني يثبت تداخلًا حقيقيًا مع خطة الوزارة في البحث، والتحرير،
والبرامج/المبادرات، والموارد، والهيكل التنظيمي. لذلك تُبنى هذه العقود كقدرات
مشتركة صغيرة بدل نسخها داخل كل منتج. أما الملف التنفيذي والتنظيمات الرسمية
فتبقى خاصة بمنتج الهيئة لاختلاف معناها وعقدها.

## 2. ملخص التصنيف

| التصنيف | العدد | الأنواع |
|---|---:|---|
| REUSE | 7 | About، Mandate، Strategy، Contact، FAQ، Services Catalogue، Service Detail |
| ADAPT | 4 | Home، News Detail، Program/Initiative Detail، Knowledge Resource Detail |
| NEW | 8 | Executive Leader، Organization Structure، Search Results، News Listing، Portfolio Listing، Knowledge Library، Regulations Library، Regulatory Detail |

`ADAPT` يعني تركيب صفحة أو mapper جديدًا مع الاحتفاظ بالمكوّنات وعقود المحتوى
القائمة. لا يعني نسخ CSS أو HTML.

## 3. جدول الأنواع المطلوبة

| النوع | القرار | الموجود القابل لإعادة الاستخدام | العمل المتبقي | المالك المقترح |
|---|---|---|---|---|
| Home | ADAPT | `templates/government/page.html`، Hero، About، Home Services، News، Feedback | ترتيب profile-driven وربط سجلات Authority | Authority composition/data |
| About Authority | REUSE | Page Intro + Heavy Content + TOC/List/Link | بيانات وتسجيل route | Authority config |
| Mandate & Legal Basis | REUSE | Heavy Content + List/Link/Card | mapper metadata بسيط إن احتاج | Shared content + Authority data |
| Strategy | REUSE | Heavy Content + Page Intro | بيانات وعلاقات؛ KPI مؤجل | Shared content + Authority data |
| Executive Leader | NEW | Avatar، Page Intro، List، Link | عقد وقالب profile غير وزاري | Authority |
| Organizational Structure | NEW | Page Intro، List، Card، Link | عقد شجرة متحقق وrenderer دلالي | Shared candidate |
| Contact | REUSE | Contact template وكل حقوله | بيانات القنوات فقط | Authority config |
| FAQ | REUSE | FAQ + Accordion + Contact CTA | الأسئلة والعلاقات | Authority config |
| Search Results | NEW | Text Input، Select، Link، Tag، Pagination | UI/contract عام + index adapter | Shared + Authority adapter |
| News Listing | NEW | Card، Tag، Link، Pagination؛ News home section جزئي | Editorial listing مؤهل | Shared candidate |
| News Detail | ADAPT | Heavy Content، Page Intro، Tag، Feedback | article mapper وmetadata | Shared candidate |
| Services Catalogue | REUSE | Service Catalogue + Service Card | بيانات وتصنيفات Authority | Authority data |
| Service Detail | REUSE | Service Detail + Tabs/List/Button/Rating | علاقات تنظيم/دليل | Shared renderer + Authority data |
| Programs/Initiatives Listing | NEW | Card، Tag، Select، Pagination | Portfolio listing | Shared candidate |
| Program/Initiative Detail | ADAPT | Heavy Content، Card، Tag، List | Portfolio detail/relations | Shared candidate |
| Knowledge Library | NEW | Text Input، Select، Card/List، Pagination | Resource library | Shared candidate |
| Knowledge Resource Detail | ADAPT | Heavy Content، Button/Link، Card | metadata + safe download item | Shared candidate |
| Regulations Library | NEW | search/filter/list primitives، Inline Alert | عقد Regulatory مستقل | Authority |
| Regulatory Document Detail | NEW | Page Intro، Heavy Content، Alert، Button/Link | version/status/relations validator | Authority |

## 4. إعادة الاستخدام المباشر

### الغلاف والتخطيط

- `templates/government/page.html`: shell مشترك مؤقتًا وفق قرار المعمارية.
- `partials/site-header/template.html`: Navigation Header دون fork.
- `partials/site-footer/template.html`: Footer من بيانات المنتج.
- `styles/base/layout.css`: Container وStack وbreakpoints الحالية.
- `token.css`: جميع القيم التصميمية الأساسية.

### مقدمات الصفحات والمحتوى

- `sections/page-intro/` و`scripts/page_intro_markup.py` لكل صفحة داخلية.
- `components/breadcrumb/` و`scripts/breadcrumb_markup.py` للمسار متغير العمق.
- `sections/heavy-content/` و`scripts/content_markup.py` لصفحات About وMandate
  وStrategy ولكتل التفاصيل الطويلة.
- `components/table-of-contents/` و`components/list/` و`components/divider/`.

### الخدمات والتفاعل

- `sections/service-catalog/` و`components/service-card/` لكتالوج الخدمات.
- `sections/service-overview/` و`templates/service/` لتفاصيل الخدمة.
- `sections/contact/` و`templates/contact/` للتواصل.
- `sections/faq/` و`components/accordion-new/` للأسئلة.
- `sections/feedback/` ومكوّنات التقييم لنهايات الصفحات.

لا تُنسخ هذه المسارات تحت `products/authority/`.

## 5. الامتدادات الآمنة المطلوبة

### 5.1 سجل Renderer متعدد المنتجات

السجل الحالي في `scripts/build_site.py` يعرّف renderer خاصًا بالوزارة داخل
ثابت Python. ظهور Authority يبرر تحويل التسجيل إلى بنية لا تشترط تعديل شرط
مركزي لكل صفحة، مع بقاء IDs allow-listed وعدم السماح لبيانات JSON بتحديد مسار
تنفيذي.

الامتداد المقبول:

- manifest أو registry موثوق يحمّله builder من مسار product templates.
- تحقق أن module/styles داخل مجلد المنتج.
- دعم قدرات مشتركة مسجلة مركزيًا بوضوح.
- بقاء legacy و`--product ministry` متوافقين.

### 5.2 هوية ومحتوى المنتج

`source_config` الانتقالي يحمل هوية ومحتوى الموقع العام. المنتج الثاني يحتاج
آلية product-owned لتجاوز الهوية والصفحة الرئيسية والخدمات دون نسخ ملف
`site/government.json` كاملًا. تُعرّف حزمة A01 أصغر overlay متحقق، مع منع حقول
التنفيذ العشوائية.

### 5.3 العلاقات بين السجلات

تضاف utility تحقق عامة لـIDs والعلاقات والدورات عند الحاجة، بدل أن يعيد كل
renderer التحقق من route والـID. لا تنشأ قاعدة بيانات أو CMS schema.

## 6. قدرات مشتركة ثبتت بالمنتج الثاني

### Search Results

الوزارة والهيئة تحتاجان بحث موقع كامل عبر أنواع محتوى متعددة. الواجهة والعقد
مشتركان، بينما استخراج الفهرس وتسميات الأنواع تخص كل منتج.

**المشترك:** form، filters، result item، empty state، pagination contract.  
**الخاص:** index adapter، الحقول المفهرسة، أنواع النتائج ومسار Header.

### Editorial Listing / Detail

News في المنتجين يملك المعنى نفسه: سجل مؤرخ، قائمة وتفاصيل article. ينبغي
تأهيل قدرة مشتركة بدل بقاء `sections/news/` قسم Home خاصًا أو إنشاء نسختين.

**المشترك:** record contract، list/detail renderers، metadata، related items.  
**الخاص:** النصوص، الترتيب المميز، تصنيفات كل منتج.

### Portfolio Listing / Detail

Programs وInitiatives لها عقد متطابق تقريبًا بين الوزارة والهيئة. kind
والstatus حقول بيانات؛ ليست أسماء قوالب.

### Resource Library / Detail

أدلة وتقارير وسياسات عامة وملفات تنزيل مطلوبة في المنتجين. Library وDetail
وDownload Item قابلة للمشاركة. **Regulatory Document** لا يدخل في هذا العقد
لأنه يضيف حالة نفاذ ورقم اعتماد وتسلسل نسخ.

### Organization Structure

الوزارة والهيئة تحتاجان شجرة وحدات بالمتطلبات نفسها: IDs، parent relation،
منع cycle/orphan، وتمثيل نصي متاح. تسمية العقد sector-neutral؛ بيانات الوحدات
تبقى للمنتج.

## 7. قدرات تبقى خاصة بالهيئة

### Executive Leader Profile

ملف الوزير يعبر عن منصب دستوري/قطاعي محدد. ملف الهيئة يحتاج تسمية دور قابلة
للتهيئة وحقولًا أقل افتراضًا. تشابه الصورة والسيرة لا يكفي لاستيراد
`products/ministry/templates/minister-profile/`.

### Regulations Library / Detail

عقد التنظيمات يملك نوعًا ورقمًا وحالة نفاذ وتاريخ اعتماد وإصدارًا وعلاقات
استبدال. تحويل Resource إلى مكوّن عالمي مليء بالحقول الاختيارية سيضعف العقدين.
تظل الصفحتان في Authority حتى يثبت منتج آخر نفس الدلالة التنظيمية.

### Profile-driven Home

ترتيب Regulatory/Enablement/Development خاص بسياسة المنتج. الأقسام المستخدمة
مشتركة، لكن composition وselection يبقيان داخل Authority.

## 8. مكوّنات مركبة مرشحة

لا تُنشأ قبل تدقيق المكوّنات الحالية في حزمها:

| المرشح | الغرض | المكوّنات الداخلة | قرار الملكية الأولي |
|---|---|---|---|
| Search Result Item | نتيجة موحدة مع نوع وملخص | Link + Tag + List/Card | Shared |
| Metadata List | أزواج label/value دلالية | List/description list | Shared |
| Download Item | اسم/صيغة/حجم/إجراء | Link/Button + metadata | Shared |
| Regulatory Result Item | وثيقة برقم وحالة | Link + Tag + Metadata List | Authority composite |
| Relationship Section | سجلات مرتبطة بعناوين وروابط | Card/Link | Shared section candidate |

إذا أمكن تكوين المرشح مباشرة بتركيب HTML داخل renderer دون عقد مستقل، لا
يُسجل كمكوّن جديد.

## 9. ترتيب الاعتماديات

```text
Product boundary + overlay seam
              ↓
Shared simple page registrations
              ↓
Shared record/relationship utilities
              ↓
Organization + Executive Leader
              ↓
Search
              ↓
Services
              ↓
Editorial
              ↓
Portfolio
              ↓
Resources
              ↓
Authority Regulations
              ↓
Home composition
              ↓
Integration + QA
```

صفحات التفاصيل تُبنى قبل القوائم، والقوائم قبل Home، حتى لا تُنشأ بطاقات
بروابط أو بيانات غير موجودة.

## 10. المخاطر والقرارات

| الخطر | القرار |
|---|---|
| تداخل العمل الجاري في Foundation | تعديلات additive صغيرة، وعدم لمس تغييرات غير مرتبطة. |
| نسخ قدرات الوزارة | ممنوع؛ تُستخرج القدرة المشتركة أو تُبنى Authority-specific. |
| تعميم Regulatory على كل Resource | ممنوع؛ عقدان منفصلان بprimitives مشتركة. |
| تضخم profile flags | التسجيل وترتيب الأقسام يكفيان؛ لا feature-flag engine. |
| بيانات demo تبدو رسمية | disclaimer وحالات «تجريبي/غير نافذ» والتحقق الآلي. |
| روابط منصات خارجية غير حقيقية | وجهات preview أو HTTPS معتمدة فقط. |
| مخطط هيكل صورة فقط | تمثيل نصي إلزامي، والصورة إضافة اختيارية. |
| بحث يوحي بمحرك إنتاجي | static adapter موثق؛ الإنتاج integration منفصل. |

## 11. قرار الجاهزية

المخطط جاهز للبناء المرحلي. لا توجد حاجة إلى مرجع إضافي لبدء A01. المرجع
البصري غير مطلوب في مرحلة تعريف التصنيف؛ أي صفحة جديدة تحتاج تصميمًا تفصيليًا
تطلب Figma node واحدًا عند بدء حزمة التنفيذ المتأثرة فقط.
