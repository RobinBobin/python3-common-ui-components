from tkinter.ttk import Button
from .smartwidget import SmartWidget

class StatefulButton(SmartWidget, Button):
   def __init__(self, master, **kw):
      self.__states = kw.pop("states")
      
      SmartWidget._setVariable(kw, "IntVar")
      
      SmartWidget.__init__(self, master, **kw)
      
      self.__setText()
   
   def nextState(self):
      self.getRawValue().set((self.getValue() + 1) % len(self.__states))
      self.__setText()
   
   def __setText(self):
      self["text"] = self.__states[self.getValue()]
