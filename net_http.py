import urllib
from config import PATH_STATIC, PROJECT_ROOT, STATUS_DICT, CONTENT_TYPE_DICT
import os
from snippets import recv_all, normalize_line_endings, response_dict


def get_response(client_sock):
    request = normalize_line_endings(recv_all(client_sock))
    try:
        request_head, request_body = request.split('\n\n', 1)
    except ValueError:
        return response_dict('No', '404', 'html', '')

    request_head = request_head.splitlines()
    request_headline = request_head[0]

    request_method, request_url, request_proto = request_headline.split(' ', 3)
    request_url = urllib.unquote(request_url)
    if 'POST' in request_method:
        return response_dict(['GET only'], '405', 'html', request_method)

    response_body = list()
    request_url = request_url.split('?')[0]

    try:
        if PROJECT_ROOT in os.path.abspath(os.path.join(PATH_STATIC, request_url[1:])):
            with open((PATH_STATIC + request_url).replace('%20', ' ')) as f:
                response_body.append(f.read())
        else:
            return response_dict(['Forbidden \n', 'You don`t have permission to access'], '403', 'html', request_method)

    except IOError as e:
        if 'Is a directory' in e.strerror:
            if os.path.isfile(os.path.join(e.filename, 'index.html')):
                return response_dict(["<html>Directory index file</html>\n"], '200', 'html', request_method)
            else:
                return response_dict(["No again"], '403', 'html', request_method)
        return response_dict(response_body, '404', request_url.split('.')[-1], request_method)
    return response_dict(response_body, '200', request_url.split('.')[-1], request_method)


def set_response_header(client_sock, response_dict):
    if not response_dict['status']:
        response_dict['status'] = '200'

    if not response_dict['content_type']:
        response_dict['content_type'] = 'html'

    if not response_dict['request_method']:
        response_dict['request_method'] = 'GET'

    response_headers = {
        'Content-Type': '{0}'.format(CONTENT_TYPE_DICT[response_dict['content_type'].lower()] if response_dict[
                                                                                                     'content_type'].lower() in CONTENT_TYPE_DICT else 'text/html'),
        'Content-Length': len(response_dict['response_body']),
        'Server': 'amazing_python',
        'Connection': 'close',
    }

    response_headers_raw = ''.join('%s: %s\r\n' % (k, v) for k, v in response_headers.iteritems())

    response_proto = 'HTTP/1.1'
    response_status_text = STATUS_DICT[response_dict['status']]

    client_sock.send('{0} {1} {2}\r\n'.format(response_proto, response_dict['status'], response_status_text))
    client_sock.send(response_headers_raw)
    client_sock.send('\r\n')
    if 'HEAD' not in response_dict['request_method']:
        client_sock.send(response_dict['response_body'])
