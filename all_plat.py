# -*-coding = utf-8 -*-
import requests
import time
from urllib import request
import random
import json
from multiprocessing.dummy import Pool as ThreadPool

def get_sougou(key):
    url = 'http://fex.sa.sogou.com/api/ans?'
    headers = {'Host': 'wd.sa.sogou.com',
           'Connection': 'keep-alive',
           'Accept': 'application/json',
           "X-Requested-With": "XMLHttpRequest'User-Agent':'DYZB/2.271 (iPhone; iOS 9.3.2; Scale/3.00)'",
           "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5903",
           "Referer": "http://wd.sa.sogou.com/",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Language": "zh-CN,en-US;q=0.8"}
    payload = {'key': key, '_': int(time.time()*1000)}
    random_number_str = ''.join([str(random.randint(0,9)) for i in  range(10)])
    cookies =  dict(dt_ssuid=random_number_str,IPLOC='CN3502')
    web_content = requests.get(url,params=payload,headers=headers,cookies=cookies,timeout = 0.5)
    web_content_json = web_content.json()
    result = json.loads(web_content_json['result'][1])['result']
    summary = json.loads(web_content_json['result'][1])['search_infos'][0]['summary']
    return result,summary

def record_result(key):
    result,summary = get_sougou(key)
    result_str = []
    result_str.append('结果 ：')
    result_str.append(result)
    result_str.append('\n\n说明 : ')
    result_str.append(summary)
    with open('{}.html'.format(key),'w') as f:
        f.write(''.join(result_str))

def main():
    global record_time
    try:
        pool = ThreadPool()#机器是多少核便填多少，卤煮实在ubuntu14.04 4核戴尔电脑上跑的程序
        results = pool.map(record_result,connect_way)
        pool.close()
        pool.join()
        if (time.time() - record_time)>3:
            record_time = time.time()
            with open('time.html','w') as f:
                f.write('当前时间戳为{}'.format(time.time()))
                print('当前时间戳为{}'.format(time.time()))
    except BaseException as e:
        print("记录失败，错误：{}".format(e))
        print(e)

record_time = time.time()
if __name__ == "__main__":
    connect_way = ['xigua','huajiao','cddh','zscr']
    update_times = 1
    print("开始记录")
    while True:
        start_time = time.time()
        try:
            main()
        except BaseException as e:
            print("记录失败，错误：{}".format(e))
        end_time = time.time()
        if end_time-start_time < 0.1:
            time.sleep(0.15-(end_time-start_time))
            print("更新停顿")
        update_times += 1
        print("已经更新了{}次".format(update_times))

    print("记录完毕")
