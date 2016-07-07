# encoding: utf8
"""
Wrapper to integrate CGI scripts into django views.

This method preserves the shortcommings of the CGI deployment, but may be adequate
when the performance hit caused by CGI spawning a new process for each request is
negligible, a legacy CGI executable needs to be embedded in a new application or
the ease of deployment is a priority.
"""

from django.http import FileResponse, HttpResponseServerError

import subprocess
import os
import tempfile
import shutil

__version__ = '0.2.0'
__all__ = [ 'cgi_wrap' ]

def try_delete(filename):
    try:
        os.unlink(filename)
    except:
        pass

class HttpResponseFile(object):
    filename = None
    fh = None
    delete_on_close = False
    headers = {}
    status = 200
    body_start = 0

    def __init__(self, filename, delete_on_close=False):
        self.filename = filename
        self.fh = open(filename, 'rb')
        self.delete_on_close = delete_on_close
        self._parse_headers()
        self.body_start = self.fh.tell()

    def _parse_headers(self):
        while True:
            headerline = self.fh.readline().strip()
            if headerline == b'': # end of headers
                break
            if headerline.startswith(b'HTTP/'):
                try:
                    self.status = int(headerline.split(b' ')[1])
                except:
                    pass
                continue
            try:
                sep_pos = headerline.index(b': ')
                self.headers[headerline[:sep_pos].decode('utf-8')] = headerline[sep_pos+2:].decode('utf-8')
            except (IndexError, ValueError):
                pass
        if 'Status' in self.headers:
            try:
                self.status = int(self.headers.pop('Status').split(' ')[0])
            except:
                pass

    def read(self, *a, **kw):
        return self.fh.read(*a, **kw)

    def close(self):
        self.fh.close()
        if self.delete_on_close:
            try_delete(self.filename)

def cgi_wrap(request, cgi_binary, env={}, cwd=None, query_string=None,
            logger=None):
    """Wrap a CGI executable to it into a django view

        Arguments:

        request: The django request object passed to the view.

        cgi_binary: path to the CGI executable. 
            When the executable needs command line arguments, a list 
            of strings starting with the path can be provided. Otherwise
            a string is sufficient.

        env: dict of environment variables to pass to the executable
            Values from this dict will overide values set by this wrapper.

        cwd: work directory to execute the CGI executable in.

        query_string: query string to send to the CGI executable.
            This is only a method to override/modify the query string
            of the original request, which will be used normaly.

        logger: instance of a logging.Logger to log eventual errors to

        
        Returns a django response object. Data returned by the CGI will
        be streamed to the client.
    """
    if type(cgi_binary) not in (list, tuple):
        cgi_binary = [cgi_binary, ]
    # set CGI environment variables
    env_predef = {}
    for _pt in [ 'HTTP_HOST',
                'HTTP_USER_AGENT',
                'QUERY_STRING',
                'REMOTE_HOST',
                'REMOTE_USER',
                'SERVER_NAME',
                'SERVER_PORT',
                'REQUEST_METHOD' ]:
        val = request.META.get(_pt)
        if val is not None:
            env_predef[_pt] = val
    env_predef['PATH'] = os.environ.get('PATH')
    env_predef['SCRIPT_NAME'] = request.path
    env_predef['SCRIPT_FILENAME'] = cgi_binary[0]
    env_predef['SCRIPT_URI'] = request.path
    env_predef['SERVER_SOFTWARE'] = __name__ # name of this module
    if query_string:
        env_predef['QUERY_STRING'] = query_string

    # use the user-supplied environment settings
    env_predef.update(env)

    tmpfh = tempfile.NamedTemporaryFile(delete=False)
    try:
        proc = subprocess.Popen(cgi_binary,
                stdin=subprocess.PIPE,
                stdout=tmpfh,
                env=env_predef,
                cwd=cwd)
        shutil.copyfileobj(request, proc.stdin)
        stdout, stderr = proc.communicate()
        rc = proc.wait()

        if logger is not None:
            if rc != 0:
                logger.err('CGI executable terminated with rc={0}'.format(rc))
            if stderr:
                for line in stderr.split('\n'):
                    logger.err('CGI err: {0}'.format(line))

        if rc != 0:
            try_delete(tmpfh.name)
            msgparts = ['CGI binary terminated with rc={0}.'.format(rc)]
            if stderr:
                msgparts.append(stderr)
            return HttpResponseServerError(
                    content = ' '.join(msgparts))

        response_file = HttpResponseFile(tmpfh.name, delete_on_close=True)
        response = FileResponse(response_file, status=response_file.status)
        for header, value in response_file.headers.items():
            response[header] = value
        return response
    except:
        try_delete(tmpfh.name)
        raise
