# فائدة الصفحة وتقييم الخدمة

## الاستخدام

- page-feedback في index.html وservices.html وnews.html وabout.html.
- service-rating في صفحات تفاصيل الخدمات الست.
- المعاينات: components/page-feedback/showcases/index.html وcomponents/service-rating/showcases/index.html. تعرض نسختين مستقلتين، والأرقام فيها بيانات توضيحية معلنة.

لإضافة الإحصاءات إلى سجل الصفحة: `feedback_statistics: {"count": 100, "percentage": 80}`؛ ولسجل الخدمة: `feedback_statistics: {"count": 1544, "average": 3.9}`. تُغذّى من مصدر موثوق عند نشر القالب، ولا تُزاد محليًا بعد المعاينة. المثالان ليسا إحصاءات المستخدمين الفعلية.

يُعاد البناء بأمر `python3 scripts/build_site.py`، وتُجدد المعاينات بأمر `python3 scripts/build_feedback_showcases.py`.

## الربط

ملف styles/composites/feedback.js يهيئ كل نسخة بشكل مستقل. بعد تحميله، اربط عنصر المكوّن بمعالج `PlatformFeedback.setSubmitHandler(element, async payload => ...)` يعيد true بعد تأكيد الخادم فقط. عند الرفض أو الخطأ تبقى المدخلات متاحة لإعادة المحاولة. لا ينفذ القالب طلب شبكة أو تخزينًا تلقائيًا. عقد كل مكوّن يوثق payload والحالات.

## المصادر

- مرجع فائدة الصفحة: https://www.kku.edu.sa/ar/portfolio/leadership-message — راجعت ترجمة RatingForm وتنفيذ المكوّن وCSS من الموقع، بما يشمل اختلاف أسباب نعم/لا وخيارين كحد أقصى. الاختلاف المقصود: الجنس اختياري، والمعاينة لا تدّعي حفظ المشاركة.
- مرجع تقييم الخدمة: https://www.figma.com/design/p5CNO0xQWQi4GjrRxXoU56/?node-id=1-4 — حالات سطح المكتب 2:111 و2:173 و2:9134 والجوال 2:9190، محفوظة في _figma مع أصول SVG الأصلية وبصماتها.
- الإرشادات: https://design.dga.gov.sa/guidelines/templates/rating-section — سؤال تقييم الخدمة والنجوم، تأكيد النجاح بعد الإرسال، وترتيب الأزرار أسفل النص على الجوال.
- قالب المعاينة الرسمي: https://design.dga.gov.sa/templates/rating.

## التحقق

tests/browser-feedback-cases.mjs يغطي 320 و430 و768 و1440 في RTL وLTR، والتحقق من السبب والنجوم، الانتظار والفشل والنجاح وإعادة المحاولة، المعاينة المحلية، النسخ المتعددة، وعدم تشغيل JavaScript. نتائج التنفيذ في feedback-components-result.json.


## تصحيح حالات عناصر الإدخال

Radio أصبح مكوّنًا أساسيًا منفذًا في components/radio، ويُستخدم في خيارات الجنس داخل Page Feedback. أزيل accent-color والتنسيق المحلي الذي كان يتجاوز مكونات Radio وCheckbox. اختبار tests/browser-radio-cases.mjs يفحص الألوان والأبعاد والتحويم والضغط والتركيز والتعطيل والاختيار الحصري بالمؤشر ولوحة المفاتيح في RTL وLTR.
