import sys
import os
import time
from PIL import ImageGrab,ImageOps,Image
import numpy as np
import cv2
# from mss import mss
import matplotlib.pyplot as plt
import pyautogui
import logging
import datetime

logging.basicConfig(filename=datetime.datetime.now().strftime("logs/%m_%d_%H_%M.log"), level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

x_pad = 0
y_pad = 0
x_frame = 2580
y_frame = 1080
screen_mid = (1270,520)


def get_screen():
    box = (x_pad, y_pad, x_pad + x_frame, y_pad + y_frame)
    frame = ImageGrab.grab(box)
    time.sleep(0.1)
    return frame

def check_template(template_path):
    current_screen = get_screen()
    img = cv2.cvtColor(np.array(current_screen), cv2.COLOR_BGR2GRAY)
    template = cv2.imread('templates/' + template_path,0)
    w, h = template.shape[::-1]
    threshold = 0.75
    if template_path == 'npc_diamond.png':
        threshold = 0.5
    # Apply template Matching
    res = cv2.matchTemplate(img,template,cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print('checking ' + template_path + "(" + "{0:.2f}".format(max_val) + ")")
    if (max_val > threshold):
        print(template_path + ' seen ( '+ str(max_val) + ' )  at ' +  str(max_loc)) 
        return True
    else:
        print(template_path + ' not seen( '+str(max_val) + ' )')
        return False

def click_template(template_path):
    current_screen = get_screen()
    img = cv2.cvtColor(np.array(current_screen), cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    threshold = 0.7
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
        click (top_left[0] + w/2 , top_left[1] + h/2)
        return True
    else:
        print(template_path + ' not seen( '+ max_val_string + ' )')
        return False

def click(x,y):
    if not ( 480 <= x <= 2080 and 70 <= y <= 1000): # check if click is within window frame
        logging.warn("out of bound click blocked! at " + str(x) +"," + str(y))
        return
    pyautogui.click(x,y)


def draw():
    time.sleep(0.5)
    print('draw')
    pyautogui.click(1280, 497)
    time.sleep(0.5)
    pyautogui.click(1280, 497)
    time.sleep(0.5)

def reset_cursor():
    pyautogui.click(950,610)

def enter_gate():
    print('entering auto_duel...')
    buttons = ['auto_duel.png','duel_confirm_yes.png','duel_btn.png','confirm_duel_btn.png','arrow.png']
    # buttons = ['npc_diamond.png','auto_duel.png','duel_confirm_yes.png','duel_btn.png','confirm_duel_btn.png','arrow.png']
    for button in buttons:
        if click_template(button): 
            if 'gate' in button: logging.info('gate entered')
            return True

def exit_duel():
    print ('checking for exit duel buttons')
    buttons = ['win_ok_btn.png','next_btn.png','arrow.png','duel_results.png','close.png','dice_challenge.png','reboot.png']
    # buttons = ['win_ok_btn.png','next_btn.png','arrow.png','duel_results.png','close.png','back.png','reboot.png']
    for button in buttons:
        if click_template(button): return True

def timmy_duel():
    if enter_gate():
        return
    elif exit_duel():
        return

def main():
    while True:
        timmy_duel()
    # pyautogui.displayMousePosition()

if __name__ == '__main__':
    main()
