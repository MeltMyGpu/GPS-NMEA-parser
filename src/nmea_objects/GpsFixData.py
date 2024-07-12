''' 
TODO:
    - Add methods for interacting with the data held by the class.
'''
# import custom_exceptions as ce
import custom_exceptions as ce 

class GpsFixData:
    """
    Holds the data from a NMEA $xxGGA sentence in an organised manor.  
    """
    msg_id : str 
    time: float         # time in UTC
    lat: float          # lat in degrees & minuets 
    ns: str             # North / south indicator
    lng: float          # longitude in degrees & minuets 
    ew: str             # East/west indicator 
    qual: int           # single digit pos fix indicator 
    num_sat: int        # number of satellites used for pos fix
    hdop: float         # Horizontal dilution of position 
    alt: float          # Altitude in meters 
    u_alt: str          # Altitude unit (fixed to 'M')
    sep: float          # Geoid separation - diff between geoid and mean sea level (in meters)
    u_sep: str          # Geoid separation unit (fixed to 'M')
    diff_age: float     # age of diff correction (blank without DGPS)
    diff_stat: float    # Id of station providing diff corrections (blank without DGPS)
    cs: hex             # CheckSum
    
    def __init__(self, sentence: list):
        try:
            test:str = sentence[0]
            test = test.removeprefix("$GS")
            if test != "GGA":
                raise ce.InvalidNmeaTypeException("The passed sentence was not of type GGA, was:  " + test)
            self.msg_id     = sentence[0]
            self.time       = sentence[1]
            self.lat        = sentence[2]
            self.ns         = sentence[3]
            self.lng        = sentence[4]
            self.ew         = sentence[5]
            self.qual       = sentence[6]
            self.num_sat    = sentence[7]
            self.hdop       = sentence[8]
            self.alt        = sentence[9]
            self.u_alt      = sentence[10]
            self.sep        = sentence[11]
            self.u_sep      = sentence[12]
            self.diff_age   = sentence[13]
            self.diff_stat  = sentence[14]
            self.cs         = sentence[15]
        
        except IndexError as e:
            raise Exception(e) #TODO: sort out log access and handle this properly 

    ...
    
    
    
    
    

