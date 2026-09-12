from pathlib import Path
from build_site import render, ASSETS
root=Path(__file__).resolve().parents[1]
for name in ['select','textarea']:
 body='<h1>'+name+'</h1><p>حقول عادية، خطأ، وتعطيل؛ جرّب التركيز بلوحة المفاتيح والتحويم.</p>'
 for state in ['default','error','disabled']:
  values=dict(id=name+'-'+state,name=name+'-'+state,label=state,placeholder='أدخل النص',attributes=' disabled' if state=='disabled' else '',options='<option>اختر الفئة</option><option>استفسار</option><option>اقتراح</option>')
  field=render('components/'+name+'/template.html',values,('attributes','options'))
  if state!='default':field=field.replace('text-input--filled-darker','text-input--filled-darker text-input--'+state)
  if name=='select' and state=='disabled':field=field.replace('<select ','<select disabled ')
  if state=='error':field=field.replace(' hidden></p>','>مثال على رسالة التحقق.</p>').replace('aria-describedby=','aria-invalid="true" aria-describedby=')
  body+='<div class="ds-reading">'+field+'</div>'
 folder=root/'components'/name/'showcases';folder.mkdir(exist_ok=True)
 (folder/'index.html').write_text('<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+name+'</title>'+''.join('<link rel="stylesheet" href="../../../'+a+'">' for a in ASSETS)+'<body><main class="ds-container ds-stack">'+body.replace('src="components/','src="../../../components/')+'</main></body></html>')
