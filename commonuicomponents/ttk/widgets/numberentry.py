import re
from commonutils import DictPopper
from .entry import Entry

class NumberEntry(Entry):
   class ValidationError(ValueError):
      pass
   
   __BASE_DATA = {
      2: ("b", bin, "01"),
      8: ("0", oct, "0-7"),
      10: ("", lambda i: f"__{i}", "0-9"),
      16: ("0x", hex, "0-9a-fA-F")
   }
   
   def __init__(self, master, **kw):
      self.__base                \
      , bitLength                \
      , self.__max               \
      , self.__min               \
      , pythonStylePrefix        \
      , showPrefix               \
      , prefix                   \
      , unsigned = DictPopper(kw)         \
         .add("base", 10)                 \
         .add("bitLength")                \
         .add("max")                      \
         .add("min")                      \
         .add("pythonStylePrefix", False) \
         .add("showPrefix", False)        \
         .add("prefix")                   \
         .add("unsigned", False)
      
      # = bitLength = #
      if self.__min is None and self.__max is None and bitLength:
         if unsigned:
            self.__min = 0
            self.__max = 2 ** bitLength - 1
         
         elif bitLength > 1:
            v = 2 ** (bitLength - 1)
            
            self.__min = -v
            self.__max = v - 1
         
         else:
            raise ValueError()
      
      # = base / prefix = #
      baseData = NumberEntry.__BASE_DATA.get(self.__base)
      
      if prefix is not None:
         pass
      
      elif pythonStylePrefix:
         prefix = baseData[1](0)[:2]
      
      else:
         prefix = baseData[0]
      
      baseData = (prefix, *baseData[1:])
      
      self.__prefix = baseData[0] if showPrefix else ""
      
      # = regexp = #
      regexp = []
      
      if not unsigned:
         regexp.append(r"[+-]?")
      
      if self.__prefix:
         regexp.append(f"({self.__prefix})")
      
      regexp.append(f"[{baseData[2]}]*$")
      
      self.__pattern = re.compile("".join(regexp))
      
      # = #
      NumberEntry._setGetValueWhenStoring(kw)
      
      super().__init__(master, **kw)
      
      rawValue = self.getRawValue()
      
      value = rawValue.get()
      
      if isinstance(value, str):
         value = 0 if not value else int(value)
      
      isNegative = value < 0
      
      value = f"{'-' if isNegative else ''}{self.__prefix}{baseData[1](value)[2 + (1 if isNegative else 0):]}"
      
      rawValue.set(value)
      
      self["validate"] = "key"
      self["validatecommand"] = (self.register(self.onValidate), "%P")
   
   def getValue(self):
      return self.__getValue(super().getValue())
   
   def onValidate(self, wouldBeValue):
      try:
         # = prefix = #
         if not self.__pattern.match(wouldBeValue):
            raise NumberEntry.ValidationError()
         
         # = min / max = #
         value = self.__getValue(wouldBeValue)
         
         if not self.__min <= value <= self.__max:
            raise NumberEntry.ValidationError()
      
      except NumberEntry.ValidationError:
         return False
      
      return True
   
   def __getValue(self, value):
      if not value or len(value) == len(self.__prefix) + (1 if value.startswith(("+", "-")) else 0):
         value += "0"
      
      return int(value, self.__base)
