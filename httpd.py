# coding: utf8
import argparse
import socket

from multiprocessing import Process

from net_http import set_response_header, get_response
from config import host, port, AMOUNT_THREAD, PROJECT_ROOT, AMOUNT_CPU


def thread_def(server_sock):
    while True:

        client_sock, client_addr = server_sock.accept()
        response_dict = get_response(client_sock)
        response_dict['response_body'] = ''.join(response_dict['response_body'])
        set_response_header(client_sock, response_dict)
        client_sock.close()


def run_forever():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-host', type=str, help="Set host address (default is {})".format(host))
    parser.add_argument('-p', type=int, help="Set port (default is {})".format(port))
    parser.add_argument('-c', type=int, help="Set number of CPU (default is {})".format(AMOUNT_CPU))
    parser.add_argument('-r', type=str, help="Set root directory (default is {}".format(PROJECT_ROOT))
    args = vars(parser.parse_args())

    new_host = args['host'] or host
    new_port = args['p'] or port
    cpu_count = args['c'] or AMOUNT_CPU

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((new_host, new_port))
    server_sock.listen(1024)

    workers = []
    for i in range(2):
        worker = Process(target=thread_def, args=(server_sock,))
        workers.append(worker)
        worker.start()
    for el in workers:
        el.join()

if __name__ == '__main__':
    run_forever()
