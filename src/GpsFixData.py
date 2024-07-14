''' 
TODO:
    - Add methods for interacting with the data held by the class.
'''
import logging 
import serial 
import custom_exceptions as ce 

LOG = logging.getLogger(":GpsFixData:")
logging.basicConfig(level=logging.DEBUG)


'''
    HELPER FUNCTIONS
'''
def to_degrees(value:str, direction:str) -> float:
    """ 
    Converts the NMEA lat / long format of Degree, minutes, seconds directly to
    degrees. 
    "dddmm.sssss" -to> just degrees as a floating point.

    Args:
        value (str): The long / lat value as a string, provided by a NMEA sentence. 
        direction (str): The NorthSouth / EastWest indicator provided by the NMEA sentence. 

    Returns:
        float: The lat / long as a decimal degree value.
    """
    if not value:
        return None
    pre, post = value.split('.')
    degrees:int = int(pre) // 100 
    minutes = int(pre) % 100
    seconds = 60.0 * int(post) / 10 ** len(post)
    
    x = minutes / 60
    y = seconds / 3600
    
    output = degrees + (minutes / 60.0 )+ (seconds / 3600.0) 
    if direction.find('S') > 0 or direction.find('W') > 0:
        output = -output
    return round(output, 8)
        



class GpsFixData:

    def __init__(self, serial_port:str, bit_rate:int):
        self.port_stream = serial.Serial(serial_port)
        self.type_handlers = { # TODO: Extend as different types are added
            b"$GPGGA" : self.gga_handle,
        }
        self.gga_data = None
        
    
    def read_line(self) -> str:
        """Reads a single line from the serial port

        Returns:
            str: The first valid line in port buffer
        """
        while True:
            line = self.port_stream.readline().strip()
            LOG.debug(line)
            if line.startswith(b'$'):
                LOG.debug(line)
                return line
    
    
    def parse_line(self) -> None:
        """Parses a NMEA string to send to the correct handler
        """
        items = self.read_line().split(b',')
        handler = self.type_handlers.get(items[0])
        if handler:
            handler(items)
        
    
    def run(self):
        while True:
            self.parse_line()
            if self.gga_data:
                for key in self.gga_data.keys():
                    print(self.gga_data.get(key))


    def gga_handle(self, data: list[str]) -> None:
        msg_id    :str   = data[0]
        time      :float = float(data[1])                  # time in UTC
        lat       :float = to_degrees(data[2], data[3])    # lat in degrees & minuets 
        lng       :float = to_degrees(data[4], data[5])    # longitude in degrees & minuets 
        qual      :int   = int(data[6])                    # single digit pos fix indicator 
        num_sat   :int   = int(data[7])                    # number of satellites used for pos fix
        hdop      :float = float(data[8])                  # Horizontal dilution of position 
        alt       :float = float(data[9])                  # Altitude in meters 
        u_alt     :str   = data[10]                        # Altitude unit (fixed to 'M') 
        sep       :float = float(data[11])                 # Geoid separation - diff between geoid and mean sea level (in meters) 
        u_sep     :str   = data[12]                        # Geoid separation unit (fixed to 'M') 
        diff_age  :float = float(data[13])                 # age of diff correction (blank without DGPS) 
        diff_stat :float = float(data[14])                 # Id of station providing diff corrections (blank without DGPS) 
        # cs        :hex   = hex(int(data[15].removeprefix('*'), 16)) # CheckSum 
        self.gga_data = dict(
            msg_id   = msg_id,
            time     = time,
            lat      = lat,
            lng      = lng,
            qual     = qual,
            num_sat  = num_sat,
            hdop     = hdop,
            alt      = alt,
            u_alt    = u_alt,
            sep      = sep,
            u_sep    = u_sep,
            diff_age = diff_age,
            diff_stat= diff_stat,
            # cs       = cs,
        )
    ...
    
    
    
    
    

obj = GpsFixData('COM4', 9600)
obj.run()
