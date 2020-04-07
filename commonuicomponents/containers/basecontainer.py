from ..smartwidget import SmartWidget, mergeJson

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "padx": [20, 0],
      "pady": [20, 0],
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
   
   def __init__(self, master = None, padAllChildren = True, **kw):
      self.__children = kw.pop("children")
      self.__padAllChildren = padAllChildren
      
      SmartWidget.__init__(self, master, **kw)
      
      self.__children = SmartWidget._inflate(self, self.__children)
      
      self.__rows = 0
      self.__columns = 0
      
      for _, child in self.__children:
         self.__rows = max(child.row, self.__rows)
         self.__columns = max(child.column, self.__columns)
      
      self.__rows += 1
      self.__columns += 1
   
   def grid(self, **kw):
      for _, child in self.__children:
         child.grid(**self._getPadding(child, "childPad"))
      
      SmartWidget.grid(self, **kw)
   
   def _getPadding(self, smartWidget, key):
      result = dict()
      
      for isY, data in enumerate((("x", "column"), ("y", "row"))):
         padding = [int(x) for x in self._style[f"{key}{data[0]}"].split()] # TODO It can also be a scalar!
         
         sentinel = getattr(smartWidget, data[1])
         
         if not sentinel:
            padding[0] = 0 if not self.__padAllChildren else padding[0] / (2 if isY else 1)
         
         if self.__padAllChildren and sentinel == ((self.__rows if isY else self.__columns) - 1):
            padding[1] = int(self._style[f"{key}x"].split()[0])
            
         result[f"pad{data[0]}"] = padding
      
      return result
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   @staticmethod
   def _defaultStyle(style = None):
      return mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
