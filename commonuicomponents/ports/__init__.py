from commonutils import Global

def writeComboboxValue(widget, cmd, *_):
   value = widget.getValueIndex() if widget.itemsAreStrings else widget.getCurrentItem().value
   
   Global.port.packet(cmd = cmd, params = [value]).write()
