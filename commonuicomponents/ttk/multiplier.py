import re
from commonutils import DictPopper
from ..staticutils import StaticUtils

class Multiplier:
   __DEFAULT_OFFSETS = { "name": -1 }
   __INDEXABLE_KEYS = ("name", "text")
   __NTH_CHILD_PATTERN = re.compile(r"(\d*n)?(\+\d+)?$")
   
   __NTH_CHILD_SPECIAL_VALUES = {
      "even": "2n",
      "every": "n",
      "odd": "2n+1"
   }
   
   def __init__(self, childType, child):
      self.__childPseudoType \
      , self.__multiply = DictPopper(child)  \
         .add("pseudoType", childType)       \
         .add("multiply", dict())
      
      self.__indexables = {key: child.pop(key, None) for key in Multiplier.__INDEXABLE_KEYS}
      
      # = nth child = #
      nthChild = StaticUtils.setIfAbsentAndGet(self.__multiply, "nthChild", dict())
      
      if self.__multiply.pop("lastChildAddsRow", False):
         nthChild["lastCell"] = "last"
      
      # = Add count if necessary = #
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
      return self.__multiply["nthChild"].get("lastCell", None) == "last"
   
   def postProcessNthChild(self, child, index):
      nthChild = self.__multiply["nthChild"]
      
      lastColumn = nthChild.pop("lastColumn", None)
      
      if lastColumn:
         nthChild["lastCell"] = lastColumn
      
      for key in ("lastCell", ):
         if key in nthChild and self.__indexMatches(index, nthChild[key]):
            child["grid"][key] = True
   
   def processChild(self, child, index):
      propagateIndex = self.__multiply.get("propagateIndexToChildren", False)
      
      for key in Multiplier.__INDEXABLE_KEYS:
         self.setIndexableToChild(child, key, index)
         
         # = Propagate index = #
         if propagateIndex:
            for ch in child["children"]:
               multiply = StaticUtils.setIfAbsentAndGet(ch, "multiply", dict())
               
               offsetKey = f"offsetOfIndexIn{key.title()}"
               multiply["count"] = 1
               multiply[offsetKey] = StaticUtils.setIfAbsentAndGet(multiply, offsetKey, Multiplier.__DEFAULT_OFFSETS.get(key, 0)) + index
      
      # print(child)
   
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
   
   def __indexMatches(self, index, value):
      result = False
      
      index += 1
      
      if value == "last":
         result = index == self.count
      
      else:
         value = Multiplier.__NTH_CHILD_SPECIAL_VALUES.get(value, value)
         
         if not Multiplier.__NTH_CHILD_PATTERN.match(value):
            raise ValueError(value)
         
         value = value.split("+")
         endsWithN = value[0].endswith("n")
         
         if endsWithN and len(value[0]) == 1:
            value[0] = "1n"
         
         step = int(value[0][:-1]) if endsWithN else 0
         offset = int(value[1]) if len(value) == 2 else int(value[0]) if not endsWithN else 0
         
         for n in range(self.count + 1):
            i = step * n + offset
            result = i == index
            
            if result or i > index:
               break
      
      return result
