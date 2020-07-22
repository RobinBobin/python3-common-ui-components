from commonutils import StaticUtils
from .. import CommonUIComponents, SmartWidget

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
   
   def __init__(self, master, **kw):
      self._baseContainerChildren = kw.pop("children")
      self._baseContainerNamedChildren = dict()
      
      self.__padAllChildren = kw.pop("padAllChildren", True)
      
      SmartWidget.__init__(self, master, **kw)
      
      if not isinstance(master, BaseContainer):
         self._parentContainer = None
         self._topLevelContainer = self
      
      if self._smartWidgetName:
         self._namePrefix = self._namePrefix.copy()
         self._namePrefix.append(self._smartWidgetName)
      
      childPad = dict()
      
      for key in [f"childPad{key}" for key in "xy"]:
         cpad = self._smartWidgetGrid.pop(key, None)
         
         if cpad:
            childPad[key] = cpad
      
      self._smartWidgetStyle = StaticUtils.mergeJson(self._smartWidgetStyle, childPad, True)
      
      self._inflateChildren()
      
      self.__rows = 0
      self.__columns = 0
      
      for widget in self._baseContainerChildren.values():
         self.__rows = max(widget.row, self.__rows)
         self.__columns = max(widget.column, self.__columns)
      
      self.__rows += 1
      self.__columns += 1
   
   def getSmartWidget(self, *keys, named = True):
      result = None
      
      if not keys:
         result = self._baseContainerNamedChildren if named else self._baseContainerChildren
      
      else:
         result = self
         
         for key in keys:
            result = (result._baseContainerNamedChildren if isinstance(key, str) else result._baseContainerChildren)[key]
      
      return result
   
   def grid(self, **kw):
      for widget in self._baseContainerChildren.values():
         widget.grid(**self._getChildPadding(widget))
      
      SmartWidget.grid(self, **kw)
   
   def reloadValue(self):
      super().reloadValue()
      
      for widget in self._baseContainerNamedChildren.values():
         widget.reloadValue()
   
   def _getChildPadding(self, smartWidget):
      result = dict()
      
      for isY, data in enumerate((("x", "column"), ("y", "row"))):
         padKey = f"pad{data[0]}"
         
         padding = smartWidget._smartWidgetStyle.get(padKey, self._smartWidgetStyle[f"childPad{data[0]}"]).copy()
         
         sentinel = getattr(smartWidget, data[1])
         
         if not sentinel:
            padding[0] = 0 if not self.__padAllChildren else padding[0] / (2 if isY else 1)
         
         if self.__padAllChildren:
            if not isY:
               columnspan = smartWidget._smartWidgetGrid.get("columnspan", 0)
               
               if columnspan:
                  sentinel += columnspan - 1
            
            if sentinel == ((self.__rows if isY else self.__columns) - 1):
               padding[1] = self._smartWidgetStyle["childPadx"][0]
         
         result[padKey] = padding
      
      return result
   
   def _inflateChildren(self):
      self._baseContainerChildren = CommonUIComponents._inflate(self, self._baseContainerChildren, self._smartWidgetStorage, self._namePrefix)
   
   @staticmethod
   def _defaultStyle(style = None):
      return StaticUtils.mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
