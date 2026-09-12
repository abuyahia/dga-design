# Foundation — الدفعة الثانية

الحالة: التوكنز وBase منفذة ومختبرة ضمن النطاق أدناه. لا تعني جاهزية جميع المكونات أوإتمام مطابقة كود المنصات.

## التحميل

```html
<html lang="ar" dir="rtl">
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="token.css">
  <link rel="stylesheet" href="styles/base/global.css">
  <link rel="stylesheet" href="styles/base/layout.css">
  <link rel="stylesheet" href="styles/base/accessibility.css">
  <!-- ثم CSS المكونات المستعملة فقط -->
</head>
```

للإنجليزية استخدم `lang="en" dir="ltr"` مع الملفات نفسها. HTML أعلاه مقتطف تحميل، وليس صفحة كاملة. لا تستخدم نسختَي Accordion أوLink معًا.

## الملفات والعقود

| الملف | المسؤولية |
|---|---|
| global.css | box-sizing، خط ولون body، وراثة الخط للحقول، الصور المتجاوبة، احترام hidden، وtypography اختيارية داخل ds-prose |
| layout.css | ds-container، ds-reading، ds-stack، ds-cluster، ds-grid |
| accessibility.css | sr-only، skip-link، focus fallback، وإيقاف الحركة عند prefers-reduced-motion |

`ds-prose` يطبق تنسيق المحتوى التحريري فقط. لا يفرض typography على كل heading داخل المكونات. ارتفاعات الصور تستجيب للنسبة الأصلية، ومكوّن Media القادم يمكنه توثيق crop مستقل.

`ds-grid` شبكة بطاقات متساوية: عمود واحد افتراضيًا، عمودان بدءًا من 768px، وثلاثة بدءًا من 1280px. ليست نظام 12 عمودًا ولا utility framework. `ds-stack` ترتيب رأسي و`ds-cluster` صف يلتف؛ كلاهما يستخدم gap بالتوكنز.

## الحاويات ونقاط التوقف

- الحد الأقصى للحاوية هو `--container-max-width` مرتبط الآن بـ`--width-3xl`، دون تغيير القيمة 1280px.
- العرض يشمل padding بنظام border-box: عند 1280px يبقى 1216px للمحتوى بعد 32px على كل طرف، متسقًا مع grid desktop الحالي.
- تحت 768px يستخدم padding الهاتف 16px؛ عندها وفوقها 32px. الحاوية تنكمش إلى الشاشة ولا تفرض عرضًا أدنى.
- `--paragraph-max-width` يضبط عرض القراءة. قيم grid-mobile/tablet الحالية أمثلة قياس عند عرض مرجعي، وليست عرضًا ثابتًا يفرض على الجهاز.
- لم نضف أسماء breakpoints موازية. media queries تحتاج literals؛ الأداة تقارنها بالتوكنز بدل استخدام var() غير صالح داخل شرط media.
- أصبح حد عرض mobile في Inline Alert متسقًا مع Toast عند max-width:767px، بدل استمراره حتى 768px. هذه تسوية مقصودة عند الحد الصحيح، لا إعادة تصميم للمكوّن.

## التوكنز والتصنيف

زاد عدد التعريفات المركزية من 437 إلى 1128: معظم الإضافات نقل لتعريفات تصميم كانت داخل المكونات أوتسجيل لأسماء عقود معلقة كانت تعتمد على fallbacks. لا تمثل 691 درجة جديدة في scales.

1. أسماء Figma مثل `--Global-spacing-lg` تستبدل بالقيمة الموجودة المناسبة، ولا تنشأ لها namespace ثانية. مثال: مصدرها هنا 12px، فتستخدم space-12؛ لا تربط عميانيًا بـspacing-lg ذي القيمة 16px.
2. توكنز المكونات الموثقة، مثل text-input وchip وtag، تسجل في token.css وتربط بالـprimitive المناسب حيث يغطي نفس القيمة. بقيت القيم الخاصة ذات الحاجة الفعلية، مثل عرض Quote أوإطار Chip، ضمن عقد المكوّن.
3. أضيفت قيم مشتركة محدودة لحاجة فعلية: space-6/10/36، لون النص القوي #161616، درجات white alpha المستخدمة، مدد 150ms و750ms، focus وz-index.
4. متغيرات اختيار variant، مثل --_link-color و--checkbox-size، تظل scoped ومحكومة بقائمة في foundation-policy.json؛ قيمها تشير إلى التوكنز العامة.
5. --fill و--fill-start و--fill-end نسب runtime على Slider، وليست توكنز تصميم. بقيت fallbacks النسبية لضمان الحالة الابتدائية.

