from commonutils import StaticUtils
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
   
   @property
   def baseTabStorage(self):
      return self.__storage
   
   def dumpNamedChildren(self):
      # pylint: disable = import-outside-toplevel
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
   
   def _inflate(self, config, storage):
      self.__config = config
      self.__storage = storage
      
      if "ui" in config:
         self.__ui = CommonUIComponents.inflate(self)
         
         self.__ui.grid()


class BaseTabLoader:
   def load(self, notebook, wholeConfig, wholeStorage, **baseTabKw):
      self.__notebook = notebook
      self.__wholeStorage = wholeStorage
      
      notebook.bind("<<NotebookTabChanged>>", self._onTabChanged)
      
      explicitAddition = wholeConfig.get("explicitAddition", False)
      selectedIndex = wholeStorage.get("selectedIndex", 0)
      tabsDir = wholeConfig["tabsDir"]
      
      tabs = dict()
      
      for name, config in wholeConfig["tabs"].items():
         if not config.get("skip", explicitAddition):
            module = import_module(f"{tabsDir}.{name}")
            
            tab = module.Tab(notebook, **baseTabKw)
            tab._inflate(config, StaticUtils.setIfAbsentAndGet(wholeStorage, name, dict()))
            
            tabs[name] = tab
            
            notebook.add(tab, text = tab.baseTabCaption)
      
      if tabs:
         if selectedIndex >= len(tabs):
            selectedIndex = len(tabs) - 1
         
         notebook.select(selectedIndex)
      
      return tabs
   
   def _onTabChanged(self, _):
      self.__wholeStorage["selectedIndex"] = self.__notebook.index(self.__notebook.select())
