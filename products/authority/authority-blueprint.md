# مخطط منتج موقع هيئة — V1

الحالة: خط أساس معتمد للتخطيط، مستند إلى البحث المقارن في
`authority-reference-research.md`. يحدد نطاق المنتج وعقود الصفحات ولا ينشئ
قوالب أو إعدادات تنفيذية.

## 1. تعريف المنتج

**اسم المنتج:** Platforms Code — Authority Website  
**التصنيف:** Government / Authority  
**الاتجاه الافتراضي:** العربية وRTL، مع قابلية LTR دون مسار HTML مستقل  
**الناتج:** موقع معلومات وخدمات ثابت قابل للتكامل مع CMS ومحركات البحث
والخدمات الخارجية، وليس نظام معاملات أو بوابة تسجيل دخول.

يخدم المنتج ثلاثة ملفات تهيئة مثبتة بالمراجع:

| الملف | الأولوية في Home والتنقل | قدرات مشروطة |
|---|---|---|
| `regulatory` | الخدمات، التنظيمات، المعرفة | التراخيص، الاستشارات العامة، الأدلة القطاعية |
| `enablement` | الخدمات، البرامج، المعرفة | المنصات، الشراكات، الأدلة والمؤشرات |
| `development` | الاستراتيجية، المشاريع، الاستثمار | ملف المنطقة/القطاع، الخريطة، الفرص |

الملف يغيّر سجل الصفحات وترتيب الأقسام والبيانات فقط؛ لا يختار CSS أو مسار
قالب عشوائيًا.

## 2. حد إصدار V1

يحتوي الكتالوج على **37 نوع صفحة/محتوى**:

- 19 REQUIRED V1.
- 10 RECOMMENDED V1.
- 8 OPTIONAL / LATER.

يُعد V1 قابلًا للبيع عند تنفيذ الأنواع المطلوبة ببيانات خيالية آمنة، وبناء
موقع مترابط مستقل تحت `dist/products/authority/`، وعدم اعتماد المنتج على
قوالب خاصة بمنتج قطاعي آخر.

| الأولوية | المعنى |
|---|---|
| REQUIRED V1 | غيابها يجعل موقع الهيئة ناقصًا في التعريف أو الخدمة أو النشر. |
| RECOMMENDED V1 | مطلوبة لملف تشغيلي محدد، ولا تحجب إطلاق النواة المشتركة. |
| OPTIONAL / LATER | تُنفذ عندما توجد بيانات وحوكمة واحتياج تشغيلي حقيقي. |
| NOT REQUIRED | تُمثل كتصفية أو علاقة أو قسم، لا صفحة مستقلة. |

## 3. معمارية المعلومات

```text
الرئيسية
├── عن الهيئة
│   ├── نبذة عن الهيئة
│   ├── الاختصاص والأساس التنظيمي
│   ├── الاستراتيجية
│   ├── المسؤول التنفيذي
│   ├── الهيكل التنظيمي
│   ├── القيادات                         [موصى به]
│   └── مجالات عمل الهيئة                [موصى به]
├── الخدمات
│   ├── جميع الخدمات
│   └── تفاصيل الخدمة
├── التنظيمات
│   ├── مكتبة التنظيمات
│   ├── تفاصيل الوثيقة التنظيمية
│   └── الاستشارات العامة                [موصى به]
├── البرامج والمبادرات
│   ├── جميع البرامج والمبادرات
│   └── التفاصيل
├── المشاريع والاستثمار                  [موصى به / development]
│   ├── المشاريع
│   └── الفرص الاستثمارية
├── المعرفة
│   ├── مكتبة المعرفة
│   ├── تفاصيل المورد
│   └── البيانات المفتوحة والمؤشرات       [موصى به]
├── المركز الإعلامي
│   ├── الأخبار
│   ├── الإعلانات                         [اختياري]
│   └── الفعاليات                         [اختياري]
├── المشاركة والتواصل
│   ├── تواصل معنا
│   ├── الأسئلة الشائعة
│   └── المشاركة الإلكترونية              [موصى به]
└── نتائج البحث
```

لا يتجاوز التنقل الأساسي مستويين. تظهر صفحات التفاصيل من القوائم والروابط
ذات الصلة ولا تُحشر جميعها في القائمة الرئيسية.

## 4. جرد الصفحات والأولوية

