from commonutils import StaticUtils
from tkinter import BooleanVar
from tkinter.ttk import Checkbutton as TtkCheckbutton
from .smartwidget import SmartWidget

class Checkbutton(SmartWidget, TtkCheckbutton):
   def __init__(self, master = None, **kw):
      value = BooleanVar()
      value.set(kw.get("value", False))
      
      kw["value"] = kw["variable"] = value
      
      SmartWidget.__init__(self, master, **kw)
      
      if self.hasValueBuffer:
         self.value.set(StaticUtils.getOrSetIfAbsent(self._smartWidgetValueBuffer, 0, self.value.get()))
         
         self.value.trace_add("write", lambda *_: StaticUtils.setSafely(self._smartWidgetValueBuffer, 0, self.value.get()))
