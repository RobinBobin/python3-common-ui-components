class PeriodicalAfter:
   def __init__(self, widget, callback, *args):
      self.__args = tuple(args)
      self.__callback = callback
      self.__id = None
      self.__widget = widget
   
   def start(self, delay_ms = 0):
      if self.__id:
         raise RuntimeError()
      
      def callback():
         self.__callback(*self.__args)
         
         setId()
      
      def setId():
         self.__id = self.__widget.after(delay_ms, callback) if delay_ms else self.__widget.after_idle(callback)
      
      setId()
      
      return self
   
   def stop(self):
      if self.__id is not None:
         self.__widget.after_cancel(self.__id)
         
         self.__id = None
