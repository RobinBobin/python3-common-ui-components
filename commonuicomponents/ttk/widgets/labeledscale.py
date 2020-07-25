from commonutils import StaticUtils
from tkinter import E, W
from tkinter.ttk import Frame, Label, Scale
from .smartwidget import SmartWidget

class LabeledScale(SmartWidget):
   def __init__(self, master, **kw):
      self.__multiplyValue = kw.pop("multiplyValue", False)
      
      twoRows = kw.pop("twoRows", False)
      
      kw["columns"] = 1 if twoRows else 3
      kw["rows"] = 1
      
      valueIsNone = "value" not in kw
      
      SmartWidget._setVariable(kw, "IntVar")
      
      self.__frame = Frame(master) if twoRows else None
      
      super().__init__(master, **kw)
      
      if self.__frame:
         master = self.__frame
      
      # = Step = #
      self.__step = kw.get("step", 1)
      
      # = Caption = #
      self.__caption = Label(master, text = kw["text"])
      self.__valueLabel = Label(master, anchor = E)
      
      # = Scale = #
      self.getRawValue().trace_add("write", self.onChanged)
      
      storage = self._getValueStorage()
      
      for index, key in enumerate(("from_", "to")):
         if key in storage:
            kw["range"][index] = storage[key]
      
      self.getRawValue().set(StaticUtils.setIfAbsentAndGet(storage, "value", (kw["range"][0] if valueIsNone else self.getValue()) // self.__step))
      
      from_, to = tuple(v // self.__step for v in kw["range"])
      
      self.__scale = Scale(
         master,
         from_ = from_,
         length = 400,
         to = to,
         variable = self.getRawValue())
      
      if "state" in kw:
         self.__scale["state"] = kw["state"]
      
      self.__setValueWidth()
   
   def __getitem__(self, key):
      return self.__scale[key]
   
   def __setitem__(self, key, value):
      self.__scale[key] = value
   
   def bindScale(self, event, handler):
      self.__scale.bind(event, handler)
   
   def getRelativeValue(self):
      return (super().getValue() - self.__scale["from"]) * (self.__step if self.__multiplyValue else 1)
   
   def getValue(self):
      return super().getValue() * (self.__step if self.__multiplyValue else 1)
   
   def grid(self, **kw):
      kw = StaticUtils.mergeJson(kw, self._smartWidgetGrid, True)
      
      if self.__frame:
         self.__frame.columnconfigure(1, weight = 1)
         self.__frame.grid(sticky = W + E, **kw)
         
         self.__caption.grid(column = 0, row = 0, sticky = W)
         self.__valueLabel.grid(column = 1, padx = (20, 0), row = 0, sticky = E)
         self.__scale.grid(column = 0, columnspan = 2, pady = (20, 0), row = 1, sticky = W + E)
      
      else:
         padxRight = kw["padx"][1] # TODO It can also be a scalar!
         kw["padx"][1] = 0 # TODO It can also be a scalar!
         self.__caption.grid(sticky = E, **kw)
         
         kw["column"] += 1
         kw["padx"] = [20, 0]
         self.__valueLabel.grid(sticky = W + E, **kw)
         
         kw["column"] += 1
         kw["padx"][1] = padxRight
         self.__scale.grid(**kw)
   
   def onChanged(self, *_):
      value = self.getRawValue().get()
      
      self.__valueLabel["text"] = value * self.__step
      
      self._getValueStorage()["value"] = value
   
   def setFrom(self, from_, **args):
      self.__scale["from"] = from_ // self.__step
      self._getValueStorage()["from_"] = from_
      self._defaultValue = self.__scale["from"]
      
      if args.get("validate", True) and self.getValue() < self._defaultValue:
         self.getRawValue().set(self._defaultValue)
      
      self.__setValueWidth()
   
   def setTo(self, to, **args):
      self.__scale["to"] = to // self.__step
      self._getValueStorage()["to"] = to
      
      if args.get("validate", True) and self.getValue() > self.__scale["to"]:
         self.getRawValue().set(self.__scale["to"])
      
      self.__setValueWidth()
   
   def __setValueWidth(self):
      self.__valueLabel["width"] = max(StaticUtils.getPlaces([x * self.__step for x in (self.__scale["from"], self.__scale["to"])]))
