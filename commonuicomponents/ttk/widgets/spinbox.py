from tkinter.ttk import Spinbox as TtkSpinbox
from .smartwidget import SmartWidget
from ...staticutils import StaticUtils

class Spinbox(SmartWidget, TtkSpinbox):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      SmartWidget._setVariable(kw, "IntVar", variableKey = "textvariable")
      
      if "width" not in kw:
         kw["width"] = max(StaticUtils.getPlaces((kw["from_"], kw["to"])))
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
