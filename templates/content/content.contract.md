# قالب صفحة المحتوى الثقيل

المعاينة: `dist/government/content.html` بعد تشغيل `python3 scripts/build_site.py`.

## التركيب

الختم الرقمي والترويسة المشتركة → مسار التنقل والعنوان والوصف → Divider → فهرس المحتويات ومتن الصفحة → تاريخ التحديث وتقييم الصفحة → التذييل المشترك.

يعرض سطح المكتب عمود فهرس بعرض 222px بجانب المحتوى وبفاصل 32px. يتبع موضع العمود اتجاه المستند: يمينًا في RTL ويسارًا في LTR. على الشاشات الأصغر من 768px يظهر الفهرس قبل المتن ويتوقف التثبيت.

## إعدادات المحتوى

تُعرّف الصفحة في `site/government.json` بقسم `heavy-content` وكائن `heavy_content`:

- `overview`: وصف الغرض من الصفحة.
- `sections`: قائمة غير فارغة؛ لكل قسم `id` فريد بصيغة slug، و`title`، و`blocks`.
- `subsections`: قائمة اختيارية بنفس حقول القسم؛ مستوى فرعي واحد مقصود في هذا القالب.
- أنواع الكتل: `paragraph`، و`ordered-list`، و`unordered-list`، و`link`، و`media`.
- الروابط تقبل صفحات القالب المولدة مع fragment أو وجهات HTTPS.
- كتلة `media` تتطلب وصفًا بديلًا، ويكون التعليق اختياريًا.

يتحقق `scripts/content_markup.py` من البنية والمعرفات والوجهات، ثم يهرب جميع النصوص والسمات عند التوليد.

## فهرس المحتويات

يستخدم `components/table-of-contents`. كل عنصر رابط fragment أصلي، ولذلك يبقى التنقل متاحًا دون JavaScript. يحدّث `templates/content/content.js` رابط `aria-current="location"` عند النقر والتمرير، ولا يضيف تمريرًا متحركًا.

## المراجع

- Figma، النسخة العربية الثقيلة: https://www.figma.com/design/jG7qQrE5ryh0OEns7Eh9w8?node-id=1-7842
- Figma، الجوال العربي: node `44:4803`
- Figma، مكوّن TOC المستخدم في الصفحة: node `1:7942`
- قالب DGA المنشور: https://design.dga.gov.sa/templates/content

استخدم التنفيذ عرض الحاوية الحالي في المشروع بدل توسيع shell، وأعاد استخدام Breadcrumb وDivider وList وLink وPage Feedback. مساحة الوسائط محايدة كما في المرجع وتستبدل بأصل معتمد في الاستخدام الفعلي.

## التحقق

- `python3 -B -m unittest discover -s tests -q`: 30 اختبارًا.
- `python3 scripts/audit.py --strict`: صفر أخطاء وصفر تحذيرات.
- `node tests/browser-foundation.mjs content . /tmp/content-browser.json`: 17 حالة لعروض 320 و430 و768 و1440، في RTL وLTR، مع التنقل الداخلي وحالة دون JavaScript.
