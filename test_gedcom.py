import unittest
import gedcom

class Test(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()