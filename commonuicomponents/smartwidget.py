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
   _STYLE = Style()
   __CLASSES = dict()
   
   def __init__(self, master, ui):
      self._newColumn = ui.pop("newColumn", False)
      
      if self.__class__.__TKINTER_BASE:
         self.__class__.__TKINTER_BASE.__init__(self, master, **ui)
   
   def _mergeStyles(self, style = None):
      def f(styleName):
         s = SmartWidget._STYLE.configure(styleName)
         
         return eval(s) if s else dict()
      
      if not style:
         style = self["style"]
      
      return mergeJson(*map(f, [self.__class__.STYLE, style]), True)
   
   def _isFirstChild(self, master = None):
      if not master:
         master = self.master
      
      return len(master.children) == 1
   
   @staticmethod
   def inflate(master, configOrChildren):
      def f(ui):
         ui = ui.copy()
         
         return SmartWidget.__CLASSES[ui.pop("type")](master, ui)
      
      ui = configOrChildren["ui"] if isinstance(configOrChildren, dict) else configOrChildren
      
      return map(f, ui)
   
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
      
      try:
         SmartWidget._STYLE.configure(clazz.STYLE, **clazz.__DEFAULT_STYLE)
      
      except:
         pass
      
      SmartWidget.__CLASSES[clazz.__name__] = clazz
   
   @staticmethod
   def wrapClass(tkinterBase):
      clazz = type(tkinterBase.__name__, (SmartWidget, tkinterBase), dict())
      
      SmartWidget.registerClass(clazz)
      
      return (tkinterBase.__name__, clazz)
