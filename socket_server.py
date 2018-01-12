# -*- coding=utf-8 -*-
import socketserver

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

if __name__ == '__main__':
    addr = ('', 80)
    server = socketserver.TCPServer(addr, MyTCPHandler)
    server.serve_forever()
