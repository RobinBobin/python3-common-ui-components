from commonutils import StaticUtils
from copy import deepcopy
from .smartwidget import SmartWidget

class Children:
   def __init__(self):
      self.__children = dict()
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   def __iter__(self):
      return iter(self.__children.items())
   
   def __len__(self):
      return len(self.__children)
   
   def __setitem__(self, rowColumn, child):
      self.__children[rowColumn] = child


class Multiply:
   def __init__(self, child):
      self.__multiply = child.pop("multiply", dict())
      self.__indexables = {key: child.pop(key, None) for key in ("text", "name")}
      
      text = self.__indexables["text"]
      
      if text and "count" not in self.__multiply and StaticUtils.isIterable(text):
         self.__multiply["count"] = len(text)
   
   def getIndexable(self, key, index):
      indexable = self.__indexables[key]
      
      return indexable if "count" not in self.__multiply else indexable[index] if StaticUtils.isIterable(indexable) else f"{indexable}{index + 1 + self.__multiply.get('offsetOfIndexInText', 0)}"
   
   def hasIndexable(self, key):
      return not not self.__indexables[key]
   
   @property
   def count(self):
      return self.__multiply.get("count", 1)
   
   @property
   def lastChildAddsRow(self):
      return self.__multiply.get("lastChildAddsRow", False)


class CommonUIComponents:
   __CLASSES = dict()
   
   @staticmethod
   def inflate(master, config, grid = True, skipTopLevel = False):
      children = CommonUIComponents._inflate(master, config["ui"], StaticUtils.getOrSetIfAbsent(config, "values", []))
      
      if grid:
         for _, child in children:
            child.grid()
      
      return children[(0, 0)] if skipTopLevel else children
   
   @staticmethod
   def init(**params):
      params = StaticUtils.mergeJson({
         "debug": False
      }, params, True)
      
      for key, value in params.items():
         setattr(CommonUIComponents, key.upper(), value)
      
      from tkinter import Canvas
      from tkinter.ttk import Button, Label, Radiobutton
      from .containers.container import Container
      from .containers.labeledcontainer import LabeledContainer
      from .containers.labeledradiobuttongroup import LabeledRadioButtonGroup
      from .entry import Entry
      from .labeledscale import LabeledScale
      
      for tkinterBase in [Button, Canvas, Label, Radiobutton]:
         CommonUIComponents.wrapClass(tkinterBase)
      
      for smartWidget in [
         Container,
         Entry,
         LabeledContainer,
         LabeledRadioButtonGroup,
         LabeledScale
      ]:
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
         print(f"registered {clazz} (TKINTER_BASE: {clazz._TKINTER_BASE}, STYLE = {clazz.STYLE}.")
   
   @staticmethod
   def wrapClass(tkinterBase):
      CommonUIComponents.registerClass(type(tkinterBase.__name__, (SmartWidget, tkinterBase), dict()))
   
   @staticmethod
   def _inflate(master, children, parentBuffer):
      result = Children()
      
      row = 0
      column = 0
      
      logicalRow = 0
      logicalColumn = 0
      
      parentBufferIndex = 0
      
      for child in children:
         child = deepcopy(child)
         
         childType = child.pop("type")
         multiply = Multiply(child)
         
         for i in range(multiply.count):
            ch = deepcopy(child)
            
            if multiply.hasIndexable("text"):
               ch["text"] = multiply.getIndexable("text", i)
            
            grid = StaticUtils.getOrSetIfAbsent(ch, "grid", dict())
            
            skipColumns = grid.pop("skipColumns", 0)
            column += skipColumns
            logicalColumn += skipColumns
            
            grid["row"] = row
            grid["column"] = column
            
            ch["parentBuffer"] = parentBuffer
            ch["parentBufferIndex"] = parentBufferIndex
            
            smartWidget = CommonUIComponents.__CLASSES[childType](master, **ch)
            
            if smartWidget.hasValueBuffer:
               parentBufferIndex += 1
            
            result[(logicalRow, logicalColumn)] = smartWidget
            
            if multiply.hasIndexable("name"):
               result[multiply.getIndexable("name", i)] = smartWidget
            
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
