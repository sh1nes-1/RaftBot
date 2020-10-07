import win32gui
import win32api
import win32con
import time

WND_TITLE = 'Raft'

def send_mouse_click(hwnd, mouse_pos, delay):
    mouse_pos = win32api.MAKELONG(mouse_pos[0], mouse_pos[1])
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, mouse_pos)
    time.sleep(delay)
    win32gui.SendMessage(hwnd, win32con.WM_LBUTTONUP, 0, mouse_pos)   

hwnd = win32gui.FindWindow(None, WND_TITLE)

while True:
    send_mouse_click(hwnd, (100, 100), 5)