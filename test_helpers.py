import unittest
import gedcom

class Test(unittest.TestCase):
    ''' User Story 2 - Oscar ''' 
    def test_us02_1(self):
        self.assertTrue(gedcom.us02_helper(['5', 'JAN', '2018'], ['1', 'JAN', '1955']))
 
    def test_us02_2(self):
        self.assertTrue(gedcom.us02_helper(['1', 'JAN', '2000'], ['1', 'JAN', '1950']))
  
    def test_us02_3(self):
        self.assertFalse(gedcom.us02_helper(['1', 'DEC', '2000'], ['1', 'JAN', '2000']))
  
    def test_us02_4(self):
        self.assertFalse(gedcom.us02_helper([], ['13', 'FEB', '1940']))
  
    def test_us02_5(self):
        self.assertFalse(gedcom.us02_helper(['1', 'JAN', '1995'], []))
    
    
    ''' User Story 3 - Mike '''
    def test_us03_1(self):
        self.assertFalse(gedcom.us03_helper([], ['1', 'JAN', '1950']))

    def test_us03_2(self):
        self.assertTrue(gedcom.us03_helper(['13', 'FEB', '1940'], []))

    def test_us03_3(self):
        self.assertTrue(gedcom.us03_helper(['1', 'NOV', '1996'], ['12', 'DEC', '2001']))

    def test_us03_4(self):
        self.assertFalse(gedcom.us03_helper([], []))
        
    def test_us03_5(self):
        self.assertFalse(gedcom.us03_helper(['1', 'JAN', '1955'], ['1', 'JAN', '1950']))
    
    ''' User Story 7 - Tarik '''
    def test_us07_1(self):
        self.assertTrue(gedcom.us07_helper(['I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14']))

    def test_us07_2(self):
        self.assertFalse(gedcom.us07_helper(['I1','I2','I3','I4','I5','I6','I7','I8','I9','I10','I11','I12','I13','I14','I15','I16']))

    def test_us07_3(self):
        self.assertTrue(gedcom.us07_helper(['I1']))

    def test_us07_4(self):
        self.assertTrue(gedcom.us07_helper([]))
        
    def test_us07_5(self):
        self.assertTrue(gedcom.us07_helper(['I1', 'I5', 'I6']))
    
    ''' User Story 9 - Austin '''
    def test_us09_1(self):
        self.assertFalse(gedcom.us09_helper([], ['1', 'JAN', '1950'], ['1', 'JAN', '1950']))

    def test_us09_2(self):
        self.assertFalse(gedcom.us09_helper(['13', 'FEB', '1940'], ['1', 'JAN', '1955'], ['1', 'JAN', '1950']))

    def test_us09_3(self):
        self.assertTrue(gedcom.us09_helper(['12', 'DEC', '2001'], ['1', 'JAN', '2001'], ['1', 'NOV', '1996']))

    def test_us09_4(self):
        self.assertFalse(gedcom.us09_helper([], [], []))
        
    def test_us09_5(self):
        self.assertFalse(gedcom.us09_helper(['1', 'JAN', '1950'], ['1', 'JAN', '1955'], []))

    ''' User Story 10 - Oscar ''' 
    def test_us10_1(self):
        self.assertFalse(gedcom.us10_helper([], ['1', 'JAN', '1950'], ['1', 'JAN', '1950']))
 
    def test_us10_2(self):
        self.assertFalse(gedcom.us10_helper(['13', 'FEB', '1940'], ['1', 'JAN', '1955'], ['1', 'JAN', '1950']))
  
    def test_us10_3(self):
        self.assertFalse(gedcom.us10_helper(['1', 'JAN', '1900'], [], ['1', 'JAN', '1950']))
  
    def test_us10_4(self):
        self.assertTrue(gedcom.us10_helper(['1', 'JAN', '2001'], ['1', 'JAN', '1915'], ['1', 'JAN', '1915']))
  
    def test_us10_5(self):
        self.assertTrue(gedcom.us10_helper(['12', 'DEC', '2001'], ['1', 'JAN', '1980'], ['1', 'NOV', '1975']))

    ''' User Story 21 - Austin '''
    def test_us21_1(self):
        self.assertTrue(gedcom.us21_helper('m', 'f'))

    def test_us21_2(self):
        self.assertTrue(gedcom.us21_helper('m', 'F'))

    def test_us21_3(self):
        self.assertFalse(gedcom.us21_helper('f', 'M'))

    def test_us21_4(self):
        self.assertFalse(gedcom.us21_helper('F', 'm'))
        
    def test_us21_5(self):
        self.assertTrue(gedcom.us21_helper('M', 'F'))
        
    ''' User Story 22 - Tarik '''
    def test_us22_1(self):
        self.assertTrue(gedcom.us22_helper(['I1','I2','I3'], ['F1']))

    def test_us22_2(self):
        self.assertFalse(gedcom.us22_helper(['I1','I2', 'I1','I3'], ['F1']))

    def test_us22_3(self):
        self.assertFalse(gedcom.us22_helper(['I1','I2', 'I1','I3'], ['F1', 'F1']))

    def test_us22_4(self):
        self.assertFalse(gedcom.us22_helper(['I1','I2','I3'], ['F1', 'I5']))
        
    def test_us22_5(self):
        self.assertTrue(gedcom.us22_helper(['I1','I2','I3', 'I5'], ['F1', 'F2']))
        
    ''' User Story 34 - Mike '''
    def test_us34_1(self):
        self.assertFalse(gedcom.us34_helper(['16', 'FEB', '1940'], ['1', 'JAN', '1955'], ['1', 'JAN', '1954']))

    def test_us34_2(self):
        self.assertTrue(gedcom.us34_helper(['13', 'FEB', '1940'], ['5', 'APR', '1955'], ['15', 'JAN', '1970']))

    def test_us34_3(self):
        self.assertTrue(gedcom.us34_helper(['13', 'FEB', '1940'], ['1', 'JAN', '1970'], ['4', 'JAN', '1955']))

    def test_us34_4(self):
        self.assertFalse(gedcom.us34_helper(['12', 'FEB', '1940'], ['7', 'JAN', '1955'], ['1', 'JAN', '1955']))
        
    def test_us34_5(self):
        self.assertFalse(gedcom.us34_helper(['13', 'MAR', '1940'], ['23', 'JUN', '1955'], ['1', 'JAN', '1954']))
        
if __name__ == "__main__":
    unittest.main()
    
    