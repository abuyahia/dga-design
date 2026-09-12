from pathlib import Path
from build_site import render, ASSETS
root=Path(__file__).resolve().parents[1]
body='<h1>Radio Button</h1><p>جرّب التحويم والضغط والتنقل بلوحة المفاتيح. تعرض المجموعات أيضًا حالتي التعطيل.</p>'
for theme in ['brand','neutral']:
 body+='<fieldset><legend>'+theme+'</legend>'
 for value,label,attributes in [('one','خيار أول',''),('two','خيار محدد',' checked'),('disabled','غير متاح',' disabled'),('disabled-checked','محدد وغير متاح',' checked disabled')]:
  name=theme if not attributes.endswith('disabled') else theme+'-'+value
  body+=render('components/radio/template.html',dict(name=name,value=value,label=label,attributes=attributes),('attributes',)).replace('radio--brand','radio--'+theme)
 body+='</fieldset>'
folder=root/'components/radio/showcases';folder.mkdir(exist_ok=True)
(folder/'index.html').write_text('<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Radio Button</title>'+''.join('<link rel="stylesheet" href="../../../'+a+'">' for a in ASSETS)+'<body><main class="ds-container">'+body+'</main></body></html>')
