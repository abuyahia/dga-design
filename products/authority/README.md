# Authority Website Product

منتج مستقل لموقع هيئة حكومية قابل للتهيئة، مبني فوق Foundation والغلاف الحكومي المشترك. هوية **هيئة نماء التجريبية** وجميع خدماتها وبرامجها ووثائقها خيالية ولا تمثل جهة حكومية فعلية.

## Build

```bash
python3 scripts/build_site.py --product authority
```

يكتب الناتج في `dist/products/authority/`. لا يقرأ المنتج أي قالب أو أصل من `products/ministry/`، ولا تختار ملفات JSON أي مسار Python أو module.

## Content ownership

- حدود المنتج والهوية والتنقل والتذييل في `products/authority/`.
- السجلات التجريبية ذات المصدر الواحد في `content/demo/`.
- المصيّرات الخاصة دلاليًا بالهيئة: Executive Profile، Regulatory، وتركيب Home.
- الأخبار والمحفظة والموارد والخدمات تستخدم عقودًا ومكوّنات مشتركة.

ملف Home الافتراضي هو `regulatory`. سياسة التركيب الواحدة تدعم أيضًا `enablement` و`development` دون fork للقالب. الإحصاءات غير معروضة لعدم وجود مصدر وقياس معتمدين في بيانات العرض.
