from tkinter.ttk import Combobox as TtkCombobox
from .smartwidget import SmartWidget

class Combobox(SmartWidget, TtkCombobox):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      
      if isinstance(kw["values"], dict):
         values = kw["values"]
         
         kw["values"] = list(map(lambda i: self.__class__.formatValueString(values["text"], i, values.get("offset", 0)), range(values["count"])))
      
      if "value" not in kw:
         kw["value"] = kw["values"][0]
      
      SmartWidget._setVariable(kw, "StringVar", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
   
   @staticmethod
   def formatValueString(text, i, offset):
      return f"{text}{i + offset}"
   
   def getValueIndex(self):
      return self["values"].index(self.getValue())
