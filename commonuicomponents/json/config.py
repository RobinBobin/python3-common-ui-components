from pathlib import Path
from .json import Json
from ..staticutils import StaticUtils

class Config(Json):
   def __init__(self):
      super().__init__(("config.json", "default_config.json", Path("..", "default_config.json")))
   
   def load(self):
      result = super().load()
      
      if result == None:
         raise ValueError("Config not loaded")
      
      StaticUtils.TITLE = Config["title"]
      
      if result:
         if "version" not in self.json:
            Config["version"] = "1.6.7"
         
         if StaticUtils.isWindows():
            widgetFont = self.json.get("widgetFont", "")
            
            if type(widgetFont) != str and len(widgetFont) > 1:
               widgetFont[1] = StaticUtils.round(widgetFont[1] / 1.2)
      
      return result
