from copy import deepcopy
from tkinter import Widget
from tkinter.ttk import Style
from .multiplier import Multiplier
from .widgets.smartwidget import SmartWidget
from ..staticutils import StaticUtils

class CommonUIComponents:
   __CLASSES = dict()
   
   @staticmethod
   def inflate(tab):
      ui = CommonUIComponents._inflate(tab.baseTabFrame, [tab.baseTabConfig["ui"]], tab.baseTabStorage, [])
      
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
      
      # pylint: disable = import-outside-toplevel
      SmartWidget._STYLE_INSTANCE = Style()
      
      from tkinter import Canvas
      from tkinter.ttk import Button, Label, Radiobutton
      from .containers import Container
      from .containers import LabeledContainer
      from .containers import LabeledRadioButtonGroup
      from .widgets import Checkbutton
      from .widgets import Combobox
      from .widgets import Entry
      from .widgets import LabeledScale
      from .widgets import Listbox
      from .widgets import Scrollbar
      from .widgets import Spinbox
      from .widgets import StatefulButton
      
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
         Listbox,
         Scrollbar,
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
      
      smartWidgetBaseFound = False
      
      for base in clazz.__bases__:
         if issubclass(base, SmartWidget):
            if smartWidgetBaseFound:
               CommonUIComponents.__raiseInheritsMoreThanOnce(clazz, SmartWidget)
               
            smartWidgetBaseFound = True
            
            CommonUIComponents.__addSmartWidgetHierarchy(clazz.STYLE, base)
         
         if clazz._TKINTER_BASE:
            CommonUIComponents.__raiseInheritsMoreThanOnce(clazz, Widget)
         
         clazz._TKINTER_BASE = CommonUIComponents.__getTKinterBase(base)
      
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
   def _inflate(master, children, storage, namePrefix):
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
            
            ch["storage"] = storage
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
   
   @staticmethod
   def __addSmartWidgetHierarchy(styleArray, clazz):
      if clazz != SmartWidget:
         styleArray.append(clazz)
      
      for base in clazz.__bases__:
         if issubclass(base, SmartWidget) and base != SmartWidget:
            CommonUIComponents.__addSmartWidgetHierarchy(styleArray, base)
   
   @staticmethod
   def __getTKinterBase(clazz):
      result = None
      
      if issubclass(clazz, Widget):
         if issubclass(clazz, SmartWidget):
            for base in clazz.__bases__:
               result = CommonUIComponents.__getTKinterBase(base)
               
               if result:
                  break
         
         else:
            result = clazz
      
      return result
   
   @staticmethod
   def __raiseInheritsMoreThanOnce(child, parent):
      raise ValueError(f"{child.__name__} inherits {parent.__name__} more than once")
