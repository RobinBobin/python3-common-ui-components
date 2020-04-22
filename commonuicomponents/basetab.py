from tkinter.ttk import Frame

class BaseTab(Frame):
   def __init__(self, master = None, **kw):
      super().__init__(master, **kw)
      
      self._frame = Frame(self)
      self._frame.pack(expand = True)
   
   @property
   def caption(self):
      return self._config["caption"]
   
   def getValue(self, *keys):
      proxy = self._ui
      
      for key in keys:
         proxy = proxy[key]
      
      return proxy.value.value.get()
   
   def onDeleteWindow(self):
      pass
   
   def _inflate(self, config):
      self._config = config
      
      if "ui" in self._config:
         from commonuicomponents import CommonUIComponents
         
         self._ui = CommonUIComponents.inflate(self._frame, self._config)
   
   @staticmethod
   def load(notebook, wholeConfig, **baseTabKw):
      from importlib import import_module
      
      tabs = dict()
      tabsDir = wholeConfig["tabsDir"]
      
      for name, config in wholeConfig["tabs"].items():
         module = import_module(f"{tabsDir}.{name}")
         
         tab = module.Tab(notebook, **baseTabKw)
         tab._inflate(config)
         
         tabs[name] = tab
         
         notebook.add(tab, text = tab.caption)
      
      return tabs
