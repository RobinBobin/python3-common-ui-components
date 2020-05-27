from importlib import import_module
from tkinter.ttk import Frame
from .ttk import CommonUIComponents

class BaseTab(Frame):
   def __init__(self, master = None, **kw):
      super().__init__(master, **kw)
      
      self.__frame = Frame(self)
      self.__frame.pack(expand = True)
   
   @property
   def baseTabCaption(self):
      return self.__config["caption"]
   
   @property
   def baseTabConfig(self):
      return self.__config
   
   @property
   def baseTabFrame(self):
      return self.__frame
   
   def dumpNamedChildren(self):
      from .ttk.containers.basecontainer import BaseContainer
      
      def dump(container):
         for name, child in container.getSmartWidget().items():
            print(name, type(child))
            
            if isinstance(child, BaseContainer):
               dump(child)
      
      print(self.baseTabCaption)
      
      dump(self.__ui)
   
   def getSmartWidget(self, *keys, named = True):
      return self.__ui.getSmartWidget(*keys, named = named)
   
   def onDeleteWindow(self):
      pass
   
   def _inflate(self, config):
      self.__config = config
      
      if "ui" in config:
         self.__ui = CommonUIComponents.inflate(self)
         
         self.__ui.grid()


class BaseTabLoader:
   def load(self, notebook, wholeConfig, **baseTabKw):
      self.__notebook = notebook
      self.__wholeConfig = wholeConfig
      
      notebook.bind("<<NotebookTabChanged>>", self._onTabChanged)
      
      selectedIndex = wholeConfig.get("selectedIndex", 0)
      
      tabs = dict()
      tabsDir = wholeConfig["tabsDir"]
      
      for name, config in wholeConfig["tabs"].items():
         module = import_module(f"{tabsDir}.{name}")
         
         tab = module.Tab(notebook, **baseTabKw)
         tab._inflate(config)
         
         tabs[name] = tab
         
         notebook.add(tab, text = tab.baseTabCaption)
      
      notebook.select(selectedIndex)
      
      return tabs
   
   def _onTabChanged(self, event):
      self.__wholeConfig["selectedIndex"] = self.__notebook.index(self.__notebook.select())