التطابق الرقمي وحده ليس مبررًا لتوحيد أدوار مختلفة. مثال: border width وspacing قد يتساويان، لكن عقودهما مستقلة. لم تُعد كتابة المقاييس الأصلية ولم يُنقل بيانات Figma أوحذفها. `token-migration.json` يسجل تصنيف الأسماء القديمة وربطها.

لا توجد تعريفات تصميم ثابتة داخل :root للمكونات بعد النقل. لا تنقل بيانات الرسم مثل rotate/scale أوعدد أسطر disclosure إلى scale للمسافات لمجرد احتوائها على رقم.

## RTL والحركة وFocus

- حولت مواضع Pagination وTab وQuote وSlider وحدود gutter إلى logical properties مع الحفاظ على overrides البصرية ذات السياق.
- Slider range يستخدم inset-inline-start لنسبة البداية، فلا تمحو قاعدة RTL النسبة وتعيدها إلى صفر. اختبر بدء التعبئة عند 25% وطولها 50% في الاتجاهين.
- أصلح transform-origin غير الصالح inline-start إلى left مع :dir(rtl) للـpressed underline؛ الموضع نفسه خاصية ذات محور physical وليس logical.
- احتفظ Checkbox بتمركز ripple عبر left:50% مع translate(-50%,-50%). واحتفظت أسماء المؤلف في Quote بمحاذاة right المقصودة في المصدر. استثناءات دقيقة وموثقة، لا سماح عام بالخصائص الفيزيائية.
- sr-only أصبح في Base بدل نسخه داخل Tab وTag؛ صفحات عرضهما تحمل accessibility.css. قيم clipping ذات البكسل الواحد استثناء تقنية إتاحة، لا قيمة بصرية مفقودة.
- رابط skip-link يظهر على focus وينقل التركيز إلى main ذي tabindex=-1. focus fallback منخفض specificity لا يغير ملكية المكوّن لنمطه الخاص.
- reduced motion يوقف animations/transitions ويعيد scroll-behavior إلى auto. المكونات المستقبلية لا تعتمد على animationend لإنهاء منطق ضروري دون مسار بديل.

z-index: base/content/decoration/control للطبقات الداخلية الموجودة، dropdown=10، sticky=100، overlay=1000، skip-link=1100. stacking context للأب يظل مؤثرًا؛ لا تعد هذه الأرقام ضمانًا لتجاوز كل سياق تكديس. الأنماط المستقبلية توثق سياقها.

## الخطوط

Base لا تطلب خطوطًا خارجية. font-sans يحتفظ بـIBM Plex Sans Arabic ثم Noto Sans Arabic ثم system fallbacks. لا توجد ملفات WOFF2 مرخصة في المستودع؛ لذلك لا ندعي تحميل الخط أوالتطابق الطباعي مع Figma على جميع الأجهزة. أضف أصول self-hosted عند توفرها دون نسخ عائلات التوكنز.

## التحقق وحدوده

- strict repository audit: تعريفات ومراجع التوكنز، دورات aliases، المتغيرات المحلية المصرح بها، القيم البصرية والاتجاهات حسب الفحص الساكن، وتطابق breakpoints.
- 15 اختبار regression للأداة، بما فيها أخطاء tokens والاستثناءات وعدم تصنيف BEM pseudo-selectors كتوكِنات.
- Chrome: أحجام 320/375/768/1280/1600 في RTL وLTR؛ overflow، container centering، أعمدة الشبكة واتجاهها، form bounds، skip-link بلوحة المفاتيح، Slider range، وreduced motion.
- مقارنة 54 حالة showcase قبل وبعد نقل التوكنز لم تجد اختلافًا في خصائص الألوان والحدود وحجم/وزن/ارتفاع سطر النص وpadding وgap المقاسة. هذه مقارنة computed styles محددة، وليست pixel-perfect لكل حالة تفاعلية أوخط مستضاف. التصحيحات الاتجاهية تمت بعد هذه المقارنة ولها فحوص منفصلة.

المثالان في tests/fixtures/foundation.html وfoundation-ltr.html أمثلة اختبار معزولة، وليسا Templates. جميع قواعد المكونات الـ309 باقية not_run. تأهيل السلوك الكامل، contrast، screen readers، المتصفحات الأخرى، ومشكلات مثل حجم Chip الصغير أوحجب focus في CSS قديم تنتمي إلى الدفعة التالية؛ لا تخفيها نتيجة strict الخاصة بهذا النطاق.
