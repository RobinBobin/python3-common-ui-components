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
   
   def grid(self, **kw):
      grid = self._mergeStyles("grid")
      
      if not self._isFirstChild():
         if kw.get("row", 0) and "pady" not in kw:
            kw["pady"] = grid["pady"]
         
         if kw.get("column", 0) and "padx" not in kw:
            kw["padx"] = grid["padx"]
      
      self.__class__.TKINTER_BASE.grid(self, **kw)
   
   def _mergeStyles(self, key):
      def f(styleName):
         s = SmartWidget._STYLE.configure(styleName, query_opt = key)
         
         return eval(s) if s else dict()
      
      return mergeJson(*map(f, [self.__class__.STYLE, self["style"]]), True)
   
   def _isFirstChild(self):
      return len(self.master.children) == 1
   
   @staticmethod
   def registerClass(clazz):
      clazz.STYLE = [clazz]
      clazz.TKINTER_BASE = None
      
      for base in clazz.__bases__:
         if issubclass(base, Widget):
            clazz.TKINTER_BASE = base
         
         if issubclass(base, SmartWidget):
            while base != SmartWidget:
               clazz.STYLE.append(base)
               
               base = base.__bases__[0]
      
      if clazz.TKINTER_BASE:
         clazz.STYLE.append(clazz.TKINTER_BASE)
      
      clazz.STYLE = f"T{'.T'.join([clz.__name__ for clz in clazz.STYLE])}"
      
      print(clazz.STYLE, clazz.TKINTER_BASE)
      
      try:
         SmartWidget._STYLE.configure(clazz.STYLE, **clazz._DEFAULT_STYLE)
      
      except:
         pass
   
   @staticmethod
   def wrapClass(tkinterBase):
      clazz = type(tkinterBase.__name__, (SmartWidget, tkinterBase), dict())
      
      globals()[tkinterBase.__name__] = clazz
      
      SmartWidget.registerClass(clazz)
