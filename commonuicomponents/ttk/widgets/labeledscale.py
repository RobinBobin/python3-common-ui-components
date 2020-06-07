from commonutils import StaticUtils
from tkinter import E, IntVar, W
from tkinter.ttk import Frame, Label, Scale
from .smartwidget import SmartWidget

class LabeledScale(SmartWidget):
   def __init__(self, master, **kw):
      self.__multiplyValue = kw.pop("multiplyValue", False)
      
      twoRows = kw.pop("twoRows", False)
      value = kw.pop("value", None)
      
      kw["columns"] = 1 if twoRows else 3
      kw["rows"] = 1
      kw["value"] = IntVar()
      
      self.__frame = Frame(master) if twoRows else None
      
      super().__init__(master, **kw)
      
      if self.__frame:
         master = self.__frame
      
      # = Step = #
      self.__step = kw.get("step", 1)
      
      storage = self._getValueStorage()
      
      if "" in storage:
         value = storage.pop("")
      
      else:
         for data in zip(range(2), ("from_", "to")):
            kw["range"][data[0]] = StaticUtils.setIfAbsentAndGet(storage, data[1], kw["range"][data[0]])
         
         value = StaticUtils.setIfAbsentAndGet(storage, "value", kw["range"][0] // self.__step if value == None else value)
      
      # = Caption = #
      self.__caption = Label(master, text = kw["text"])
      self.__value = Label(master, anchor = E)
      
      # = Scale = #
      self.getRawValue().trace_add("write", self.onChanged)
      self.getRawValue().set(value)
      
      from_, to = tuple(v // self.__step for v in kw["range"])
      
      self.__scale = Scale(
         master,
         from_ = from_,
         length = 400,
         to = to,
         variable = self.getRawValue())
      
      self.__setValueWidth()
   
   def getValue(self):
      return super().getValue() * (self.__step if self.__multiplyValue else 1)
   
   def grid(self, **kw):
      kw = StaticUtils.mergeJson(kw, self._smartWidgetGrid, True)
      
      if self.__frame:
         self.__frame.columnconfigure(1, weight = 1)
         self.__frame.grid(sticky = W + E, **kw)
         
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
   
   def onChanged(self, *_):
      value = self.getRawValue().get()
      
      self.__value["text"] = value * self.__step
      
      self._getValueStorage()["value"] = value
   
   def setFrom(self, from_):
      self.__scale["from"] = from_
      self._getValueStorage()["from_"] = from_
      
      if self.getValue() < from_:
         self.getRawValue().set(from_)
      
      self.__setValueWidth()
   
   def setTo(self, to):
      self.__scale["to"] = to
      self._getValueStorage()["to"] = to
      
      if self.getValue() > to:
         self.getRawValue().set(to)
      
      self.__setValueWidth()
   
   def __setValueWidth(self):
      self.__value["width"] = max(StaticUtils.getPlaces([x * self.__step for x in (self.__scale["from"], self.__scale["to"])]))
