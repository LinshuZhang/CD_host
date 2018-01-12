# -*- coding=utf-8 -*-
import os
import objc, Quartz
from AppKit import NSBitmapImageRep
from Quartz.CoreGraphics import CGMainDisplayID
import pyautogui as pag
import send
import time
from config import image_path

def get_pixel_color_init():
    global mainID
    objc.parseBridgeSupport( """<?xml version='1.0'?>
<!DOCTYPE signatures SYSTEM "file://localhost/System/Library/DTDs/BridgeSupport.dtd">
<signatures version='1.0'>
  <depends_on path='/System/Library/Frameworks/CoreFoundation.framework/CoreFoundation' />
  <depends_on path='/System/Library/Frameworks/IOKit.framework/IOKit' />
  <depends_on path='/System/Library/Frameworks/CoreServices.framework/CoreServices' />
  <function name='CGDisplayCreateImageForRect'>
    <retval already_cfretained='true' type='^{CGImage=}' />
    <arg type='I' />
    <arg type='{CGRect={CGPoint=ff}{CGSize=ff}}' type64='{CGRect={CGPoint=dd}{CGSize=dd}}' />
  </function>
</signatures>
""", globals(), '/System/Library/Frameworks/ApplicationServices.framework/Frameworks/CoreGraphics.framework')
    mainID = CGMainDisplayID()

def get_color_pixel(x,y):
    image = CGDisplayCreateImageForRect(mainID, ((x-1,y-1), (x+1,y+1)))
    bitmap = NSBitmapImageRep.alloc()
    bitmap.initWithCGImage_(image)
    # Get the RGB color (float values from 0 to 1 per color, plus alpha) at a particular point
    return bitmap.colorAtX_y_(1, 1)

def is_white(x,y):
    # Get the RGB color (float values from 0 to 1 per color, plus alpha) at a particular point
    results = get_color_pixel(x,y)
    result_list = str(results).split(' ')
    for i in range(1,4,1):
        if float(result_list[i])<245/255:
            return False
    return True

if __name__ == '__main__':
    white_times = 0
    get_pixel_color_init()
    while True:
        time.sleep(0.1)
        if is_white(133,63) and is_white(385,505):
            if white_times%2 == 0:
                print("发现题目,获取提示中:{}".format(time.time()))
                white_times += 1
                question_img = pag.screenshot(region=(40,200,345,310))
                question_img.save(image_path)
                send.send_file(image_path)
                print(" 开始15秒的等待时间")
                for i in range(12):
                    print(i)
                    time.sleep(1)
            else:
                print("答案公布时间")
                white_times += 1
                print(" 开始15秒的等待时间")
                for i in range(13):
                    print(i)
                    time.sleep(1)
