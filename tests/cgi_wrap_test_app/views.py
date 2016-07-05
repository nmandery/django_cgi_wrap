# encoding: utf8

from django_cgi_wrap import cgi_wrap
import os

EXAMPLE_CGI = os.path.abspath(os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'example_cgi.py'
))
EXAMPLE_ARGS = ['foo', 'bar']

def example_cgi(request):
    return cgi_wrap(request, EXAMPLE_CGI)

def example_cgi_with_args(request):
    return cgi_wrap(request, [EXAMPLE_CGI,] + EXAMPLE_ARGS)
