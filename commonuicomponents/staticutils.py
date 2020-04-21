from commonutils import StaticUtils as StaticUtilsBase
from tkinter.messagebox import showerror, showinfo

class StaticUtils(StaticUtilsBase):
   @staticmethod
   def showerror(message, **options):
      showerror(StaticUtils.TITLE, message, **options)
   
   @staticmethod
   def showinfo(message, **options):
      showinfo(StaticUtils.TITLE, message, **options)
