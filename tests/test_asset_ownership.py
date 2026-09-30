"""Targeted canonical-owner asset checks for F03."""
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser
from scripts.build_site import build


class Assets(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.css, self.js = [], []
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'link' and a.get('rel') == 'stylesheet': self.css.append(a['href'])
        if tag == 'script' and a.get('src'): self.js.append(a['src'])


class OwnershipTests(unittest.TestCase):
    def test_canonical_assets_exist_once_in_dependency_order(self):
        expected = {
            'faq.html': ['sections/page-intro/page-intro.css', 'sections/faq/faq.css', 'sections/contact-cta/contact-cta.css', 'sections/faq/faq.runtime.js'],
            'content.html': ['sections/heavy-content/heavy-content.css', 'components/table-of-contents/table-of-contents.js'],
            'service-new-request.html': ['components/tab/tab.js', 'templates/service/service.js'],
            'form.html': ['components/progress-indicator/progress-indicator.js', 'templates/form/form.js'],
            'contact.html': ['components/file-upload/file-upload.js', 'templates/contact/contact.js'],
            'about.html': ['sections/page-intro/page-intro.css'],
            'news.html': ['sections/page-intro/page-intro.css'],
            'services.html': ['sections/page-intro/page-intro.css', 'templates/service/service.js'],
        }
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            build('site/government.json', output)
            for page, required in expected.items():
                with self.subTest(page=page):
                    text = (output / page).read_text()
                    assets = Assets(text)
                    refs = assets.css + assets.js
                    self.assertEqual(len(refs), len(set(refs)))
                    for ref in refs: self.assertTrue((output / ref).is_file(), ref)
                    for ref in required: self.assertIn(ref, refs)
                    self.assertNotIn('templates/faq/', text)
                    self.assertNotIn('templates/content/content.js', text)
                    self.assertNotIn('{{', text)
                    if page != 'contact.html':
                        self.assertNotIn('templates/contact/contact.css', refs)
                    for owner, consumer in [('components/tab/tab.js', 'templates/service/service.js'), ('components/file-upload/file-upload.js', 'templates/contact/contact.js'), ('components/progress-indicator/progress-indicator.js', 'templates/form/form.js')]:
                        if owner in assets.js: self.assertLess(assets.js.index(owner), assets.js.index(consumer))
            faq = (output / 'faq.html').read_text()
            self.assertIn('sections/contact-cta/assets/contact.svg', faq)
            self.assertTrue((output / 'sections/contact-cta/assets/contact.svg').is_file())

    def test_old_files_no_longer_own_contracts(self):
        self.assertNotIn('.page-intro', Path('templates/government/composition.css').read_text())
        self.assertNotIn('.heavy-content__blocks', Path('templates/content/content.css').read_text())
        self.assertFalse(Path('templates/content/content.js').exists())
        self.assertFalse(Path('templates/faq/faq.css').exists())
        self.assertNotIn("addEventListener('keydown'", Path('templates/service/service.js').read_text())
        self.assertNotIn("file.addEventListener('change'", Path('templates/contact/contact.js').read_text())
