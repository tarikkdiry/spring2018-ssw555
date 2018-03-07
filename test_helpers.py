import unittest
import gedcom

class Test(unittest.TestCase):
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

    ''' User Story 2 & 10 - Oscar ''' 
'''
    def test_us02_1(self):
        self.assertTrue(gedcom.us02_helper(['5', 'JAN', '2050'], ['1', 'JAN', '1955'], ['13', 'FEB', '1955']))
 
    def test_us02_2(self):
        self.assertFalse(gedcom.us02_helper(['1', 'JAN', '1855'], ['1', 'JAN', '1950'], ['13', 'FEB', '1940']))
  
    def test_us02_3(self):
        self.assertFalse(gedcom.us02_helper(['1', 'JAN', '2000'], ['1', 'JAN', '2000'], ['1', 'JAN', '2000']))
  
    def test_us02_4(self):
        self.assertTrue(gedcom.us02_helper([], [], ['13', 'FEB', '1940']))
  
    def test_us02_5(self):
        self.assertTrue(gedcom.us02_helper(['1', 'JAN', '1995'], [], ['13', 'FEB', '1980']))

    def test_us10_1(self):
        self.assertTrue(gedcom.us10_helper(['5', 'JAN', '2050'], ['1', 'JAN', '1955'], ['13', 'FEB', '1955']))
 
    def test_us10_2(self):
        self.assertFalse(gedcom.us10_helper(['1', 'JAN', '1855'], ['1', 'JAN', '1950'], ['13', 'FEB', '1940']))
  
    def test_us10_3(self):
        self.assertFalse(gedcom.us10_helper(['1', 'JAN', '2000'], ['1', 'JAN', '2000'], ['1', 'JAN', '2000']))
  
    def test_us10_4(self):
        self.assertTrue(gedcom.us10_helper([], [], ['13', 'FEB', '1940']))
  
    def test_us10_5(self):
        self.assertTrue(gedcom.us10_helper(['1', 'JAN', '1995'], [], ['13', 'FEB', '1980']))
'''
        
if __name__ == "__main__":
    unittest.main()
    
    