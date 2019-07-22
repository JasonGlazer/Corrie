import gettext

from corrie.interface.application import CorrieApplication

gettext.install("app")  # replace with the appropriate catalog name
app = CorrieApplication(0)
app.MainLoop()
