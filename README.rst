Wrapper to integrate CGI scripts into django views.

.. image:: https://travis-ci.org/nmandery/django_cgi_wrap.svg?branch=master
       :target: https://travis-ci.org/nmandery/django_cgi_wrap

Simple function to wrap old-style CGI scripts/binaries to integrate them
into the views of a django app.

This method preserves the shortcommings of the CGI deployment, but may be adequate
when the performance hit caused by CGI spawning a new process for each request is
negligible, a legacy CGI executable needs to be embedded in a new application or
the ease of deployment is a priority.

Data returned by the CGI will be streamed to the client.

Example:

.. code::

    from django_cgi_wrap import cgi_wrap

    def example_view(request):
        return cgi_wrap(request, "/usr/bin/mapserv")


Also see the "tests" directory for a working example as well as the doc-strings of the
module itself.
