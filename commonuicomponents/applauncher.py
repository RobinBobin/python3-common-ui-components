from os import sys, path
from tkinter import Tk
from tkinter.ttk import Notebook, Style
from .basetab import BaseTabLoader
from .json import Config, Storage
from .ttk import CommonUIComponents, SmartWidget

def _maximizeUnderWindows(_):
   try:
      # pylint: disable = import-outside-toplevel
      from ctypes import WinDLL
      
      user32 = WinDLL("user32")
      user32.ShowWindow(user32.GetForegroundWindow(), 3)
   
   except ImportError:
      pass

class AppLauncher:
   def __init__(self):
      self.__root = Tk()
      
      self.__configurationFiles = {"config": Config, "storage": Storage}
      self.__notebook = Notebook()
      self.__notebook.bind("<Map>", _maximizeUnderWindows)
   
   @property
   def root(self):
      return self.__root
   
   def run(self, entry, baseTabLoader = BaseTabLoader()):
      self._loadConfigurationFiles()
      self._createStyles()
      self._configureRoot()
      
      CommonUIComponents.init(**self._getCommonUIComponentsInitParams())
      SmartWidget.setFont(Config["widgetFont"])
      
      sys.path.append(path.dirname(path.dirname(path.abspath(entry))))
      
      baseTabLoader.load(self.__notebook, Config.INSTANCE.json, Storage.INSTANCE.json)
      
      self.__notebook.place(relwidth = 1, relheight = 1)
      
      self.__root.mainloop()
   
   def _configureRoot(self):
      self.__root.geometry(f"{self.__root.winfo_screenwidth()}x{self.__root.winfo_screenheight()}")
      
      #
      # There's a bug under Linux: if height == False, window contents
      # aren't centered vertically. Moreover, the app must be maximized
      # under Windows, otherwise vertical scrollbars don't scroll content
      # to the end.
      #
      self.__root.resizable(False, True)
      self.__root.title(Config["title"])
      self.__root.protocol("WM_DELETE_WINDOW", self._onDeleteWindow)
   
   def _createStyles(self):
      font = Config["widgetFont"]
      
      self.__root.style = Style()
      self.__root.style.configure(".", font = font)
      self.__root.style.configure("TButton", padding = [12, 7])
      self.__root.style.configure("TNotebook.Tab", padding = [13, 7])
      self.__root.style.configure("Horizontal.TScale", sliderthickness = 25)
      self.__root.style.configure("Horizontal.TScrollbar", arrowsize = 25)
      self.__root.style.configure("Vertical.TScrollbar", arrowsize = 25)
      self.__root.style.configure("TSpinbox", arrowsize = 30)
      
      self.__root.option_add('*TCombobox*Listbox.font', font)
      
      colors = {
         "Cyan": "cyan",
         "LGreen": "lightgreen",
         "Pink": "pink",
         "Yellow": "yellow"
      }
      
      styles = {
         "": "Frame",
         "Labeled": "Labelframe"
      }
      
      for style in styles.items():
         for color in colors.items():
            self.__root.style.configure(f"{color[0]}.T{style[0]}Container.TBaseContainer.T{style[1]}", background = color[1])
   
   # pylint: disable = no-self-use
   def _getCommonUIComponentsInitParams(self):
      return dict()
   
   def _loadConfigurationFiles(self):
      result = dict()
      
      for name in self.__configurationFiles:
         self.__configurationFiles[name] = self.__configurationFiles[name]()
         
         result[name] = self.__configurationFiles[name].load()
      
      return result
   
   def _onDeleteWindow(self):
      for name in self.__notebook.tabs():
         self.__notebook.nametowidget(name).onDeleteWindow()
      
      for config in self.__configurationFiles.values():
         config.INSTANCE.dump()
      
      self.__root.destroy()
