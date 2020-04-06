from ..smartwidget import SmartWidget, mergeJson

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "padx": [20, 0],
      "pady": [20, 0],
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
   
   def __init__(self, master = None, **kw):
      self.__children = kw.pop("children")
      
      SmartWidget.__init__(self, master, **kw)
      
      self.__children = SmartWidget._inflate(self, self.__children)
   
   def grid(self, **kw):
      self.__children.grid()
      
      SmartWidget.grid(self, **kw)
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   @staticmethod
   def _defaultStyle(style = None):
      return mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
