import wx

from corrie.interface.frame import CorrieFrame


class CorrieApplication(wx.App):

    def __init__(self, x):
        super(CorrieApplication, self).__init__(x)
        self.frame_corrie = None  # This is purely to get flake8 to hush about where the instantiation occurs

    def OnInit(self):
        self.frame_corrie = CorrieFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame_corrie)
        self.frame_corrie.Show()
        return True
