from ..smartwidget import SmartWidget, mergeJson

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "grid": {
         "padx": [20, 0],
         "pady": [20, 0],
         "childPadx": [20, 0],
         "childPady": [20, 0]
      }
   }
   
   @staticmethod
   def _defaultStyle(style = None):
      return mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
