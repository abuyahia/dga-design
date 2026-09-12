# تشغيل التدقيق

المتطلب: Python 3.9+ فقط، دون تنزيل packages أوFramework أوnpm.

من جذر المشروع:

```sh
python3 scripts/audit.py
python3 scripts/audit.py --output /tmp/design-system-audit.json
python3 scripts/audit.py --strict
python3 -B -m unittest discover -s tests -v
```

الأداة تحلل JSON في components/standards/docs، بما فيه كشف المفاتيح المكررة، وتطبق schemas على المراجع وملفات audit والجرد. تفحص IDs والمحاور، وسجل أنواع القواعد، والمسارات المسجلة والتبعيات والدورات، وتراجع tokens المستهلكة وCSS source، وروابط stylesheet وscript المحلية في HTML. مراجع ملفات variants.files تفحص كتحذيرات للمصدر.

الفحص العادي يفشل exit 1 عند أخطاء البنية/العقود/الأصول. التحذيرات لا تمنع إكمال دفعة البيانات، لكنها تبقى في التقرير. `--strict` يفشل أيضًا عند أي تحذير؛ نجاح الفحص العادي لا يعني اجتياز Foundation. التقرير الكامل اختياري ويكتب في المسار المحدد دون تعديل compliance. لا يقرأ مجلد docs/reports لتفادي تدقيق مخرجاته الخاصة.

## حدود الفحص

- token_not_central يبلّغ عن كل اسم مستهلك غير معرف في token.css؛ قد يكون له تعريف محلي أوfallback أوغرض runtime. يحتاج تصنيفًا في الدفعة الثانية.
- visual_literal_review وphysical_css_review فحص نصي مساعد، لا CSS parser ولا حكم نهائي على المطابقة. يحتفظ بموقع السطر، ويستبعد التعليقات؛ قد يتطلب استثناء هندسيًا موثقًا.
- لا يتحقق من روابط التنقل المقصودة إلى صفحات مستقبلية، أوصور Figma المذكورة داخل نثر حر.
- لا ينفذ قواعد DOM/browser/manual للمكونات، ولا يقيس contrast أوfocus أوresponsive أوقارئ الشاشة.
- لا يثبت أن قيم colors متوافقة، ولا أن ARIA أوkeyboard behavior صحيحان لمجرد وجود strings في المصدر.

اختبارات الأداة تختبر اكتشاف ملفات تالفة ومحاور غير صالحة وأنواع قواعد مجهولة وروابط مفقودة وتبعيات دورية، وعدم احتساب التعليقات كتوكِنات، ورموز خروج CLI. لا تستبدل اختبارات المكونات القادمة.

نتيجة الدفعة الأولى محفوظة في `batch-1-result.json` كملخص قابل للمراجعة؛ أعد التشغيل للحصول على القائمة التفصيلية الحالية. لا تُستخدم أرقام التحذيرات كbaseline يسمح بتجاوزها مستقبلًا.

## إضافات الدفعة الثانية

يشمل الفحص الآن styles/base وCSS/JS المرتبطين بأمثلة tests/fixtures، ودورات aliases المركزية وتعريفات custom properties المحلية غير المسجلة. السياسة في standards/foundation-policy.json تقصر المتغيرات المحلية على ملفات وأسماء محددة. الاستثناءات البصرية/الاتجاهية لها قيمة حرفية وسبب وعدد occurrences؛ إضافة استعمال أوتغيير القيمة يفشل الفحص بدل توسيع الاستثناء تلقائيًا. media query literals تقارن بالـtoken المحدد.

`batch-2-result.json` نتيجة مستقلة لا تمحو التاريخ في batch-1. نجاح strict يعني نجاح الفحوص الساكنة المنفذة مع الاستثناءات المعلنة، ولا يعني تنفيذ قواعد الوصول للمكونات.

### اختبار Chrome المحلي

يتطلب Node 22+ وChrome. شغل متصفح اختبار مستقل ثم الأداة؛ لا npm packages:

```sh
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-first-run --remote-debugging-port=9337 --user-data-dir=/tmp/ds-foundation-chrome about:blank
```

وفي terminal آخر من جذر المشروع:

```sh
node tests/browser-foundation.mjs foundation . /tmp/ds-foundation-browser.json
```

تكتب الأداة JSON وPNG للمثال. تحجب الطلبات الخارجية أثناء الفحص، وتغلق tab الاختبار بعده؛ أغلق عملية متصفح الاختبار عند الانتهاء. وضع snapshot اختياري لمراجعة الخصائص المقاسة في showcases:

```sh
node tests/browser-foundation.mjs snapshot . /tmp/ds-component-styles.json
```
