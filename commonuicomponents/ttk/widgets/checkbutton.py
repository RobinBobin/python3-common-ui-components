from tkinter.ttk import Checkbutton as TtkCheckbutton
from .smartwidget import SmartWidget

class Checkbutton(SmartWidget, TtkCheckbutton):
   def __init__(self, master, **kw):
      hasValueBuffer = kw.pop("hasValueBuffer", False)
      
      SmartWidget._setVariable(kw, "BooleanVar", variableKey = "variable")
      
      SmartWidget.__init__(self, master, **kw)
      
      if hasValueBuffer:
         self._initValueAndTraceAdd()
