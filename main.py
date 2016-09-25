# coding: utf8

import socket
from threading import Thread
from net_http import set_response_header, get_response
from config import host, port, amount_thread


def thread_def(server_sock):
    while True:

        client_sock, client_addr = server_sock.accept()
        response_dict = get_response(client_sock)
        response_dict['response_body'] = ''.join(response_dict['response_body'])
        set_response_header(client_sock, response_dict)
        client_sock.close()


def run_forever():

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(10)

    for x in range(amount_thread):
            thread = Thread(target=thread_def, args=(server_sock,))
            thread.start()

if __name__ == '__main__':
    run_forever()
