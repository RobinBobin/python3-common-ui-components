from commonutils import StaticUtils
from os import sys, path
from tkinter import Tk
from tkinter.ttk import Notebook, Style
from .basetabloader import BaseTabLoader
from .json import Config, Storage
from .ttk import CommonUIComponents, SmartWidget
from .version import __version__

user32 = None

if StaticUtils.isWindows():
   from ctypes import WinDLL
   
   user32 = WinDLL("user32")


class AppLauncher:
   def __init__(self):
      self.__root = Tk()
      
      self.__notebook = Notebook()
      
      if user32:
         self.__notebook.bind("<Map>", self._maximizeUnderWindows)
   
   @property
   def root(self):
      return self.__root
   
   def run(self, entry, baseTabLoader = BaseTabLoader()):
      self.__configurationFiles = self._createConfigurationInstances()
      
      self._loadConfigurationFiles()
      self._upgradeConfigurationFiles()
      
      Config["version"] = __version__
      
      self._createStyles()
      self._createLayouts()
      self._configureRoot()
      
      CommonUIComponents.init(**self._getCommonUIComponentsInitParams())
      SmartWidget.setFont()
      
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
   
   def _createConfigurationInstances(self):
      _ = self
      
      return {"config": Config(), "storage": Storage()}
   
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
   
   def _createLayouts(self):
      name = "Scrollbar"
      
      for orient in ("Horizontal", "Vertical"):
         self.__root.style.layout(f"{orient}.T{name}.T{name}", self.__root.style.layout(f"{orient}.T{name}"))
   
   def _getCommonUIComponentsInitParams(self):
      _ = self
      
      return dict()
   
   def _loadConfigurationFiles(self):
      for configurationFile in self.__configurationFiles.values():
         configurationFile.load()
   
   def _maximizeUnderWindows(self, _):
      _ = self
      
      user32.ShowWindow(user32.GetForegroundWindow(), 3)
   
   def _onDeleteWindow(self):
      for name in self.__notebook.tabs():
         self.__notebook.nametowidget(name).onDeleteWindow()
      
      for configurationFile in self.__configurationFiles.values():
         configurationFile.dump()
      
      self.__root.destroy()
   
   def _upgradeConfigurationFiles(self):
      for configurationFile in self.__configurationFiles.values():
         configurationFile.upgrade(Config.INSTANCE.json.get("version", "1.6.7"))
