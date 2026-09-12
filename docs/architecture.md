# Product Architecture — قرار الدفعة الأولى

الحالة: معتمدة كاتجاه تنفيذ للدفعة الأولى، وليست اعتماد جاهزية إنتاجية. لا تشمل هذه الدفعة تنفيذ Base أو تغيير Tokens أو بناء صفحات.

## الطبقات والمسؤوليات

| الطبقة | المسؤولية | تعتمد على |
|---|---|---|
| Foundation | التوكنز، الخطوط، Base، قواعد layout والإتاحة | لا تعتمد على المكونات |
| Core | عنصر أو سلوك عام مستقل عن القطاع | Foundation |
| Composite | تجميع عناصر لها عقود مستقلة | Foundation، Core، وتركيبات أصغر دون دورات |
| Global Partial | جزء متكرر من shell الموقع | Foundation، Core، Composite |
| Section | كتلة محتوى قابلة لإعادة الاستخدام | Foundation، Core، Composite |
| Archetype | عقد slots وترتيب أجزاء الصفحة | Partials وSections |
| Template | تجميع HTML كامل بمحتوى فعلي | Archetype والطبقات المعتمدة |
| Sector Kit | تكوين وامتدادات محتوى قطاعية | Templates والعقود العامة |

Global Partials تأتي مبكرًا في تخطيط المنتج، لكنها تستهلك Core عند التنفيذ. لا تفرض السلسلة النظرية اعتماد Core على Header أوFooter. ولا يلزم المرور عبر Composite إذا أمكن لقسم استخدام Core مباشرة.

ممنوع اعتماد الطبقات الأدنى على أعلى، أو تكرار CSS لمكوّن داخل Section، أو إنشاء نسخة قطاعية عندما يكفي variant. Drupal وNext.js المستقبلية طبقات تكامل تستهلك HTML contracts؛ لا تدخل الأساس.

## المسارات

نحافظ على `token.css` و`REFERENCE.md` و`standards/` و`components/` ومسارات CSS الحالية. `docs/inventory.json` يحدد الطبقة المنطقية؛ ليس كل ما داخل `components/` من نوع Core. Card وAlert وToast وFile Upload وCode Snippet وRating وPagination مصنفة Composites حسب عقودها أو مراجعها الحالية.

المجلدات القادمة لا تنشأ فارغة:

```text
styles/base/       global.css + layout.css + accessibility.css
composites/        التركيبات الجديدة؛ القائمة تبقى في مساراتها
partials/          shell الموقع
sections/          كتل محتوى عامة
archetypes/        عقود slots وأمثلة assembly
templates/         core ثم university/ministry/authority/municipality/healthcare
sector-kits/       تكوين القطاعات وامتداداتها الوظيفية
assets/            fonts/icons/images عند إضافة أصول فعلية
scripts/           أدوات المطور والتدقيق
tests/             اختبارات الأدوات والمكونات عند الحاجة
docs/              القرارات والجرد وخطة التنفيذ
```

كل حزمة جديدة تحتفظ بـ`reference.json` و`[name].css` و`template.html` و`[name].contract.md` و`audit-rules.json` و`compliance.json` و`showcases/index.html`. يضاف `[name].js` فقط لسلوك يحتاج JavaScript، كـES module دون inline handlers أو global namespace. `template.html` داخل حزمة مكوّن مثال عقد محلي وليس Template موقع كاملًا.

## الجرد وحالاته

السجل يشمل كل مجلد موجود باستثناء أداة `_showcase`، ثم Core/Composites/Partials/Sections المخطط لها. المسارات الفارغة تعني مخططًا فقط. لا تنشأ ملفات implementation من السجل آليًا.

- `selection: canonical`: المسار المختار للعمل القادم؛ لا يعني production-ready.
- `legacy`: نسخة محفوظة، مع `replacement`؛ لا تستخدم في تركيب جديد.
- `not_implemented`: بيانات مصدر أو placeholder فقط.
- `status: needs_improvement`: تنفيذ موجود يحتاج معالجة وفحوصًا.
- `planned`: غير منفذ؛ dependencies خطة slots وقد تكون اختيارية بحسب variant.
- `production_ready`: لا يتغير إلى true بمجرد وجود عقد مكتوب عليه stable.

