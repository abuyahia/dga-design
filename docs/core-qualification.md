# تأهيل Core — الدفعة 3.1

تحميل CSS بالترتيب: token.css ثم styles/base ثم ملفات المكونات المطلوبة. لا تجمع accordion القديم وaccordion-new في الصفحة نفسها.

استخدم `import { initCore } from './scripts/core/index.js'` ثم `const dispose = initCore(container)`. الاستدعاء الثاني للجذر نفسه يعيد cleanup نفسه. استدعِ cleanup قبل إزالة الجذر، ولا تستخدم جذورًا متداخلة. لا يوجد تشغيل تلقائي أو global namespace؛ قدّم الملفات عبر HTTP، لا file://.

| المكوّن | العقد التنفيذي |
|---|---|
| Button | استخدم button مع type صريح؛ disabled الأصلي للتعطيل. aria-disabled يحتاج initCore. لا يغيّر المكوّن aria-pressed آليًا؛ مالك الحالة يحدّثه. التركيز يبقى أثناء الضغط والنص الطويل يلتف. |
| Link | التنقل عبر a وhref فعلي. للرابط المعطل احذف href واستخدم role=link وaria-disabled=true؛ tabindex=0 فقط إذا أردت إبقاءه قابلًا للاكتشاف بالتركيز. الحارس لا يمنع فتح href من قائمة السياق، لذا حذف href إلزامي للتعطيل الكامل. |
| Label | label وfor يطابقان id فريدًا لحقل حقيقي. علامة المطلوب aria-hidden؛ required على الحقل نفسه. لا تستخدم aria-disabled على label بدل تعطيل الحقل. |
| Text Input | label مرتبط؛ disabled وreadonly الأصليان إلزاميان مع modifier البصري المناسب. الخطأ aria-invalid=true وaria-describedby يشير إلى رسالة موجودة. readonly قابل للتركيز والنسخ. |
| Checkbox | native input، وlabel مرتبط. mixed عبر data-indeterminate ثم الخاصية native indeterminate؛ checked مستقل عنها، ولا يلزم aria-checked مكرر. readonly لا تدعمه HTML: استخدم wrapper checkbox--readonly وinput disabled data-readonly-fallback؛ initCore يتيح التركيز ويمنع التغيير. disabled العادي لا يحمل fallback. reset يعيد mixed الأولية. |
| Accordion | عنوان heading بمستوى مناسب يحتوي button وaria-controls يشير إلى panel فريد داخل النسخة نفسها. المحتوى ظاهر افتراضيًا وaria-expanded=true. استخدم disabled data-enhancement-disabled للتعطيل حتى التحسين، وdata-initial-expanded=false للطي بعده. hidden يعكس الحالة؛ Enter/Space من الزر الأصلي. cleanup يعيد المحتوى ظاهرًا. |

تباين الروابط الأساسي والمحايد وحالة hover للزر الأساسي عُدّل بتوكنات موجودة. on-color يتطلب سطحًا داكنًا مناسبًا وفحصًا ضمن الصفحة المستهلكة؛ ليس ضمانًا فوق صور عشوائية.

المراجع: [نمط Accordion](https://www.w3.org/WAI/ARIA/apg/patterns/accordion/)، [حالات input الأصلية](https://html.spec.whatwg.org/multipage/input.html). عند التعارض مع أوصاف Figma القديمة، هذا العقد يحدد السلوك التنفيذي؛ تبقى المراجع الأصلية محفوظة للمقارنة. ليست هذه شهادة WCAG أو تشغيلًا لقواعد التدقيق التاريخية الـ309.
