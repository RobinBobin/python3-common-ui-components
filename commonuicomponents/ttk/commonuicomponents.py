from copy import deepcopy
from tkinter.ttk import Style
from .multiplier import Multiplier
from .widgets.smartwidget import SmartWidget
from ..staticutils import StaticUtils

class CommonUIComponents:
   __CLASSES = dict()
   
   @staticmethod
   def inflate(tab):
      ui = CommonUIComponents._inflate(tab.baseTabFrame, [tab.baseTabConfig["ui"]], tab.baseTabConfig, [])
      
      if len(ui) != 1:
         raise ValueError("len(ui) != 1")
      
      for value in ui.values():
         ui = value
      
      return ui
   
   @staticmethod
   def init(**params):
      params = StaticUtils.mergeJson({
         "debug": False
      }, params, True)
      
      for key, value in params.items():
         setattr(CommonUIComponents, key.upper(), value)
      
      SmartWidget._STYLE_INSTANCE = Style()
      
      from tkinter import Canvas
      from tkinter.ttk import Button, Label, Radiobutton
      from .containers.container import Container
      from .containers.labeledcontainer import LabeledContainer
      from .containers.labeledradiobuttongroup import LabeledRadioButtonGroup
      from .widgets.checkbutton import Checkbutton
      from .widgets.combobox import Combobox
      from .widgets.entry import Entry
      from .widgets.labeledscale import LabeledScale
      from .widgets.spinbox import Spinbox
      from .widgets.statefulbutton import StatefulButton
      
      for tkinterBase in (Button, Canvas, Label, Radiobutton):
         CommonUIComponents.wrapClass(tkinterBase)
      
      for smartWidget in (
         Checkbutton,
         Combobox,
         Container,
         Entry,
         LabeledContainer,
         LabeledRadioButtonGroup,
         LabeledScale,
         Spinbox,
         StatefulButton
      ):
         CommonUIComponents.registerClass(smartWidget)
   
   @staticmethod
   def registerClass(clazz):
      if not issubclass(clazz, SmartWidget):
         raise ValueError(f"{clazz.__name__} must subclass {SmartWidget.__name__}")
      
      clazz.STYLE = [clazz]
      clazz._TKINTER_BASE = None
      
      from tkinter import Widget
      
      for base in clazz.__bases__:
         if issubclass(base, Widget):
            clazz._TKINTER_BASE = CommonUIComponents.__CLASSES["LabeledContainer"]._TKINTER_BASE if clazz.__name__ == "LabeledRadioButtonGroup" else base # TODO Dirty hack :( .
         
         if issubclass(base, SmartWidget):
            while base != SmartWidget:
               clazz.STYLE.append(base)
               
               for b in base.__bases__:
                  if issubclass(b, SmartWidget):
                     base = b
                     break
      
      if clazz._TKINTER_BASE:
         clazz.STYLE.append(clazz._TKINTER_BASE)
      
      clazz.STYLE = f"T{'.T'.join([clz.__name__ for clz in clazz.STYLE])}"
      
      if hasattr(clazz, "_DEFAULT_STYLE"):
         SmartWidget._STYLE_INSTANCE.configure(clazz.STYLE, **clazz._DEFAULT_STYLE)
      
      CommonUIComponents.__CLASSES[clazz.__name__] = clazz
      
      if CommonUIComponents.DEBUG:
         print(f"registered {clazz} (TKINTER_BASE: {clazz._TKINTER_BASE}, STYLE: '{clazz.STYLE}'.")
   
   @staticmethod
   def wrapClass(tkinterBase):
      CommonUIComponents.registerClass(type(tkinterBase.__name__, (SmartWidget, tkinterBase), dict()))
   
   @staticmethod
   def _inflate(master, children, config, namePrefix):
      result = dict()
      
      row = 0
      column = 0
      
      logicalRow = 0
      logicalColumn = 0
      
      for child in children:
         child = deepcopy(child)
         
         childType = child.pop("type")
         multiply = Multiplier(child)
         
         for i in range(multiply.count):
            ch = deepcopy(child)
            
            multiply.setIndexableToChild(ch, "text", i)
            
            grid = StaticUtils.setIfAbsentAndGet(ch, "grid", dict())
            
            skipColumns = grid.pop("skipColumns", 0)
            column += skipColumns
            logicalColumn += skipColumns
            
            grid["row"] = row
            grid["column"] = column
            
            ch["config"] = config
            ch["namePrefix"] = namePrefix
            
            multiply.setIndexableToChild(ch, "name", i)
            
            smartWidget = CommonUIComponents.__CLASSES[childType](master, **ch)
            
            result[(logicalRow, logicalColumn)] = smartWidget
            
            if multiply.lastChildAddsRow and i == multiply.count - 1:
               grid["lastColumn"] = True
            
            if grid.pop("lastColumn", False):
               row += smartWidget.rows
               logicalRow += 1
               
               column = logicalColumn = 0
            
            else:
               column += smartWidget.columns
               logicalColumn += 1
      
      return result
