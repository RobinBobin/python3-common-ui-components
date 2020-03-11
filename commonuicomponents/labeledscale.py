from math import floor, log10
from tkinter import E, Frame, IntVar, W
from tkinter.ttk import Label, Scale, Style

class LabeledScale(Frame):
   def __init__(self, master, config, **kwargs):
      super().__init__(master, background = "cyan")
      
      style = Style()
      
      CAPTION = "TLabeledScale.Caption.TLabel"
      
      print(style.lookup(CAPTION, "padx", default = "20 10"))
      
      Label(self, text = caption).grid(row = 0, column = 0, padx = (20, 10), sticky = E)
      
      self.__value = Label(self, anchor = E, text = from_, width = floor(log10(to)) + 1)
      self.__value.grid(row = 0, column = 1, sticky = E)
      
      self.__variable = IntVar()
      self.__variable.set(from_)
      
      Scale(
         self,
         command = self.onCommand,
         from_ = from_,
         length = 400,
         to = to,
         variable = self.__variable).grid(
            row = 0,
            column = 2,
            padx = 20,
            pady = 20)
   
   def onCommand(self, _ = "dummy"):
      self.__value.configure(text = self.__variable.get())













# {
#    "caption":"Термокамера",
#    "ui": [[
#       "labeledContainer", {
#          "caption": "Нагреватель",
#          "children": [{
#             "type": "labeledScale",
#             "caption":"Задержка (с):",
#             "range": [0, 30]
#          }, {
#             "type": "labeledScale",
#             "caption": "Интенсивность (%):",
#             "range": [0, 100]
#          }],
#          "repeatCount": 3
#       }
#    ], [
      
#    ]]
# }
