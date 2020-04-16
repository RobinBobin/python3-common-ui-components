from commonutils import StaticUtils
from tkinter.ttk import Style

class SmartWidget:
   _STYLE_INSTANCE = Style()
   
   def __init__(self, master = None, **kw):
      self._smartWidgetGrid = kw.pop("grid")
      
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
