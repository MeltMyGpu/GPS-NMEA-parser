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
    pre, post = value.split(b'.')
    degrees:int = int(pre) // 100 
    minutes = int(pre) % 100
    seconds = 60.0 * int(post) / 10 ** len(post)
    
    x = minutes / 60
    y = seconds / 3600
    
    output = degrees + (minutes / 60.0 )+ (seconds / 3600.0) 
    if direction.find(b'S') > 0 or direction.find(b'W') > 0:
        output = -output
    return round(output, 8)

def parse_float(target:str) -> float | None:
    """Parses a string to a float, returns None if string is empty"""
    if not target: 
        return None 
    else: 
        return float(target) 

def parse_int(target:str) -> int | None:
    """Parses a string to a int, returns None if string is empty"""
    if not target: 
        return None 
    else: 
        return int(target) 


class GpsFixData:

    def __init__(self, serial_port:str, bit_rate:int = 9600):
        self.port_stream = serial.Serial(serial_port)
        self.type_handlers = { # TODO: Extend as different types are added
            b"$GPGGA" : self.gga_parser,
            b"$GPGSV" : self.gsv_parser, 
        }
        self.gga_data = None
        self.gsv_data = None
        
        
    def read_line(self) -> str:
        """Reads a single line from the serial port

        Returns:
            str: The first valid line in port buffer
        """
        while True:
            line = self.port_stream.readline().strip()
            if line.startswith(b'$'):
                LOG.debug(line)
                return line
    
    
    def parse_line(self) -> None:
        """Parses a NMEA string from the port buffer and forward to the correct handler method 
        """
        nmea, _ = self.read_line().split(b'*')
        items = nmea.split(b',')
        handler = self.type_handlers.get(items[0])
        if handler:
            handler(items)
        
    
    ''' TODO:   Currently in testing format to check that parsing is working correctly, 
                should be refactored to the test module later '''
    def run(self):
        while True:
            self.parse_line()
            # if self.gga_data:
                # for key in self.gga_data.keys():
                    # print(self.gga_data.get(key))


    def gga_parser(self, data: list[str]) -> None:
        
        '''NOTE:    All data in the NMEA sentence has a variable assignment below for context reasons,
                    data that is not required, guaranteed blank, or fix to a certain value has been 
                    commented out, but left in it's relative position in the sentence.'''
        msg_id    : str       = data[0]
        time      :float|None = parse_float(data[1])                    # time in UTC
        lat       :float|None = to_degrees(data[2], data[3])            # lat in degrees & minuets 
        lng       :float|None = to_degrees(data[4], data[5])            # longitude in degrees & minuets 
        qual      : int |None = parse_int(data[6])                      # single digit pos fix indicator 
        num_sat   : int |None = parse_int(data[7])                      # number of satellites used for pos fix
        hdop      :float|None = parse_float(data[8])                    # Horizontal dilution of position 
        alt       :float|None = parse_float(data[9])                    # Altitude in meters 
        # u_alt     :str  |None = data[10]                                # Altitude unit (fixed to 'M') 
        geo_sep   :float|None = parse_float(data[11])                   # Geoid separation - diff between geoid and mean sea level (in meters) 
        # u_sep     :str  |None = data[12]                                # Geoid separation unit (fixed to 'M') 
        # diff_age  :float|None = parse_float(data[13])                   # age of diff correction (blank without DGPS) 
        # diff_stat :float|None = parse_float(data[14])                   # Id of station providing diff corrections (blank without DGPS) 
        self.gga_data = dict(
            msg_id   = msg_id,
            time     = time,
            lat      = lat,
            lng      = lng,
            qual     = qual,
            num_sat  = num_sat,
            hdop     = hdop,
            alt      = alt,
            # u_alt    = u_alt,
            geo_sep  = geo_sep,
            # u_sep    = u_sep,
            # diff_age = diff_age,
            # diff_stat= diff_stat,
        )
        LOG.debug(self.gga_data)
        
    
    def gsv_parser(self, data: list[str]) -> None:
        
        '''NOTE:    All data in the NMEA sentence has a variable assignment below for context reasons,
                    data that is not required, guaranteed blank, or fix to a certain value has been 
                    commented out, but left in it's relative position in the sentence.'''
        msg_id    :str        = data[0]
        num_of    :int|None   = parse_int(data[1])                      # Total number of GSV messages in output
        msg_num   :int|None   = parse_int(data[2])                      # The number of this message (starting at 1)
        num_sat   :int|None   = parse_int(data[3])                      # Number of satellites in view                       
        assert len(data) % 4 == 0, 'Error in data' 
        sat_list :list[dict[str,int]] = []
        tot_sat:int = (len(data) - 4 ) /  4
        for x in range(0, int(tot_sat - 1)):
            sat_list.append( dict(
                sat_id          = parse_int(data[1 + (4 * x)]),         # The satellites ID
                elevation       = parse_int(data[2 + (4 * x)]),         # Elevation angle (range 0->90)
                azimuth         = parse_int(data[3 + (4 * x)]),         # Azimuth (range 0->359)
                sig_strength    = parse_int(data[4 + (4 * x)]),         # Signal strength (0->99 or blank)
            )) 
            
        self.gsv_data = dict(
            sat_id  = msg_id,
            num_of  = num_of,
            msg_num = msg_num,
            num_sat = num_sat,
            sat_list = sat_list,
        )
        LOG.debug(self.gsv_data)
        
        
        
    
    ...
    
    

# obj = GpsFixData('COM4', 9600)
# obj.gga_parser("$GPGGA,092725.00,4717.11399,N,00833.91590,E,1,08,1.01,499.6,M,48.0,M,,*5B".split(','))
# obj.run()
