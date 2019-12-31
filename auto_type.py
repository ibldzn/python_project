import pyautogui
import pytesseract
from PIL import Image
import time

pytesseract.pytesseract.tesseract_cmd = r'D:\Tesseract-OCR\tesseract.exe'

time.sleep(3)

# It's not advised to use while loop
# There is a built-in mechanism in pyautogui to terminate program if we
# move our cursor to top left. This will cause program to break

while True:
    # region may vary for different screen
    im = pyautogui.screenshot(region=(275, 306, 965, 56))
    im.save('data.png')

    # To click text area and start typing
    # pyautogui.click(x=465, y=445)

    # To get text from given image
    value = pytesseract.image_to_string(Image.open('data.png'))

    # To replace new line from it and make one clean list
    value = value.replace('\n\n', ' ')
    b = value.split(' ')

    print(b)

    # Backspace is used to avoid any error
    for i in b:
        pyautogui.press('backspace')
        pyautogui.typewrite(i)
        pyautogui.press('space')
    if len(b) <= 4:
        break
        
