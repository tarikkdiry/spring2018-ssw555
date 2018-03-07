import os
import ast
import sqlite3
import gedcomDatabase
from sqlite3 import Error
from shutil import copyfile
from datetime import datetime
from prettytable import PrettyTable

MONTHS = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP' : '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

'''
#TARIK + OSCAR TEST STUFF
TEST_ID = True
TEST_HUSBAND_NAME = True
TEST_WIFE_NAME = True
TEST_HUSBAND_ID = True
TEST_WIFE_ID = True
TEST_MARRAGE_VALID = True

            #TARIK TEST STUFF
            #Sets are unique, if the len of the set ID isn't the same as len of list ID, not all are unique
            if len(id) > len(set(id)):
                TEST_ID = False
            if len(Husband_Name) > len(set(Husband_Name)):
                TEST_HUSBAND_NAME = False
            if len(Wife_Name) > len(set(Wife_Name)):
                TEST_WIFE_NAME = False
            if len(Husband_ID) > len(set(Husband_ID)):
                TEST_HUSBAND_ID = False
            if len(Wife_ID) > len(set(Wife_ID)):
                TEST_Wife_ID = False
            #OSCAR TEST STUFF
            if Married != 'None':
                MarriedPeople = GetFromDB('individuals', '*', 'spouse', "!= [NULL]")
                Married_ID_Date = []
                for x in MarriedPeople:
                    Married_ID_Date = ([x[0],x[1]])
                    Gender = x[2]
                    if ((Gender == "M") | (GetFromDB('families', 'Married', 'Husband_ID', Married_ID_Date[0])[2] < Married_ID_Date[1])):
                        TEST_MARRAGE_VALID = False
                        break
                        
                    if ((Gender == "F") | (GetFromDB('families', 'Married', 'Husband_ID', Married_ID_Date[0])[2] < Married_ID_Date[1])):
                        TEST_MARRAGE_VALID = False
                        break
                        
#OSCAR TEST STUFF            
def GetFromDB(table, column, thisData, condition): 
    connection = sqlite3.connect('database.sqlite3')
    cursor = connection.cursor()
    cursor.execute('SELECT '+ column +' from ' + table + ' where' + thisData + + condition )
    row = cursor.fetchone()
    data = []
    while row is not None:
        data.append(row)
        row = cursor.fetchone()
    return data       

#TARIK TESTING STUFF
def TAGS_SIZE(TAGS):
    return len(TAGS) == 17
def LEVELS_SIZE(LEVELS):
    return len(LEVELS) == 17
def uniqueID():
    return TEST_ID
def uniqueHusbandID():
    return TEST_HUSBAND_ID
def uniqueWifeID():
    return TEST_WIFE_ID
def uniqueHusbandName():
    return TEST_HUSBAND_NAME
def uniqueWifeName():
    return TEST_WIFE_NAME
     
def us06(divorce_date, husband_death, wife_death):
    "Marriage should occur before death of either spouse"
    if not divorce_date or not (husband_death, wife_death):
        return False


def us02(db, marriage_date, individual_ID): #Oscar
    "Birth should occur before marriage of an individual"
    if not marriage_date:
        return False
    query = queryDict(db, "Individuals", individual_ID, "Birthday")['Birthday']
    if(query == "None"):
        return False
    query = ''.join(c for c in query if c not in " (){}<>[]''")
    query = query.split(',')
    ib = datetime(int(query[2]), int(MONTHS[query[1]]), int(query[0]))
    md = datetime(int(marriage_date[2]), int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    return md < ib
    

def us10(marriage_date, husband_birth, wife_birth): #Oscar
    """Marriage should be at least 14 years after birth of both spouses 
       (parents must be at least 14 years old)"""
    if not marriage_date:
        return False
    test = True
    md = datetime(int(marriage_date[2]) - 14, int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    if(husband_birth):
        hb = datetime(int(husband_birth[2]), int(MONTHS[husband_birth[1]]), int(husband_birth[0]))
        test *= hb < md
    if(wife_birth):
        wb = datetime(int(wife_birth[2]), int(MONTHS[wife_birth[1]]), int(wife_birth[0]))
        test *= wb < md
    return test
'''


