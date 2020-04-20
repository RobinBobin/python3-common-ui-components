from tkinter.ttk import Frame

class BaseTab(Frame):
   def __init__(self, master):
      super().__init__(master)
      
      self._frame = Frame(self)
      self._frame.pack(expand = True)
   
   @property
   def caption(self):
      return self._config["caption"]
   
   def onDeleteWindow(self):
      pass
   
   def _inflate(self, config):
      self._config = config
      
      if "ui" in self._config:
         from commonuicomponents import CommonUIComponents
         
         self._ui = CommonUIComponents.inflate(self._frame, self._config)
   
   @staticmethod
   def load(notebook, wholeConfig, tabsDir):
      from importlib import import_module
      
      for module, config in wholeConfig["tabs"].items():
         module = import_module(f"{tabsDir}.{module}")
         
         tab = module.Tab(notebook)
         tab._inflate(config)
         
         notebook.add(tab, text = tab.caption)
