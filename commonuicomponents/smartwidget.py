from commonutils import StaticUtils
from tkinter.ttk import Style

class SmartWidget:
   _STYLE_INSTANCE = Style()
   
   def __init__(self, master = None, **kw):
      self._style = StaticUtils.mergeJson(*map(lambda styleName: SmartWidget._STYLE_INSTANCE.configure(styleName) or dict(), [self.__class__.STYLE, kw.get("style", "")]), True)
      
      self.__grid = kw.pop("grid")
      self.__rows = kw.pop("rows", 1)
      self.__columns = kw.pop("columns", 1)
      
      if self.__class__._TKINTER_BASE:
         if "style" not in kw:
            kw["style"] = self.__class__.STYLE
         
         self.__class__._TKINTER_BASE.__init__(self, master, **kw)
   
   def grid(self, **kw):
      self.__class__._TKINTER_BASE.grid(self, **StaticUtils.mergeJson(kw, self.__grid, True))
   
   @property
   def row(self):
      return self.__grid["row"]
   
   @property
   def rows(self):
      return self.__rows
   
   @property
   def columns(self):
      return self.__columns
   
   @property
   def column(self):
      return self.__grid["column"]
