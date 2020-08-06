from commonutils import DictPopper
from tkinter.ttk import Button
from .smartwidget import SmartWidget

class StatefulButton(SmartWidget, Button):
   def __init__(self, master, **kw):
      hasValueBuffer, self.__states = DictPopper(kw).add("hasValueBuffer", False).add("states")
      
      SmartWidget._setVariable(kw, "IntVar")
      
      SmartWidget.__init__(self, master, **kw)
      
      if hasValueBuffer:
         self._initValueAndTraceAdd()
      
      self.traceWrite(self.onStateChanged)
      
      self.onStateChanged()
   
   def nextState(self):
      self.getRawValue().set((self.getValue() + 1) % len(self.__states))
   
   def onStateChanged(self):
      self["text"] = self.__states[self.getValue()]
