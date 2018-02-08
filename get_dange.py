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
    ws[key] = create_connection("wss://selab.baidu.com/nv/answer.sock/?EIO=3&transport=websocket")
    ws[key].recv()
    ws[key].recv()
    ws[key].send(b'21')
    ws[key].recv()
    ws[key].send('40/nv/{}/answer'.format(key).encode())
    ws[key].recv()
    ws[key].send('42/nv/{}/answer'.format(key).encode())
    result =  ws[key].recv()

    ws[key].send(b'2')
    result =  ws[key].recv()
    ws[key].send(b'2')
    result =  ws[key].recv()
    if result[:1] == '3':
        print("{} Connect Succeed".format(key))

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
    connect_way = ['haokan','tieba','xiguashipin','huajiao','chongdingdahui','zhishichaoren','youku']
    ws = {}
    main()
