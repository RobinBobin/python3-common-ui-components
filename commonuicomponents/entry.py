from commonutils import StaticUtils
from tkinter import StringVar
from tkinter.ttk import Entry as TtkEntry
from .smartwidget import SmartWidget

class Entry(SmartWidget, TtkEntry):
   __FONT = None
   
   def __init__(self, master = None, **kw):
      if "font" not in kw and Entry.__FONT:
         kw["font"] = Entry.__FONT
      
      value = StringVar()
      value.set(kw.get("text", ""))
      
      kw["hasValueBuffer"] = True
      kw["value"] = kw["textvariable"] = value
      
      SmartWidget.__init__(self, master, **kw)
      
      self.value.set(StaticUtils.getOrSetIfAbsent(self._smartWidgetValueBuffer, 0, self.value.get()))
      
      self.value.trace_add("write", lambda *_: StaticUtils.setSafely(self._smartWidgetValueBuffer, 0, self.value.get()))
   
   @staticmethod
   def setFont(font):
      Entry.__FONT = font
