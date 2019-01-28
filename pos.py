# import numpy
from PIL import ImageGrab,ImageOps,Image;
import os
import time
import pyautogui

# x_pad = 314
# y_pad = 4
x_pad = 160
y_pad = 70
    
def get_cords():
    x,y = pyautogui.position()
    x -= x_pad
    y -= y_pad
    box = (x_pad+1, y_pad + 1, x_pad + 1596, y_pad + 921)
    im = ImageGrab.grab(box)
    color = im.getpixel((x,y))
    print('Pos:', x,y)
    print('Color:', color)

def main():
    while True:
        get_cords()
        time.sleep(1)
 
if __name__ == '__main__':
    main()