| # | النوع | العائلة | الأولوية | المبرر |
|---:|---|---|---|---|
| 1 | Home | Core | REQUIRED V1 | بوابة المهام والمحتوى ذي الأولوية. |
| 2 | About Authority | Institutional | REQUIRED V1 | تعريف الهوية والغرض والمسؤوليات. |
| 3 | Mandate & Legal Basis | Institutional | REQUIRED V1 | يوضح الاختصاص والأساس التنظيمي دون دفنه في About. |
| 4 | Strategy | Institutional | REQUIRED V1 | الرؤية والرسالة والأهداف والممكنات. |
| 5 | Executive Leader Profile | Leadership | REQUIRED V1 | صفحة قابلة لتسمية المحافظ/الرئيس/الرئيس التنفيذي. |
| 6 | Organizational Structure | Institutional | REQUIRED V1 | عرض مسؤوليات الوحدات بهيكل نصي متاح. |
| 7 | Contact | Interaction | REQUIRED V1 | القنوات الرسمية والدعم والاستفسار. |
| 8 | FAQ | Interaction | REQUIRED V1 | إجابات قابلة للتصفح تقلل طلبات الدعم. |
| 9 | Search Results | Discovery | REQUIRED V1 | اكتشاف الموقع كاملًا عبر العائلات. |
| 10 | News Listing | Media | REQUIRED V1 | سجل زمني قابل للبحث. |
| 11 | News Detail | Media | REQUIRED V1 | خبر ثابت قابل للمشاركة والفهرسة. |
| 12 | Services Catalogue | Services | REQUIRED V1 | مدخل موحد للخدمات حسب الجمهور والمجال. |
| 13 | Service Detail | Services | REQUIRED V1 | شرح الخدمة وبدؤها وقنوات الدعم. |
| 14 | Programs / Initiatives Listing | Portfolio | REQUIRED V1 | عرض محفظة الهيئة دون تكرار القوالب. |
| 15 | Program / Initiative Detail | Portfolio | REQUIRED V1 | الهدف والحالة والمخرجات والعلاقات. |
| 16 | Knowledge Resources Library | Knowledge | REQUIRED V1 | أدلة وتقارير ودراسات ومواد توعوية. |
| 17 | Knowledge Resource Detail | Knowledge | REQUIRED V1 | سياق وبيانات وصفية وتنزيل آمن. |
| 18 | Regulations Library | Regulatory | REQUIRED V1 | مرجع مميز للسياسات واللوائح والقرارات. |
| 19 | Regulatory Document Detail | Regulatory | REQUIRED V1 | الرقم والحالة والاعتماد والإصدار والملف. |
| 20 | Leadership Directory | Leadership | RECOMMENDED V1 | عندما تنشر الهيئة قيادات متعددة. |
| 21 | Areas of Work / Sector Directory | Institutional | RECOMMENDED V1 | يربط مجالات الاختصاص بالمحتوى ذي الصلة. |
| 22 | Public Consultations Listing | Participation | RECOMMENDED V1 | أساسي للهيئة التنظيمية ذات المرئيات. |
| 23 | Consultation Detail | Participation | RECOMMENDED V1 | المدة والوثيقة وطريقة الإرسال والنتيجة. |
| 24 | Projects Listing | Development | RECOMMENDED V1 | أساسي لهيئات التطوير. |
| 25 | Project Detail | Development | RECOMMENDED V1 | الموقع والحالة والمراحل والإنجازات. |
| 26 | Investment Opportunities Listing | Development | RECOMMENDED V1 | يتيح اكتشاف الفرص حسب القطاع والموقع. |
| 27 | Investment Opportunity Detail | Development | RECOMMENDED V1 | المتطلبات والموعد والملفات ووجهة التقديم. |
| 28 | Open Data / Indicators | Knowledge | RECOMMENDED V1 | ينشر بيانات موثقة ذات مالك وتاريخ. |
| 29 | Procurement / Tenders Landing | Utility | RECOMMENDED V1 | رابط موحد للمنافسات والفرص الخارجية. |
| 30 | Events Listing | Media | OPTIONAL / LATER | عند وجود برنامج فعاليات مستمر. |
| 31 | Event Detail | Media | OPTIONAL / LATER | يضاف مع المواعيد والمكان أو التسجيل. |
| 32 | Announcements Listing | Media | OPTIONAL / LATER | للإشعارات المنتهية الصلاحية غير المناسبة للأخبار. |
| 33 | Announcement Detail | Media | OPTIONAL / LATER | يدعم الحالة وتاريخ الانتهاء. |
| 34 | Media Library | Media | OPTIONAL / LATER | يتطلب أصولًا وحقوق استخدام وحوكمة. |
| 35 | Partnerships Directory | Institutional | OPTIONAL / LATER | عندما توجد علاقات معتمدة قابلة للنشر. |
| 36 | Region / Sector Profile | Development | OPTIONAL / LATER | لهيئة تطوير أو تنظيم تحتاج ملف مكان/سوق. |
| 37 | Careers Landing | Utility | OPTIONAL / LATER | غالبًا رابط إلى جدارات أو منصة خارجية. |

ليست صفحات مستقلة في V1:

- تصنيف خدمة: تصفية محفوظة داخل كتالوج الخدمات.
- نوع وثيقة: تصفية داخل المكتبة المناسبة.
- مركز إعلامي عام: مجموعة تنقل، إلا إذا ظهر محتوى تجميعي حقيقي لاحقًا.
- إحصاءات الرئيسية: قسم اختياري ببيانات موثقة.
- الشركاء المرتبطون ببرنامج/مشروع: علاقة داخل السجل قبل إنشاء دليل مستقل.

## 5. قواعد مشتركة لكل الصفحات المطلوبة

- H1 واحد، وعناوين الأقسام تبدأ من H2 بترتيب دلالي.
- Page Intro هو منطقة العنوان الداخلية الافتراضية، مع Breadcrumb متغير العمق.
- كل تاريخ يعرض قيمة قابلة للقراءة و`datetime` معياريًا عند استخدام `<time>`.
- كل رابط خارجي أو تنزيل يوضح نوع الوجهة؛ لا يُخفى فتح منصة خارجية.
- تخطيط RTL يستخدم الخصائص المنطقية ويعمل في LTR دون نسخة Markup أخرى.
- الجداول والقوائم لا تفرض تمرير الصفحة أفقيًا؛ تستخدم غلاف overflow محليًا.
- الحالة الأساسية تعمل دون JavaScript؛ البحث والتصفية تحسين تدريجي.
- التركيز ظاهر، والأزرار أصلية، والأسماء والوصف البديل مطلوبان للصور المفيدة.
- العنوان الوصفي: `[عنوان الصفحة] | [اسم الهيئة]`، والوصف من ملخص السجل.
- canonical من route المعتمد؛ لا canonical لوجهة تنزيل خارجية بدل صفحة التفاصيل.
- تقييم الصفحة وتاريخ التحديث يظهران حيث ينطبق عقد Foundation.

