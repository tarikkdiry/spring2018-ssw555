import unittest
import gedcom, gedcomDatabase

TEST_FILE = 'sample_arocha.ged'
DATABASE = TEST_FILE.replace(gedcom.EXTENSION, '.sqlite3')
gedcomDatabase.database(TEST_FILE, DATABASE)
INDIVIDUALS, FAMILIES, DICTIONARY = gedcomDatabase.dictify(DATABASE)

class Test(unittest.TestCase):

    def test_TAGS(self):
        self.assertEqual(gedcomDatabase.TAGS, ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE'])

    def test_LEVELS(self):
        self.assertEqual(gedcomDatabase.LEVELS, {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'})

    def test_us02(self):
        self.assertTrue(gedcom.us02(INDIVIDUALS, FAMILIES, DICTIONARY))

    def test_us03(self):
        self.assertTrue(gedcom.us03(INDIVIDUALS, FAMILIES, DICTIONARY))

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

    def test_us29(self):
        self.assertEqual(gedcom.us29(INDIVIDUALS, FAMILIES, DICTIONARY), ['I1', 'I6'])
    
    '''def test_us34(self):
        self.assertEqual(gedcom.us34(INDIVIDUALS, FAMILIES, DICTIONARY), [])'''
    
if __name__ == "__main__":
    unittest.main()
    
    