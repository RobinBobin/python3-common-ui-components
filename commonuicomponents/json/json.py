from json import dump, load
from ..staticutils import StaticUtils

class JsonMeta(type):
   def __getitem__(cls, key):
      return cls.INSTANCE.json[key]
   
   def __setitem__(cls, key, value):
      cls.INSTANCE.json[key] = value


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
            return Result(bool(created))
