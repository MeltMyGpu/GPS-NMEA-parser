

import serial.tools.list_ports as port_list
import serial
import logging
import inspect
import os


# GLOBAL CONST
FILE_PATH = os.path.dirname(__file__)
# os.environ["PYTHONPYCACHEPREFIX"] = FILE_PATH + "/../Cache"

LOG = logging.getLogger(":serial_reader:")
ERR_STR = "{caller}:: {Error}"


# STREAM = serial.Serial('COM4')
def start_up():
    open(FILE_PATH + "/../myapp.log", "w").close() # Clear log file 
    logging.basicConfig(filename= FILE_PATH + "/../myapp.log",level=logging.DEBUG)
    LOG.info(ERR_STR.format(caller= inspect.currentframe().f_code.co_name, Error= "Startup completed"))
 

def get_com_ports() -> list | None:
    """Gets a list of the active COM ports on the current device

    Returns:
        list | None: Returns a list of active ports, or None 
    """
    ports = list(port_list.comports())
    try:
        ports[0]
    except IndexError as e:
        LOG.exception(e)
        return None
    else:
        return ports
   
        
def display_com_ports():
    """
    Prints the available COM ports to the console

    Raises:
        Exception: If no ports are available 
    """
    ports = get_com_ports()
        
    if ports == None:
        LOG.warning(ERR_STR.format(caller= inspect.currentframe().f_code.co_name, Error= "No active COM ports"))
        raise Exception(" No valid COM ports could be located, is the device plugged in?")
    
    i = 1 
    for port in ports:
        print(i, ":: ", port.name) 
        i =+ 1
        

def _stream_readline(stream: serial) -> str:
    """
    Reads a line from the provided serial port buffer

    Args:
        stream (serial): connection to the serial port for your GPS receiver.

    Returns:
        str: A single line from the serial ports output buffer
    """
    word  = ''
    while True:
        res = stream.read()
        if not (res == b'\r'):
            word += bytes.decode(res)
        else:
            stream.read() # removes the newline character from the stream buffer
            return word
    
          
def display_com_stream(stream: serial = None):
    """
    Reads and prints lines from the connected COM ports output stream.
    
    Args:
        stream (serial, optional): connection to the serial port for your GPS receiver. Defaults to None.

    Raises:
        Exception: If there is not an allocated serial port
    """
    if stream == None:
        LOG.warning(ERR_STR.format(caller= inspect.currentframe().f_code.co_name, Error= "Trying to read COM stream without providing active serial object"))
        return 
    while True:
        print(_stream_readline(stream) + "\n")
    


def write_stream_to_file(stream: serial = None):
    if stream == None:
        LOG.warning(ERR_STR.format(caller= inspect.currentframe().f_code.co_name, Error= "Trying to read COM stream without providing active serial object"))
        return
    with open(FILE_PATH + "/../streamData.txt","w") as file: 
        i=0
        while i < 20:
            file.write(_stream_readline(stream) + "\n")
            i += 1

        
            
        
start_up()
    
display_com_ports()
# display_com_stream()
stream = serial.Serial('COM4')
write_stream_to_file(stream)
# display_com_stream(stream)


'''
TODO:
    - Sort through the types of NMEA sentences
    - Create a form of serialization for sentences
    - Learn how to interpret the sentences in order to obtain information from them
    - Refactor code base
'''


def GpsFixData_init_test():
    from nmea_objects.GpsFixData import GpsFixData
    test_list = ["$GSGPA", " BLANK"]
    try:
        GpsFixData(test_list)
        LOG.debug(ERR_STR.format(caller= inspect.currentframe().f_code.co_name, Error= "failed"))
    except ce.InvalidNmeaTypeException as e:
        LOG.debug(ERR_STR.format(caller= inspect.currentframe().f_code.co_name, Error= "Passed: giving" ))
        LOG.exception(e)
        

''' TEST BLOCK'''
# GpsFixData_init_test()