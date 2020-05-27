from tkinter.ttk import Entry as TtkEntry
from .smartwidget import SmartWidget

class Entry(SmartWidget, TtkEntry):
   def __init__(self, master, **kw):
      SmartWidget._setFont(kw)
      
      SmartWidget._setVariable(kw, "StringVar", defaultValueKey = "text", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