التبعيات تسجل IDs لحزم مستقلة؛ لا تسجل عناصر HTML الداخلية أو ملفات Figma. Field Group يقبل أنواع control متعددة، وText Input مثال البداية. Service Card يحتاج أولًا تسوية عقد Card للسماح بالروابط/slots المناسبة؛ ليس تركيبًا معتمدًا حاليًا. File Item وDrop Zone داخل File Upload ليسا مكوّنين مستقلين جديدين.

## Global Partials

- Required: Header، Primary Navigation، Mobile Navigation كسلوك responsive، Skip Link، Main، Footer، Page Title كوظيفة يمكن للـHero امتلاكها.
- Contextual: Brand Bar، Breadcrumb للداخلية، Secondary Navigation، Search Interface/Trigger، Language Switcher عند وجود ترجمة، Feedback placement، Consent عند دخول الحاجة ضمن المنتج.
- Optional: Accessibility Controls بوظائف محددة، Back to Top.

Breadcrumb يبقى المكوّن القائم؛ Feedback يستخدم Section واحدة. لا ننشئ package مكررًا لتغيير موضع العرض. Mobile Navigation يستخدم بيانات التنقل نفسها.

## Sections وvariants

Required for Core library: Hero، Page Intro، Services Grid، News Grid، Events Listing، Statistics، Quick Links، Documents، Related Content، Contact Information، CTA، FAQ، Search، Feedback. Required يعني توفيره في المكتبة، وليس عرضه في كل صفحة.

Optional: Leadership، Featured Content، Locations، Partners، Media Gallery. Initiatives وPrograms يستخدمان Featured Content حتى يظهر اختلاف وظيفي. Featured Services وLatest News وLatest Events تكوينات محدودة العدد من الأقسام العامة. Hero يدعم لاحقًا standard/image/split/search-led. لا مكونات قطاعية في هذه الدفعة.

## Archetypes

Keep: Homepage، Landing، Listing، Directory، Profile، Service Detail، Process/Journey، Document/Regulation، Form، Search Results.

Merge: Standard/Rich Content في Content Detail؛ Filtered Listing variant من Listing؛ Timeline نمط عرض داخل Content Detail أوJourney.

Split: Statistics المنشورة مقابل Dashboard تفاعلي مؤجل؛ Location Detail مقابل Map Explorer مؤجل. Add: System/Outcome لصفحات الخطأ والنجاح وعدم التوفر.

## Base القادمة

ثلاثة ملفات فقط: `global.css` للـreset المحدود وtypography العامة، `layout.css` للـcontainer وreading width وgrid/stack، و`accessibility.css` للـskip link وvisually-hidden وسياسة الحركة المخفضة. لا utilities عامة قبل حاجة متكررة. لا نسختي RTL/LTR ولا قيم بصرية جديدة قبل البحث في التوكنز.

## Definition of Done

المكوّن: JSON صالح، عقد موثق، tokens معرفة ومستهلكة، قيم بصرية مطابقة، scoped CSS وBEM، حالات وvariants موثقة، RTL/LTR وresponsive، semantic HTML، اسم وإتاحة لوحة مفاتيح وfocus وARIA المناسبة، سلوك مستقل عند الحاجة، وعدم تكرار مكوّن موجود.

القسم: مبني من الحزم المعتمدة؛ ترتيب عناوين صحيح؛ محتوى طويل/قصير/فارغ؛ RTL/LTR وresponsive؛ variants موثقة؛ وإثبات إعادة استخدامه في تركيبين.

لا يعتبر audit لم يُنفذ passed. اختبارات المتصفح والقراءة البشرية تبقى بوابات منفصلة. هدف 80–90% إعادة استخدام داخل Templates اتجاه تصميم وليس قياسًا لعدد الأسطر.
