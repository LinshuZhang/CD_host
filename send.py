# -*- coding=utf-8 -*-

from socket import *
import os.path
import sys
from config import image_path,server_host,client_socket_port
target = (server_host, client_socket_port)

def get_header (name):
    leng = len(name)
    assert leng < 250
    return chr(leng) + name

def send_file (name):
    basename = os.path.basename(name)
    header = get_header(basename).encode()
    cont = open(name,'rb').read()
    s = socket (AF_INET, SOCK_STREAM)
    s.connect(target)
    s.sendall (header)
    s.sendall (cont)
    s.close()

if __name__ == '__main__':
    target = (server_host, client_socket_port)
    send_file(image_path)
