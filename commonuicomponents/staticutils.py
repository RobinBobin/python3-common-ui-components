from commonutils import StaticUtils as StaticUtilsBase
from tkinter.messagebox import showerror, showinfo
from .config import Config

class StaticUtils(StaticUtilsBase):
   @staticmethod
   def showerror(message, **options):
      showerror(Config["title"], message, **options)
   
   @staticmethod
   def showinfo(message, **options):
      showinfo(Config["title"], message, **options)
