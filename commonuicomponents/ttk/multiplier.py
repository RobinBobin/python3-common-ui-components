from ..staticutils import StaticUtils

class Multiplier:
   __DEFAULT_OFFSETS = {
      "name": -1
   }
   
   def __init__(self, child):
      self.__multiply = child.pop("multiply", dict())
      self.__indexables = {key: child.pop(key, None) for key in ("text", "name")}
      
      text = self.__indexables["text"]
      
      if text and "count" not in self.__multiply and StaticUtils.isIterable(text):
         self.__multiply["count"] = len(text)
   
   def setIndexableToChild(self, child, key, index):
      indexable = self.__indexables[key]
      
      if indexable != None:
         child[key] = indexable if "count" not in self.__multiply else indexable[index] if StaticUtils.isIterable(indexable) else "{0}{1}".format(indexable, index + 1 + self.__multiply.get(f"offsetOfIndexIn{key.title()}", Multiplier.__DEFAULT_OFFSETS.get(key, 0)))
   
   @property
   def count(self):
      return self.__multiply.get("count", 1)
   
   @property
   def lastChildAddsRow(self):
      return self.__multiply.get("lastChildAddsRow", False)
