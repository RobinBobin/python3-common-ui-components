from tkinter import IntVar
from .labeledcontainer import LabeledContainer

class LabeledRadioButtonGroup(LabeledContainer):
   def __init__(self, master = None, **kw):
      kw["value"] = IntVar()
      
      super().__init__(master, **kw)
   
   def _inflateChildren(self):
      for child in self._baseContainerChildren:
         if "type" not in child:
            child["type"] = "Radiobutton"
      
      LabeledContainer._inflateChildren(self)
      
      for index, (_, child) in enumerate(self._baseContainerChildren):
         child.configure(value = index, variable = self.value)
