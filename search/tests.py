from django.core.urlresolvers import reverse
from django.test import Client, TestCase


class TestSearch(TestCase):
    fixtures = ['test.json']

    def setUp(self):
        self.client = Client()

    def test_search_url_name(self):
        response = self.client.get(reverse('search'))
        self.assertEqual(200, response.status_code)

    def test_search_no_results(self):
        response = response = self.client.get(reverse('search'))
        self.assertIsNone(response.context[-1]['search_query'])
        self.assertEqual(0, response.context[-1]['search_results'].count())

        q = ''
        response = response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(0, response.context[-1]['search_results'].count())

        q = 'missing'
        response = response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(0, response.context[-1]['search_results'].count())

    def test_search_with_results(self):
        q = 'event'
        response = response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(3, response.context[-1]['search_results'].count())

        q = 'blog'
        response = response = self.client.get(reverse('search'), {'q': q})
        self.assertEqual(q, response.context[-1]['search_query'])
        self.assertEqual(1, response.context[-1]['search_results'].count())
