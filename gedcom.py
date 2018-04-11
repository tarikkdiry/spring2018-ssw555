import os
import ast
import sqlite3
import gedcomDatabase
import datetime as dt
import collections
from sqlite3 import Error
from shutil import copyfile
from datetime import datetime
from prettytable import PrettyTable
from _datetime import timedelta
from sqlalchemy.sql.expression import false

MONTHS = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP' : '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

def us01_helper(date):
    if not date:
        return True
    d = datetime(int(date[2]), int(MONTHS[date[1]]), int(date[0]))
    n = datetime.now()
    return d < n

def us01(ind, fam, dict): #Austin
    ''' Dates (birth, marriage, divorce, death) should not be after the current date '''
    test = True
    for i in ind:
        test *= us01_helper(dict[i]['Birthday'])
        test *= us01_helper(dict[i]['Death'])
    for f in fam:
        test *= us01_helper(dict[f]['Married'])
    return test

def us02_helper(marriage_date, individual_birth):
    if not marriage_date or not individual_birth:
        return False
    return int(marriage_date[2]) > int(individual_birth[2])

def us02(ind, fam, dict): #Oscar
    ''' Birth should occur before marriage of an individual '''
    test = True
    for f in fam:
        for i in [dict[f]['Husband_ID'], dict[f]['Wife_ID']]:
            test *= us02_helper(dict[f]['Married'], dict[i]['Birthday'])
    return test

def us03_helper(birth, death):
    if not birth:
        return False
    elif not death:
        return True
    bd = datetime(int(birth[2]), int(MONTHS[birth[1]]), int(birth[0]))
    dd = datetime(int(death[2]), int(MONTHS[death[1]]), int(death[0]))
    return bd < dd

def us03(ind, fam, dict): #Mike
    ''' Birth should occur before death of an individual '''
    test = True
    for i in ind:
        test *= us03_helper(dict[i]['Birthday'], dict[i]['Death'])
    return test

def us04_helper(divorce_date, marriage_date):
    if not marriage_date:
        return False
    if divorce_date:
        return int(divorce_date[2]) > int(marriage_date[2])
    return True

def us04(ind, fam, dict): #Austin
    ''' Marriage should occur before birth '''
    test = True
    for f in fam:
        test *= us04_helper(dict[f]['Divorced'], dict[f]['Married'])
    return test

