import unittest
import gedcom

class Test(unittest.TestCase):

    def testTAGS(self):
        TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
        self.assertEqual(gedcom.TAGS_SIZE(TAGS), True)

    def testLEVELS(self):
        LEVELS = {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'}
        self.assertEqual(gedcom.LEVELS_SIZE(LEVELS), True)

    def testID(self):
        self.assertEqual(gedcom.unique_ID(), True)


if __name__ == "__main__":
    unittest.main()
