from tkinter.ttk import Combobox as TtkCombobox
from .smartwidget import SmartWidget

class Combobox(SmartWidget, TtkCombobox):
   def __init__(self, master = None, **kw):
      SmartWidget._setFont(kw)
      
      SmartWidget._setVariable(kw, "StringVar", variableKey = "textvariable")
      
      SmartWidget.__init__(self, master, **kw)
      
      popdown = self.tk.eval(f"ttk::combobox::PopdownWindow {self}")
      self.tk.call(f"{popdown}.f.l", "configure", "-font", self["font"])
      
      self._initValueAndTraceAdd()
