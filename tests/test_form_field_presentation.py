"""Focused ownership and markup checks for shared form-field presentation."""
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

from scripts.build_site import build


class FieldDOM(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.ids = set()
        self.labels = []
        self.required_markers = 0
        self.affixes = 0
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if 'id' in attrs:
            self.ids.add(attrs['id'])
        if tag == 'label':
            self.labels.append(attrs.get('for'))
        if 'label__required' in classes:
            self.required_markers += 1
            self.assert_hidden(attrs)
        if 'input-affix' in classes:
            self.affixes += 1

    def assert_hidden(self, attrs):
        if attrs.get('aria-hidden') != 'true':
            raise AssertionError('Required marker must remain decorative')


class FormFieldPresentationTests(unittest.TestCase):
    def test_contact_and_form_use_shared_field_contracts(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            build('site/government.json', output)
            contact = (output / 'contact.html').read_text()
            form = (output / 'form.html').read_text()

            for name, markup in [('contact', contact), ('form', form)]:
                with self.subTest(page=name):
                    dom = FieldDOM(markup)
                    self.assertGreater(dom.required_markers, 0)
                    associated = [target for target in dom.labels if target is not None]
                    self.assertTrue(associated)
                    self.assertTrue(all(target in dom.ids for target in associated))
                    self.assertIn('components/text-input/text-input.css', markup)
                    self.assertNotIn('contact-required', markup)

            self.assertEqual(FieldDOM(form).affixes, 4)
            self.assertIn('components/input-affix/input-affix.css', form)
            self.assertIn('components/file-upload/file-upload.css', contact)
            self.assertNotIn('templates/contact/contact.css', form)
            self.assertIn('templates/contact/contact.css', contact)

    def test_shared_selectors_have_one_canonical_owner(self):
        text_input = Path('components/text-input/text-input.css').read_text()
        affix = Path('components/input-affix/input-affix.css').read_text()
        upload = Path('components/file-upload/file-upload.css').read_text()
        contact = Path('templates/contact/contact.css').read_text()
        form = Path('templates/form/form.css').read_text()

        self.assertIn('.label__required', Path('components/label/label.css').read_text())
        self.assertIn('.text-input--label-semibold .text-input__label', text_input)
        self.assertIn('.text-input__field > .input-affix', affix)
        for selector in ('.file-upload__file', '.file-item__name', '.file-item__row'):
            self.assertIn(selector, upload)
            self.assertNotIn(selector, contact)
        for selector in ('contact-required', '.text-input__label', '.input-affix'):
            self.assertNotIn(selector, contact)
            self.assertNotIn(selector, form)

        builder = Path('scripts/build_site.py').read_text()
        self.assertIn("'templates/contact/contact.css': {'contact'}", builder)
        self.assertNotIn("'templates/contact/contact.css': {'contact', 'form-template'}", builder)
