from re import split
from tkinter.ttk import Style, Widget

def mergeJson(a, b, overwrite = False):
   c = a.copy()
   
   for key, value in b.items():
      splitKey = split("[\[\]]", key)
      l = len(splitKey)
      
      if l == 1:
         if (key not in c) or overwrite:
            c[key] = value
         
         else:
            invalidType = type(c[key]) if not isinstance(c[key], dict) else type(value) if not isinstance(value, dict) else None
            
            if invalidType:
               raise ValueError(f"'{key}' exists in both JSONs but is a '{invalidType}' in one of them")
            
            c[key] = mergeJson(c[key], b[key])
      
      elif l == 3 and not len(splitKey[2]):
         c[splitKey[0]][int(splitKey[1])] = value
      
      else:
         raise ValueError(f"Something terrible happened: {key}, {splitKey}")
   
   return c


class Children:
   def __init__(self):
      self.__children = dict()
   
   def grid(self):
      for child in self.__children.values():
         child.grid()
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   def __iter__(self):
      return iter(self.__children)
   
   def __len__(self):
      return len(self.__children)
   
   def __setitem__(self, rowColumn, child):
      self.__children[rowColumn] = child


class SmartWidget:
   _STYLE_INSTANCE = Style()
   __CLASSES = dict()
   
   def __init__(self, master = None, **kw):
      self._style = mergeJson(*map(lambda styleName: SmartWidget._STYLE_INSTANCE.configure(styleName) or dict(), [self.__class__.STYLE, kw.get("style", "")]), True)
      
      self.__grid = kw.pop("grid", dict())
      
      if self.__class__._TKINTER_BASE:
         self.__class__._TKINTER_BASE.__init__(self, master, **kw)
   
   def grid(self, **kw):
      self.__class__._TKINTER_BASE.grid(self, **mergeJson(kw, self.__grid, True))
   
   def _isFirstChild(self, master = None):
      if not master:
         master = self.master
      
      return len(master.children) == 1
   
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
      clazz._TKINTER_BASE = None
      
      for base in clazz.__bases__:
         if issubclass(base, Widget):
            clazz._TKINTER_BASE = base
         
         if issubclass(base, SmartWidget):
            while base != SmartWidget:
               clazz.STYLE.append(base)
               
               for b in base.__bases__:
                  if issubclass(b, SmartWidget):
                     base = b
                     break
      
      if clazz._TKINTER_BASE:
         clazz.STYLE.append(clazz._TKINTER_BASE)
      
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
      
      row = -1
      column = 0
      
      for child in children:
         child = child.copy()
         
         grid = None
         
         if "grid" in child:
            grid = child["grid"]
         
         else:
            grid = dict()
            child["grid"] = grid
         
         newColumn = grid.pop("newColumn", False)
         
         if not newColumn:
            row += 1
         
         else:
            row = 0
            column += 1
         
         grid["row"] = row
         grid["column"] = column
         
         result[(row, column)] = SmartWidget.__CLASSES[child.pop("type")](master, **child)
      
      return result
