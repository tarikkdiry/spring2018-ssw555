from datetime import datetime
LEVELS = {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'}

def us07(Children):
    '''Check to see if there are fifteen siblings, 15 kids is ridiculous'''
    amountChildren = True
    for l in line:
        if len(Children) >= 15:
            amountChildren = False
