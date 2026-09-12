# عقود البيانات والتدقيق

`REFERENCE.md` هو مرجع التأليف العام. المخططات التنفيذية موجودة في `standards/schemas/` ويستخدمها `scripts/audit.py`. هذه مخططات JSON Schema؛ المدقق المحلي ينفذ فقط الكلمات المستخدمة فيها ولا يدعي دعم JSON Schema كاملًا.

## reference.json 2.1

حقول موحدة: `component` كائن له name مطابق لاسم مجلد الحزمة، و`axes` قائمة أسماء، و`axis_values` كائن له المفاتيح نفسها وكل قيمة قائمة، و`variants` قائمة كائنات ذات IDs فريدة، و`variant_coverage`.

لا نفرض تسمية جديدة لقيم المحاور أوCSS. اختلاف `Small` و`small` و`sm` يحتفظ به حيث يمثل العقد القائم؛ لا يُحوّل إلى class جديد تلقائيًا. تفاصيل المصدر محفوظة في `axis_details` و`source_measurements` و`source_model` و`variant_summary` حسب الحاجة. `components` داخل Tab/Tag محفوظة، والمحاور العليا تخص العنصر الرئيسي. Group/Status Tag يحتفظان بمحاورهما الداخلية.

- `axes_only`: المصدر يصف المحاور دون قائمة variants صريحة.
- `documented_subset`: توجد قائمة موثقة؛ لا ادعاء أنها حاصل الضرب الكامل.
- `complete`: للاستخدام بعد تحقق فعلي من التغطية فقط.

IDs من الشكل `*-documented-001` معرفات للسجلات الموجودة التي لم يكن لها ID؛ لا تمثل variants جديدة. لا تُنشأ combinations لم يذكرها المصدر. محتوى `variants` الإضافي يظل مفتوحًا لحفظ خصائص Figma؛ envelope موحد، لكن تحويل جميع properties إلى مخطط بصري موحد مؤجل لتأهيل المكونات.

File Upload يعلن `state_single` و`state_drop_zone` و`state_file_item` بدل محور state بلا قيم؛ هذه حالات عناصر مختلفة وليست حاصل ضرب صالحًا لكل mode. Textarea ما زال placeholder؛ إصلاح ملفه الفارغ لا ينشئ reference أوتنفيذًا.

## audit-rules.json 1.1

كل ملف له `component_id` و`rules` ومؤشر سجل الأنواع. كل قاعدة لها ID ثابت و`rule_type` مسجل وseverity من error/warning/info و`validation_status`.

`rule_type` هو حقل dispatch الوحيد. `check` ومحتواه التاريخي، بما فيه `check.type` أوتعبيرات تشبه JavaScript، بيانات مرجعية محفوظة، ولا تُنفذ بواسطة eval. `source_rule_type` و`source_type` و`source_severity` تحفظ التسميات السابقة عند تغيير envelope.

التصنيفات مثل structure وaccessibility لا تحدد خوارزمية اختبار. القواعد الوصفية أوغير القابلة للتعيين بثقة تصنف `manual_review`. الأنواع الأخرى توحد دلاليًا في السجل؛ وجود نوع مسجل لا يعني وجود interpreter له.

جميع الـ309 قواعد الحالية تظل `not_run` في نتيجة الأداة، حتى لو كان ملف تاريخي يقول خلاف ذلك. الأداة تنفذ فحوص repository مستقلة ولا تحدث ملفات compliance. لا تحويل للمطابقة الداخلية إلى رسمية. مراجعة صحة الربط الدلالي لكل `standard_id` وكل شرط قديم تتم ضمن تأهيل المكوّن، لا باستبدال IDs آليًا.

## الأولوية عند تعارض الوثائق القديمة

السياسة العامة المحدثة في REFERENCE والمعايير تسري على العمل القادم. العقود والقواعد القديمة التي تصف قيودًا مختلفة دليل backlog، وليست استثناءات تمنح النجاح تلقائيًا. مثل إخفاء focus أثناء pressed أوالحاجة إلى ARIA إضافية لعنصر HTML أصلي. لا تتغير صور العرض أوCSS ضمن تسوية الوثائق.

تصحيح مسارات المصدر: صورة Button subtle-hovered تشير الآن إلى اسم الملف الموجود فعلًا `hovred.png` دون إعادة تسمية المصدر، ورابط stylesheet في showcase الخاص بـCode Snippet يصل إلى token.css في الجذر.
