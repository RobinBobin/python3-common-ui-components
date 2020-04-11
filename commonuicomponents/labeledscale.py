from commonutils import StaticUtils
from math import floor, log10
from tkinter import E, IntVar, W
from tkinter.ttk import Label, Scale
from .smartwidget import SmartWidget

class LabeledScale(SmartWidget):
   def __init__(self, master = None, **kw):
      kw["rows"] = 1
      kw["columns"] = 3
      kw["hasValueBuffer"] = True
      
      super().__init__(master, **kw)
      
      # = Caption = #
      self.__caption = Label(master, text = kw["text"])
      
      # = Value = #
      self.__step = kw.get("step", 1)
      
      from_, to = [value // self.__step for value in kw["range"]]
      
      value = StaticUtils.getOrSetIfAbsent(self._valueBuffer, 0, from_)
      
      self.__value = Label(master, anchor = E, text = value * self.__step, width = floor(log10(abs(to) * self.__step)) + 1)
      
      # = Scale = #
      self.__variable = IntVar()
      self.__variable.set(value)
      
      self.__scale = Scale(
         master,
         command = self.onChanged,
         from_ = from_,
         length = 400,
         to = to,
         variable = self.__variable)
   
   def grid(self, **kw):
      kw["row"] = self.row
      kw["column"] = self.column
      
      self.__caption.grid(sticky = E, **kw)
      
      padx = kw["padx"]
      kw["padx"] = [20, 0]
      
      kw["column"] += 1
      self.__value.grid(sticky = W + E, **kw)
      
      kw["column"] += 1
      kw["padx"][1] = padx[1] # TODO It can also be a scalar!
      self.__scale.grid(**kw)
   
   def onChanged(self, _):
      value = self.__variable.get()
      
      self.__value.configure(text = value * self.__step)
      
      StaticUtils.setSafely(self._valueBuffer, 0, value)
