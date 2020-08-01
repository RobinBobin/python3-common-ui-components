from commonutils import Global, StaticUtils
from copy import deepcopy
from tkinter import E
from . import Container

class LabeledWidgetsContainer(Container):
   def _inflateChildren(self):
      def deepcopyAndAddGrid(w):
         w = deepcopy(w)
         
         StaticUtils.setIfAbsentAndGet(w, "grid", dict())
         
         return w
      
      children = []
      
      for child in self._baseContainerChildren:
         widgets = tuple(map(child.pop, ("label", "widget")))
         
         StaticUtils.setIfAbsentAndGet(widgets[0], "type", "Label")
         
         multipliers = tuple(Global.MULTIPLIER_TYPE(w["type"], w) for w in widgets)
         
         if multipliers[0].count > 1:
            multipliers[1].count = multipliers[0].count
         
         noLeftPadding = widgets[1].pop("noLeftPadding", False)
         
         for i in range(multipliers[1].count):
            widgetsCopy = tuple(map(deepcopyAndAddGrid, widgets))
            
            widgetsCopy[0]["grid"]["sticky"] = E
            widgetsCopy[1]["grid"]["lastCell"] = True
            
            if noLeftPadding:
               widgetsCopy[1]["grid"]["padx"] = 0
            
            for multiplier, w in zip(multipliers, widgetsCopy):
               for key in ("text", "name"):
                  multiplier.setIndexableToChild(w, key, i)
            
            children.extend(widgetsCopy)
      
      self._baseContainerChildren = children
      
      super()._inflateChildren()
