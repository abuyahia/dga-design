import copy,json,unittest
from pathlib import Path
from scripts.contact_markup import contact_page,validate_contact
from scripts.build_site import render
class ContactTests(unittest.TestCase):
 def setUp(self):self.data=json.loads(Path('site/government.json').read_text())['contact']
 def test_escape_configured_content(self):
  self.data['description']='<script>alert(1)</script>'
  self.data['channels'][0]['value']='<img src=x>'
  markup=contact_page(self.data,render)
  self.assertNotIn('<script>',markup);self.assertIn('&lt;img',markup)
 def test_reject_unsafe_contact_destination(self):
  for href in ['javascript:alert(1)','//evil.example','http://insecure.example','https://user@host.test']:
   d=copy.deepcopy(self.data);d['channels'][0]['href']=href
   with self.assertRaises(ValueError):validate_contact(d)
 def test_configurable_contact_links(self):
  self.data['channels'][0]['href']='tel:+966123456789'
  self.assertIn('href="tel:+966123456789"',contact_page(self.data,render))
  self.data['categories']=[]
  with self.assertRaises(ValueError):validate_contact(self.data)
