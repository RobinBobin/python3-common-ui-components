from re import split
from tkinter.ttk import Style

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
   def grid(self, **kw):
      grid = self._mergeStyle("grid")
      
      if not self._isFirstChild():
         if kw.get("row", 0) and "pady" not in kw:
            kw["pady"] = grid["pady"]
         
         if kw.get("column", 0) and "padx" not in kw:
            kw["padx"] = grid["padx"]
      
      super().grid(**kw)
   
   def _mergeStyle(self, key):
      style = Style()
      
      default = eval(style.configure(self.__class__.STYLE, query_opt = key))
      custom = style.configure(self["style"], query_opt = key)
      
      return mergeJson(default, eval(custom), True) if custom else default
   
   def _isFirstChild(self):
      return len(self.master.children) == 1
