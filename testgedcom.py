import unittest
import gedcom

class Test(unittest.TestCase):

    def test_TAGS(self):
        TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
        self.assertEqual(gedcom.TAGS_SIZE(TAGS), True)

    def test_LEVELS(self):
        LEVELS = {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'}
        self.assertEqual(gedcom.LEVELS_SIZE(LEVELS), True)

    def test_ID(self):
        self.assertEqual(gedcom.uniqueID(), True)

    def test_husbandID(self):
        self.assertEqual(gedcom.uniqueHusbandID(), True)

    def test_wifeID(self):
        self.assertEqual(gedcom.uniqueWifeID(), True)

    def test_husbandName(self):
        self.assertEqual(gedcom.uniqueHusbandName(), True)

    def test_wifeName(self):
        self.assertEqual(gedcom.uniqueWifeName(), True)

    def test_marrageAfterBirth(self):
        self.assertEquals(gedcom.marrageAfterBirth(), True)
    
    def test_marrageExist(self):
        self.assertNotEqual(gedcom.marrageExist(), ["NULL"])
    
    def test_husbandExist(self):
        self.assertNotEqual(gedcom.husbandExist(), ["NULL"])
        
    def test_wifeExist(self):
        self.assertNotEqual(gedcom.wifeExist(), ["NULL"])
    
    def test_familyUnique(self):
        self.assertNotEqual(gedcom.familyUnique(), ["NULL"])
        
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
    
#     "User Story 2 - Oscar"  
#     def test_6(self):
#         self.assertEqual(gedcom.us02(['5', 'JAN', '2050'], ['1', 'JAN', '1955'], ['13', 'FEB', '1955']), True)
# 
#     def test_7(self):
#         self.assertEqual(gedcom.us02(['1', 'JAN', '1855'], ['1', 'JAN', '1950'], ['13', 'FEB', '1940']), False)
#  
#     def test_8(self):
#         self.assertEqual(gedcom.us02(['1', 'JAN', '2000'], ['1', 'JAN', '2000'], ['1', 'JAN', '2000']), False)
#  
#     def test_9(self):
#         self.assertEqual(gedcom.us02([], [], ['13', 'FEB', '1940']), False)
#  
#     def test_10(self):
#         self.assertEqual(gedcom.us02(['1', 'JAN', '1995'], [], ['13', 'FEB', '1980']), True)

    "User Story 10 - Oscar"  
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
