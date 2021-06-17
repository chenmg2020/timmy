import sys
import os
import time
from PIL import ImageGrab,ImageOps,Image #pip install pillow
import numpy as np  #pip install numpy
import cv2 #pip install opencv-python  
import pyautogui #pip install pyautogui
# from mss import mssimport pyautogui
import logging

logging.basicConfig(filename='staking.log', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

btn_pos_list = []
def get_positions(template_path):
    img = ImageGrab.grab(bbox = None)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    threshold = 0.65

    template = cv2.imread('templates/' + template_path,0)
    w, h = template.shape[::-1]
    img = img2.copy()

    # Apply template Matching
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    max_val_string = "{0:.2f}".format(max_val)
    if (max_val > threshold):
        print(template_path + ' seen ( '+ max_val_string + ' )  at ' +  str(max_loc)) 
        top_left = max_loc
        btn_pos_list.append((top_left[0] + w/2 , top_left[1] + h/2))
    else:
        print(template_path + ' not seen( '+ max_val_string + ' )')
print(btn_pos_list)

def click(x,y):
    pyautogui.click(x, y)

def spam_click(btn_pos_list, index):
    btn_pos = btn_pos_list[index]
    pyautogui.click(btn_pos[0],btn_pos[1])
    time.sleep(0.001)
    if index == (len(btn_pos_list) - 1):
        spam_click(btn_pos_list, 0)
    else:
        spam_click(btn_pos_list, index+1)

# 

def main():
    get_positions('click_speed.PNG')
    spam_click(btn_pos_list,0)
 
if __name__ == '__main__':
    main()
