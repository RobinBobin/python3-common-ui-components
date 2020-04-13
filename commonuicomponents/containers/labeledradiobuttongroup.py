from commonutils import StaticUtils
from tkinter import IntVar
from .labeledcontainer import LabeledContainer

class LabeledRadioButtonGroup(LabeledContainer):
   def __init__(self, master = None, **kw):
      kw["value"] = IntVar()
      
      super().__init__(master, **kw)
      
      kw["value"].set(StaticUtils.getOrSetIfAbsent(self._valueBuffer, 0, 0))
      
      kw["value"].trace_add("write", lambda *_: StaticUtils.setSafely(self._valueBuffer, 0, self.value.get()))
   
   def _inflateChildren(self):
      for child in self._baseContainerChildren:
         if "type" not in child:
            child["type"] = "Radiobutton"
      
      LabeledContainer._inflateChildren(self)
      
      for index, (_, child) in enumerate(self._baseContainerChildren):
         child.configure(value = index, variable = self.value)
