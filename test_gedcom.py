import unittest
import gedcom

TEST_FILE = 'sample_arocha.ged'
DATABASE = TEST_FILE.replace(gedcom.EXTENSION, '.sqlite3')
gedcom.database(TEST_FILE, DATABASE)
INDIVIDUALS, FAMILIES, DICTIONARY = gedcom.dictify(DATABASE)

class Test(unittest.TestCase):

    def test_us09(self):
        self.assertTrue(gedcom.us09(INDIVIDUALS, FAMILIES, DICTIONARY))
    
    def test_us21(self):
        self.assertTrue(gedcom.us21(INDIVIDUALS, FAMILIES, DICTIONARY))
    
    def test_us29(self):
        self.assertEqual(gedcom.us29(INDIVIDUALS, FAMILIES, DICTIONARY), ['I1', 'I6'])
    
if __name__ == "__main__":
    unittest.main()
    
    