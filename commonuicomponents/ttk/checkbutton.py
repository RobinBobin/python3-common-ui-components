from tkinter.ttk import Checkbutton as TtkCheckbutton
from .smartwidget import SmartWidget

class Checkbutton(SmartWidget, TtkCheckbutton):
   def __init__(self, master = None, **kw):
      SmartWidget._setVariable(kw, "BooleanVar", setHasValueBuffer = False, variableKey = "variable")
      
      SmartWidget.__init__(self, master, **kw)
      
      if self.hasValueBuffer:
         self._initValueAndTraceAdd()
