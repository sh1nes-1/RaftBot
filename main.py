import win32gui
import win32ui
from ctypes import windll
from PIL import Image
from PIL import ImageChops
import pyvda
import pyautogui
import time
import win32api
import win32con
from cv2 import cv2
import numpy

WND_TITLE = 'Raft'
PATTERN_PATH = 'pattern.png'

def send_mouse_click(hwnd, mouse_pos, delay):
    mouse_pos = win32api.MAKELONG(mouse_pos[0], mouse_pos[1])
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, mouse_pos)
    time.sleep(delay)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, mouse_pos)   

pattern = Image.open(PATTERN_PATH).convert('RGB')
open_cv_pattern = cv2.cvtColor(numpy.array(pattern), cv2.COLOR_RGB2BGR)

hwnd = win32gui.FindWindow(None, WND_TITLE)

while True:
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        open_cv_im = cv2.cvtColor(numpy.array(im), cv2.COLOR_RGB2BGR)
        result = cv2.matchTemplate(open_cv_pattern, open_cv_im, cv2.TM_CCOEFF_NORMED)
        
        threshold = .95
        loc = numpy.where(result >= threshold)
        found_x, found_y = loc[1], loc[0]
        
        #OLD CODE
        #selected_area = im.crop((FROM_PIXEL[0], FROM_PIXEL[1], TO_PIXEL[0], TO_PIXEL[1])).convert('RGB')
        #diff = ImageChops.difference(pattern, selected_area)
        #if #not diff.getbbox():

        if len(found_x) > 0 and len(found_y) > 0:             
            is_valid_x = False
            is_valid_y = False

            for x in found_x:
                if abs(x - w/2) < 100:
                    is_valid_x = True

            for y in found_y:
                if abs(y - h/2) < 100:
                    is_valid_y = True

            if is_valid_x and is_valid_y:
                #OLD CODE
                #prev_desk = pyvda.GetCurrentDesktopNumber()
                #pyvda.GoToDesktopNumber(2)
                #win32gui.SetForegroundWindow(hwnd)
                #pyautogui.click(left + 1, top + 1)
                #pyautogui.mouseDown()
                #time.sleep(0.1)            
                #pyautogui.mouseUp()
                #pyvda.GoToDesktopNumber(prev_desk)                    

                mouse_pos = (left + 1, top + 1)

                send_mouse_click(hwnd, mouse_pos, 0.1)
                time.sleep(0.1)
                send_mouse_click(hwnd, mouse_pos, 1)                     

                print('Catched!')

    time.sleep(0.2)