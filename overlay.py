import wx
import win32gui
from wx import *

class gui(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, None, id)
        hwnd = win32gui.FindWindow(None, 'Raft')
        self.AssociateHandle(hwnd)
        #dc = wx.WindowDC(self)
    
        wx.StaticText(self, -1, 'my text', (20, 100))

        #dc.Destroy()

if __name__=='__main__':
    app = wx.App()
    frame = gui(parent=None, id=-1, title="Transparent Window Demo")
    frame.Show()
    app.MainLoop()    