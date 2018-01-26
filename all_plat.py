# -*-coding = utf-8 -*-
import requests
import time
from urllib import request
import random
import json
from multiprocessing.dummy import Pool as ThreadPool
import re

def get_sougou(key):
    url = 'http://140.143.49.31/api/ans2'
    headers = {'Host': '140.143.49.31',
           'Connection': 'keep-alive',
           'Accept': 'application/json',
           "X-Requested-With": "XMLHttpRequest'User-Agent':'DYZB/2.271 (iPhone; iOS 9.3.2; Scale/3.00)'",
           "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5903",
           "Referer": "http://nb.sa.sogou.com/",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.sogou.activity.src"}
    random_number_str = ''.join([str(random.randint(0,9)) for i in  range(17)])
    jQuery_word = 'jQuery3210{}'.format(random_number_str)
    payload = {'key': key, 'wdcallback': jQuery_word,'_': int(time.time()*1000)}
    web_content = requests.get(url,params=payload,headers=headers)
    web_content_json = web_content.text.replace(jQuery_word,'').replace('\\','')
    choice = re.findall('"answers":\[(.+?)\]',web_content_json)[-1].replace("\"",'').split(',')
    result = re.findall('result":"(.+?)","search_infos"',web_content_json)[-1]
    summary = re.findall('summary":"(.*?)","title"',web_content_json)[-1]
    right_number = 3
    for i in range(3):
        if result in choice[i]:
            right_number = i
            # print("Get choice :{}".format(right_number))
    return result,summary,right_number

def record_result(key):
    result,summary,right_number = get_sougou(key)
    result_str = []
    result_str.append('结果 ：')
    if result.__len__()>2:
        if '汪仔' in result:
            result = '大概没辙了...'
    result_str.append(result)
    result_str.append('\n\n说明 : ')
    result_str.append(summary)
    result_str.append(str(right_number))
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
                f.write(u'当前时间戳为{}'.format(time.time()))
                print('Now:{}'.format(time.time()))
    except BaseException as e:
        print("Record Fail：{}".format(e))
        print(e)

record_time = time.time()
if __name__ == "__main__":
    connect_way = ['xigua','huajiao','cddh','zscr','hjsm']
    update_times = 1
    print("Strat record")
    while True:
        start_time = time.time()
        try:
            main()
        except BaseException as e:
            print("Record Fail:{}".format(e))
        end_time = time.time()
        if end_time-start_time < 0.1:
            time.sleep(0.15-(end_time-start_time))
            #print("Update Stop")
        update_times += 1
        #print("Update Times {}".format(update_times))

    print("Record finished")
