import unittest



''' Test specific imports '''
from nmea_objects.GpsFixData import GpsFixData
import custom_exceptions as ce


class DataObjectTests(unittest.TestCase):
    
    def test_GpsFixData_init(self):
        """Tests the type validation from nmea string on class init
        """
        test_list = ["$GSGPA", " BLANK"]
        self.assertRaises(ce.InvalidNmeaTypeException, lambda: GpsFixData(test_list))




if __name__ == '__main__':
    unittest.main()
    ...