from pathlib import Path
from .json import Json
from .storage import Storage
from ..staticutils import StaticUtils

class Config(Json):
   def __init__(self):
      super().__init__(("config.json", "default_config.json", Path("..", "default_config.json")), True)
   
   def load(self):
      super().load()
      
      StaticUtils.TITLE = Config["title"]
      
      if "version" not in self.json:
         Config["version"] = "1.6.7"
      
      if self.result.created:
         if StaticUtils.isWindows():
            widgetFont = self.json.get("widgetFont", "")
            
            if not isinstance(widgetFont, str) and len(widgetFont) > 1:
               widgetFont[1] = StaticUtils.round(widgetFont[1] / 1.2)
   
   def _upgrader_1_6_7(self):
      if Storage.INSTANCE.json:
         raise ValueError()
      
      for name, config in self.json["tabs"].items():
         if "values" in config:
            Storage.INSTANCE.json[name] = {"values": config.pop("values")}
