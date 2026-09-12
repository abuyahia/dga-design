"""Generate a card showcase from the canonical service data and renderer."""
from pathlib import Path
import json
try:
 from .build_site import render
 from .service_markup import service_card
except ImportError:
 from build_site import render
 from service_markup import service_card
ROOT=Path(__file__).resolve().parents[1]
data=json.loads((ROOT/'site/government.json').read_text())
styles=['token.css','styles/base/global.css','styles/base/layout.css','assets/fonts/fonts.css','components/card/card.css','components/tag/tag.css','components/button/button.css','components/service-card/service-card.css','templates/service/service.css']
body=''.join(service_card(service,render,'example-') for service in data['services'])
# Relative links deliberately point to the built site; it contains all canonical assets and destinations.
body=body.replace('src="components/', 'src="../../../dist/government/components/').replace('src="templates/', 'src="../../../dist/government/templates/').replace('href="service-', 'href="../../../dist/government/service-')
page='<!doctype html><html lang="ar" dir="rtl"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>بطاقات الخدمات</title>'+''.join('<link rel="stylesheet" href="../../../'+s+'">' for s in styles)+'<body><main class="ds-container"><h1>بطاقات الخدمات</h1><div class="service-catalog__grid">'+body+'</div></main></body></html>'
base=ROOT/'components/service-card/showcases';base.mkdir(exist_ok=True);(base/'index.html').write_text(page)
