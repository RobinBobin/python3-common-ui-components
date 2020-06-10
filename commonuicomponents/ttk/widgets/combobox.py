from tkinter.ttk import Combobox as TtkCombobox
from .smartwidget import SmartWidget

class Combobox(SmartWidget, TtkCombobox):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      
      if "value" not in kw:
         kw["value"] = kw["values"][0]
      
      SmartWidget._setVariable(kw, "StringVar", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
   
   def getValueIndex(self):
      return self["values"].index(self.getValue())
