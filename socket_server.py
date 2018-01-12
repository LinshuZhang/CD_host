# -*- coding=utf-8 -*-
import socketserver
import time
import os
from config import image_path
from result_class import Result
from config import server_socket_port
# Format: name_len      --- one byte
#         name          --- name_len bytes
#         data          --- variable length
# Save data to name into current directory
class MyTCPHandler (socketserver.StreamRequestHandler):
        def handle (self):
                name_len = ord(self.rfile.read(1))
                name = self.rfile.read(name_len)
                print("Get request:%s"%name)
                fd = open(name, 'wb')
                cont = self.rfile.read(4096)
                while cont:
                        fd.write(cont)
                        cont = self.rfile.read(4096)
                fd.close()
                print("Out :%s"%name)
                print("已经收到图片，开始尝试获取结果 {}".format(time.time()))
                result = Result(image_path)
                os.remove(image_path)
                print("已经收到结果删除图片 {}".format(time.time()))

if __name__ == '__main__':
    addr = ('', server_socket_port)
    server = socketserver.TCPServer(addr, MyTCPHandler)
    server.serve_forever()