def us02_helper(marriage_date, individual_birth):
    if not marriage_date or not individual_birth:
        return False
    ib = datetime(int(individual_birth[2]), int(MONTHS[individual_birth[1]]), int(individual_birth[0]))
    md = datetime(int(marriage_date[2]), int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    return md < ib

def us02(ind, fam, dict): #Oscar
    ''' Birth should occur before marriage of an individual '''
    test = true
    for f in fam:
        for i in [dict[f]['Husband_ID'], dict[f]['Wife_ID']]:
            test *= us02_helper(dict[f]['Married'], dict[i]['Birthday'])
    return test

def us03_helper(birth, death):
    if not death:
        return True
    elif not birth:
        return False
    bd = datetime(int(birth[2]), int(MONTHS[birth[1]]), int(birth[0]))
    dd = datetime(int(death[2]), int(MONTHS[death[1]]), int(death[0]))
    return bd < dd

def us03(ind, fam, dict): #Mike
    ''' Birth should occur before death of an individual '''
    test = True
    for i in ind:
        test *= us03_helper(dict[i]['Birthday'], dict[i]['Death'])
    return test

def us07_helper(children):
    return len(Children) < 15

def us07(ind, fam, dict): #Tarik
    '''Check to see if there are fifteen siblings, 15 kids is ridiculous'''
    test = True
    for f in fam:
        test *= us07_helper(dict[f]['Children'])
    return test

def us09_helper(mother_death, father_death, child_birth):
    if not child_birth:
        return False
    elif not mother_death and not father_death:
        return True
    
    cb = datetime(int(child_birth[2]), int(MONTHS[child_birth[1]]), int(child_birth[0]))
    
    if(father_death and not mother_death):
        fd = datetime(int(father_death[2]), int(MONTHS[father_death[1]]), int(father_death[0]))
        return ((fd.year - cb.year) * 12 + fd.month - cb.month) >= 9
    
    elif(mother_death and not father_death):
        md = datetime(int(mother_death[2]), int(MONTHS[mother_death[1]]), int(mother_death[0]))
        return md > cb
    
    fd = datetime(int(father_death[2]), int(MONTHS[father_death[1]]), int(father_death[0]))
    md = datetime(int(mother_death[2]), int(MONTHS[mother_death[1]]), int(mother_death[0]))
    return md > cb and ((fd.year - cb.year) * 12 + fd.month - cb.month) >= 9

def us09(ind, fam, dict): #AUSTIN
    ''' Child born after mother deaths and before 9 months of fathers death'''
    test = True
    for f in fam:
        for i in dict[f]['Children']:
            try:
                test *= us09_helper(dict[dict[f]['Wife_ID']]['Death'], dict[dict[f]['Husband_ID']]['Death'], dict[i]['Birthday'])
            except:
                return False
    return test

def us10_helper(marriage_date, husband_birth, wife_birth):
    if not marriage_date or not (husband_birth or wife_birth):
        return False
    md = datetime(int(marriage_date[2]) - 14, int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    hb = datetime(int(husband_birth[2]), int(MONTHS[husband_birth[1]]), int(husband_birth[0]))
    wb = datetime(int(wife_birth[2]), int(MONTHS[wife_birth[1]]), int(wife_birth[0]))
    return hb < md and wb < md

def us10(ind, fam, dict): #Oscar
    ''' Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old) '''
    test = True
    for f in fam:
        test *= us10_helper(dict[f]['Married'], dic[dict[f]['Husband_ID']]['Birthday'], dic[dict[f]['Wife_ID']]['Birthday'])
    return test

def us21_helper(husband_gender, wife_gender):
    return (husband_gender.upper()+wife_gender.upper()) == 'MF';

def us21(ind, fam, dict): #AUSTIN
    ''' Husband is male, wife is female '''
    test = True
    for f in fam:
        try:
            test *= us21_helper(dict[dict[f]['Husband_ID']]['Gender'], dict[dict[f]['Wife_ID']]['Gender'])
        except:
            return False
    return test

def us29_helper(individual, alive):
    if not alive:
        return individual
    else:
        return None

def us29(ind, fam, dict): #AUSTIN
    ''' Return List of Deceased '''
    deceased = []
    for i in ind:
        temp = us29_helper(i, dict[i]['Alive'])
        if temp:
            deceased.append(temp)
    return deceased

def us34(marriage_date, husband_birth, wife_birth, couple):
    if not marriage_date or not (husband_birth or wife_birth):
        return False
    md = datetime(int(marriage_date[2]) - 14, int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    hb = datetime(int(husband_birth[2]), int(MONTHS[husband_birth[1]]), int(husband_birth[0]))
    wb = datetime(int(wife_birth[2]), int(MONTHS[wife_birth[1]]), int(wife_birth[0]))
    if((((md.year-wb.year)*2) >= (md.year-hb.year)) or (((md.year-wb.year) <= (md.year-hb.year)*2))):
       return couple
    return None

def us34(ind, fam, dict): #Mike
    ''' List all couples who were married when the older spouse was more than twice as old as the younger spouse '''
    couples = []
    for f in fam:
        temp = us34_helper(dict[f]['Married'], dic[dict[f]['Husband_ID']]['Birthday'], dic[dict[f]['Wife_ID']]['Birthday'], (dict[f]['Husband_ID'], dict[f]['Wife_ID']))
        if temp:
            couples.append(temp)
    return couples

if __name__ == '__main__':
    ged = gedcomDatabase.file()
    db = ged.replace(gedcomDatabase.EXTENSION, '.sqlite3')
    gedcomDatabase.database(ged, db)
    ind, fam, dict = gedcomDatabase.dictify(db)
    
    print(us21(ind, fam, dict))
    print(us09(ind, fam, dict))
    print(us29(ind, fam, dict))
    gedcomDatabase.tables(db)
