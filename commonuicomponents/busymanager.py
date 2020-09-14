from commonutils import Global
from tkinter import Frame

class BusyManager:
   @staticmethod
   def start():
      BusyManager.__frame = Frame(Global.appLauncher.root)
      BusyManager.__frame.pack()
      BusyManager.__frame.wait_visibility()
      BusyManager.__frame.grab_set()
      
      Global.appLauncher.root["cursor"] = "watch"
   
   @staticmethod
   def stop():
      BusyManager.__frame.grab_release()
      BusyManager.__frame.destroy()
      Global.appLauncher.root["cursor"] = ""