## 6. مواصفات الصفحات المطلوبة

### 6.1 Home — الرئيسية

- **الهوية:** `index.html`؛ عائلة Core؛ العنوان المقترح «الهيئة الوطنية لتنمية
  المنظومات والخدمات» / “National Authority for Ecosystem and Service
  Development”.
- **الغرض:** توجيه الزائر إلى أهم مهمة أو معلومة بحسب ملف الهيئة.
- **نموذج المحتوى:** مطلوب: قيمة تعريفية، إجراء رئيسي، أقسام مرتبة، IDs
  للخدمات/البرامج/الأخبار المميزة. اختياري: بحث، إحصاءات موثقة، مورد مميز،
  تنبيه، شركاء.
- **البنية:** Hero ثم الأولويات الخاصة بالملف، نبذة قصيرة، أخبار، Contact CTA،
  Feedback. لا نسخة طويلة من About.
- **العرض:** أقسام قابلة لإعادة الاستخدام وبطاقات من السجلات الأصلية.
- **السلوك:** بحث أو مرشح خدمات إن فُعّل؛ المسارات الأفقية يدوية ولا تدور آليًا.
- **الجوال:** إجراء واحد أساسي ظاهر، الشبكات عمود واحد، لا قص للمحتوى المهم.
- **RTL:** ترتيب DOM دلالي ثابت، واتجاه الحركة يراعي `dir`.
- **الوصول:** Hero يملك H1 الوحيد؛ لا نص داخل صورة؛ احترام reduced motion.
- **SEO:** وصف المنتج من البيان التعريفي؛ Organization structured data فقط بعد
  تكامل بيانات جهة حقيقية.
- **المكوّنات:** Government Shell، Header، Footer، Hero، Card، Service Card،
  Button، Link، أقسام News/About/Feedback.
- **الملكية:** تركيب Authority وبياناته؛ المكوّنات Foundation.

### 6.2 About Authority — عن الهيئة

- **الهوية:** `about.html`؛ Institutional؛ «عن الهيئة» / “About the Authority”.
- **الغرض:** شرح النشأة والغرض والدور والمسؤوليات بوضوح.
- **نموذج المحتوى:** مطلوب: title، summary، establishment context، mandate
  summary، responsibilities، updated. اختياري: values، history، image، links.
- **البنية:** Page Intro، نبذة، المسؤوليات، القيم أو المبادئ، روابط إلى
  الاختصاص والاستراتيجية.
- **العرض:** Heavy Content بفهرس عند تعدد الأقسام؛ قوائم لا بطاقات زخرفية.
- **السلوك:** روابط أجزاء الصفحة تعمل دون JS.
- **الجوال:** الفهرس أعلى المحتوى؛ الوسائط ضمن العرض.
- **RTL:** محاذاة start وترتيب القوائم منطقي.
- **الوصول:** القوائم دلالية والصور المفيدة لها alt.
- **SEO:** الوصف من summary؛ لا تكرار نص Mandate الكامل.
- **المكوّنات:** Page Intro، Breadcrumb، Heavy Content، TOC، List، Link،
  Feedback.
- **الملكية:** تهيئة المنتج؛ renderer مشترك.

### 6.3 Mandate & Legal Basis — الاختصاص والأساس التنظيمي

- **الهوية:** `mandate.html`؛ Institutional؛ «اختصاص الهيئة وأساسها التنظيمي» /
  “Mandate and Legal Basis”.
- **الغرض:** بيان ما تنظمه أو تطوره الهيئة وحدود مسؤوليتها ومصدر التكليف.
- **نموذج المحتوى:** مطلوب: basis title/type/date/source URL، mandate، ordered
  responsibilities، updated. اختياري: amendments، jurisdictions، downloads.
- **البنية:** Page Intro، ملخص، الأساس، المسؤوليات، النطاق، وثائق مرتبطة.
- **العرض:** Content Detail؛ البيانات المرجعية كـmetadata list، لا مخطط صورة.
- **السلوك:** نسخ رابط القسم اختياري؛ الملفات تفتح بوسم نوعها.
- **الجوال:** metadata يتكدس عموديًا.
- **RTL:** الأرقام والرموز القانونية تعزل اتجاهيًا عند الحاجة.
- **الوصول:** مصدر رسمي مسمى بوضوح؛ لا تعتمد المعلومة على PDF وحده.
- **SEO:** canonical للصفحة؛ تحديث الوصف عند تغير الاختصاص.
- **المكوّنات:** Page Intro، Breadcrumb، Heavy Content، List، Link، Card،
  Feedback.
- **الملكية:** سجل Authority؛ renderer مشترك مع عقد metadata بسيط إن لزم.

### 6.4 Strategy — الاستراتيجية

- **الهوية:** `strategy.html`؛ Institutional؛ «استراتيجية الهيئة» / “Authority
  Strategy”.
