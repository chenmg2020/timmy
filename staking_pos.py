import pyautogui #pip install pyautogui
# from mss import mssimport pyautogui
import logging

logging.basicConfig(filename='staking.log', level=logging.INFO,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
pyautogui.PAUSE = 0.01

def main():
    # pyautogui.displayMousePosition()
    while True: 
        pyautogui.click(1129,572)
        pyautogui.click(1769,572)
        pyautogui.click(2347,572)
 
if __name__ == '__main__':
    main()
