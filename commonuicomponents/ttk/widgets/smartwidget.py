from commonutils import DictPopper, StaticUtils
from numbers import Number
from tkinter import BooleanVar, IntVar, StringVar
from tkinter.ttk import Widget
from ...json import Config

class SmartWidget:
   __FONT = None
   __VALUE_TYPES = { t.__name__: t for t in (BooleanVar, IntVar, StringVar) }
   
   def __init__(self, master, **kw):
      self._parentContainer = master
      
      self.__getValueWhenStoring \
      , self._namePrefix         \
      , self._smartWidgetStorage \
      , self._smartWidgetGrid    \
      , self._smartWidgetName = DictPopper(kw)  \
         .add("getValueWhenStoring", False)     \
         .add("namePrefix")                     \
         .add("storage")                        \
         .add("grid")                           \
         .add("name", None)
      
      # Can be reset in children.
      self._smartWidgetStyle = StaticUtils.mergeJson(*map(lambda styleName: SmartWidget._STYLE_INSTANCE.configure(styleName) or dict(), [self.__class__.STYLE, kw.get("style", "")]), True)
      
      if hasattr(self._parentContainer, "_topLevelContainer"):
         self._topLevelContainer = self._parentContainer._topLevelContainer
      
      if self._smartWidgetName:
         result = self._topLevelContainer.getSmartWidget(*self._namePrefix)
         
         if isinstance(result, SmartWidget):
            result = result._baseContainerNamedChildren
         
         result[self._smartWidgetName] = self
      
      for d in (self._smartWidgetGrid, self._smartWidgetStyle):
         for key, value in d.items():
            if key in ("padx", "pady", "childPadx", "childPady"):
               value = [value] if isinstance(value, Number) else [float(v) for v in value.split()] if isinstance(value, str) else value if isinstance(value, list) else None
               
               if len(value) == 1:
                  value.append(value[0])
               
               d[key] = value
      
      self.__columns = kw.pop("columns", 1)
      self.__rows = kw.pop("rows", 1)
      self.__value = kw.pop("value", None)
      
      if self.__value:
         self._defaultValue = self.__value.get()
      
      self.__valueDomains = tuple(map(self.__processValueDomains, kw.pop("valueDomains", [])))
      
      if not self.__value and self.__valueDomains:
         raise ValueError(f"'valueDomains' specified for '{self._smartWidgetName}', but there's no value to serialize")
      
      if self.__class__._TKINTER_BASE:
         if issubclass(self.__class__._TKINTER_BASE, Widget) and "style" not in kw:
            kw["style"] = self.__class__.STYLE
         
         self.__class__._TKINTER_BASE.__init__(self, master, **kw)
   
   def getRawValue(self):
      return self.__value
   
   def getValue(self):
      return self.__value.get()
   
   def grid(self, **kw):
      self.__class__._TKINTER_BASE.grid(self, **StaticUtils.mergeJson(kw, self._smartWidgetGrid, True))
   
   def reloadValue(self):
      if self.__valueDomains:
         self.__loadValue()
   
   def traceWrite(self, handler):
      return self.__value.trace_add("write", lambda *_: handler())
   
   @property
   def column(self):
      return self._smartWidgetGrid["column"]
   
   @property
   def columns(self):
      return self.__columns
   
   @property
   def row(self):
      return self._smartWidgetGrid["row"]
   
   @property
   def rows(self):
      return self.__rows
   
   @property
   def smartWidgetName(self):
      return self._smartWidgetName
   
   def _getValueStorage(self):
      if not self._smartWidgetName:
         raise ValueError("Can't serialize nameless widgets")
      
      storage = self._smartWidgetStorage
      
      for domain in self.__valueDomains:
         storage = StaticUtils.setIfAbsentAndGet(storage, f"{'.'.join(domain)}={str(self._topLevelContainer.getSmartWidget(*domain).getValue())}", dict())
      
      for name in (*self._namePrefix, self._smartWidgetName):
         storage = StaticUtils.setIfAbsentAndGet(storage, name, dict())
      
      return storage
   
   def _initValueAndTraceAdd(self):
      self.__loadValue()
      
      def _set():
         self._getValueStorage()["value"] = self.getValue() if self.__getValueWhenStoring else self.__value.get()
      
      self.traceWrite(_set)
   
   def __loadValue(self):
      self.__value.set(StaticUtils.setIfAbsentAndGet(self._getValueStorage(), "value", self._defaultValue))
   
   def __processValueDomains(self, valueDomain):
      valueDomain = valueDomain.split(".")
      
      if not valueDomain[0]:
         valueDomain[:1] = self._namePrefix
      
      return valueDomain
   
   @staticmethod
   def setFont():
      SmartWidget.__FONT = Config["widgetFont"]
   
   @staticmethod
   def _setFont(kw):
      if "font" not in kw and SmartWidget.__FONT:
         kw["font"] = SmartWidget.__FONT
   
   @staticmethod
   def _setGetValueWhenStoring(kw):
      kw["getValueWhenStoring"] = True
   
   @staticmethod
   def _setVariable(kw, defaultTypeName, defaultValueKey = "value", variableKey = None):
      value = SmartWidget.__VALUE_TYPES[kw.pop('valueType', defaultTypeName)]()
      value.set(kw.get(defaultValueKey, value.get()))
      
      kw["value"] = value
      
      if variableKey:
         kw[variableKey] = value
