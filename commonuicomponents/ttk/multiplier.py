from ..staticutils import StaticUtils

class Multiplier:
   __DEFAULT_OFFSETS = {
      "name": -1
   }
   
   def __init__(self, childType, child):
      self.__multiply = child.pop("multiply", dict())
      self.__indexables = {key: child.pop(key, None) for key in ("text", "name")}
      self.__childPseudoType = child.pop("pseudoType", childType)
      
      text = self.__indexables["text"]
      
      if text and "count" not in self.__multiply and StaticUtils.isIterable(text):
         self.__multiply["count"] = len(text)
   
   @property
   def childPseudoType(self):
      return self.__childPseudoType
   
   @property
   def count(self):
      return self.__multiply.get("count", 1)
   
   @count.setter
   def count(self, count):
      # = For LabeledWidgetsContainer and the like = #
      self.__multiply["count"] = count
   
   @property
   def lastChildAddsRow(self):
      return self.__multiply.get("lastChildAddsRow", False)
   
   def setIndexableToChild(self, child, key, index):
      indexable = self.__indexables[key]
      
      if indexable is not None:
         if "count" not in self.__multiply:
            child[key] = indexable
         
         elif StaticUtils.isIterable(indexable):
            child[key] = indexable[index]
         
         else:
            offset = 1 + self.__multiply.get(f"offsetOfIndexIn{key.title()}", Multiplier.__DEFAULT_OFFSETS.get(key, 0))
            
            child[key] = f"{indexable}{index + offset}" if key == "name" else self._formatIndexable(indexable, index, offset)
   
   def _formatIndexable(self, indexable, index, offset):
      _ = self
      
      return f"{indexable}{index + offset}"
