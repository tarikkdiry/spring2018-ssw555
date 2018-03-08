import os
import ast
import sqlite3
import gedcomDatabase
from sqlite3 import Error
from shutil import copyfile
from datetime import datetime
from prettytable import PrettyTable

MONTHS = {'JAN': '01', 'FEB': '02', 'MAR': '03', 'APR': '04', 'MAY': '05', 'JUN': '06', 'JUL': '07', 'AUG': '08', 'SEP' : '09', 'OCT': '10', 'NOV': '11', 'DEC': '12'}

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
        if us34_helper(dict[f]['Married'], dic[couple[0]]['Birthday'], dic[couple[1]]['Birthday']):
            couples.append(couple)
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
