from commonutils import StaticUtils
from math import floor, log10
from tkinter import E, IntVar, W
from tkinter.ttk import Frame, Label, Scale
from .smartwidget import SmartWidget

class LabeledScale(SmartWidget):
   def __init__(self, master = None, **kw):
      twoRows = kw.pop("twoRows", False)
      
      kw["columns"] = 1 if twoRows else 3
      kw["rows"] = 1
      kw["hasValueBuffer"] = True
      kw["value"] = IntVar()
      
      self.__frame = Frame(master) if twoRows else None
      
      super().__init__(master, **kw)
      
      if self.__frame:
         master = self.__frame
      
      # = Caption = #
      self.__caption = Label(master, text = kw["text"])
      
      # = Value = #
      self.__step = kw.get("step", 1)
      
      from_, to = [value // self.__step for value in kw["range"]]
      
      value = StaticUtils.getOrSetIfAbsent(self._smartWidgetValueBuffer, 0, from_)
      
      self.__value = Label(master, anchor = E, text = value * self.__step, width = floor(log10(abs(to) * self.__step)) + 1)
      
      # = Scale = #
      self.value.set(value)
      
      self.__scale = Scale(
         master,
         command = self.onChanged,
         from_ = from_,
         length = 400,
         to = to,
         variable = self.value)
   
   def grid(self, **kw):
      kw = StaticUtils.mergeJson(kw, self._smartWidgetGrid, True)
      
      if self.__frame:
         self.__frame.grid(**kw)
         
         self.__caption.grid(column = 0, row = 0, sticky = W)
         self.__value.grid(column = 1, padx = (20, 0), row = 0, sticky = E)
         self.__scale.grid(column = 0, columnspan = 2, pady = (20, 0), row = 1, sticky = W + E)
      
      else:
         padxRight = kw["padx"][1] # TODO It can also be a scalar!
         kw["padx"][1] = 0 # TODO It can also be a scalar!
         self.__caption.grid(sticky = E, **kw)
         
         kw["column"] += 1
         kw["padx"] = [20, 0]
         self.__value.grid(sticky = W + E, **kw)
         
         kw["column"] += 1
         kw["padx"][1] = padxRight
         self.__scale.grid(**kw)
   
   def onChanged(self, _):
      value = self.value.get()
      
      self.__value.configure(text = value * self.__step)
      
      StaticUtils.setSafely(self._smartWidgetValueBuffer, 0, value)
