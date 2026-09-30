from html.parser import HTMLParser
import importlib.util
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT / 'products/authority'
SPEC = importlib.util.spec_from_file_location('build_site', ROOT / 'scripts/build_site.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)


class InteractionDocument(HTMLParser):
    def __init__(self):
        super().__init__()
        self.h1 = 0
        self.accordions = 0
        self.expanded = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get('class', '').split())
        if tag == 'h1':
            self.h1 += 1
        if tag == 'button' and 'accordion__trigger' in classes:
            self.accordions += 1
            self.expanded.append(attributes.get('aria-expanded'))


class AuthorityInteractionTests(unittest.TestCase):
    def test_a07_contact_uses_product_channels_privacy_and_help(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            BUILDER.build_product('authority', output)
            markup = (output / 'contact.html').read_text()

        document = InteractionDocument()
        document.feed(markup)
        self.assertEqual(document.h1, 1)
        self.assertIn('demo@example.invalid', markup)
        self.assertIn('رقم عرض غير مخصص للاتصال', markup)
        self.assertIn('لا تُرسل أو تُخزن الرسالة أو المرفقات', markup)
        self.assertIn('راجع الخدمات والأسئلة الشائعة', markup)
        self.assertIn('<fieldset class="contact-form__fields" disabled>', markup)
        self.assertNotIn('الجهة النموذجية', markup)

    def test_a08_faq_uses_all_approved_questions_and_contact_cta(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            BUILDER.build_product('authority', output)
            markup = (output / 'faq.html').read_text()

        document = InteractionDocument()
        document.feed(markup)
        self.assertEqual(document.h1, 1)
        self.assertEqual(document.accordions, 6)
        self.assertEqual(document.expanded, ['true'] * 6)
        self.assertIn('هل تصدر هيئة نماء تراخيص رسمية؟', markup)
        self.assertIn('href="contact.html"', markup)
        self.assertIn('sections/faq/faq.runtime.js', markup)
        self.assertIn('<html lang="ar" dir="rtl">', markup)

    def test_a07_a08_use_only_shared_templates(self):
        for name in ('contact', 'faq'):
            self.assertFalse((PRODUCT / 'templates' / name).exists())
            self.assertFalse((PRODUCT / 'assets' / f'{name}.css').exists())
        source = '\n'.join(
            path.read_text()
            for path in (
                PRODUCT / 'content/demo/contact.json',
                PRODUCT / 'content/demo/faq.json',
                PRODUCT / 'pages/contact.json',
                PRODUCT / 'pages/faq.json',
            )
        )
        self.assertNotIn('products/ministry/', source)


if __name__ == '__main__':
    unittest.main()
