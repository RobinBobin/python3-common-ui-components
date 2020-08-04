from tkinter.ttk import Combobox as TtkCombobox
from .smartwidget import SmartWidget

class Combobox(SmartWidget, TtkCombobox):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      
      if isinstance(kw["values"], dict):
         values = kw["values"]
         
         kw["values"] = list(map(lambda i: self.__class__.formatValueString(values.get("text", ""), i, values.get("offset", 0)), range(values["count"])))
      
      self.__itemsAreStrings = isinstance(kw["values"][0], str)
      
      if not self.__itemsAreStrings:
         self.__items = kw["values"]
      
      if "value" not in kw:
         kw["value"] = kw["values"][0]
      
      SmartWidget._setVariable(kw, "StringVar", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
   
   @property
   def itemsAreStrings(self):
      return self.__itemsAreStrings
   
   def bindOnSelected(self, handler):
      self.bind("<<ComboboxSelected>>", lambda _: handler())
   
   def getCurrentItem(self):
      return self.__items[self.getValueIndex()]
   
   def getValueIndexOrItemValue(self):
      return self.getValueIndex() if self.__itemsAreStrings else self.getCurrentItem().value
   
   def getValueIndex(self):
      return self["values"].index(self.getValue())
   
   @staticmethod
   def formatValueString(text, i, offset):
      if "{}" not in text:
         text += "{}"
      
      return text.format(i + offset)


class CommonCombobox(Combobox):
   def __init__(self, master, **kw):
      for key, value in (("justify", "center"), ("state", "readonly")):
         if key not in kw:
            kw[key] = value
      
      super().__init__(master, **kw)
