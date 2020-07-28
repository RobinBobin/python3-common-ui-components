from pathlib import Path
from .json import Json
from ..staticutils import StaticUtils

class Config(Json):
   def __init__(self):
      super().__init__(("config.json", "default_config.json", Path("..", "default_config.json")), True)
   
   def load(self):
      super().load()
      
      StaticUtils.TITLE = Config["title"]
      
      if self.result.created:
         if StaticUtils.isWindows():
            widgetFont = self.json.get("widgetFont", "")
            
            if not isinstance(widgetFont, str) and len(widgetFont) > 1:
               widgetFont[1] = StaticUtils.round(widgetFont[1] / 1.2)
   
   def _upgrader_1_6_7(self):
      _ = self
      
      raise Exception("Not implemented")
      
      # # = The storage file must not exist = #
      # if Storage.INSTANCE.result is not None:
      #    raise ValueError()
      
      # # = valueDomain -> valueDomains = #
      # for keys in StaticUtils.findKeyInDictionary(self.json, "valueDomain"):
      #    c = StaticUtils.indexDictionary(self.json, keys)
         
      #    c["valueDomains"] = [c.pop("valueDomain")]
      
      # # = Transfer relevant data to Storage = #
      # def transfer(config, storage):
      #    storage["selectedIndex"] = config.pop("selectedIndex", 0)
      #    storage["tabs"] = dict()
         
      #    storage = storage["tabs"]
         
      #    for name, tab in config["tabs"].items():
      #       storage[name] = dict()
            
      #       if "values" in tab:
      #          storage[name]["values"] = tab.pop("values").pop("")
            
      #       if "tabs" in tab:
      #          transfer(tab, storage[name])
      
      # transfer(self.json, Storage)
      
      # # = "" -> "value" = #
      # for keys in StaticUtils.findKeyInDictionary(Storage.INSTANCE.json, ""):
      #    s = StaticUtils.indexDictionary(Storage, keys)
         
      #    s["value"] = s.pop("")
      
      # # = Upgrade valueDomains = #
      # for keys in StaticUtils.findKeyInDictionary(self.json, "valueDomains"):
      #    print(keys)
