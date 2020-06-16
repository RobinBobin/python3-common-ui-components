from commonutils import StaticUtils
from importlib import import_module

class BaseTabLoader:
   @property
   def tabs(self):
      return self.__tabs
   
   def load(self, notebook, wholeConfig, wholeStorage, **baseTabKw):
      self.__notebook = notebook
      self.__wholeStorage = wholeStorage
      
      notebook.bind("<<NotebookTabChanged>>", self._onTabChanged)
      
      explicitAddition = wholeConfig.get("explicitAddition", False)
      selectedIndex = wholeStorage.get("selectedIndex", 0)
      tabsDir = wholeConfig["tabsDir"]
      
      self.__tabs = dict()
      
      for name, config in wholeConfig["tabs"].items():
         if not config.get("skip", explicitAddition):
            default = dict()
            
            if "values" in config:
               default["values"] = config.pop("values")
            
            tab = import_module(f"{tabsDir}.{name}").Tab(notebook, config, StaticUtils.setIfAbsentAndGet(wholeStorage, name, default), **baseTabKw)
            
            self.__tabs[name] = tab
            
            notebook.add(tab, text = tab.baseTabCaption)
      
      if self.__tabs:
         if selectedIndex >= len(self.__tabs):
            selectedIndex = len(self.__tabs) - 1
         
         notebook.select(selectedIndex)
      
      return self.__tabs
   
   def _onTabChanged(self, _):
      self.__wholeStorage["selectedIndex"] = self.__notebook.index(self.__notebook.select())
