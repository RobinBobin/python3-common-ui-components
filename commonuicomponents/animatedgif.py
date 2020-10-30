from PIL import Image, ImageTk
from tkinter.ttk import Label

from .periodicalafter import PeriodicalAfter

class AnimatedGif(Label):
   def __init__(self, master, filename):
      im = Image.open(filename)
      
      seq = []
      
      try:
         while True:
            seq.append(im.copy())
            im.seek(len(seq))
      
      except EOFError:
         pass
      
      try:
         self.__delay = im.info["duration"]
      
      except KeyError:
         self.__delay = 100
      
      first = seq[0].convert("RGBA")
      
      self.__frames = [ImageTk.PhotoImage(first)]
      
      Label.__init__(self, master, image = self.__frames[0])
      
      temp = seq[0]
      
      for image in seq[1:]:
         temp.paste(image)
         frame = temp.convert("RGBA")
         
         self.__frames.append(ImageTk.PhotoImage(frame))
      
      self.__frameIndex = 0
      
      self.__periodicalAfter = PeriodicalAfter(self, self.__nextFrame)
   
   def play(self):
      self.__periodicalAfter.start(self.__delay)
   
   def stop(self):
      self.__periodicalAfter.stop()
   
   def __nextFrame(self):
      if self.__frameIndex == len(self.__frames) - 1:
         self.__frameIndex = 0
      
      else:
         self.__frameIndex += 1
      
      self.config(image = self.__frames[self.__frameIndex])
