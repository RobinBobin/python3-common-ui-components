from commonutils import StaticUtils
from numbers import Number
# pylint: disable = unused-import
from tkinter import BooleanVar, IntVar, StringVar # _setVariable()
from tkinter.ttk import Widget

class SmartWidget:
   __FONT = None
   
   def __init__(self, master, **kw):
      self._namePrefix = kw.pop("namePrefix")
      self._parentContainer = master
      self._smartWidgetStorage = kw.pop("storage")
      self._smartWidgetGrid = kw.pop("grid")
      self._smartWidgetName = kw.pop("name", None)
      
      # Can be reset in children. pylint: disable = no-member
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
         self.__valueKeyInStorage = kw.pop("valueKeyInStorage")
      
      self.__processValueDomains(kw)
      
      if not self.__value and self.__valueDomains:
         raise ValueError(f"'valueDomain(s)' specified for '{self._smartWidgetName}', but there's no value to serialize")
      
      if self.__class__._TKINTER_BASE:
         if issubclass(self.__class__._TKINTER_BASE, Widget) and "style" not in kw:
            kw["style"] = self.__class__.STYLE
         
         self.__class__._TKINTER_BASE.__init__(self, master, **kw)
   
   def getRawValue(self):
      return self.__value
   
   def getValue(self):
      return self.__value.get()
   
   def grid(self, **kw):
      # pylint: disable = no-member, protected-access
      self.__class__._TKINTER_BASE.grid(self, **StaticUtils.mergeJson(kw, self._smartWidgetGrid, True))
   
   def reloadValue(self):
      if self.__valueDomains:
         self.__loadValue()
   
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
      
      for keys in (("values", ""), *self.__valueDomains):
         for k in keys:
            storage = StaticUtils.setIfAbsentAndGet(storage, k, dict())
      
      for domain in self.__valueDomains:
         storage = StaticUtils.setIfAbsentAndGet(storage, str(self._topLevelContainer.getSmartWidget(*domain).getValue()), dict())
      
      for name in (*self._namePrefix, self._smartWidgetName):
         storage = StaticUtils.setIfAbsentAndGet(storage, name, dict())
      
      return storage
   
   def _initValueAndTraceAdd(self):
      self.__loadValue()
      
      def _set(*_):
         self._getValueStorage()[""] = self.__value.get()
      
      self.__value.trace_add("write", _set)
   
   def __loadValue(self):
      self.__value.set(StaticUtils.setIfAbsentAndGet(self._getValueStorage(), self.__valueKeyInStorage, self._defaultValue))
   
   def __processValueDomains(self, kw):
      domainPresent = "valueDomain" in kw
      
      if all((domainPresent, "valueDomains" in kw)):
         raise ValueError(f"Only one of {('valueDomain', 'valueDomains')} can be present")
      
      self.__valueDomains = [kw.pop("valueDomain")] if domainPresent else kw.pop("valueDomains", [])
      
      for i in range(len(self.__valueDomains)):
         if isinstance(self.__valueDomains[i], str) and self.__valueDomains[i]:
            self.__valueDomains[i] = self.__valueDomains[i].split(".")
            
            if not self.__valueDomains[i][0]:
               self.__valueDomains[i][:1] = self._namePrefix
         
         elif not isinstance(self.__valueDomains[i], list):
            raise ValueError()
   
   @staticmethod
   def setFont(font):
      SmartWidget.__FONT = font
   
   @staticmethod
   def _setFont(kw):
      if "font" not in kw and SmartWidget.__FONT:
         kw["font"] = SmartWidget.__FONT
   
   @staticmethod
   def _setVariable(kw, defaultTypeName, defaultValueKey = "value", valueKeyInStorage = "", variableKey = None):
      # pylint: disable = eval-used
      value = eval(f"{kw.pop('valueType', defaultTypeName)}()")
      value.set(kw.get(defaultValueKey, value.get()))
      
      kw["value"] = value
      kw["valueKeyInStorage"] = valueKeyInStorage
      
      if variableKey:
         kw[variableKey] = value
