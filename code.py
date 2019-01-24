from PIL import ImageGrab,ImageOps
# import numpy
import os
import time
import pyautogui

x_pad = 314
y_pad = 4
def screenGrab():
    """
    Coordinate based on 1080p by 1920p screen where Duel Links Steam is dragged to top right corner
    """
    box = (x_pad+1, y_pad + 1, x_pad + 1596, y_pad + 921)
    im = ImageGrab.grab(box)
    # im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
    return im

def getCurrentState():
    im = screenGrab()
    print(im.getpixel(875,825))
    
def get_cords():
    x,y = pyautogui.position()
    x -= x_pad
    y -= y_pad
    print(x,y)

def click(x,y):
    pyautogui.click(x + x_pad , y + y_pad)
    time.sleep(1)

def enter_gate():
    print('enter_gate')
    click(900,420)
    time.sleep(1)
    
def start_duel():
    print('start_duel')
    click(800,800)

def accept_duel():
    print('accept_duel')
    click(783,804)
    click(783,804)

def change_phase():
    print('change_phase')
    click(1104,597)
    click(1104,597)

def end_turn():
    click(1060,450)
    print('end_turn')

def draw():
    print('draw')
    click(747,684)
    click(747,684)

def summon_monster():
    click(747,851) #select from hand
    time.sleep(1)
    click(747,684)
    print('summon_monster')
    time.sleep(6)

def attack():
    click(815,540)
    click(815,680)
    print('attack')
    print('waiting for animation and effect to resolve')
    time.sleep(13) #buffer for animation and effect activations

def main():
    # enter_gate()
    # start_duel()
    # accept_duel()
    draw()
    summon_monster()
    change_phase()
    attack()
    change_phase()
    # time.sleep(30)
    # get_cords()
    # getCurrentState():
 
if __name__ == '__main__':
    main()