- **الغرض:** ربط الرؤية والرسالة والأهداف والممكنات بالبرامج المنشورة.
- **نموذج المحتوى:** مطلوب: vision، mission، objectives، updated. اختياري:
  pillars، enablers، dated KPIs، strategy period، document، related IDs.
- **البنية:** Page Intro، الرؤية والرسالة، المحاور، الأهداف، الممكنات، العلاقات.
- **العرض:** Heavy Content وقوائم؛ KPI cards فقط بقيمة ومصدر وتاريخ.
- **السلوك:** روابط داخلية وعلاقات إلى البرامج.
- **الجوال:** بطاقات المؤشرات تتكدس؛ لا مخطط أفقي إلزامي.
- **RTL:** الأرقام والفترات قابلة للقراءة في الاتجاهين.
- **الوصول:** بديل نصي كامل لأي رسم استراتيجي.
- **SEO:** الوصف من الرؤية/الملخص؛ العنوان يذكر فترة الاستراتيجية إن كانت
  جزءًا رسميًا منها.
- **المكوّنات:** Page Intro، Heavy Content، TOC، List، Card، Link، Feedback.
- **الملكية:** تهيئة المنتج؛ مرشح لتركيب مشترك من المنتج الحالي.

### 6.5 Executive Leader Profile — المسؤول التنفيذي

- **الهوية:** `leadership.html`؛ Leadership؛ تسمية الدور من config: محافظ أو
  رئيس أو رئيس تنفيذي / Governor, President or CEO.
- **الغرض:** تقديم صاحب المسؤولية التنفيذية وسيرته ورسالة معتمدة عند توفرها.
- **نموذج المحتوى:** مطلوب: name، role label، portrait/alt، biography، updated.
  اختياري: message، appointment date، qualifications، experience، links.
- **البنية:** Page Intro، profile summary، biography، experience، message،
  related leadership.
- **العرض:** ملف شخصي تركيبي لا يكرر Minister Profile الخاص بمنتج الوزارة.
- **السلوك:** لا سلوك مطلوب؛ الروابط الخارجية الموثقة فقط.
- **الجوال:** الصورة قبل السيرة بصريًا وDOM منطقيًا.
- **RTL:** حقول الأسماء والألقاب تبدأ منطقيًا.
- **الوصول:** alt يصف هوية الشخص، ولا تُستخدم الصورة كعنوان.
- **SEO:** Person structured data مؤجل حتى بيانات حقيقية وموافقة نشر.
- **المكوّنات:** Page Intro، Breadcrumb، Avatar، List، Link، Feedback.
- **الملكية:** قالب Authority مستقل؛ لا يستورد Minister Profile.

### 6.6 Organizational Structure — الهيكل التنظيمي

- **الهوية:** `organization.html`؛ Institutional؛ «الهيكل التنظيمي» /
  “Organizational Structure”.
- **الغرض:** توضيح تسلسل المسؤوليات والوحدات وإتاحة تفاصيلها نصيًا.
- **نموذج المحتوى:** مطلوب: unique node IDs، labels، parent relationships،
  ordered roots، updated. اختياري: descriptions، contacts، chart/file.
- **البنية:** Page Intro، ملخص، hierarchy، تفاصيل الوحدة الاختيارية، تنزيل.
- **العرض:** شجرة نصية دلالية؛ الرسم اختياري وليس المصدر الوحيد.
- **السلوك:** disclosure اختياري، والمحتوى يبقى متاحًا دون JS.
- **الجوال:** لا لوحة عريضة؛ مستويات متداخلة بحدود ومسافات منطقية.
- **RTL:** خطوط الربط والمسافات تستخدم inline-start.
- **الوصول:** قوائم متداخلة أو headings؛ cycle/orphan ممنوعان.
- **SEO:** وصف من summary؛ لا فهرسة مستقلة للعقد دون صفحات فعلية.
- **المكوّنات:** Page Intro، Breadcrumb، List، Card، Link، Button، Feedback.
- **الملكية:** قالب Authority؛ يمكن تقييمه للترقية عند اكتمال منتج ثانٍ.

### 6.7 Contact — تواصل معنا

- **الهوية:** `contact.html`؛ Interaction؛ «تواصل معنا» / “Contact Us”.
- **الغرض:** عرض القنوات الصحيحة وتوجيه الاستفسار أو البلاغ.
- **نموذج المحتوى:** مطلوب: categories، official channels، labels، privacy/help
  text. اختياري: hours، location، attachment policy، submission adapter.
- **البنية:** Page Intro المملوك لقالب Contact، قنوات، نموذج، مساعدة، Feedback.
- **العرض:** Contact المشترك؛ لا نموذج مخصص للهيئة دون اختلاف دلالي.
- **السلوك:** تحقق native وتحسين رفع الملفات؛ الإرسال الحقيقي adapter.
- **الجوال:** حقول عمود واحد وأهداف لمس مناسبة.
- **RTL:** الهاتف والبريد يعزلان اتجاهيًا؛ الحقول logical.
- **الوصول:** labels مرتبطة، errors معلنة، الموافقة صريحة عند الحاجة.
- **SEO:** بيانات الاتصال العامة فقط؛ لا تنشر تفاصيل شخصية.
- **المكوّنات:** Contact، Text Input، Textarea، Select، File Upload، Button،
  Card، Feedback.
- **الملكية:** تهيئة المنتج؛ قالب مشترك.

### 6.8 FAQ — الأسئلة الشائعة

