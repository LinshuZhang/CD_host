import time
import requests
import random

def get_UC():
    headers = {'Host': 'crop-answer.sm.cn',
       'Connection': 'keep-alive',
       'Accept': 'application/json',
        "X-Requested-With": "XMLHttpRequest'User-Agent':'DYZB/2.271 (iPhone; iOS 9.3.2; Scale/3.00)'",
       "User-Agent": "Mozilla/5.0 (Linux; Android 5.0; Samsung Galaxy S6 - 5.0.0 - API 21 - 1440x2560 Build/LRX21M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/37.0.0.0 Mobile Safari/537.36 SogouSearch Android1.0 version3.0 AppVersion/5903",
       "Referer": "http://crop-answer.sm.cn/answer/index?activity=million&from=generalsc",
       "Accept-Encoding": "gzip,deflate",
       "Accept-Language": "zh-CN,en-US;q=0.8"}
    cookie = dict(sm_diu='e40b5e11cd8d50947ba0f5fb2e471f7f%7C%7C13ecf325494ec63ebf%7C1516098861',
          cna='LsPkEqE/4moCAbf7FmPyql2V; sm_sid=add851962da042112f17bb34988c0343',
          sm_uuid='33b19164da9a52f2377f40c32f7a94aa%7C%7C%7C1516098892',
          isg='AhsbLl0jxf_MeDkLKKYfN20koXaP8Cz9s76aGQ1Y9pox7DrOlcABQqNulnQd')
    url = 'http://crop-answer.sm.cn/answer/curr?'
    payload = {'format': 'json', 'activity': 'million','_t': int(time.time()*1000),'activity':'million'}
    web_content = requests.get(url,params=payload,headers=headers,cookies=cookie)
    UC_data = web_content.json()['data']
    correct_number = UC_data['correct']
    if correct_number:
        correct_option = 'UC答题: {}'.format(UC_data['options'][int(correct_number)]['title'])
    else:
        correct_option = '无法获取UC结果,等待开始中'
    return correct_option

def main():
    while True:
        time.sleep(0.3)
        try:
            result = get_UC()
            #print(result)
            with open('xigua_UC.html','w') as f:
                f.write(result)
        except BaseException as e:
            print("Error: {}".format(e))

if __name__ == '__main__':
    main()
