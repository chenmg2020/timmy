import sys
import os
import time
from PIL import ImageGrab,ImageOps,Image
import numpy as np
import cv2
# from mss import mss
import matplotlib.pyplot as plt
import pyautogui

x_pad = 314
y_pad = 4
x_frame = 1596
y_frame = 921
screen_mid = (800,420)

# def screen_grab():
#     """
#     Coordinate based on 1080p by 1920p screen where Duel Links Steam is dragged to top right corner
#     """
#     box = (x_pad+1, y_pad + 1, x_pad + 1596, y_pad + 921)
#     cv2.namedWindow('window', cv2.WINDOW_KEEPRATIO)
#     while(True):
#         frame = ImageGrab.grab(box)
#         frame = np.array(frame.getdata(), dtype = 'uint8').reshape((frame.size[1], frame.size[0], 3))
#         frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#         cv2.imshow('window', frame)
#         if cv2.waitKey(0) & 0xFF == ord('q'):
#             cv2.destroyAllWindows()
#             break
#         time.sleep(1)
#     # cv2.imshow('image',im)
#     # cv2.waitKey(0)
#     # cv2.destroyAllWindows()
#     # # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
#     # return im

def get_screen(screen_padding= (0,0)):
    box = (x_pad + screen_padding[0], y_pad + screen_padding[1], x_pad + x_frame, y_pad + y_frame)
    frame = ImageGrab.grab(box)
    time.sleep(0.1)
    return frame

def get_current_state():

    img = get_screen()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img2 = img.copy()

    template =cv2.imread('gate.png',0)
    w, h = template.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
                'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

    for meth in methods:
        img = img2.copy()
        method = eval(meth)

        # Apply template Matching
        res = cv2.matchTemplate(img,template,method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        cv2.rectangle(img,top_left, bottom_right, 255, 2)

        plt.subplot(121),plt.imshow(res,cmap = 'gray')
        plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
        plt.subplot(122),plt.imshow(img,cmap = 'gray')
        plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        plt.suptitle(meth)

        plt.show()

def click_template(template_path):
    img = get_screen()
    img = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2GRAY)
    img2 = img.copy()
    threshold = 0.6

    template = cv2.imread('templates/' + template_path,0)
    w, h = template.shape[::-1]
    img = img2.copy()
    method = eval('cv2.TM_CCOEFF_NORMED')

    # Apply template Matching
    res = cv2.matchTemplate(img,template,method)

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
    time.sleep(1)
    
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

def summon_monster():
    click(747,851) #select from hand
    time.sleep(1)
    click(747,684)
    print('summon_monster')
    time.sleep(6)

def check_template(template_path,screen_padding =(0,0)):
    time.sleep(1)
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

def enter_gate_duel():
    while not click_template('gate.PNG'):
        pass
    while not click_template('duel_btn.PNG'):
        pass
    while not click_template('dialog_arrow.PNG'):
        pass
    while not click_template('confirm_duel_btn.PNG'):
        pass
    timmy_duel()

def timmy_duel():
    while(get_screen().getpixel((1018,74)) != (9,51,185)): 
        print('waiting for your turn')
    else:
        #draw_phase
        print('entering your turn,checking phase')
        if check_template('phase_draw.PNG') > 0.9:
            print('enter draw phase')
            draw()
        #main_phase
        if check_template('phase_main.PNG') > 0.9:
            print('enter main phase')
            click(747,851) #select from hand
            time.sleep(1)
            if check_template('monster_level.PNG',screen_padding=(0,y_frame/2)) < 0.6:
                summon_monster()
            if click_template('phase_btn.PNG'):
                change_phase()
        #battle_phase
        if check_template('phase_battle.PNG') > 0.9:
            print('enter battle_phase')
            if check_template('monster_level.PNG') > 0.8:
                click_template('monster_level.PNG')
                click_template('atk_btn.PNG')
                print('monster attack')
                click(screen_mid[0],screen_mid[1])
            while (check_template('phase_btn.PNG') < 0.9 and check_template('win_ok_btn.PNG')<0.9):
                ('Waiting for board to update')
                click(screen_mid[0],screen_mid[1]) #need to clear for opponent card effect
            if (check_template('phase_btn.PNG') > 0.9):
                print ('ending phase')
                if click_template('phase_btn.PNG'):
                    change_phase()
                    time.sleep(5)
                    timmy_duel()
            elif(check_template('win_ok_btn.PNG') > 0.9):
                print ('Duel won, collecting rewards and exiting')
                while not click_template('win_ok_btn.PNG'):
                    pass
                while not click_template('next_btn.PNG'):
                    pass
                while not click_template('next_btn.PNG'):
                    pass
                while not click_template('win_ok_btn.PNG'):
                    pass
                while not click_template('next_btn.PNG'):
                    pass
                while not click_template('dialog_arrow.PNG'):
                    pass
                enter_gate_duel()

def main():

    enter_gate_duel()
    timmy_duel()
    # enter_gate_duel()
    # summon_monster()
    # get_current_state()
    # screen_grab()
    # enter_gate()
    # start_duel()
    # accept_duel()
    # draw()
    # summon_monster()
    # change_phase()
    # attack()
    # change_phase()
    # time.sleep(30)
    # get_cords()
    # getCurrentState():
 
if __name__ == '__main__':
    main()
