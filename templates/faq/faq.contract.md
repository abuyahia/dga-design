# قالب الأسئلة الشائعة

المعاينة: `dist/government/faq.html` بعد `python3 scripts/build_site.py`.

تركيب الصفحة: مقدمة compact → faq → contact-cta → feedback، ضمن shell والترويسة والتذييل المشتركين. رابط الصفحة في قائمة «عن الجهة» والتذييل.

المحتوى في صفحة faq.html داخل `site/government.json`: questions قائمة غير فارغة من id (slug فريد)، question وanswer (نصان غير فارغين؛ يُهربان عند البناء). contact_cta يتضمن title/description/label وhref لصفحة مولدة. المحتوى تجريبي عام قابل للاستبدال؛ ليس نقلًا لسياسات الجامعة.

الأكورديون يستخدم ملف التركيب `components/accordion-new/item.html` ونفس CSS وسلوك `scripts/core/index.js`. يُركب runtime أثناء البناء لدعم معاينة file://. الأسئلة مغلقة أولًا مع JavaScript، والإجابات ظاهرة بدونه؛ أزرار أصلية وروابط ARIA وعناوين h3.

## المراجع والاختيارات

- DGA: https://design.dga.gov.sa/guidelines/templates/faqs-page وhttps://design.dga.gov.sa/templates/faqs. أمكن تنزيل shell المعاينة؛ لم تتوفر الإرشادات عبر أداة الويب.
- Figma: https://www.figma.com/design/cVZ4X4omkJoO8qNpekshcJ?node-id=2114-4411. النسخة البسيطة العربية، والجوال 2325:12045. تم فحص النسخة المصنفة أيضًا؛ البحث والتصفية ليسا ضمن النسخة البسيطة المختارة.
- بطاقة التواصل: node 2085:13716؛ الأيقونة الأصلية محفوظة في assets/contact.svg من تصدير Figma.
- صفحة الاستخدام: https://www.kku.edu.sa/ar/faq. المحتوى المسترجع يُظهر العنوان والبحث والتاريخ دون الأسئلة المحملة ديناميكيًا.

تُستخدم هوية المشروع وترويسته وتذييله وعرض container الحالي (1216px للمحتوى) بدل عرض Figma البالغ 1280px، وفق أولوية إعادة الاستخدام. لا ادعاء مطابقة بكسلية. لا تكرار للترويسة والتذييل أو CSS المكوّنات.

## التحقق

`python3 -B -m unittest discover -s tests -p test_site_build.py -q`: 8 اختبارات بناء، روابط وأصول وIDs وتهريب نصوص.

`node tests/browser-foundation.mjs faq . /tmp/faq-browser.json`: 17 حالة؛ أربعة عروض × اتجاهين، طي وفتح، ومحتوى دون JavaScript. متصفح Chrome؛ LTR فحص اتجاه لا ترجمة.
