import os;
import sqlite3;
from sqlite3 import Error;
from prettytable import PrettyTable
INPUT_EXTENSION = '.ged'
OUTPUT_EXTENSION = '.txt'
TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
LEVELS = {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'}
TEST_ID = True
TEST_HUSBAND_NAME = True
TEST_WIFE_NAME = True
TEST_HUSBAND_ID = True
TEST_WIFE_ID = True

def file():
    geds = []
    for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if file.endswith(INPUT_EXTENSION):
            geds.append(file)
    if(len(geds) <= 1):
        if(len(geds) == 0):
            print("NO FILE FOUND: Place "+INPUT_EXTENSION+" in same folder as python script.")
        return geds[0]
    else:
        print("Files in Local Directory: ")
        for file in geds:
            print("- " + file)
        print('\n')
        while(True):
            name = input("Enter desired GEDCOM file name: ")
            if not INPUT_EXTENSION in name:
                name += INPUT_EXTENSION
            if name in geds:
                return name
            print("FILE NAME NOT FOUND, TRY AGAIN.\n")

def read(file):
    gedcom = open(file,'r')
    output = open(file.replace(INPUT_EXTENSION, OUTPUT_EXTENSION),'w')
    for line in gedcom:
        id = None
        output.write("--> " + line.rstrip() + "\n")
        data = line.split(' ')
        level = data[0].rstrip()

        if ('INDI' or 'FAM') in line:
            id = data[1].rstrip()
            tag = data[2].rstrip()
            arguments = line.replace((level+ " " + id + " " + tag), 'id').rstrip()
        else:
            tag = data[1].rstrip()
            arguments = line.replace((level + " " + tag + " "), '').rstrip()

        if tag in TAGS and LEVELS[tag] == level:
            valid = 'Y'
        else:
            valid = 'N'

        output.write("<-- " + level + "|" + tag + "|" + valid + "|" + arguments + "\n")

    gedcom.close()
    output.close()

    output = open(file.replace(INPUT_EXTENSION, OUTPUT_EXTENSION),'r')
    print('')
    for line in output:
        print(line.rstrip())
    output.close()
    return output

# def save(file):
#    return 0

'''
So far, does not check for duplicates
'''
def Database(file):
    gedcom = open(file,'r')
    lastLevel = 0
    familyTime = False
    Name = ["NULL"]
    Gender = ["NULL"]
    Birthday = ["NULL"]
    Age = ["NULL"]
    Alive = True
    Death =  ["NULL"]
    Child = ["NULL"]
    Spouse = ["NULL"]
    dateType = ["NULL"]
    id = ["NULL"]

    ID = ["NULL"]
    Married = ["NULL"]
    Divorced = ["NULL"]
    Husband_ID = ["NULL"]
    Husband_Name = ["NULL"]
    Wife_ID = ["NULL"]
    Wife_Name = ["NULL"]
    Children = ["NULL"]

    for line in gedcom:
        data = line.split(' ')
        level = data[0].rstrip()

        # BUG: need a way to start an unload without missing data
        if (level == "0" and lastLevel == "1" and Gender != ["NULL"] and familyTime == False):
            if Alive == False:
                Age = int(Death[2]) - int(Birthday[2])
            elif (Birthday != ["NULL"]):
                Age = 2018 - int(Birthday[2])

            db = sqlite3.connect("database.sqlite3")
            cursor = db.cursor()
            cursor.execute('''INSERT INTO Individuals(Name,Gender,Birthday,Age,Alive,Death,Child,Spouse,ID)
                  VALUES(?,?,?,?,?,?,?,?,?);''', (str(Name), str(Gender), str(Birthday), str(Age), str(Alive), str(Death), str(Child), str(Spouse), str(id)))


            db.commit()
            db.close()
            Alive = True
            Birthday = ["NULL"]
            Death = ["NULL"]
            Child = ["NULL"]
        if (level == "0"):
            if ('FAM') in line:
                familyTime = True

        if (familyTime == False):
#         #this is for individuals only, must make different one for fam
            if ('INDI') in line:
                id = [data[1].rstrip()]
            if ('FAMS') in line:
                Spouse = data[2].rstrip()
            if ('FAMC') in line:
                if (Child == ["NULL"]):
                    Child = data[2].rstrip()
                else:
                    Child = Child + data[2].rstrip()
            if ('NAME') in line:
                Name = data[2:]
                if (len(data[2:]) > 1):
                    Name = [Name[0]] + [Name[1].rstrip('/').rstrip('/\n').replace('/', ' ')]
            if ('SEX') in line:
                Gender = data[2].rstrip('\n')
            if dateType == 'BIRT':
                Birthday = data[2:]
                Birthday = Birthday[:2] + [Birthday[2].rstrip('\n')]
                dateType = ["NULL"]
            if dateType == 'DEAT':
                Death = data[2:]
                Death = Death[:2] + [Death[2].rstrip('\n')]
                Alive = False
                dateType = ["NULL"]
            if ('BIRT') in line:
                dateType = 'BIRT'
            if ('DEAT') in line:
                dateType = 'DEAT'

            lastLevel = level

        ### Getting the Wife and Husband Name still not working
        if (familyTime == True):
            if (level == "0" and lastLevel == "1" and (Husband_ID != ["NULL"] or Wife_ID != ["NULL"])):
                db = sqlite3.connect("database.sqlite3")
                cursor = db.cursor()
                cursor.execute('''SELECT Name FROM Individuals WHERE ID =?''', (Husband_ID))
                Husband_Name = cursor.fetchall()
                #This print statement is used for testing if it is correctly pulling from the database
                #print (cursor.fetchall())

                cursor.execute('''SELECT Name FROM Individuals WHERE ID =?''', (Wife_ID))
                Wife_Name = cursor.fetchall()
                #print (cursor.fetchall())

                cursor.execute('''INSERT INTO Families(ID,Married,Divorced,Husband_ID,Husband_Name,Wife_ID,Wife_Name,Children)
                      VALUES(?,?,?,?,?,?,?,?);''', (str(ID), str(Married), str(Divorced), str(Husband_ID), str(Husband_Name), str(Wife_ID), str(Wife_Name), str(Children)))

                db.commit()
                db.close()
                ID = ["NULL"]
                Married = ["NULL"]
                Divorced = ["NULL"]
                Husband_ID = ["NULL"]
                Husband_Name = ["NULL"]
                Wife_ID = ["NULL"]
                Wife_Name = ["NULL"]
                Children = ["NULL"]
            if ('FAM') in line:
                ID = [data[1].rstrip()]
            if ('HUSB') in line:
                Husband_ID = [data[2].rstrip()]
            if ('WIFE') in line:
                Wife_ID = [data[2].rstrip()]
            if ('CHIL') in line:
                #put children in one array i guess (fix afterwards)
                if (Children == ["NULL"]):
                    Children = [data[2].rstrip()]
                else:
                    Children = Children + [data[2].rstrip()]
            if dateType == 'MARR':
                Married = data[2:]
                Married = Married[:2] + [Married[2].rstrip('\n')]
                dateType = ["NULL"]
            if ('MARR') in line:
                dateType = 'MARR'

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

#TESTING
def TAGS_SIZE(TAGS):
    if len(TAGS) != 17:
        return False
    return True

def LEVELS_SIZE(LEVELS):
    if len(LEVELS) != 17:
        return False
    return True

def uniqueID():
    if TEST_ID == True:
        return True
    return False

def uniqueHusbandID():
    if TEST_HUSBAND_ID == True:
        return True
    return False

def uniqueWifeID():
    if TEST_WIFE_ID == True:
        return True
    return False

def uniqueHusbandName():
    if TEST_HUSBAND_NAME == True:
        return True
    return False

def uniqueWifeName():
    if TEST_WIFE_NAME == True:
        return True
    return False


#END TESTING

def printTable(database):

    connection = sqlite3.connect('database.sqlite3')
    cursor = connection.cursor()
    print("Gedcom Data - Individuals:")
    print('-'*40)

    x = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
    #x.set_field_align("ID", "l")
    #x.set_padding_width(1)

    cursor.execute('SELECT * from Individuals')
    row = cursor.fetchone()
    while row is not None:
        x.add_row(row)
        row = cursor.fetchone()

    print(x)
    print("=" * 40)
    print("Gedcom Data - Families:")
    print('-'*40)

    x = PrettyTable(['ID', 'Married', 'Divorced', 'Husband_ID', 'Husband_Name', 'Wife_ID', 'Wife_Name', 'Children'])
    #x.set_field_align("ID", "l")
    #x.set_padding_width(1)

    cursor.execute('SELECT * from Families')
    row = cursor.fetchone()
    while row is not None:
        x.add_row(row)
        row = cursor.fetchone()

    print(x)
    cursor.close()
if __name__ == '__main__':
    #read(file())
    Database("sample_arocha.ged")
    printTable('database.sqlite3')
