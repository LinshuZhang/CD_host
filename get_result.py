# -*- coding=utf-8 -*-
import os
from result_class import Result
from config import image_path
def main():

    while True:
        time.sleep(0.01)
        if os.path.isfile(image_path):
            result = Result(image_path)
            os.remove(image_path)

if __name__ == '__main__':
    main()
