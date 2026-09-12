import unittest
from scripts.feedback_markup import render_feedback
from scripts.build_site import render

class FeedbackTests(unittest.TestCase):
 def test_statistics_validate_and_do_not_invent_activity(self):
  self.assertNotIn('1544',render_feedback('service','x',render))
  for stats in [{'count':-1,'average':3},{'count':2,'average':float('nan')},{'count':True,'average':2},{'count':4,'average':6}]:
   with self.assertRaises(ValueError):render_feedback('service','x',render,stats)
  self.assertIn('3.9',render_feedback('service','x',render,{'count':1544,'average':3.9}))
 def test_subject_and_identifier_are_escaped(self):
  markup=render_feedback('page','"><script>alert(1)</script>',render,prefix='x" onmouseover="bad')
  self.assertNotIn('<script>',markup)
  self.assertIn('&quot;',markup)
 def test_page_and_service_have_distinct_controls(self):
  page=render_feedback('page','about.html',render)
  service=render_feedback('service','new-request',render)
  self.assertIn('data-feedback="yes"',page)
  self.assertNotIn('name="score"',page)
  self.assertEqual(service.count('name="score"'),5)
  self.assertNotIn('name="reason"',service)
