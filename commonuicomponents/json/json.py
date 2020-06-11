from json import dump, load
from ..staticutils import StaticUtils

class JsonMeta(type):
   def __getitem__(self, key):
      return self.INSTANCE.json[key]
   
   def __setitem__(self, key, value):
      self.INSTANCE.json[key] = value


class Result:
   def __init__(self, created):
      self.__created = created
   
   def __bool__(self):
      return self.__created


class Json(metaclass = JsonMeta):
   def __init__(self, paths):
      if hasattr(self.__class__, "INSTANCE"):
         raise ValueError()
      
      self.__class__.INSTANCE = self
      
      self.__json = dict()
      self.__paths = paths if StaticUtils.isIterable(paths) else (paths, )
   
   @property
   def json(self):
      return self.__json
   
   def dump(self):
      try:
         with open(self.__paths[0], "w", encoding = "utf-8") as f:
            dump(self.__json, f, ensure_ascii = False, indent = 3)
      
      except Exception as e:
         StaticUtils.showerror(e)
   
   def load(self):
      for created, path in enumerate(self.__paths):
         try:
            with open(path, encoding = "utf-8") as f:
               self.__json = load(f)
         
         except FileNotFoundError:
            pass
         
         else:
            return Result(not not created)
