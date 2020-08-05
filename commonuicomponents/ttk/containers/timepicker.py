from functools import partial
from . import Container

HOURS = "hours"
MINUTES = "minutes"
SECONDS = "seconds"

class TimePicker(Container):
   HOURS = HOURS
   MINUTES = MINUTES
   SECONDS = SECONDS
   
   __DEFAULT_MAX_VALUES = { HOURS: 24, MINUTES: 60, SECONDS: 60 }
   
   def __init__(self, master, **kw):
      valueDomains = kw.pop("valueDomains", [])
      
      kw["children"] = [{
         "type": "CommonCombobox",
         "grid": { "padx": 10 },
         "name": name,
         "valueDomains": valueDomains,
         "values": { "count": count },
         "width": 5
      } for name, count in TimePicker.__DEFAULT_MAX_VALUES.items()]
      
      for i in (2, 1):
         kw["children"].insert(i, {
            "type": "Label",
            "grid": { "padx": 10 },
            "text": ":"
         })
      
      super().__init__(master, **kw)
   
   def bindOnTimeSelected(self, handler):
      for widget in self.getSmartWidget().values():
         widget.bindOnSelected(partial(handler, widget.smartWidgetName))
   
   def getTime(self, index = None):
      if index:
         return int(self.getSmartWidget(index).getValue())
      
      return {widget.smartWidgetName: int(widget.getValue()) for widget in self.getSmartWidget().values()}
