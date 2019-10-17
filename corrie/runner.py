import gettext
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from corrie.interface.application import CorrieApplication


gettext.install("app")  # replace with the appropriate catalog name
app = CorrieApplication(0)
app.MainLoop()
