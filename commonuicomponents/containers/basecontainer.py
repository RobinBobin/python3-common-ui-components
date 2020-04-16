from commonutils import StaticUtils
from ..smartwidget import SmartWidget
from .. import CommonUIComponents

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
   
   def __init__(self, master = None, **kw):
      self._baseContainerChildren = kw.pop("children")
      self.__padAllChildren = kw.pop("padAllChildren", True)
      
      kw["hasValueBuffer"] = True
      
      SmartWidget.__init__(self, master, **kw)
      
      self._inflateChildren()
      
      self.__rows = 0
      self.__columns = 0
      
      for proxy in self._baseContainerChildren.values():
         self.__rows = max(proxy.value.row, self.__rows)
         self.__columns = max(proxy.value.column, self.__columns)
      
      self.__rows += 1
      self.__columns += 1
   
   def grid(self, **kw):
      for proxy in self._baseContainerChildren.values():
         proxy.value.grid(**self._getChildPadding(proxy.value))
      
      SmartWidget.grid(self, **kw)
   
   def _getChildPadding(self, smartWidget):
      result = dict()
      
      for isY, data in enumerate((("x", "column"), ("y", "row"))):
         padding = [int(x) for x in self._smartWidgetStyle[f"childPad{data[0]}"].split()] # TODO It can also be a scalar!
         
         sentinel = getattr(smartWidget, data[1])
         
         if not sentinel:
            padding[0] = 0 if not self.__padAllChildren else padding[0] / (2 if isY else 1)
         
         if self.__padAllChildren:
            if not isY:
               columnspan = smartWidget._smartWidgetGrid.get("columnspan", 0)
               
               if columnspan:
                  sentinel += columnspan - 1
            
            if sentinel == ((self.__rows if isY else self.__columns) - 1):
               padding[1] = int(self._smartWidgetStyle["childPadx"].split()[0])
         
         result[f"pad{data[0]}"] = padding
      
      return result
   
   def _inflateChildren(self):
      self._baseContainerChildren = CommonUIComponents._inflate(self, self._baseContainerChildren, self._smartWidgetValueBuffer)
   
   @staticmethod
   def _defaultStyle(style = None):
      return StaticUtils.mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
