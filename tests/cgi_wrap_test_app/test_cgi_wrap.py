#!/usr/bin/env python

from django.test import SimpleTestCase
import json
import urlparse

from .views import EXAMPLE_CGI, EXAMPLE_ARGS


class ExampleCgiTests(SimpleTestCase):

    uri = '/example_cgi'
    uri_with_args = '/example_cgi_with_args'

    def data_from_response(self, response):
        self.assertEqual(response.status_code, 200)
        return json.loads(''.join(response.streaming_content))

    def test_cgi_output(self):
        data = self.data_from_response(self.client.get(self.uri))
        self.assertTrue('greeting' in data)
        self.assertTrue('env' in data)
        self.assertTrue('args' in data)
        self.assertEquals(data['env']['REQUEST_METHOD'], 'GET')
        self.assertEquals(data['env']['SCRIPT_NAME'], self.uri)
        self.assertEquals(data['env']['SCRIPT_FILENAME'], EXAMPLE_CGI)
        self.assertEquals(data['args'], [])

    def test_cgi_output_with_args(self):
        data = self.data_from_response(self.client.get(self.uri_with_args))
        self.assertTrue('greeting' in data)
        self.assertTrue('env' in data)
        self.assertTrue('args' in data)
        self.assertEquals(data['args'], EXAMPLE_ARGS)


    def test_cgi_get_queryparams(self):
        data_in = {
            'val1': ['foo',],
            'val2': ['BAR',],
        }
        response = self.data_from_response(self.client.get(self.uri, data_in))
        query_string = response['env']['QUERY_STRING']
        data_out = urlparse.parse_qs(query_string)
        self.assertEquals(data_in, data_out)

    def test_cgi_post_queryparams(self):
        data_in = {
            'val1': ['foofoofoo',],
        }
        response = self.data_from_response(self.client.post(self.uri, data_in))
        self.assertTrue('foofoofoo', response['body'])
