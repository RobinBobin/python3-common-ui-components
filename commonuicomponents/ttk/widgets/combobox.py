from tkinter.ttk import Combobox as TtkCombobox
from .smartwidget import SmartWidget

class Combobox(SmartWidget, TtkCombobox):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      
      if isinstance(kw["values"], dict):
         values = kw["values"]
         text = values["text"]
         count = values["count"]
         offset = values.get("offset", 0)
         
         kw["values"] = [f"{text}{i + offset}" for i in range(count)]
      
      if "value" not in kw:
         kw["value"] = kw["values"][0]
      
      SmartWidget._setVariable(kw, "StringVar", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
   
   def getValueIndex(self):
      return self["values"].index(self.getValue())
