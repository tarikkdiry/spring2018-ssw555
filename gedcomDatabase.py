import os
import sqlite3
from sqlite3 import Error
from shutil import copyfile
from datetime import datetime
from prettytable import PrettyTable

LEVELS = {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'}
TAGS = LEVELS.keys()
EXTENSION = '.ged'

def file():
    geds = []
    for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if file.endswith(EXTENSION):
            geds.append(file)
    if(len(geds) <= 1):
        if(len(geds) == 0):
            print("NO FILE FOUND: Place "+EXTENSION+" in same folder as python script.")
        return geds[0]
    else:
        print("Files in Local Directory: ")
        for file in geds:
            print("- " + file)
        print('\n')
        while(True):
            name = input("Enter desired GEDCOM file name: ")
            if not EXTENSION in name:
                name += EXTENSION
            if name in geds:
                return name
            print("FILE NAME NOT FOUND, TRY AGAIN.\n")

def read(file):
    gedcom = open(file,'r')
    output = open(file.replace(EXTENSION, '.txt'),'w')
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
        
        str = "<-- " + level + "|" + tag + "|" + valid + "|" + arguments + "\n"
        
        output.write(str)
        print(str.rstrip())

    gedcom.close()
    output.close()
    return output

def tables(database):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    
    print("\nGedcom Data - Individuals:\n")
    
    table = PrettyTable(["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"])
    cursor.execute('SELECT * from Individuals')
    row = cursor.fetchone()
    while row is not None:
        table.add_row(row)
        row = cursor.fetchone()
        
    print(table)
    print("\nGedcom Data - Families:\n")
    
    table = PrettyTable(['ID', 'Married', 'Divorced', 'Husband_ID', 'Husband_Name', 'Wife_ID', 'Wife_Name', 'Children'])
    cursor.execute('SELECT * from Families')
    row = cursor.fetchone()
    while row is not None:
        table.add_row(row)
        row = cursor.fetchone()

    print(table)
    cursor.close()

def database(gedcom, database):
    file = open(gedcom,'r')
    lastLevel = 0
    familyTime, Divorced, Alive = False, False, True
    id, Name, Gender, Birthday, Age, Death, Child, Spouse, ID, Married, Husband_ID, Husband_Name, Wife_ID, Children, Wife_Name, dateType = ('None',)*16
    
    try:
        os.remove(os.getcwd()+'/'+database)
    except:
        pass
    
    if not os.path.exists(database):
        copyfile(os.getcwd()+"/template.sqlite3", os.getcwd()+'/'+database)
    
    for line in file:
        data = line.split(' ')
        level = data[0].rstrip()

        if (level == "0" and lastLevel == "1" and Gender != 'None' and familyTime == False):
            if Alive == False:
                Age = int(Death[2]) - int(Birthday[2])
            elif (Birthday != 'None'):
                Age = datetime.now().year - int(Birthday[2])
            db = sqlite3.connect(database)
            cursor = db.cursor()
            cursor.execute('''INSERT INTO Individuals(Name,Gender,Birthday,Age,Alive,Death,Child,Spouse,ID)
                  VALUES(?,?,?,?,?,?,?,?,?);''', (str(Name), str(Gender), str(Birthday), str(Age), str(Alive), str(Death), str(Child), str(Spouse), str(id)))
            db.commit()
            db.close()
            Alive = True
            Birthday, Death, Child = ('None',)*3
            
        if (level == "0") and ('FAM') in line:
            familyTime = True

        if (not familyTime):
#         #this is for individuals only, must make different one for fam
            if ('INDI') in line:
                id = data[1].rstrip().replace('@', '')
            if ('FAMS') in line:
                Spouse = data[2].rstrip().replace('@', '')    
            if ('FAMC') in line:
                if (Child == 'None'):
                    Child = data[2].rstrip().replace('@', '')
                else:
                    Child = Child + data[2].rstrip().replace('@', '')
            if ('NAME') in line:
                Name = data[2:]
                if (len(data[2:]) > 1):
                    Name = [Name[0]] + [Name[1].rstrip('/').rstrip('/\n').replace('/', ' ')]
            if ('SEX') in line:
                Gender = data[2].rstrip('\n')
            if dateType == 'BIRT':
                Birthday = data[2:]
                Birthday = Birthday[:2] + [Birthday[2].rstrip('\n')]
                dateType = 'None'
            if dateType == 'DEAT':
                Death = data[2:]
                Death = Death[:2] + [Death[2].rstrip('\n')]
                Alive = False
                dateType = 'None'
            if ('BIRT') in line:
                dateType = 'BIRT'
            if ('DEAT') in line:
                dateType = 'DEAT'
            lastLevel = level
            
        if (familyTime):
            if (level == "0" and lastLevel == "1" and (Husband_ID != 'None' or Wife_ID != 'None')):
                db = sqlite3.connect(database)
                cursor = db.cursor()
                cursor.execute("SELECT Name FROM Individuals WHERE ID = '"+Wife_ID+"'")
                Wife_Name = cursor.fetchone()[0]
                cursor.execute("SELECT Name FROM Individuals WHERE ID = '"+Husband_ID+"'")
                Husband_Name = cursor.fetchone()[0]
                cursor.execute('''INSERT INTO Families(ID,Married,Divorced,Husband_ID,Husband_Name,Wife_ID,Wife_Name,Children)
                      VALUES(?,?,?,?,?,?,?,?);''', (str(ID), str(Married), str(Divorced), str(Husband_ID), str(Husband_Name), str(Wife_ID), str(Wife_Name), str(Children)))
                db.commit()
                db.close()
                Divorced = False;
                ID, Married, Husband_ID, Husband_Name, Wife_ID, Wife_Name, Children = ('None',)*7
            if ('FAM') in line:
                ID = data[1].rstrip().replace('@', '')
            if ('HUSB') in line:
                Husband_ID = data[2].rstrip().replace('@', '')
                Husband_Name = 'TEMP'
            if ('WIFE') in line:
                Wife_ID = data[2].rstrip().replace('@', '')
                Wife_Name = 'TEMP'
            if ('CHIL') in line:
                if (Children == 'None'):
                    Children = [data[2].rstrip().replace('@', '')]
                else:
                    Children += [data[2].rstrip().replace('@', '')]
            if dateType == 'MARR':
                Married = data[2:]
                Married = Married[:2] + [Married[2].rstrip('\n')]
                dateType = 'None'
            if ('MARR') in line:
                dateType = 'MARR'
            if ('DIV') in line:
                Divorced = True
    
def query(db, tag, table, id='None'):
    if(table not in {'Individuals', 'Families'}):
        raise ValueError
    con = sqlite3.connect(db)
    #con.row_factory = lambda c, r: dict(zip([col[0] for col in c.description], r))
    cur = con.cursor()
    if(id != 'None'):
        cur.execute("SELECT "+tag+" FROM "+table+" WHERE ID = '"+id+"'")
    else:
        cur.execute("SELECT "+tag+" FROM "+table)
    fetch = cur.fetchall()
    
    if(len(fetch) == 1 and fetch[0][0] == 'None'):
        fetch[0] = (False,)
        
    return fetch
    
def dictify(db):
    Individuals, Families = [], [];
    Dictionary = {}

    for id in query(db, 'ID', 'Families'):
        Families.append(id[0])
        
    for id in query(db, 'ID', 'Individuals'):
        Individuals.append(id[0])
    
    for id in Families:
        Dictionary[id] = {}
        try:
            Dictionary[id]['Married'] = ast.literal_eval(query(db, 'Married', 'Families', id)[0][0])
        except:
            Dictionary[id]['Married'] = query(db, 'Married', 'Families', id)[0][0]
        Dictionary[id]['Divorced'] = query(db, 'Divorced', 'Families', id)[0][0] == 'True'
        Dictionary[id]['Husband_ID'] = query(db, 'Husband_ID', 'Families', id)[0][0]
        Dictionary[id]['Wife_ID'] = query(db, 'Wife_ID', 'Families', id)[0][0]
        try:
            Dictionary[id]['Children'] = ast.literal_eval(query(db, 'Children', 'Families', id)[0][0])
        except:
            Dictionary[id]['Children'] = query(db, 'Children', 'Families', id)[0][0]
        
    for id in Individuals:
        Dictionary[id] = {}
        try:
            Dictionary[id]['Name'] = ast.literal_eval(query(db, 'Name', 'Individuals', id)[0][0])
        except:
            Dictionary[id]['Name'] = query(db, 'Name', 'Individuals', id)[0][0]
        Dictionary[id]['Gender'] = query(db, 'Gender', 'Individuals', id)[0][0]
        try:
            Dictionary[id]['Birthday'] = ast.literal_eval(query(db, 'Birthday', 'Individuals', id)[0][0])
        except:
            Dictionary[id]['Birthday'] = query(db, 'Birthday', 'Individuals', id)[0][0]
        try:
            Dictionary[id]['Age'] = int(query(db, 'Age', 'Individuals', id)[0][0])
        except:
            Dictionary[id]['Age'] = query(db, 'Age', 'Individuals', id)[0][0]
        Dictionary[id]['Alive'] = query(db, 'Alive', 'Individuals', id)[0][0] == 'True'
        try:
            Dictionary[id]['Death'] = ast.literal_eval(query(db, 'Death', 'Individuals', id)[0][0])
        except:
            Dictionary[id]['Death'] = query(db, 'Death', 'Individuals', id)[0][0]
        Dictionary[id]['Child'] = query(db, 'Child', 'Individuals', id)[0][0]
        Dictionary[id]['Spouse'] = query(db, 'Spouse', 'Individuals', id)[0][0]
        
    return (Individuals, Families, Dictionary)