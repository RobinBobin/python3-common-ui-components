from commonutils import StaticUtils
from copy import deepcopy
from .smartwidget import SmartWidget

class Children:
   def __init__(self):
      self.__children = dict()
   
   def grid(self):
      for child in self.__children.values():
         child.grid()
   
   def __getitem__(self, rowColumn):
      return self.__children[rowColumn]
   
   def __iter__(self):
      return iter(self.__children.items())
   
   def __len__(self):
      return len(self.__children)
   
   def __setitem__(self, rowColumn, child):
      self.__children[rowColumn] = child


class CommonUIComponents:
   __CLASSES = dict()
   
   @staticmethod
   def inflate(master, config, grid = True):
      children = CommonUIComponents._inflate(master, config["ui"])
      
      if grid:
         children.grid()
      
      return children
   
   @staticmethod
   def init(**params):
      params = StaticUtils.mergeJson({
         "debug": False
      }, params, True)
      
      for key, value in params.items():
         setattr(CommonUIComponents, key.upper(), value)
      
      from tkinter.ttk import Button, Label
      from .containers.container import Container
      from .containers.labeledcontainer import LabeledContainer
      from .labeledscale import LabeledScale
      
      for tkinterBase in [Button, Label]:
         CommonUIComponents.wrapClass(tkinterBase)
      
      for smartWidget in [Container, LabeledContainer, LabeledScale]:
         CommonUIComponents.registerClass(smartWidget)
   
   @staticmethod
   def registerClass(clazz):
      from tkinter.ttk import Widget
      
      if not issubclass(clazz, SmartWidget):
         raise ValueError(f"{clazz.__name__} must subclass {SmartWidget.__name__}")
      
      clazz.STYLE = [clazz]
      clazz._TKINTER_BASE = None
      
      for base in clazz.__bases__:
         if issubclass(base, Widget):
            clazz._TKINTER_BASE = base
         
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
   
   @staticmethod
   def wrapClass(tkinterBase):
      CommonUIComponents.registerClass(type(tkinterBase.__name__, (SmartWidget, tkinterBase), dict()))
   
   @staticmethod
   def _inflate(master, children):
      result = Children()
      
      row = 0
      column = 0
      
      for child in children:
         child = deepcopy(child)
         
         repeatCount = child.pop("repeatCount", 1)
         text = child.pop("text", None)
         childType = child.pop("type")
         
         for i in range(repeatCount):
            ch = deepcopy(child)
            
            if text != None:
               ch["text"] = text if repeatCount == 1 else text[i] if StaticUtils.isIterable(text) else f"{text}{i + 1}"
            
            grid = StaticUtils.getOrSetIfAbsent(ch, "grid", dict())
            
            column += grid.pop("skipColumns", 0)
            
            grid["row"] = row
            grid["column"] = column
            
            if grid.pop("lastColumn", False):
               row += 1
               column = 0
            
            else:
               column += 1
            
            result[(row, column)] = CommonUIComponents.__CLASSES[childType](master, **ch)
      
      return result
