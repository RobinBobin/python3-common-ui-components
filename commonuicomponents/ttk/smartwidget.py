from commonutils import StaticUtils
from tkinter import BooleanVar, IntVar, StringVar # _setVariable()

class SmartWidget:
   __FONT = None
   
   def __init__(self, master = None, **kw):
      self._smartWidgetGrid = kw.pop("grid")
      
      # Can be reset in children.
      self._smartWidgetStyle = StaticUtils.mergeJson(*map(lambda styleName: SmartWidget._STYLE_INSTANCE.configure(styleName) or dict(), [self.__class__.STYLE, kw.get("style", "")]), True)
      
      self.__columns = kw.pop("columns", 1)
      self.__rows = kw.pop("rows", 1)
      self.__smartWidgetName = kw.pop("name", None)
      self.__value = kw.pop("value", None)
      
      parentBuffer = kw.pop("parentBuffer")
      parentBufferIndex = kw.pop("parentBufferIndex")
      
      if kw.pop("hasValueBuffer", False):
         self._smartWidgetValueBuffer = StaticUtils.getOrSetIfAbsent(parentBuffer, parentBufferIndex, [])
      
      if self.__class__._TKINTER_BASE:
         from tkinter.ttk import Widget
         
         if issubclass(self.__class__._TKINTER_BASE, Widget) and "style" not in kw:
            kw["style"] = self.__class__.STYLE
         
         self.__class__._TKINTER_BASE.__init__(self, master, **kw)
   
   def grid(self, **kw):
      self.__class__._TKINTER_BASE.grid(self, **StaticUtils.mergeJson(kw, self._smartWidgetGrid, True))
   
   @property
   def column(self):
      return self._smartWidgetGrid["column"]
   
   @property
   def columns(self):
      return self.__columns
   
   @property
   def hasValueBuffer(self):
      return hasattr(self, "_smartWidgetValueBuffer")
   
   @property
   def row(self):
      return self._smartWidgetGrid["row"]
   
   @property
   def rows(self):
      return self.__rows
   
   @property
   def smartWidgetName(self):
      return self.__smartWidgetName
   
   @property
   def value(self):
      return self.__value
   
   def _initValueAndTraceAdd(self):
      self.__value.set(StaticUtils.getOrSetIfAbsent(self._smartWidgetValueBuffer, 0, self.__value.get()))
         
      self.__value.trace_add("write", lambda *_: StaticUtils.setSafely(self._smartWidgetValueBuffer, 0, self.__value.get()))
   
   @staticmethod
   def setFont(font):
      SmartWidget.__FONT = font
   
   @staticmethod
   def _setFont(kw):
      if "font" not in kw and SmartWidget.__FONT:
         kw["font"] = SmartWidget.__FONT
   
   @staticmethod
   def _setVariable(kw, defaultTypeName, defaultValueKey = "value", setHasValueBuffer = True, variableKey = None):
      value = eval(f"{kw.pop('valueType', defaultTypeName)}()")
      value.set(kw.get(defaultValueKey, value.get()))
      
      kw["value"] = value
      
      if variableKey:
         kw[variableKey] = value
      
      if setHasValueBuffer:
         kw["hasValueBuffer"] = True
