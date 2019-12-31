import pyautogui
import time

time.sleep(3)
MOUSE_X, MOUSE_Y = pyautogui.position()
color = pyautogui.screenshot(region=(MOUSE_X, MOUSE_Y, 1, 1)).getcolors()

while True:
    color_2 = pyautogui.screenshot(region=(MOUSE_X, MOUSE_Y, 1, 1)).getcolors()
    if color_2 != color:
        print('Clicked at {} {}'.format(MOUSE_X, MOUSE_Y))
        pyautogui.click(MOUSE_X, MOUSE_Y)
        break
