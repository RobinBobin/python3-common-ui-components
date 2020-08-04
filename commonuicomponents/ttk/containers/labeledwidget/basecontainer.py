from commonutils import Global
from copy import deepcopy
from tkinter import E, W

def inflateChildren(self):
   def deepcopyAndAddGrid(w):
      w = deepcopy(w)
      
      w.setdefault("grid", dict())
      
      return w
   
   children = []
   
   for child in self._baseContainerChildren:
      widgets = tuple(map(child.pop, ("label", "widget")))
      
      widgets[0].setdefault("type", "Label")
      
      multipliers = tuple(Global.MULTIPLIER_TYPE(w["type"], w) for w in widgets)
      
      if multipliers[0].count > 1:
         multipliers[1].count = multipliers[0].count
      
      noLeftPadding = widgets[1].pop("noLeftPadding", False)
      
      for i in range(multipliers[1].count):
         widgetsCopy = tuple(map(deepcopyAndAddGrid, widgets))
         
         widgetsCopy[0]["grid"]["sticky"] = E
         
         grid = widgetsCopy[1]["grid"]
         grid["lastCell"] = True
         
         if "width" not in widgetsCopy[1] and "sticky" not in grid:
            widgetsCopy[1]["width"] = 0
            grid["sticky"] = W + E
         
         if noLeftPadding:
            widgetsCopy[1]["grid"]["padx"] = 0
         
         for multiplier, w in zip(multipliers, widgetsCopy):
            for key in ("text", "name"):
               multiplier.setIndexableToChild(w, key, i)
         
         children.extend(widgetsCopy)
   
   self._baseContainerChildren = children