- **الهوية:** `faq.html`؛ Interaction؛ «الأسئلة الشائعة» / “Frequently Asked
  Questions”.
- **الغرض:** إجابات مباشرة تربط بالخدمة أو التنظيم الصحيح.
- **نموذج المحتوى:** مطلوب: unique id، question، answer. اختياري: category،
  related IDs/links، Contact CTA.
- **البنية:** Page Intro، مجموعات أو قائمة أسئلة، CTA للدعم، Feedback.
- **العرض:** Accordion المشترك؛ لا بحث مستقل في V1.
- **السلوك:** keyboard وARIA من العقد المشترك؛ المحتوى ظاهر دون JS.
- **الجوال:** عرض كامل دون تمرير أفقي.
- **RTL:** الأيقونة في الطرف المنطقي الصحيح.
- **الوصول:** button لكل سؤال وحالة expanded متزامنة.
- **SEO:** FAQ structured data فقط عندما تكون الإجابات منشورة ومطابقة للصفحة.
- **المكوّنات:** Page Intro، Breadcrumb، FAQ، Accordion، Contact CTA، Feedback.
- **الملكية:** تهيئة المنتج؛ renderer مشترك.

### 6.9 Search Results — نتائج البحث

- **الهوية:** `search.html?q=`؛ Discovery؛ «نتائج البحث» / “Search Results”.
- **الغرض:** البحث عبر الخدمات والتنظيمات والبرامج والمعرفة والإعلام.
- **نموذج المحتوى:** مطلوب: query، total، title، route، summary، content type.
  اختياري: type filter، date، pagination، suggestion.
- **البنية:** Page Intro compact، form، status، filters، results، empty state.
- **العرض:** قائمة نتائج لا شبكة بطاقات؛ نوع المحتوى ظاهر.
- **السلوك:** GET progressive enhancement؛ الإنتاج يحتاج search adapter.
- **الجوال:** filters ككتلة قبل النتائج؛ لا drawer إلزامي.
- **RTL:** ترتيب الأيقونات والحقول منطقي؛ highlights لا تكسر النص.
- **الوصول:** label صريح، status معلن باعتدال، focus على العنوان بعد الإرسال عند
  الحاجة.
- **SEO:** `noindex,follow` لصفحات الاستعلام؛ الروابط الأصلية قابلة للفهرسة.
- **المكوّنات:** Page Intro، Text Input، Select، Button، Link، Tag، List،
  Pagination، Feedback.
- **الملكية:** قدرة مشتركة جديدة مع index adapter خاص بالمنتج.

### 6.10 News Listing — الأخبار

- **الهوية:** `news.html`؛ Media؛ «أخبار الهيئة» / “Authority News”.
- **الغرض:** تصفح الأخبار المنشورة زمنيًا.
- **نموذج المحتوى:** مطلوب: ID، title، summary، published date، detail route.
  اختياري: image/alt، category، tags، featured.
- **البنية:** Page Intro، search/filter اختياري، featured item، list، pagination.
- **العرض:** Editorial Listing مشترك مستقبلًا؛ البطاقات من نفس السجلات.
- **السلوك:** فرز تاريخي وتصفية؛ empty state واضح.
- **الجوال:** بطاقة عمودية؛ الصورة لا تدفع التاريخ أو العنوان خارج العرض.
- **RTL:** تسلسل metadata logical.
- **الوصول:** عنوان البطاقة رابط واحد واضح؛ alt بحسب وظيفة الصورة.
- **SEO:** CollectionPage؛ روابط canonical للتفاصيل.
- **المكوّنات:** Page Intro، Card، Tag، Link، Pagination، Feedback.
- **الملكية:** قالب Authority أولًا، مرشح للترقية المشتركة مع المنتج الآخر.

### 6.11 News Detail — تفاصيل الخبر

- **الهوية:** `news-<slug>.html`؛ Media؛ العنوان العربي والإنجليزي من السجل.
- **الغرض:** نشر مقال موثوق قابل للمشاركة والربط.
- **نموذج المحتوى:** مطلوب: ID، title، published date، body blocks، canonical
  route، updated. اختياري: lead image/alt، category، tags، attachments، related.
- **البنية:** article intro، metadata، body، attachments، related news، Feedback.
- **العرض:** Article composition حول Heavy Content.
- **السلوك:** روابط الأجزاء والتنزيلات؛ مشاركة اجتماعية ليست مطلوبة.
- **الجوال:** النص بعرض قراءة مناسب؛ الوسائط responsive.
- **RTL:** الاقتباسات والعناصر المختلطة تحترم dir.
- **الوصول:** `<article>` و`<time>`؛ لا تكرار عنوان داخل الصورة.
- **SEO:** NewsArticle فقط عند توفر بيانات حقيقية كاملة؛ canonical للسجل.
- **المكوّنات:** Page Intro/Breadcrumb، Heavy Content، Tag، Link، Feedback.
- **الملكية:** قالب Authority أولًا؛ عقد السجل قابل للمشاركة.

### 6.12 Services Catalogue — دليل الخدمات

- **الهوية:** `services.html`؛ Services؛ «الخدمات» / “Services”.
- **الغرض:** العثور على خدمة حسب الجمهور أو المجال أو النص.
- **نموذج المحتوى:** مطلوب: services collection بعقد Foundation، audiences،
  categories، detail routes. اختياري: channel، featured، owner.
