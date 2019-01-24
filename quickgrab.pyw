from PIL import ImageGrab
import os
import time

x_pad = 314
y_pad = 4
def screenGrab():
    """
    Coordinate based on 1080p by 1920p screen where Duel Links Steam is dragged to top right corner
    """

    box = (x_pad+1, y_pad + 1, x_pad + 1596, y_pad + 921)
    im = ImageGrab.grab(box)
    im.save(os.getcwd() + '\\full_snap__' + str(int(time.time())) +'.png', 'PNG')
 
def main():
    screenGrab()
 
if __name__ == '__main__':
    main()