def us05_helper(mother_death, father_death, marriage_date):
    if not marriage_date:
        return False
    elif not mother_death and not father_death:
        return True
    
    mar = datetime(int(marriage_date[2]), int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    
    if(father_death and not mother_death):
        fd = datetime(int(father_death[2]), int(MONTHS[father_death[1]]), int(father_death[0]))
        return fd > mar
    
    elif(mother_death and not father_death):
        md = datetime(int(mother_death[2]), int(MONTHS[mother_death[1]]), int(mother_death[0]))
        return md > mar
    
    fd = datetime(int(father_death[2]), int(MONTHS[father_death[1]]), int(father_death[0]))
    md = datetime(int(mother_death[2]), int(MONTHS[mother_death[1]]), int(mother_death[0]))
    return fd > mar and md > mar

def us05(ind, fam, dict): #Austin
    ''' Marriage should occur before death of either spouse '''
    test = True
    for f in fam:
        test *= us03_helper(dict[dict[f]['Wife_ID']]['Death'], dict[dict[f]['Husband_ID']]['Death'], dict[f]['Married'])
    return test

def us06_helper(death_date, divorce_date):
    if not death_date or not divorce_date:
        return True
    return int(death_date[2]) > int(divorce_date[2])

def us06(ind, fam, dict): #Austin
    ''' Divorce should occur before death '''
    test = True
    for f in fam:
        test *= us06_helper(dict[dict[f]['Husband_ID']]['Death'], dict[f]['Divorced'])
        test *= us06_helper(dict[dict[f]['Wife_ID']]['Death'], dict[f]['Divorced'])
    return test

def us07_helper(children):
    return len(children) < 15

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
    if not marriage_date or not husband_birth or not wife_birth:
        return False
    md = datetime(int(marriage_date[2]), int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    hb = datetime(int(husband_birth[2]), int(MONTHS[husband_birth[1]]), int(husband_birth[0]))
    wb = datetime(int(wife_birth[2]), int(MONTHS[wife_birth[1]]), int(wife_birth[0]))
    return md.year-hb.year >= 14 and md.year-wb.year >= 14

def us10(ind, fam, dict): #Oscar
    ''' Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old) '''
    test = True
    for f in fam:
        test *= us10_helper(dict[f]['Married'], dict[dict[f]['Husband_ID']]['Birthday'], dict[dict[f]['Wife_ID']]['Birthday'])
    return test

def us12(ind, fam, dict):
    """Mother should be less than 60 years older than her children
     and father should be less than 80 years older than his children"""
    '''' NOT SURE IF THIS WORKS FOR OUR DICTIONARY'''
    test = True
    for f in fam:
        children = dict[f]['Children']
        fatherID = dict[f]['Husband_ID'];
        motherID = dict[f]['Wife_ID'];
        fatherBirth = dict[fatherID]['Birthday'];
        motherBirth = dict[motherID]['Birthday'];
        for c in children:
            test *= us12_helper(fatherBirth, motherBirth, dict[c]['Birthday']);
    return test
 
def us12_helper(fatherBirth, motherBirth, childBirthday):
    if not fatherBirth or not motherBirth or not childBirthday:
        return False
    fb = datetime(int(fatherBirth[2]), int(MONTHS[fatherBirth[1]]), int(fatherBirth[0]))
    mb = datetime(int(motherBirth[2]), int(MONTHS[motherBirth[1]]), int(motherBirth[0]))
    cb = datetime(int(childBirthday[2]), int(MONTHS[childBirthday[1]]), int(childBirthday[0]))
    motherCompare = True
    if cb.year-mb.year > 60:
        motherCompare = False
    elif cb.year-mb.year == 60:
        if mb.month < cb.month:
            motherCompare = False
        elif mb.month == cb.month:
            if mb.day <= cb.day:
                motherCompare = False
    fatherCompare = True
    if cb.year-fb.year > 80:
        fatherCompare = False
    elif cb.year-fb.year == 80:
        if fb.month < cb.month:
            fatherCompare = False
        elif fb.month == cb.month:
            if fb.day <= cb.day:
                fatherCompare = False
    return fatherCompare and motherCompare

def us14(ind, fam, dict):
    "No more than five siblings should be born at the same time"
    ""
    test = True
    birthdays = []
    for f in fam:
        children = dict[f]['Children']
    for c in children:
        birthdays += dict[c]['Birthday']
    for b in birthdays:
        test *= us14_helper(birthdays);
    return test

def us14_helper(birthdays):
    if not birthdays:
        return False
    counter = collections.Counter(birthdays)
    for c in counter:
        if c > "5":
            return False
    return True;

def us15_helper(children):
    return (len(children)) < 15;

def us15(ind, fam, dict):
    "There should be fewer than 15 siblings in a family"
    test = True
    for f in fam:
        test *= us15_helper(dict[f]['Children'])
    return test

def us16_helper(fatherLastName, childLastName):
    return fatherLastName == childLastName;

def us16(ind, fam, dict):
    "There should be fewer than 15 siblings in a family"
    '''' NOT SURE IF THIS WORKS FOR OUR DICTIONARY'''
    test = True
    for f in fam:
        children = dict[f]['Children']
        fatherLastName = dict[f]['Husband_Name'][1];
        for c in children:
            test *= us16_helper(fatherLastName, dict[c]['Name'][1]);
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

def us22_helper(ind, fam):
    for i in ind:
        if not 'I' in i.upper():
            return False
    for f in fam:
        if not 'F' in f.upper():
            return False
    return len(ind) == len(set(ind)) and len(fam) == len(set(fam))

def us22(ind, fam, dict): #Tarik
    ''' Unique Individual and Family IDs '''
    return us22_helper(ind, fam)

def us23_helper(name, birthday):
    return name[0]+' '+name[1]+' : '+birthday[0]+' '+birthday[1]+' '+birthday[2]

def us23(ind, fam, dict): #Austin
    ''' Unique Names and Birthdays'''
    unique = []
    for i in ind:
        unique.append(us23_helper(dict[i]['Name'], dict[i]['Birthday']))
    return len(unique) == len(set(unique))

def us26(ind, fam, dict): #Mike
    ''' Include Individual Ages '''
    test = True
    for i in ind:
        if dict[i]['Child']:
            f = dict[i]['Child']
        else:
            f = dict[i]['Spouse']
        l = []
        l.append(dict[f]['Husband_ID'])
        l.append(dict[f]['Wife_ID'])
        l.append(dict[f]['Children']) 
        test *= i in l
    return test

def us27_helper(age):
    return not not age

def us27(ind, fam, dict): #Mike
    ''' Include Individual Ages '''
    test = True
    for i in ind:
        test *= us27_helper(dict[i]['Age'])
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

def us34_helper(marriage_date, husband_birth, wife_birth):
    if not marriage_date or not (husband_birth or wife_birth):
        return False
    md = datetime(int(marriage_date[2]), int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    hb = datetime(int(husband_birth[2]), int(MONTHS[husband_birth[1]]), int(husband_birth[0]))
    wb = datetime(int(wife_birth[2]), int(MONTHS[wife_birth[1]]), int(wife_birth[0]))
    return (((md.year-wb.year)*2) >= (md.year-hb.year)) or (((md.year-wb.year) <= (md.year-hb.year)*2))

def us34(ind, fam, dict): #Mike
    ''' List all couples who were married when the older spouse was more than twice as old as the younger spouse '''
    couples = []
    for f in fam:
        couple = (dict[f]['Husband_ID'], dict[f]['Wife_ID'])
        if us34_helper(dict[f]['Married'], dict[couple[0]]['Birthday'], dict[couple[1]]['Birthday']):
            couples.append(couple)
    return couples

def us35_helper(birthday, current_date): 
    bd = datetime(int(birthday[2]), int(MONTHS[birthday[1]]), int(birthday[0]))
    cd = datetime(int(current_date[2]), int(MONTHS[current_date[1]]), int(current_date[0]))
    cd_minus_30 = (cd - timedelta(days = 30))
    return cd_minus_30 <= bd <= cd

def us35(ind, fam, dict): #Oscar
    "List all people in a GEDCOM file who were born in the last 30 days"
    born_last_30_days = []
    for i in ind:
        if us36_helper(dict[i]['Birthday'], datatime.now()): # Now datetime doesn't work
            birthday = (dict[i]['Birthday'])
            born_last_30_days.append(birthday)
    return born_last_30_days

def us36_helper(birthday, current_date): 
    dd = datetime(int(birthday[2]), int(MONTHS[birthday[1]]), int(birthday[0]))
    cd = datetime(int(current_date[2]), int(MONTHS[current_date[1]]), int(current_date[0]))
    cd_minus_30 = (cd - timedelta(days = 30))
    return cd_minus_30 <= dd <= cd

def us36(ind, fam, dict): #Oscar
    "List all people in a GEDCOM file who died in the last 30 days"
    died_last_30_days = []
    for i in ind:
        if (dict[i]['Death'] == "null"):
            pass
        elif (us36_helper(dict[i]['Death'], datatime.now())): # Now datetime doesn't work
            death = (dict[i]['Death'])
            died_last_30_days.append(death)
    return died_last_30_days

def us36_helper(birthday, current_date): 
    dd = datetime(int(birthday[2]), int(MONTHS[birthday[1]]), int(birthday[0]))
    cd = datetime(int(current_date[2]), int(MONTHS[current_date[1]]), int(current_date[0]))
    cd_minus_30 = (cd - timedelta(days = 30))
    return cd_minus_30 <= dd <= cd

def us36(ind, fam, dict): #Oscar
    "List all people in a GEDCOM file who died in the last 30 days"
    died_last_30_days = []
    for i in ind:
        if (dict[i]['Death'] == "null"):
            pass
        elif (us36_helper(dict[i]['Death'], datatime.now())): # Now datetime doesn't work
            death = (dict[i]['Death'])
            died_last_30_days.append(death)
    return died_last_30_days

def us38_helper(birthday, current_date): 
    bd = datetime(int(birthday[2]), int(MONTHS[birthday[1]]), int(birthday[0]))
    cd = datetime(int(current_date[2]), int(MONTHS[current_date[1]]), int(current_date[0]))
    cd_plus_30 = (cd + timedelta(days = 30))
    return cd <= bd <= cd_plus_30

def us38(ind, fam, dict): #Oscar
    "List all living people in a GEDCOM file whose birthdays occur in the next 30 days"
    upcoming_birthday = []
    for i in ind:
        if us38_helper(dict[i]['Birthday'], datatime.now()): # Now datetime doesn't work
            birthday = (dict[i]['Birthday'])
            upcoming_birthday.append(birthday)
    return upcoming_birthday

def us42_helper(date): #Oscar
    if (date == "null"):
        return True
    try :
        dt.datetime(int(date[2]), int(MONTHS[date[1]]), int(date[0]))
    except ValueError :
        return False
    return True

def us42(ind, fam, dict):
    "All dates should be legitimate dates for the months specified (e.g., 2/30/2015 is not legitimate)"
    test = True
    for f in fam:
        test *= us42_helper(dict[f]['Married'])
    for i in ind:
        test *= us42_helpeer(dict['Birthday'])
        test *= us42_helpeer(dict['Death'])
    return test

if __name__ == '__main__':
    ged = gedcomDatabase.file()
    db = ged.replace(gedcomDatabase.EXTENSION, '.sqlite3')
    gedcomDatabase.database(ged, db)
    ind, fam, dict = gedcomDatabase.dictify(db)
    
    print(us21(ind, fam, dict))
    print(us09(ind, fam, dict))
    print(us29(ind, fam, dict))
    
    gedcomDatabase.tables(db)
