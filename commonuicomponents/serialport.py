from commonutils.serialport import SerialException, SerialPort
from .staticutils import StaticUtils

SerialPort.setErrorProcessor(StaticUtils.showerror)

# = Dummy statement to quiet the linter = #
type(SerialException)
