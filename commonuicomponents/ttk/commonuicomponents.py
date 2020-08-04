from commonutils import DictPopper, Global
from copy import deepcopy
from enum import Enum, auto
from stringcase import constcase, snakecase
from tkinter import Widget
from tkinter.ttk import Style
from .multiplier import Multiplier
from .widgets import SmartWidget
from ..staticutils import StaticUtils

class CellInsertionOrder(Enum):
   leftToRight = auto()
   topToBottom = auto()


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
      for key, default in (
         ("debug", False),
         ("multiplierType", Multiplier)
      ):
         for o in (CommonUIComponents, Global):
            setattr(o, constcase(snakecase(key)), params.get(key, default))
      
      SmartWidget._STYLE_INSTANCE = Style()
      
      # pylint: disable = import-outside-toplevel
      from tkinter import Canvas
      from tkinter.ttk import Button, Label, Radiobutton
      from .containers import             \
         Container                        \
         , LabeledContainer               \
         , LabeledRadioButtonGroup        \
         , LabeledWidgetContainer         \
         , LabeledWidgetLabeledContainer  \
         , LabeledWidgetsContainer
      from .widgets import    \
         Checkbutton          \
         , Combobox           \
         , CommonCombobox     \
         , Entry              \
         , LabeledScale       \
         , Listbox            \
         , NumberEntry        \
         , Scrollbar          \
         , Spinbox            \
         , StatefulButton
      
      for tkinterBase in (Button, Canvas, Label, Radiobutton):
         CommonUIComponents.wrapClass(tkinterBase)
      
      for smartWidget in (
         Checkbutton,
         Combobox,
         CommonCombobox,
         Container,
         Entry,
         LabeledContainer,
         LabeledRadioButtonGroup,
         LabeledWidgetContainer,
         LabeledWidgetsContainer,
         LabeledWidgetLabeledContainer,
         LabeledScale,
         Listbox,
         NumberEntry,
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
   def registerClasses(*classes):
      for clazz in classes:
         CommonUIComponents.registerClass(clazz)
   
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
         multiplier = CommonUIComponents.MULTIPLIER_TYPE(childType, child)
         
         for index in range(multiplier.count):
            ch = deepcopy(child)
            
            multiplier.processChild(ch, index)
            
            grid = StaticUtils.setIfAbsentAndGet(ch, "grid", dict())
            
            if grid.pop("lastColumn", False):
               grid["lastCell"] = True
            
            cellInsertionOrder = CellInsertionOrder.__members__[grid.pop("cellInsertionOrder", CellInsertionOrder.leftToRight.name)]
            
            skipColumns = grid.pop("skipColumns", 0)
            column += skipColumns
            logicalColumn += skipColumns
            
            grid["row"] = row
            grid["column"] = column
            
            ch["storage"] = storage
            ch["namePrefix"] = namePrefix
            
            smartWidget = CommonUIComponents.__CLASSES[childType](master, **ch)
            
            result[(logicalRow, logicalColumn)] = smartWidget
            
            multiplier.postProcessNthChild(ch, index)
            
            lastCell, = DictPopper(grid).add("lastCell")
            
            if lastCell:
               if cellInsertionOrder == CellInsertionOrder.leftToRight:
                  row += smartWidget.rows
                  logicalRow += 1
                  
                  column = logicalColumn = 0
               
               elif cellInsertionOrder == CellInsertionOrder.topToBottom:
                  column += smartWidget.columns
                  logicalColumn += 1
                  
                  row = logicalRow = 0
               
               else:
                  raise ValueError()
            
            else:
               if cellInsertionOrder == CellInsertionOrder.leftToRight:
                  column += smartWidget.columns
                  logicalColumn += 1
               
               elif cellInsertionOrder == CellInsertionOrder.topToBottom:
                  row += smartWidget.rows
                  logicalRow += 1
               
               else:
                  raise ValueError()
      
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
