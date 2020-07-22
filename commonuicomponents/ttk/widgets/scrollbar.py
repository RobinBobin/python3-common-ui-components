from tkinter import HORIZONTAL
from tkinter.ttk import Scrollbar as TScrollbar
from .smartwidget import SmartWidget

class Scrollbar(SmartWidget, TScrollbar):
   _DEFAULT_STYLE = {
      "arrowsize": 25
   }
   
   def __init__(self, master, **kw):
      buddy = kw.pop("buddy")
      
      SmartWidget.__init__(self, master, **kw)
      
      buddy = self._parentContainer.getSmartWidget(buddy)
      
      axis = "x" if str(self["orient"]) == HORIZONTAL else "y"
      
      self["command"] = getattr(buddy, f"{axis}view")
      buddy[f"{axis}scrollcommand"] = self.set
