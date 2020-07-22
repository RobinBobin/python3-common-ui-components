from json import load
from subprocess import check_output
from .staticutils import StaticUtils

class AppBuilder:
   def __init__(self):
      self._hiddenImports = []
      
      if StaticUtils.isWindows():
         self._hiddenImports.append("pkg_resources.py2_warn")
   
   def build(self, entry):
      with open("default_config.json", encoding = "utf-8") as f:
         self._fillHiddenImports(load(f))
         
         self._hiddenImports = [f" --hidden-import={hiddenImport}" for hiddenImport in self._hiddenImports]
         
         check_output(f"pyinstaller --onefile {''.join(self._hiddenImports)} {entry}", shell = True)
   
   def _fillHiddenImports(self, config):
      def f(cfg, parentTabsDir = None):
         tabsDir = f"{parentTabsDir}{cfg['tabsDir']}" if parentTabsDir else cfg["tabsDir"]
         
         for key, value in cfg["tabs"].items():
            self._hiddenImports.append(f"{tabsDir}.{key}")
            
            if "tabs" in value:
               f(value, tabsDir)
      
      f(config)
