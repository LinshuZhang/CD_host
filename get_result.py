# -*- coding=utf-8 -*-
import os
from result_class import Result
from config import image_path
import time
def main():
    with open("results.html",'w') as f:
        f.write("服务器已经打开等待大会开始")
    while True:
        time.sleep(0.1)
        if os.path.isfile(image_path):
            print("已经收到图片，开始尝试获取结果 {}".format(time.time()))
            result = Result(image_path)
            os.remove(image_path)
            print("已经收到结果删除图片 {}".format(time.time()))
if __name__ == '__main__':
    main()
