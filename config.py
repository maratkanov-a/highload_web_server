#coding: utf-8
import os

AMOUNT_THREAD = 1

AMOUNT_CPU = 1

MAX_PACKET = 32768

host = 'localhost'
port = 80


STATUS_DICT = {
        '200': 'OK',
        '403': 'Forbidden',
        '404': 'Not Found',
        '405': 'Method Not Allowed'
    }

CONTENT_TYPE_DICT = {
        'html': 'text/html',
        'css': 'text/css',
        'js': 'text/javascript',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'swf': 'application/x-shockwave-flash'
    }


PROJECT_ROOT = os.path.dirname(__file__)
PATH_STATIC = PROJECT_ROOT + ''
