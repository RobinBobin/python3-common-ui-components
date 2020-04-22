from json import dump, load
from pathlib import Path
from platform import system
from .staticutils import StaticUtils

class Result:
   def __init__(self, configCreated):
      self.__configCreated = configCreated
      self.__isLinux = system() == "Linux"
      
      if configCreated and not self.__isLinux:
         widgetFont = Config._CONFIG.get("widgetFont", "")
         
         if type(widgetFont) != str and len(widgetFont) > 1:
            widgetFont[1] = StaticUtils.round(widgetFont[1] / 1.2)
   
   def __bool__(self):
      return self.__configCreated
   
   @property
   def isLinux(self):
      return self.__isLinux


class ConfigMeta(type):
   def __getitem__(clazz, key):
      return clazz._CONFIG[key]
   
   def __setitem__(clazz, key, value):
      clazz._CONFIG[key] = value


class Config(metaclass = ConfigMeta):
   __PATHS = ["config.json", "default_config.json", Path("..", "default_config.json")]
   
   @staticmethod
   def dump():
      try:
         with open(Config.__PATHS[0], "w", encoding = "utf-8") as f:
            dump(Config._CONFIG, f, ensure_ascii = False, indent = 3)
      
      except Exception as e:
         StaticUtils.showerror(e)
   
   @staticmethod
   def get(key, default):
      return Config._CONFIG.get(key, default)
   
   @staticmethod
   def load():
      for configCreated, path in enumerate(Config.__PATHS):
         try:
            with open(path, encoding = "utf-8") as f:
               Config._CONFIG = load(f)
               StaticUtils.TITLE = Config["title"]
         
         except FileNotFoundError:
            pass
         
         else:
            return Result(not not configCreated)
      
      raise ValueError("Config not loaded")
