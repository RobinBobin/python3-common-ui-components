from pathlib import Path
from .json import Json
from ..staticutils import StaticUtils

class Version:
   def __init__(self, version):
      self.__version = tuple(int(x) for x in version.split("."))
      
      if len(self.__version) != 3:
         raise ValueError()
   
   def __eq__(self, other):
      return self.__version == other.version
   
   @property
   def version(self):
      return self.__version


class Config(Json):
   def __init__(self):
      super().__init__(("config.json", "default_config.json", Path("..", "default_config.json")))
   
   def load(self):
      result = super().load()
      
      if result is None:
         raise ValueError("Config not loaded")
      
      StaticUtils.TITLE = Config["title"]
      
      if result.created:
         if "version" not in self.json:
            Config["version"] = "1.6.7"
         
         if StaticUtils.isWindows():
            widgetFont = self.json.get("widgetFont", "")
            
            if not isinstance(widgetFont, str) and len(widgetFont) > 1:
               widgetFont[1] = StaticUtils.round(widgetFont[1] / 1.2)
      
      return result
