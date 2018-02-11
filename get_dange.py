# -*-coding = utf-8 -*-
import time
from multiprocessing.dummy import Pool as ThreadPool
import re
import socket
from websocket import create_connection
import websocket
from multiprocessing.dummy import Pool as ThreadPool

baseList = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-'

def changeBase(n,b):
    x,y = divmod(n,b)
    if x>0:
        return changeBase(x,b) + baseList[y]
    else:
        return baseList[y]

def to_connect(key):
    global ws
    header = {'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 SearchCraft/1.6.2 (Baidu; P1 5.0)',
          'Cookie': 'BAIDUID=DFAB19B2EA574D3C16184EE5FB3DFC24:FG=1; BAIDUCUID=7F84EDC811B9B674C59DBFD5DB2E2067|000000000000000',
          'Origin': 'https://secr.baidu.com',
          'Host': 'selab.baidu.com'
         }
    url = "wss://selab.baidu.com/nv/answer.sock/\
    ?xc=461df84f9425052f277326817299f973&EIO=3&transport=websocket"
    ws[key] = create_connection(url,header=header)
    ws[key].recv()
    ws[key].recv()
    ws[key].send(b'21')
    ws[key].recv()
    ws[key].send('40/nv/{}/answer'.format(key).encode())
    ws[key].recv()
    result =  ws[key].recv()
    if 'greet' in result:
        print("{} Connect Succeed".format(key))
    ws[key].recv()
def get_dange(key):
    first_time = 0
    to_connect(key)
    while True:
        try:
            ws[key].send(b'2')
            result =  ws[key].recv()
            result =  ws[key].recv()
            if result[:1] == '3':
                first_time += 1
                if first_time%20==0:
                    print("{} Connect Succeed".format(key))
            elif result[:1] == '4':
                print(time.time())
                print(read_result(result,key))
            else:
                print("{} Connect Failed".format(key))
            time.sleep(0.2)
        except:
            print("{} Connect Failed,try to reconnect".format(key))
            to_connect(key)

def read_result(result,key):
    tip = ''.join(re.findall('"tips":\"(.+?)\"',result))
    choice = re.findall('"text":\"(.+?)\"',result)
    prop = re.findall('"prop":(.+?)\}',result)
    string_list = []
    string_list.append(tip)
    string_list.append("\n选项概率：\n")
    for i in range(3):
        string_list.append('{} : {}\n'.format(choice[i+1],prop[i]))
    result_str = ''.join(string_list)
    result_to_write = ''.join(result_str)
    if not ('欢迎' in result_to_write):
        with open('./dange/{}.html'.format(key),'w') as f:
            f.write(result_to_write)
        return result_str
    else:
        return '已过滤'

def main():
    pool = ThreadPool(7)#机器是多少核便填多少，卤煮实在ubuntu14.04 4核戴尔电脑上跑的程序
    results = pool.map(get_dange,connect_way)
    pool.close()
    print("Pool is closed")
    pool.join()
    if (time.time() - record_time)>3:
        record_time = time.time()
        with open('./dange/time.html','w') as f:
            f.write(u'当前时间戳为{}'.format(time.time()))
            print('Now:{}'.format(time.time()))

if __name__ == "__main__":
    connect_way = ['haokan','weibo','xiguashipin','huajiao','chongdingdahui','zhishichaoren','youku']
    ws = {}
    main()
