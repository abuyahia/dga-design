"""Focused build checks for Page Intro adoption, not a browser suite."""
import json
import tempfile
import unittest
from pathlib import Path
from html.parser import HTMLParser
from scripts.build_site import build, render
from scripts.page_intro_markup import render_page_intro


class IntroDOM(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.h1 = self.intros = self.intro_h1 = self.crumbs = self.current = 0
        self.stack = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get('class', '').split()
        if tag == 'section':
            self.stack.append('page-intro' in classes)
            self.intros += 'page-intro' in classes
        if tag == 'h1':
            self.h1 += 1
            self.intro_h1 += any(self.stack)
        if any(self.stack):
            self.crumbs += tag == 'li' and 'breadcrumb__item' in classes
            self.current += attrs.get('aria-current') == 'page'

    def handle_endtag(self, tag):
        if tag == 'section' and self.stack:
            self.stack.pop()


class AdoptionTests(unittest.TestCase):
    def test_consumers_build_with_one_canonical_intro_and_hierarchy(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            build('site/government.json', output)
            names = ['contact.html', 'content.html', 'service-new-request.html',
                     'faq.html', 'form.html', 'about.html', 'news.html', 'services.html']
            for name in names:
                with self.subTest(page=name):
                    markup = (output / name).read_text()
                    dom = IntroDOM(markup)
                    self.assertEqual((dom.h1, dom.intros, dom.intro_h1, dom.current), (1, 1, 1, 1))
                    self.assertEqual(dom.crumbs, 3 if name.startswith('service-') else 2)
                    self.assertNotIn('{{', markup)
                    for old in ('contact-page__intro', 'heavy-content__header', 'heavy-content__lead', 'heavy-content__overview', 'class="service-page__title"'):
                        self.assertNotIn(old, markup)
            self.assertIn('page-intro--compact', (output / 'faq.html').read_text())
            self.assertIn('page-intro--featured', (output / 'form.html').read_text())
            self.assertIn('form-page__required-note', (output / 'form.html').read_text())
            self.assertIn('data-table-of-contents', (output / 'content.html').read_text())
            self.assertIn('service-page__sidebar', (output / 'service-new-request.html').read_text())

    def test_optional_slots_omitted_and_custom_hierarchy_escaped(self):
        markup = render_page_intro({'title': '<Title>'}, render, breadcrumb_items=[
            {'label': '<Root>', 'href': 'root.html'}, {'label': '<Title>'},
        ])
        for optional in ('page-intro__eyebrow', 'page-intro__description', 'page-intro__extra'):
            self.assertNotIn(optional, markup)
        self.assertIn('&lt;Title&gt;', markup)
        self.assertIn('&lt;Root&gt;', markup)
        self.assertNotIn('<Title>', markup)
