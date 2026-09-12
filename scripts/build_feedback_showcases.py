"""Generate standalone examples from the canonical feedback renderers."""
from pathlib import Path
from build_site import render, ASSETS
from feedback_markup import render_feedback
ROOT=Path(__file__).resolve().parents[1]
for name,kind in [('page-feedback','page'),('service-rating','service')]:
    stats={'count':1544,'average':3.9} if kind=='service' else {'count':100,'percentage':80}
    body='<h1>معاينة المكوّن</h1><p>الأرقام في هذا المثال بيانات توضيحية فقط.</p>' + render_feedback(kind,'example',render,stats,prefix='example') + render_feedback(kind,'second-example',render,prefix='second-example')
    body=body.replace('src="components/', 'src="../../../components/')
    page='<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>'+name+'</title>'+''.join('<link rel="stylesheet" href="../../../'+s+'">' for s in ASSETS)+'<body><main>'+body+'</main><script src="../../../styles/composites/feedback.js"></script></body></html>'
    folder=ROOT/'components'/name/'showcases';folder.mkdir(exist_ok=True);(folder/'index.html').write_text(page)
