from tkinter.ttk import Entry as TtkEntry
from .smartwidget import SmartWidget

class Entry(SmartWidget, TtkEntry):
   def __init__(self, master, **kw):
      self.__uppercase = kw.pop("uppercase", False)
      
      SmartWidget._setFont(kw)
      
      SmartWidget._setVariable(kw, "StringVar", defaultValueKey = "text", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
      
      if self.__uppercase:
         self.bind("<KeyRelease>", self.onKeyRelease)
   
   @property
   def uppercase(self):
      return self.__uppercase
   
   def onKeyRelease(self, _):
      text = self.getRawValue().get()
      uppercase = text.upper()
      
      if text != uppercase:
         self.getRawValue().set(uppercase)
