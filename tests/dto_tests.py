import unittest



''' Test specific imports '''
from GpsFixData import GpsFixData as gfp
import GpsFixData as gfp
import custom_exceptions as ce


class DataObjectTests(unittest.TestCase):
    
    # def test_GpsFixData_init(self):
    #     """Tests the type validation from nmea string on class init
    #     """
    #     test_list = ["$GSGPA", " BLANK"]
    #     self.assertRaises(ce.InvalidNmeaTypeException, lambda: gfp.GpsFixData(test_list))
        
    def test_to_degrees(self):
        degrees = gfp.to_degrees("4717.112671", "N")
        self.assertEqual(degrees, 47.28521118)




if __name__ == '__main__':
    unittest.main()
    ...