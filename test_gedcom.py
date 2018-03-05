import unittest
import gedcom

class Test(unittest.TestCase):
    "User Story 9 - Austin"
    def test_1(self):
        self.assertEqual(gedcom.us09([], ['1', 'JAN', '1950'], ['1', 'JAN', '1950']), False)

    def test_2(self):
        self.assertEqual(gedcom.us09(['13', 'FEB', '1940'], ['1', 'JAN', '1955'], ['1', 'JAN', '1950']), False)

    def test_3(self):
        self.assertEqual(gedcom.us09(['12', 'DEC', '2001'], ['1', 'JAN', '2001'], ['1', 'NOV', '1996']), True)

    def test_4(self):
        self.assertEqual(gedcom.us09([], [], []), False)
        
    def test_5(self):
        self.assertEqual(gedcom.us09(['1', 'JAN', '1950'], ['1', 'JAN', '1955'], []), False)
    
    "User Story 2 - Oscar"  
    def test_6(self):
        self.assertEqual(gedcom.us02(['5', 'JAN', '2050'], ['1', 'JAN', '1955'], ['13', 'FEB', '1955']), True)

    def test_7(self):
        self.assertEqual(gedcom.us02(['1', 'JAN', '1855'], ['1', 'JAN', '1950'], ['13', 'FEB', '1940']), False)
 
    def test_8(self):
        self.assertEqual(gedcom.us02(['1', 'JAN', '2000'], ['1', 'JAN', '2000'], ['1', 'JAN', '2000']), False)
 
    def test_9(self):
        self.assertEqual(gedcom.us02([], [], ['13', 'FEB', '1940']), False)
 
    def test_10(self):
        self.assertEqual(gedcom.us02(['1', 'JAN', '1995'], [], ['13', 'FEB', '1980']), True)

if __name__ == "__main__":
    unittest.main()