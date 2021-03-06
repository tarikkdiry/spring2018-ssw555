import unittest
import gedcom, gedcomDatabase

TEST_FILE = 'sample_arocha.ged'
DATABASE = TEST_FILE.replace('.ged', '.sqlite3')
gedcomDatabase.database(TEST_FILE, DATABASE)
INDIVIDUALS, FAMILIES, DICTIONARY = gedcomDatabase.dictify(DATABASE)

class Test(unittest.TestCase):
    
    def test_us01(self):
        self.assertTrue(gedcom.us01(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us02(self):
        self.assertTrue(gedcom.us02(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us03(self):
        self.assertTrue(gedcom.us03(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us04(self):
        self.assertTrue(gedcom.us04(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us05(self):
        self.assertTrue(gedcom.us05(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us06(self):
        self.assertTrue(gedcom.us06(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us07(self):
        self.assertTrue(gedcom.us07(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us09(self):
        self.assertTrue(gedcom.us09(INDIVIDUALS, FAMILIES, DICTIONARY))
 
    def test_us10(self):
        self.assertTrue(gedcom.us10(INDIVIDUALS, FAMILIES, DICTIONARY))
    
    def test_us21(self):
        self.assertTrue(gedcom.us21(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us22(self):
        self.assertTrue(gedcom.us22(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us26(self):
        self.assertTrue(gedcom.us26(INDIVIDUALS, FAMILIES, DICTIONARY))
        
    def test_us27(self):
        self.assertTrue(gedcom.us27(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us29(self):
        self.assertEqual(gedcom.us29(INDIVIDUALS, FAMILIES, DICTIONARY), ['I1', 'I6'])
    
    def test_us42(self):
        self.assertTrue(gedcom.us22(INDIVIDUALS, FAMILIES, DICTIONARY))
    
    '''def test_us34(self):
        self.assertEqual(gedcom.us34(INDIVIDUALS, FAMILIES, DICTIONARY), [])'''
    
if __name__ == "__main__":
    unittest.main()
    
    