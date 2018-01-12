# -*- coding=utf-8 -*-

import os
from result_class import Result

def main():
    image_path = 'question.png'
    while True:
        if os.path.isfile('question.png'):
            result = Result(image_path)
            os.remove(image_path)

if __name__ == '__main__':
    main()
