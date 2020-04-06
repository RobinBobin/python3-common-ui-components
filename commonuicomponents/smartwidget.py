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

class SmartWidget:
   _STYLE_INSTANCE = Style()
   __CLASSES = dict()
   
   def __init__(self, master = None, **kw):
      self._style = mergeJson(*map(lambda styleName: SmartWidget._STYLE_INSTANCE.configure(styleName) or dict(), [self.__class__.STYLE, kw.get("style", "")]), True)
      
      self.__row = kw.pop("row", None)
      self.__column = kw.pop("column", None)
      
      if self.__class__._TKINTER_BASE:
         self.__class__._TKINTER_BASE.__init__(self, master, **kw)
   
   def grid(self, **kw):
      kw["row"] = self.__row
      kw["column"] = self.__column
      
      self.__class__._TKINTER_BASE.grid(self, **kw)
   
   def _isFirstChild(self, master = None):
      if not master:
         master = self.master
      
      return len(master.children) == 1
   
   @staticmethod
   def inflate(master, config):
      return SmartWidget._inflate(master, config["ui"])
   
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
      widgets = []
      
      row = -1
      column = 0
      
      for child in children:
         child = child.copy()
         
         newColumn = child.pop("newColumn", False)
         
         if not newColumn:
            row += 1
         
         else:
            row = 0
            column += 1
         
         child["row"] = row
         child["column"] = column
         
         widgets.append(SmartWidget.__CLASSES[child.pop("type")](master, **child))
      
      return widgets