- **البنية:** Page Intro، بحث، filters، count، cards، empty state.
- **العرض:** Service Catalogue وService Card الحاليان.
- **السلوك:** تصفية قابلة لإعادة الضبط؛ URL state اختياري لاحقًا.
- **الجوال:** filters أعلى الشبكة؛ عمود واحد.
- **RTL:** اتجاه البحث والأيقونات منطقي.
- **الوصول:** نتائج وحالة خالية واضحة؛ لا custom checkbox غير مؤهل.
- **SEO:** ItemList؛ صفحات التصنيف المفلترة لا تحتاج canonical مستقلًا.
- **المكوّنات:** Page Intro، Service Card، Text Input، Tag، Button، Link،
  Feedback.
- **الملكية:** بيانات المنتج؛ renderer مشترك.

### 6.13 Service Detail — تفاصيل الخدمة

- **الهوية:** `service-<slug>.html`؛ Services؛ العنوان من السجل.
- **الغرض:** شرح الأهلية والمتطلبات والخطوات والقناة ثم بدء الخدمة.
- **نموذج المحتوى:** الحقول المطلوبة والاختيارية من عقد Service Detail الحالي،
  مع relations إلى regulation/resource/FAQ IDs.
- **البنية:** Page Intro، CTA، metadata، tabs/sections، related، support، rating.
- **العرض:** Service Detail الحالي دون fork.
- **السلوك:** Tabs progressive، hash links، رابط بدء واضح كخارجي عند الحاجة.
- **الجوال:** tabs قابلة للتمرير أو العرض وفق العقد الحالي؛ CTA لا يغطي المحتوى.
- **RTL:** تنقل الأسهم يحترم الاتجاه.
- **الوصول:** tab semantics وfocus؛ الخطوات قائمة مرتبة.
- **SEO:** Service structured data فقط بعد تكامل بيانات الجهة؛ canonical للتفاصيل.
- **المكوّنات:** Page Intro، Tabs، List، Button، Link، Service Card، Rating،
  Feedback.
- **الملكية:** بيانات وعلاقات Authority؛ renderer مشترك.

### 6.14 Programs / Initiatives Listing — البرامج والمبادرات

- **الهوية:** `programs.html`؛ Portfolio؛ «البرامج والمبادرات» / “Programs and
  Initiatives”.
- **الغرض:** اكتشاف محفظة الهيئة حسب النوع والحالة والمجال.
- **نموذج المحتوى:** مطلوب: ID، kind، title، summary، status، detail route.
  اختياري: dates، owner، image/alt، featured، area IDs.
- **البنية:** Page Intro، filters، featured، list، pagination/empty state.
- **العرض:** Portfolio Listing واحد؛ لا قالب منفصل للمبادرات.
- **السلوك:** تصفية النوع والحالة؛ فرز حديث/أبجدي.
- **الجوال:** filters متكدسة والبطاقات عمودية.
- **RTL:** الحالة والتاريخ بترتيب منطقي.
- **الوصول:** status نص لا لون فقط؛ عناوين البطاقات روابط.
- **SEO:** CollectionPage؛ query variants canonical إلى القائمة الأساسية.
- **المكوّنات:** Page Intro، Card، Tag، Link، Select، Pagination، Feedback.
- **الملكية:** قالب Authority مع عقد قابل للترقية المشتركة.

### 6.15 Program / Initiative Detail — تفاصيل البرنامج أو المبادرة

- **الهوية:** `program-<slug>.html` أو `initiative-<slug>.html` من kind؛ Portfolio.
- **الغرض:** توضيح الهدف والجمهور والحالة والمخرجات والعلاقات.
- **نموذج المحتوى:** مطلوب: ID، kind، title، summary، objectives، status، owner،
  body، canonical route، updated. اختياري: dates، metrics، partners، services،
  resources، news.
- **البنية:** Page Intro، metadata، objectives، content، verified outcomes،
  related content.
- **العرض:** Content Detail مع Tag وrelationship sections.
- **السلوك:** لا progress تفاعلي؛ الروابط من IDs المحلولة.
- **الجوال:** metadata عمودي؛ العلاقات شبكات صغيرة.
- **RTL:** مؤشرات النسب تعزل اتجاهيًا.
- **الوصول:** status مكتوب؛ المقاييس لها label/source/date.
- **SEO:** وصف من summary؛ لا ادعاء بنتائج غير موثقة.
- **المكوّنات:** Page Intro، Heavy Content، Card، Tag، List، Link، Feedback.
- **الملكية:** قالب Authority؛ مكوّنات العرض مشتركة.

### 6.16 Knowledge Resources Library — مكتبة المعرفة

- **الهوية:** `knowledge.html`؛ Knowledge؛ «مكتبة المعرفة» / “Knowledge
  Library”.
- **الغرض:** إيجاد دليل أو تقرير أو دراسة أو مادة توعوية.
- **نموذج المحتوى:** مطلوب: ID، kind، title، summary، published/updated date،
  format، detail route. اختياري: topic، audience، language، file size، cover.
- **البنية:** Page Intro، search، type/topic filters، list، pagination.
- **العرض:** Resource Library بعرض list افتراضي لظهور metadata.
- **السلوك:** بحث وتصفية وإعادة ضبط؛ تنزيل من التفاصيل لا البطاقة افتراضيًا.
- **الجوال:** الفلاتر متكدسة؛ metadata يلتف.
- **RTL:** أسماء الملفات والامتدادات معزولة اتجاهيًا.
- **الوصول:** صيغة الملف وحجمه معلنان؛ الصور الزخرفية alt فارغ.
- **SEO:** CollectionPage؛ صفحات التصفية لا تتنافس مع المكتبة.
- **المكوّنات:** Page Intro، Text Input، Select، Card/List، Tag، Pagination،
  Feedback.
