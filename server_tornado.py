import tornado.ioloop
import tornado.web
from config import server_http_port
# 配置你的操作系统或是进程管理器来开启服务器运行这个程序.
# 请注意增加打开文件描述符的个数是十分重要的
# (来避免 “Too many open files”-的错误).
# 如果要增加这个限制 ( 假设要把它设置为50000 )
# 你可以使用 ulimit 命令, 修改 /etc/security/limits.conf
# 或者在你的 supervisord 中配置 minfds .
#http://blog.sina.com.cn/s/blog_5f66526e0100xl5t.html

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        with open('results.html','r') as f:
            self.write(f.read())
        #application.count += 1
        #print(application.count)
class XiguaHandler(tornado.web.RequestHandler):
    def get(self):
        with open('xigua.html','r') as f:
            self.write(f.read())

class HuajiaoHandler(tornado.web.RequestHandler):
    def get(self):
        with open('huajiao.html','r') as f:
            self.write(f.read())

class CddhHandler(tornado.web.RequestHandler):
    def get(self):
        with open('cddh.html','r') as f:
            self.write(f.read())

class ZscrHandler(tornado.web.RequestHandler):
    def get(self):
        with open('zscr.html','r') as f:
            self.write(f.read())

class HjsmHandler(tornado.web.RequestHandler):
    def get(self):
        with open('hjsm.html','r') as f:
            self.write(f.read())

class TimeHandler(tornado.web.RequestHandler):
    def get(self):
        with open('time.html','r') as f:
            self.write(f.read())

class Dan_HaokanHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/haokan.html','r') as f:
            self.write(f.read())

class Dan_TiebaHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/tieba.html','r') as f:
            self.write(f.read())

class Dan_XiguashipinHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/xiguashipin.html','r') as f:
            self.write(f.read())

class Dan_HuajiaoHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/huajiao.html','r') as f:
            self.write(f.read())

class Dan_ChongdingdahuiHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/chongdingdahui.html','r') as f:
            self.write(f.read())

class Dan_ZhishichaorenHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/zhishichaoren.html','r') as f:
            self.write(f.read())

class Dan_YoukuHandler(tornado.web.RequestHandler):
    def get(self):
        with open('./dange/youku.html','r') as f:
            self.write(f.read())

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/xigua", XiguaHandler),
    (r"/huajiao", HuajiaoHandler),
    (r"/cddh", CddhHandler),
    (r"/zscr", ZscrHandler),
    (r"/hjsm", HjsmHandler),
    (r"/time", TimeHandler),
    (r"/dange/haokan", Dan_HaokanHandler),
    (r"/dange/tieba", Dan_TiebaHandler),
    (r"/dange/xiguashipin", Dan_XiguashipinHandler),
    (r"/dange/huajiao", Dan_HuajiaoHandler),
    (r"/dange/chongdingdahui", Dan_ChongdingdahuiHandler),
    (r"/dange/zhishichaoren", Dan_ZhishichaorenHandler),
    (r"/dange/youku", Dan_YoukuHandler)
])
if __name__ == "__main__":
    #application.count = 0
    print("Server Start")
    application.listen(server_http_port)
    tornado.ioloop.IOLoop.instance().start()
