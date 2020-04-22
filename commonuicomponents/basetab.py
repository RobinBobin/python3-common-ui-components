from importlib import import_module
from tkinter.ttk import Frame
from .ttk import CommonUIComponents

class BaseTab(Frame):
   def __init__(self, master = None, **kw):
      super().__init__(master, **kw)
      
      self._frame = Frame(self)
      self._frame.pack(expand = True)
   
   @property
   def caption(self):
      return self._config["caption"]
   
   def onDeleteWindow(self):
      pass
   
   def _getValue(self, *keys):
      proxy = self._ui
      
      for key in keys:
         proxy = proxy[key]
      
      return proxy.value.value.get()
   
   def _inflate(self, config):
      self._config = config
      
      if "ui" in self._config:
         self._ui = CommonUIComponents.inflate(self._frame, self._config)


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
         
         notebook.add(tab, text = tab.caption)
      
      notebook.select(selectedIndex)
      
      return tabs
   
   def _onTabChanged(self, event):
      self.__wholeConfig["selectedIndex"] = self.__notebook.index(self.__notebook.select())