- **الملكية:** قالب Authority أولًا، مرشح لقدرة مشتركة.

### 6.17 Knowledge Resource Detail — تفاصيل المورد المعرفي

- **الهوية:** `resource-<slug>.html`؛ Knowledge؛ العنوان من السجل.
- **الغرض:** شرح المورد وإظهار بياناته قبل التنزيل أو الانتقال.
- **نموذج المحتوى:** مطلوب: ID، kind، title، summary، date، format، safe
  file/HTTPS URL، route. اختياري: version، author/owner، language، size، cover,
  body، related.
- **البنية:** Page Intro، metadata، summary/body، download CTA، related.
- **العرض:** Content Detail مع Download Item.
- **السلوك:** التنزيل أو الرابط الخارجي واضح؛ لا embed PDF إلزامي.
- **الجوال:** CTA ضمن التدفق؛ لا ارتفاع viewport ثابت للملف.
- **RTL:** metadata logical والملف dir auto عند الحاجة.
- **الوصول:** اسم الرابط يضم الصيغة والحجم؛ alt للغلاف إن كان مفيدًا.
- **SEO:** canonical للتفاصيل؛ الملف ليس بديل metadata للصفحة.
- **المكوّنات:** Page Intro، Heavy Content، Metadata List، Button/Link، Card،
  Feedback.
- **الملكية:** قالب Authority وعقد تنزيل آمن؛ مرشح للترقية.

### 6.18 Regulations Library — مكتبة التنظيمات

- **الهوية:** `regulations.html`؛ Regulatory؛ «الأنظمة واللوائح والقرارات» /
  “Regulations and Decisions”.
- **الغرض:** العثور على النسخة التنظيمية الصحيحة والحديثة.
- **نموذج المحتوى:** مطلوب: ID، document type، title، authority، adoption date،
  status، detail route. اختياري: number، topic، version، effective date، tags.
- **البنية:** Page Intro، تنبيه مرجعية، search، filters، results، empty state.
- **العرض:** Regulatory Library مستقل بعقده، ويعيد استخدام نفس primitives.
- **السلوك:** تصفية النوع/الموضوع/الحالة، وفرز تاريخ الاعتماد.
- **الجوال:** metadata الأساسية تحت العنوان؛ الفلاتر متكدسة.
- **RTL:** أرقام القرارات والتواريخ قابلة للنسخ والقراءة.
- **الوصول:** status نصي؛ العنوان الكامل هو الرابط، ولا يعتمد على أيقونة PDF.
- **SEO:** CollectionPage؛ الوثائق الملغاة تبقى قابلة للاكتشاف مع status واضح.
- **المكوّنات:** Page Intro، Text Input، Select، Tag، List/Card، Pagination،
  Inline Alert، Feedback.
- **الملكية:** قالب Authority خاص دلاليًا؛ primitives مشتركة.

### 6.19 Regulatory Document Detail — تفاصيل الوثيقة التنظيمية

- **الهوية:** `regulation-<slug>.html`؛ Regulatory؛ العنوان من الوثيقة.
- **الغرض:** إظهار السياق القانوني والنسخة والحالة قبل فتح الملف.
- **نموذج المحتوى:** مطلوب: ID، type، title، issuing authority، adoption date،
  status، version، summary، safe file، canonical route، updated. اختياري: number،
  effective date، supersedes/superseded by IDs، topics، amendments، body.
- **البنية:** Page Intro، status alert عند غير نافذة، metadata، summary، file CTA،
  relations، Feedback.
- **العرض:** Regulatory Detail؛ لا يعامل كخبر أو مورد عام.
- **السلوك:** روابط النسخة السابقة/اللاحقة محلولة؛ تنزيل واضح.
- **الجوال:** metadata عمودي وCTA غير ثابت.
- **RTL:** الأرقام الرسمية ضمن عناصر `bdi` عند الحاجة.
- **الوصول:** الحالة معلنة نصيًا؛ تحذير أن محتوى العرض غير رسمي في demo.
- **SEO:** canonical؛ status لا يُخفى؛ structured data القانونية غير مفترضة.
- **المكوّنات:** Page Intro، Inline Alert، Metadata List، Heavy Content، Link،
  Button، Feedback.
- **الملكية:** قالب Authority دلالي مستقل وعقد تحقق صارم.

## 7. تركيب الصفحة الرئيسية حسب الملف

| الترتيب | Regulatory | Enablement | Development |
|---:|---|---|---|
| 1 | Hero + بحث/خدمة أولوية | Hero + خدمة/برنامج أولوية | Hero + بيان الاستراتيجية |
| 2 | الخدمات المميزة | الخدمات المميزة | المشاريع المميزة |
| 3 | أحدث التنظيمات | البرامج المميزة | محاور الاستراتيجية |
| 4 | الأدلة والمعرفة | المعرفة والأدلة | فرص الاستثمار |
| 5 | البرامج والمبادرات | المنصات/الشراكات المهيأة | الخدمات الرقمية |
| 6 | الأخبار/الاستشارات | الأخبار | الأخبار |
| 7 | نبذة مختصرة | نبذة مختصرة | نبذة عن الهيئة/المنطقة |
| 8 | Contact CTA + Feedback | Contact CTA + Feedback | Contact CTA + Feedback |

