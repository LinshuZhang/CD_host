# -*-coding=utf-8-*-
import requests
import time
from urllib import request
import random
import json
from multiprocessing.dummy import Pool as ThreadPool
import re
import base64

def get_sougou(key):
    url = 'https://wdpush.sogoucdn.com/api/anspush'
    headers = {'Host': 'wdpush.sogoucdn.com',
           'Connection': 'keep-alive',
           'Accept': '*/*',
           "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5903",
           "Referer": "https://assistant.sogoucdn.com/v5/cheat-sheet?channel=cddh",
           "Accept-Encoding": "gzip,deflate",
           "Accept-Language": "zh-CN,en-US;q=0.8",
            "X-Requested-With": "com.sogou.activity.src"}
    cookie = {'APP-SGS-ID':'13661516023176817%7C701697'}
    random_number_str = ''.join([str(random.randint(0,9)) for i in  range(16)])+'_{}'.format(int(time.time()*1000))
    jQuery_word = 'jQuery2000{}'.format(random_number_str)
    payload = {'key': key, 'wdcallback': jQuery_word,'_': int(time.time()*1000)}
    web_content = requests.get(url,params=payload,headers=headers,cookies=cookie)
    web_content_json = web_content.text.replace(jQuery_word,'').replace('\\','')
    result_base64 = re.findall('"result": "(.+?)"',web_content_json)[0]
    web_content_json = str(json.loads(base64.b64decode(result_base64)))
    right_number = 3
    if web_content_json.__len__() > 30:
        choice = ''
        try:
            result = re.findall('result":"(.+?)","search_infos"',web_content_json)[-1]
        except:
            result = re.findall('result":"(.+?)"',web_content_json)[-1]
        try:
            summary = re.findall('summary":"(.*?)","title"',web_content_json)[-1]
        except:
            summary = ''
    else:
        choice = ''
        result = ''
        summary = ''

    return result,summary

def record_result(key):
    result,summary= get_sougou(key)
    if result:
        result_str = []
        result_str.append('结果 ：')
        if result.__len__()>2:
            if '汪仔' in result:
                result = '大概没辙了...'
        result_str.append(result)
        result_str.append('\n\n说明 : ')
        result_str.append(summary)
        with open('{}.html'.format(key),'w') as f:
            f.write(''.join(result_str))

def main():
    global record_time
    try:
        pool = ThreadPool(6)
        results = pool.map(record_result,connect_way)
        pool.close()
        pool.join()
        if (time.time() - record_time)>3:
            record_time = time.time()
            with open('time.html','w') as f:
                f.write(u'当前时间戳为{}'.format(time.time()))
                print('Now:{}'.format(time.time()))
    except:
        print("Record Fail")

record_time = time.time()
if __name__ == "__main__":
    connect_way = ['xigua','huajiao','cddh','zscr','hjsm']
    update_times = 1
    print("Strat record")
    while True:
        start_time = time.time()
        try:
            main()
        except:
            print("Record Fail")
        end_time = time.time()
        if end_time-start_time < 0.18:
            time.sleep(0.23-(end_time-start_time))
            #print("Update Stop")
        update_times += 1
        #print("Update Times {}".format(update_times))

    print("Record finished")
