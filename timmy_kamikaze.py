import sys
import os
import time
from typing import cast
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

def click(x,y):
    if not ( 480 <= x <= 2080 and 70 <= y <= 1000): # check if click is within window frame
        logging.warn("out of bound click blocked! at " + str(x) +"," + str(y))
        return
    pyautogui.click(x,y)

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
        click(top_left[0] + w/2 , top_left[1] + h/2)
        return True
    else:
        print(template_path + ' not seen( '+ max_val_string + ' )')
        return False

def change_phase():
    reset_cursor()
    if click_template('ok_btn.png'): #exit on last winning turn
        return
    wait_to_click('phase_btn.png',1)
    wait_to_click('end.png', 1)

def draw():
    time.sleep(0.5)
    print('draw')
    click(1280, 497)
    time.sleep(1)
    click(1280, 497)
    time.sleep(1)

def wait_to_click(template, duration):
    t_end = time.time() + duration
    while time.time() < t_end:
        clicked = click_template(template)
    return clicked

def cast_st(duration):
    print('casting st')
    t_end = time.time() + duration 
    while time.time() < t_end:
        click(1256,967) #select
        if wait_to_click('activate_effect.png',0.5):
            wait_to_click('confirm_rug.png', 0.8) 
            wait_to_click('confirm_rug.png', 0.8)
            return True
        if click_template('set.png'):
            return True
    return False


def reset_cursor():
    click(950,610)

def enter_casual():
    print('checking casual duel buttons')
    buttons = ['casual_duel_btn.png','duel_btn.png','confirm_duel_btn.png','arrow.png', 'initiate_link.png', 'duel_dome_gate.png', 'duel_dome_gate_day.png', 'casual_duel_bar.png']
    # buttons = ['npc_diamond.png','auto_duel.png','duel_confirm_yes.png','duel_btn.png','confirm_duel_btn.png','arrow.png']
    for button in buttons:
        if click_template(button): 
            if 'casual_duel' in button: logging.info('casual duel entered')
            return True

def exit_duel():
    print ('checking for exit duel buttons')
    # buttons = ['ok_btn.png','next_btn.png','arrow.png','duel_results.png','close.png','back.png','dice_challenge.png','reboot.png']
    buttons = ['ok_btn.png','next_btn.png','arrow.png','duel_results.png','close.png','back.png','reboot.png']
    for button in buttons:
        if click_template(button): return True

def timmy_duel():
    if check_template('opponent.png'): #opponent's turn
        if wait_to_click('dod.png', 0.5):
            wait_to_click('activate_dod.png', 3)
            wait_to_click('ok_btn.png', 0.3)
        if wait_to_click('cybernetic.png', 0.5):
            wait_to_click('activate_dod.png', 3)
            wait_to_click('ok_btn.png', 0.3)
        
        reset_cursor()    
    if check_template('you.png'): #your turn
        click_template('yes.png')  
        print('in duel turn, checking phase')
       #main_phase
        if check_template('phase_draw.png'): #draw_phase
            print('enter draw phase') 
            draw()
            return 
        if check_template('phase_main.png'): #main_phase
            print('enter main phase')
            while cast_st(2):
                cast_st(3)
            change_phase()
            return
        if check_template('phase_battle.png'): #battle_phase
            change_phase()
            return
        click_template('back.png')
        click_template('yes.png')  
    elif exit_duel():
        return
    elif enter_casual():
        return


def main():
    while True:
        timmy_duel()

if __name__ == '__main__':
    main()