الإحصاءات والشركاء اختيارية في الملفات الثلاثة وتتطلب مصدرًا وتاريخًا وعلاقة
معتمدة. Header وDigital Stamp وFooter من الغلاف وليست أقسام Home.

## 8. مخطط التنقل

### Regulatory

| العنصر | المستوى الثاني |
|---|---|
| عن الهيئة | نبذة؛ الاختصاص؛ الاستراتيجية؛ المسؤول التنفيذي؛ الهيكل |
| الخدمات | جميع الخدمات |
| التنظيمات | المكتبة؛ الاستشارات العامة عند تفعيلها |
| البرامج | البرامج والمبادرات |
| المعرفة | المكتبة؛ البيانات المفتوحة عند تفعيلها |
| المركز الإعلامي | الأخبار؛ الفعاليات/الإعلانات عند تفعيلها |
| تواصل معنا | رابط مباشر |

### Development

يستبدل موضع «التنظيمات» بعنصر «المشاريع والاستثمار»، وتبقى التنظيمات داخل
«عن الهيئة» أو «المعرفة» بحسب حجمها. هذا اختلاف IA لا قالب Header جديد.

## 9. مخطط التذييل

| المجموعة | روابط أساسية |
|---|---|
| الهيئة | عن الهيئة؛ الاختصاص؛ الاستراتيجية؛ المسؤول التنفيذي؛ الهيكل |
| الخدمات والمحتوى | الخدمات؛ البرامج؛ التنظيمات؛ المعرفة؛ الأخبار |
| المشاركة والدعم | تواصل؛ FAQ؛ المشاركة عند تفعيلها؛ بيانات الاتصال |
| السياسات والإتاحة | الخصوصية؛ الاستخدام؛ الوصول؛ حرية المعلومات؛ خريطة الموقع |

يعرض التذييل ختم التسجيل والهوية الحقيقية عند التكامل فقط. حسابات التواصل أو
شعارات الشركاء لا تُنشأ في demo.

## 10. نموذج العلاقات

```text
Area of Work
├── Services
├── Regulations
├── Programs / Initiatives
├── Knowledge Resources
└── News

Service
├── supporting Regulation IDs
├── guide Resource IDs
├── related Service IDs
└── FAQ / support destination

Program / Initiative
├── strategic Objective IDs
├── Service IDs
├── Resource IDs
├── Project IDs [development]
└── News IDs

Regulatory Document
├── previous / next version IDs
├── Consultation ID
└── explanatory Resource IDs
```

العلاقات IDs متحققة أثناء البناء. لا يسمح بسجل يشير إلى route أو ملف غير موجود.

## 11. متطلبات Responsive وRTL والوصول

### Responsive

- اعتماد breakpoints الحالية فقط.
- القوائم تعرض عمودًا واحدًا على الجوال، مع metadata ملتف.
- Sidebar يتحول إلى كتلة قبل المحتوى أو بعده حسب التسلسل الدلالي.
- الشجرة التنظيمية لا تعتمد على canvas أو عرض ثابت.
- التصفية لا تحجب النتائج عند غياب JavaScript.

### RTL/LTR

- `margin-inline` و`padding-inline` و`inset-inline` و`text-align:start`.
- `bdi` أو `dir="auto"` لأرقام القرارات والملفات والبريد.
- اتجاه الأسهم والتنقل في المسارات والتبويبات يتبع `dir`.
- لا stylesheet ولا HTML منفصل لـRTL.

### Accessibility

- landmarks والعناوين الصحيحة ورابط تخطي.
- روابط التنزيل تذكر الصيغة والحجم.
- حالات السجل لا تعتمد على اللون.
- بديل نصي كامل للمخططات والرسوم.
- forms بعناوين وتعليمات وأخطاء مرتبطة.
- focus restoration في dialog/drawer، وreduced motion.

## 12. SEO والبيانات المنظمة

- عناوين ووصف وcanonical من عقود السجلات.
- `noindex` لنتائج البحث وصفحات المعاينة غير المنشورة.
- NewsArticle وEvent وOrganization وService لا تُفعل إلا بعد توفر بيانات حقيقية
  مكتملة ومراجعة.
- الملفات التنظيمية والموارد تملك صفحات تفاصيل ثابتة؛ لا يعتمد الاكتشاف على
  ملفات PDF وحدها.
- صفحات النسخ الملغاة تبقى قابلة للوصول مع روابط إلى النسخة السارية.

## 13. معايير اكتمال V1

- الأنواع المطلوبة التسعة عشر منفذة وممثلة بمحتوى خيالي آمن.
- الملف الافتراضي `regulatory` يبني موقعًا كاملًا، ويثبت اختبار تهيئة واحد على
  الأقل لكل من `enablement` و`development` دون fork للقوالب.
- التنقل والعلاقات والبحث الداخلي لا تحتوي وجهات مكسورة.
- Foundation لا يعتمد على المنتج، والمنتج لا يعتمد على `products/ministry/`.
- RTL وLTR والجوال واللوحي والحاسوب متحققة على الصفحات عالية المخاطر.
- keyboard والوضع دون JavaScript وحالات empty/error متحققة.
- لا أرقام أو لوائح أو خدمات تبدو رسمية في محتوى العرض.
- سجل المكوّنات محدث فقط بالقدرات الجديدة المثبتة.
