from tkinter.ttk import Frame
from .ttk import CommonUIComponents

class BaseTab(Frame):
   def __init__(self, master, config, storage, **kw):
      super().__init__(master, **kw)
      
      self.__config = config
      self.__frame = Frame(self)
      self.__storage = storage
      
      self._addFrame()
      
      if "ui" in config:
         self.__ui = CommonUIComponents.inflate(self)
         
         self.__ui.grid()
   
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
   
   @property
   def baseTabUi(self):
      return self.__ui
   
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
   
   def onTabChanged(self):
      pass
   
   def _addFrame(self):
      self.__frame.pack(expand = True)
