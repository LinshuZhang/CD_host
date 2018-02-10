# -*-coding=utf-8-*-
import requests
import time
from urllib import request
import random
import json
from multiprocessing.dummy import Pool as ThreadPool
import re
import base64

class Sougou(object):
    def __init__(self,key):
        self.key = key
        self.url = 'https://wdpush.sogoucdn.com/api/anspush'
        self.headers = {'Host': 'wdpush.sogoucdn.com',
               'Connection': 'keep-alive',
               'Accept': '*/*',
               "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5903",
               "Referer": "https://assistant.sogoucdn.com/v5/cheat-sheet?channel=cddh",
               "Accept-Encoding": "gzip,deflate",
               "Accept-Language": "zh-CN,en-US;q=0.8",
                "X-Requested-With": "com.sogou.activity.src"}
        self.cookie = {'APP-SGS-ID':'13661516023176817%7C701697'}

    @property
    def payload(self):
        random_number_str = ''.join([str(random.randint(0,9)) for i in  range(16)])+'_{}'.format(int(time.time()*1000))
        self.jQuery_word = 'jQuery2000{}'.format(random_number_str)
        return {'key': self.key, 'wdcallback': self.jQuery_word,'_': int(time.time()*1000)}

    @property
    def web_content_json(self):
        web_content = requests.get(self.url,params=self.payload,headers=self.headers,cookies=self.cookie)
        web_content_json = web_content.text.replace(self.jQuery_word,'').replace('\\','')
        result_base64 = re.findall('"result": "(.+?)"',web_content_json)[0]
        return str(json.loads(base64.b64decode(result_base64)))

    def update(self):
        web_content_json = self.web_content_json
        if web_content_json.__len__() > 30:
            try:
                self.result = re.findall('result":"(.+?)","search_infos"',web_content_json)[-1]
            except:
                self.result = re.findall('result":"(.+?)"',web_content_json)[-1]
            try:
                self.summary = re.findall('summary":"(.*?)","title"',web_content_json)[-1]
            except:
                self.summary = ''
        else:
            self.result = ''
            self.summary = ''

        if self.result:
            self.result_str = []
            self.result_str.append('结果 ：')
            self.result = self.result.replace('汪仔','')
            self.result_str.append(self.result)
            self.result_str.append('\n\n说明 : ')
            self.result_str.append(self.summary)
            with open('{}.html'.format(self.key),'w') as f:
                f.write(''.join(self.result_str))

def write(key):
    #print(key)
    to_update[key].update()

record_time = time.time()
if __name__ == "__main__":
    connect_way = ['xigua','huajiao','cddh','zscr','hjsm','tb','qf','yk']
    update_times = 1
    print("Strat record")
    to_update = {}
    for key in connect_way:
        to_update[key] = Sougou(key)
    while True:
        start_time = time.time()
        try:
            pool = ThreadPool(8)
            results = pool.map(write,connect_way)
            pool.close()
            pool.join()
        except:
            print("Record Fail")
        if (time.time() - record_time)>5:
            record_time = time.time()
            with open('time.html','w') as f:
                f.write(u'当前时间戳为{}'.format(time.time()))
                print('Now:{}'.format(time.time()))
        end_time = time.time()
        if end_time-start_time < 0.35:
            time.sleep(0.4-(end_time-start_time))
            #print("Update Stop")
        update_times += 1
        #print("Update Times {}".format(update_times))

    print("Record finished")
