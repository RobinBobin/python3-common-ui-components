from commonutils import StaticUtils
from tkinter import IntVar
from .labeledcontainer import LabeledContainer

class LabeledRadioButtonGroup(LabeledContainer):
   def __init__(self, master = None, **kw):
      kw["value"] = IntVar()
      
      super().__init__(master, **kw)
      
      kw["value"].set(StaticUtils.getOrSetIfAbsent(self._smartWidgetValueBuffer, 0, 0))
      
      kw["value"].trace_add("write", lambda *_: StaticUtils.setSafely(self._smartWidgetValueBuffer, 0, self.value.get()))
   
   def _inflateChildren(self):
      for child in self._baseContainerChildren:
         if "type" not in child:
            child["type"] = "Radiobutton"
      
      LabeledContainer._inflateChildren(self)
      
      for index, proxy in enumerate(self._baseContainerChildren.values()):
         proxy.value.configure(value = index, variable = self.value)
