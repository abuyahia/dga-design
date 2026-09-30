"""Focused Breadcrumb contract and consumer integration checks."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path
from scripts.breadcrumb_markup import render_breadcrumb
from scripts.build_site import render
from scripts.contact_markup import contact_page
from scripts.service_markup import overview
from scripts.page_intro_markup import render_page_intro


class BreadcrumbDOM(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.nodes = []
        self.depth = 0
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'nav' and attrs.get('class') == 'breadcrumb':
            self.depth += 1
        if self.depth:
            self.nodes.append((tag, attrs))

    def handle_endtag(self, tag):
        if tag == 'nav' and self.depth:
            self.depth -= 1


class BreadcrumbTests(unittest.TestCase):
    def assert_breadcrumb(self, markup, count):
        nodes = BreadcrumbDOM(markup).nodes
        self.assertEqual(sum(tag == 'nav' for tag, _ in nodes), 1)
        self.assertEqual(sum(tag == 'ol' for tag, _ in nodes), 1)
        self.assertEqual(sum(tag == 'li' for tag, _ in nodes), count)
        self.assertEqual(sum(tag == 'a' for tag, _ in nodes), count - 1)
        self.assertEqual(sum(a.get('aria-current') == 'page' for _, a in nodes), 1)
        self.assertEqual(sum(a.get('class') == 'breadcrumb__separator' for _, a in nodes), count - 1)

    def test_one_two_three_and_deeper_levels(self):
        for count in (1, 2, 3, 7):
            with self.subTest(count=count):
                items = [{'label': str(i), 'href': f'page-{i}.html'} for i in range(count)]
                items[-1] = {'label': 'Current', 'current': True}
                self.assert_breadcrumb(render_breadcrumb(items, render), count)

    def test_escaped_configurable_labels_and_destinations(self):
        markup = render_breadcrumb([
            {'label': '<Home & "root">', 'href': 'custom.html?q="a"&b=2'},
            {'label': '<Current>', 'href': 'ignored.html', 'current': True},
        ], render, navigation_label='Custom <trail>')
        self.assertIn('&lt;Home &amp; &quot;root&quot;&gt;', markup)
        self.assertIn('custom.html?q=&quot;a&quot;&amp;b=2', markup)
        self.assertIn('&lt;Current&gt;', markup)
        self.assertIn('Custom &lt;trail&gt;', markup)
        self.assertNotIn('ignored.html', markup)
        self.assertNotIn('index.html', markup)
        self.assert_breadcrumb(markup, 2)

    def test_reject_unsafe_urls_and_invalid_hierarchies(self):
        for href in ('javascript:alert(1)', 'data:text/html,x', '//evil.example', 'https://user@host.test', 'bad\n.html', '\\evil.test', 'http://host.test'):
            with self.subTest(href=href), self.assertRaises(ValueError):
                render_breadcrumb([{'label': 'Root', 'href': href}, {'label': 'Current'}], render)
        for items in ([], [{'label': ''}], [{'label': 'Root', 'current': True}, {'label': 'Last'}], [{'label': 'Last', 'current': False}], [{'label': 'Root'}, {'label': 'Last'}]):
            with self.subTest(items=items), self.assertRaises(ValueError):
                render_breadcrumb(items, render)

    def test_two_level_compatibility_and_page_intro(self):
        markup = render('components/breadcrumb/two-level.html', {
            'root_href': 'home.html', 'root_label': 'Home', 'current_label': 'Current',
        })
        self.assert_breadcrumb(markup, 2)
        self.assertNotIn('{{', markup)
        self.assertIn('home.html', markup)
        self.assert_breadcrumb(render_page_intro({'title': 'Current'}, render), 2)

    def test_service_and_contact_use_canonical_breadcrumb(self):
        data = json.loads(Path('site/government.json').read_text())
        service = overview(data['services'][0], data['services'], render, 'contact.html')
        contact = contact_page(data['contact'], render)
        self.assert_breadcrumb(service, 3)
        self.assert_breadcrumb(contact, 2)
        self.assertIn('href="services.html"', service)
        self.assertNotIn('{{breadcrumb}}', contact)
        self.assertNotIn('desktop-imgElements1.svg', contact)
        self.assertNotIn('templates/service/assets/main-imgElements.svg', service)
