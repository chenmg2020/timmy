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

logging.basicConfig(filename='gate.log', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

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
        click (top_left[0] + w/2 , top_left[1] + h/2)
        return True
    else:
        print(template_path + ' not seen( '+ max_val_string + ' )')
        return False

def click(x,y):
    pyautogui.click(x + x_pad , y + y_pad)
    
def change_phase():
    print('change_phase')
    click(1104,597)

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
    w, h = template.shape[::-1]
    img = img2.copy()
    method = eval('cv2.TM_CCOEFF_NORMED')

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    print('checking ' + template_path + "(" + "{0:.2f}".format(max_val) + ")")
    return max_val

def enter_gate():
    print('finding gate...')
    buttons = ['gate.PNG','duel_btn.PNG', 'dialog_arrow.PNG','confirm_duel_btn.PNG','retry.PNG']
    for button in buttons:
        if click_template(button):
            time.sleep(1)
            enter_gate()
    timmy_duel()

def timmy_duel():
    print('checking for duel status...')
    turn_status_pixel = (985,75)
    if (get_screen().getpixel(turn_status_pixel) != (9,51,185) and get_screen().getpixel(turn_status_pixel) != (173,3,3)): #turn status neither red nor blue , means not in duel
        print('no duel detected, finding gate...')
        enter_gate()
    while(get_screen().getpixel(turn_status_pixel) != (9,51,185)): 
        print('waiting for your turn')
    else:
        #draw_phase
        print('checking phase')
        if check_template('phase_draw.PNG') > 0.9:
            print('enter draw phase')
            draw()
            timmy_duel()

        #main_phase
        if check_template('phase_main.PNG') > 0.9:
            print('enter main phase')
            click(747,851) #select from hand
            time.sleep(1)
            if check_template('normal_summon.PNG') < 0.9:
                print('cant normal summon')
                click (screen_mid[0],screen_mid[1])
            else:
                click_template('normal_summon.PNG')
            while not click_template('phase_btn.PNG'):
                pass
            change_phase()
            time.sleep(3.5)
            timmy_duel() #first turn has no battle phase

        #battle_phase
        if check_template('phase_battle.PNG') > 0.9:
            print('enter battle_phase')
            img = get_screen() #player's monster zones screen_padding=(660, 470, 970 , 600)
            img_gray = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
            template = cv2.imread('templates/monster_atk.PNG',0)
            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
            threshold = 0.9
            loc = np.where(res >= threshold)
            for pt in zip(*loc[::-1]):
                if ( 660 < pt[0] < 970 and  470 < pt[1] < 600):
                    click(pt[0], pt[1])
                    i = 0
                    while not click_template('atk_btn.PNG'):
                        i += 1
                        click(pt[0], pt[1])
                        if (i >= 10):
                            break
                    print('monster attack')
                    duel_won  = check_exit()
                    if (duel_won):
                        exit_duel()
                    else:
                        continue
            print('All monsters have attacked, ending turn')
            click_template('phase_btn.PNG') #end turn
            change_phase()
            time.sleep(10)
            timmy_duel()

def exit_duel():
    print ('Duel won, collecting rewards and exiting')
    logging.info('gate_cleared')
    buttons = ['win_ok_btn.PNG','next_btn.PNG','dialog_arrow.PNG']
    while check_template('gate.PNG') < 0.65:
        # click(screen_mid[0],screen_mid[1])
        for button in buttons:
            click_template(button)
    enter_gate()

def check_exit():
    while (check_template('phase_btn.PNG') < 0.9 and check_template('win_ok_btn.PNG') < 0.9):
        ('Waiting for board to update')
        click(screen_mid[0],screen_mid[1]) #need to clear for opponent card effect
    if (check_template('phase_btn.PNG') >= 0.9):
        return False
    if (check_template('win_ok_btn.PNG') >= 0.9):
        return True

def main():
    timmy_duel()
 
if __name__ == '__main__':
    main()
