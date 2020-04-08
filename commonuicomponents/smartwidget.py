from commonutils import StaticUtils
from tkinter.ttk import Style, Widget

class Children:
   def __init__(self):
      self.__children = dict()
   
   def grid(self):
      for child in self.__children.values():
         child.grid()
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   def __iter__(self):
      return iter(self.__children.items())
   
   def __len__(self):
      return len(self.__children)
   
   def __setitem__(self, rowColumn, child):
      self.__children[rowColumn] = child


class SmartWidget:
   _STYLE_INSTANCE = Style()
   __CLASSES = dict()
   
   def __init__(self, master = None, **kw):
      self._style = StaticUtils.mergeJson(*map(lambda styleName: SmartWidget._STYLE_INSTANCE.configure(styleName) or dict(), [self.__class__.STYLE, kw.get("style", "")]), True)
      
      self.__grid = kw.pop("grid", dict())
      
      if self.__class__.__TKINTER_BASE:
         if "style" not in kw:
            kw["style"] = self.__class__.STYLE
         
         self.__class__.__TKINTER_BASE.__init__(self, master, **kw)
   
   def grid(self, **kw):
      self.__class__.__TKINTER_BASE.grid(self, **StaticUtils.mergeJson(kw, self.__grid, True))
   
   @property
   def row(self):
      return self.__grid["row"]
   
   @property
   def column(self):
      return self.__grid["column"]
   
   @staticmethod
   def inflate(master, config, grid = True):
      children = SmartWidget._inflate(master, config["ui"])
      
      if grid:
         children.grid()
      
      return children
   
   @staticmethod
   def registerClass(clazz):
      if not issubclass(clazz, SmartWidget):
         raise ValueError(f"{clazz.__name__} must subclass {SmartWidget.__name__}")
      
      clazz.STYLE = [clazz]
      clazz.__TKINTER_BASE = None
      
      for base in clazz.__bases__:
         if issubclass(base, Widget):
            clazz.__TKINTER_BASE = base
         
         if issubclass(base, SmartWidget):
            while base != SmartWidget:
               clazz.STYLE.append(base)
               
               for b in base.__bases__:
                  if issubclass(b, SmartWidget):
                     base = b
                     break
      
      if clazz.__TKINTER_BASE:
         clazz.STYLE.append(clazz.__TKINTER_BASE)
      
      clazz.STYLE = f"T{'.T'.join([clz.__name__ for clz in clazz.STYLE])}"
      
      if hasattr(clazz, "_DEFAULT_STYLE"):
         SmartWidget._STYLE_INSTANCE.configure(clazz.STYLE, **clazz._DEFAULT_STYLE)
      
      SmartWidget.__CLASSES[clazz.__name__] = clazz
   
   @staticmethod
   def wrapClass(tkinterBase):
      clazz = type(tkinterBase.__name__, (SmartWidget, tkinterBase), dict())
      
      SmartWidget.registerClass(clazz)
      
      return (tkinterBase.__name__, clazz)
   
   @staticmethod
   def _inflate(master, children):
      result = Children()
      
      row = 0
      column = -1
      
      for child in children:
         child = child.copy()
         
         repeatCount = child.pop("repeatCount", 1)
         text = child.pop("text", None)
         childType = child.pop("type")
         
         for i in range(repeatCount):
            ch = child.copy()
            
            if text != None:
               ch["text"] = text if repeatCount == 1 else text[i] if StaticUtils.isIterable(text) else f"{text}{i + 1}"
            
            grid = None
            
            if "grid" in ch:
               grid = ch["grid"]
            
            else:
               grid = dict()
               ch["grid"] = grid
            
            newRow = grid.pop("newRow", False)
            skipColumns = grid.pop("skipColumns", 0)
            
            if not newRow:
               column += 1 + skipColumns
            
            else:
               row += 1
               column = skipColumns
            
            grid["row"] = row
            grid["column"] = column
            
            result[(row, column)] = SmartWidget.__CLASSES[childType](master, **ch)
      
      return result
