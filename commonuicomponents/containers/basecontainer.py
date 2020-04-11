from commonutils import StaticUtils
from ..smartwidget import SmartWidget
from .. import CommonUIComponents

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
   
   def __init__(self, master = None, **kw):
      self.__children = kw.pop("children")
      self.__padAllChildren = kw.pop("padAllChildren", True)
      
      kw["hasValueBuffer"] = True
      
      SmartWidget.__init__(self, master, **kw)
      
      self.__children = CommonUIComponents._inflate(self, self.__children, self._valueBuffer)
      
      self.__rows = 0
      self.__columns = 0
      
      for _, child in self.__children:
         self.__rows = max(child.row, self.__rows)
         self.__columns = max(child.column, self.__columns)
      
      self.__rows += 1
      self.__columns += 1
   
   def grid(self, **kw):
      for _, child in self.__children:
         child.grid(**self._getChildPadding(child))
      
      SmartWidget.grid(self, **kw)
   
   def _getChildPadding(self, smartWidget):
      result = dict()
      
      for isY, data in enumerate((("x", "column"), ("y", "row"))):
         padding = [int(x) for x in self._style[f"childPad{data[0]}"].split()] # TODO It can also be a scalar!
         
         sentinel = getattr(smartWidget, data[1])
         
         if not sentinel:
            padding[0] = 0 if not self.__padAllChildren else padding[0] / (2 if isY else 1)
         
         if self.__padAllChildren and sentinel == ((self.__rows if isY else self.__columns) - 1):
            padding[1] = int(self._style["childPadx"].split()[0])
            
         result[f"pad{data[0]}"] = padding
      
      return result
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   def __iter__(self):
      return iter(self.__children)
   
   @staticmethod
   def _defaultStyle(style = None):
      return StaticUtils.mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
