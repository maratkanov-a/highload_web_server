#coding: utf-8
import socket
from config import MAX_PACKET


def recv_all(sock):
    """
    Читает данные из сокета, хак со временем
    """
    return sock.recv(MAX_PACKET)


def normalize_line_endings(s):
    """
    Переводим строку с разными разделителями,
    к универсальному формату \n

    Спасибо python :)
    """
    return ''.join((line + '\n') for line in s.splitlines())


def response_dict(body, status, content_type, request_method):
    return {
        'response_body': body,
        'status': status,
        'content_type': content_type,
        'request_method': request_method
    }