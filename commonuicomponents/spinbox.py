from tkinter.ttk import Spinbox as TtkSpinbox
from .smartwidget import SmartWidget

class Spinbox(SmartWidget, TtkSpinbox):
   def __init__(self, master = None, **kw):
      SmartWidget._setFont(kw)
      SmartWidget._setVariable(kw, "IntVar", "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      self._initValueAndTraceAdd()
