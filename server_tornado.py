import tornado.ioloop
import tornado.web

# 配置你的操作系统或是进程管理器来开启服务器运行这个程序. 
# 请注意增加打开文件描述符的个数是十分重要的 
# (来避免 “Too many open files”-的错误). 
# 如果要增加这个限制 ( 假设要把它设置为50000 ) 
# 你可以使用 ulimit 命令, 修改 /etc/security/limits.conf 
# 或者在你的 supervisord 中配置 minfds .
#http://blog.sina.com.cn/s/blog_5f66526e0100xl5t.html

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        with open('results.txt','r') as f:
            self.write(f.read())
        #application.count += 1
        #print(application.count)

application = tornado.web.Application([
    (r"/", MainHandler),
])
if __name__ == "__main__":
    #application.count = 0
    application.listen(7768)
    tornado.ioloop.IOLoop.instance().start()
