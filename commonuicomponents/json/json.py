from itertools import dropwhile
from json import dump, load
from os import remove
from pathlib import Path
from ..staticutils import StaticUtils

class JsonMeta(type):
   def __getitem__(cls, key):
      return cls.INSTANCE.json[key]
   
   def __setitem__(cls, key, value):
      cls.INSTANCE.json[key] = value


class Result:
   def __init__(self, created):
      self.__created = created
   
   @property
   def created(self):
      return self.__created


class Json(metaclass = JsonMeta):
   def __init__(self, paths, raiseIfFailsToLoad):
      if hasattr(self.__class__, "INSTANCE"):
         raise ValueError()
      
      self.__class__.INSTANCE = self
      
      self.__json = dict()
      self.__paths = paths if StaticUtils.isIterable(paths) else (paths, )
      self.__raiseIfFailsToLoad = raiseIfFailsToLoad
      self.__result = None
      self.__upgraders = dict()
   
   @property
   def json(self):
      return self.__json
   
   @property
   def result(self):
      return self.__result
   
   def dump(self):
      try:
         self.__dump(self.__paths[0])
      
      except BaseException as e:
         StaticUtils.showerror(e)
   
   def load(self):
      for created, path in enumerate(self.__paths):
         try:
            with open(path, encoding = "utf-8") as f:
               self.__json = load(f)
         
         except FileNotFoundError:
            pass
         
         else:
            self.__result = Result(bool(created))
            
            break
      
      if self.__result is None and self.__raiseIfFailsToLoad:
         raise ValueError(f"{self.__class__.__name__} not loaded")
      
      # = Find upgraders = #
      prefix = "_upgrader_"
      
      for version in StaticUtils.sortStringsAsIntegers(map(lambda upgraderName: upgraderName[len(prefix):], filter(lambda entry: entry.startswith(prefix), dir(self.__class__))), "_"):
         self.__upgraders[version.replace("_", ".")] = getattr(self, f"{prefix}{version}")
   
   def upgrade(self, currentVersion):
      for version, upgrader in dropwhile(lambda e: e[0] != currentVersion, self.__upgraders.items()):
         p = Path(self.__paths[0])
         backup = f"{p.stem}_{version}{p.suffix}"
         
         self.__dump(backup)
         
         upgrader()
         
         remove(backup)
   
   def __dump(self, path):
      with open(path, "w", encoding = "utf-8") as f:
         dump(self.__json, f, ensure_ascii = False, indent = 3)
         f.write("\n")
