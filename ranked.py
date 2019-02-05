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

logging.basicConfig(filename='ranked.log', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

x_pad = 160
y_pad = 70
x_frame = 1596
y_frame = 921
screen_mid = (800,420)


def get_screen(screen_padding= (0,0,x_frame,y_frame)):
    box = (x_pad + screen_padding[0], y_pad + screen_padding[1], x_pad + x_frame, y_pad + y_frame)
    frame = ImageGrab.grab(box)
    time.sleep(0.1)
    return frame

def click_template(template_path):
    img = get_screen()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    threshold = 0.8

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
    pyautogui.click(x + x_pad , y + y_pad)
    
def draw():
    print('draw')
    click(747,684)
    time.sleep(1)
    click(747,684)
    time.sleep(1)
    click(747,684)

def check_template(template_path,screen_padding =(0,0)):
    img = get_screen(screen_padding)
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    template = cv2.imread('templates/' + template_path,0)
    w,h = template.shape[::-1]
    img = img2.copy()
    method = eval('cv2.TM_CCOEFF_NORMED')

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print('checking ' + template_path + "(" + "{0:.2f}".format(max_val) + ")")
    return max_val

def check_connection():
    print ('Scanning connection buttons')
    buttons = ['retry.PNG','initiate_link.PNG']
    for button in buttons:
        if click_template(button):
            check_connection()
            time.sleep(10)

def enter_auto_duel():
    check_connection()
    for i in range(4):
        img = get_screen() #player's monster zones screen_padding=(660, 470, 970 , 600)
        img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
        template = cv2.imread('templates/bubble_point.PNG',0)
        print('Checking bubble')
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.55
        loc = np.where(res >= threshold)
        for pt in zip(*loc[::-1]):
            if not( 541 < pt[0] < 651 and 663 < pt[1] < 753) and not( 690 < pt[0] < 796 and 665 < pt[1] < 761): #card trader and ex trader
                click(pt[0] , pt[1] -10)
                time.sleep(2)
                if (click_template('dialog_arrow.PNG')):
                    time.sleep(1)
                    if (click_template('auto_duel.PNG')):
                        print('Entering auto_duel')
                        auto_duel()
        print('Screen cleared, swiping right')
        time.sleep(1)
        click_template('swipe_right.PNG')

def auto_duel():
    print('Scanning auto duel exit conditions')
    buttons = ['win_ok_btn.PNG','ok_btn.PNG','next_btn.PNG','retry.PNG','dialog_arrow.PNG']
    while check_template('duel_orb.PNG') < 0.9:
        for button in buttons:
            if click_template(button):
                auto_duel()
    logging.info('auto_duel')

 
def enter_ranked_duel():
    print('Scanning ranked buttons')
    buttons = ['win_ok_btn.PNG','ok_btn.PNG','next_btn.PNG','plat_icon.PNG','quick_duel.PNG','rank_duel.PNG','initiate_link.PNG']
    for button in buttons:
        if click_template(button):
            enter_ranked_duel()
    ranked_duel()

def ranked_duel():
    print('checking for duel status...')
    turn_status_pixel = (985,75)
    if (get_screen().getpixel(turn_status_pixel) != (9,51,185) and get_screen().getpixel(turn_status_pixel) != (173,3,3)): #turn status neither red nor blue , means not in duel
        print('no duel detected, entering ranked...')
        enter_ranked_duel()
    while(get_screen().getpixel(turn_status_pixel) == ((173,3,3))): 
        print("opponent's turn, checking for duel exit status")
        if (check_exit()):
            print('Ranked round cleared')
            logging.info('ranked_cleared')
            enter_ranked_duel()
    else:
        #draw_phase
        print('checking phase')
        if check_template('phase_draw.PNG') > 0.9:
            print('enter draw phase')
            draw()
        #main_phase
        elif check_template('phase_main.PNG') > 0.9:
            print('enter main phase')
            click_template('phase_btn.PNG') 
            time.sleep(0.5)
            click_template('end.PNG')
            print('ending turn')
            time.sleep(5)

        #battle_phase
        elif check_template('phase_battle.PNG') > 0.9:
            print('enter battle_phase')
            click_template('phase_btn.PNG')
            time.sleep(0.5)
            click_template('end.PNG')
            time.sleep(5)
        
        if (check_exit()):
            print('Ranked round cleared')
            logging.info('ranked_cleared')
            enter_ranked_duel()
        #discard from full hand or select random card
        # elif check_template('discard.PNG') > 0.9:
        #     click(522,617)
        #     time.sleep(0.5)
        #     click(787,787)
        if (check_exit()):
            print('Ranked round cleared')
            logging.info('ranked_cleared')
            enter_ranked_duel()
        click(522,617)
        time.sleep(0.5)
        click(787,787)
        ranked_duel()

def check_exit():
    while (check_template('phase_btn.PNG') < 0.9 and check_template('win_ok_btn.PNG') < 0.9):
        ('Waiting for board to update')
        click(screen_mid[0],screen_mid[1]) #need to clear for opponent card effect
        #to selct first card from left if needed
        click(522,617)
        time.sleep(0.5)
        click(787,787)
    if (check_template('phase_btn.PNG') >= 0.9):
        return False
    if (check_template('win_ok_btn.PNG') >= 0.9):
        return True

def main():
    enter_auto_duel()
    enter_ranked_duel()
 
if __name__ == '__main__':
    main()
