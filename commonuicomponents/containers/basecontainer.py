from ..smartwidget import SmartWidget, mergeJson

class BaseContainer(SmartWidget):
   __DEFAULT_STYLE = {
      "padx": [20, 0],
      "pady": [20, 0],
      "childPadx": [20, 0],
      "childPady": [20, 0]
   }
   
   def __init__(self, master, ui):
      children = SmartWidget.inflate(self, ui.pop("ui"))
      
      SmartWidget.__init__(self, master, ui)
      
      row = -1
      column = 0
      
      for child in children:
         if not child._newColumn:
            row += 1
         
         else:
            row = 0
            column += 1
         
         child.grid(row = row, column = column)
   
   @staticmethod
   def _defaultStyle(style = None):
      return mergeJson(BaseContainer.__DEFAULT_STYLE, style) if style else BaseContainer.__DEFAULT_STYLE
