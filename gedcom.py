import os;
INPUT_EXTENSION = '.ged'
OUTPUT_EXTENSION = '.txt'
TAGS = ['INDI', 'NAME', 'SEX', 'BIRT', 'DEAT', 'FAMC', 'FAMS', 'FAM', 'MARR', 'HUSB', 'WIFE', 'CHIL', 'DIV', 'DATE', 'HEAD', 'TRLR', 'NOTE']
LEVELS = {'INDI':'0', 'NAME':'1', 'SEX':'1', 'BIRT':'1', 'DEAT':'1', 'FAMC':'1', 'FAMS':'1', 'FAM':'0', 'MARR':'1', 'HUSB':'1', 'WIFE':'1', 'CHIL':'1', 'DIV':'1', 'DATE':'2', 'HEAD':'0', 'TRLR':'0', 'NOTE':'0'}

def file():
    geds = []
    for file in os.listdir(os.path.dirname(os.path.realpath(__file__))):
        if file.endswith(INPUT_EXTENSION):
            geds.append(file)
    if(len(geds)<=1):
        if(len(geds)==0):
            print("NO FILE FOUND: Place "+INPUT_EXTENSION+" in same folder as python script.")
        return geds[0]
    else:
        print("Files in Local Directory: ")
        for file in geds:
            print("- "+file)
        print('\n')
        while(True):
            name = input("Enter desired GEDCOM file name: ")
            if not INPUT_EXTENSION in name:
                name+=INPUT_EXTENSION
            if name in geds:
                return name
            print("FILE NAME NOT FOUND, TRY AGAIN.\n")

def read(file):
    gedcom = open(file,'r')
    output = open(file.replace(INPUT_EXTENSION, OUTPUT_EXTENSION),'w')
    for line in gedcom:
        id = None
        output.write("--> "+line.rstrip()+"\n")
        data = line.split(' ')
        level = data[0].rstrip()
        
        if ('INDI' or 'FAM') in line:
            id = data[1].rstrip()
            tag = data[2].rstrip()
            arguments = line.replace((level+" "+id+" "+tag), 'id').rstrip()
        else:
            tag = data[1].rstrip()
            arguments = line.replace((level+" "+tag+" "), '').rstrip()
        
        if tag in TAGS and LEVELS[tag] == level:
            valid = 'Y'
        else:
            valid = 'N'
        
        output.write("<-- "+level+"|"+tag+"|"+valid+"|"+arguments+"\n")
        
    gedcom.close()
    output.close()
    
    output = open(file.replace(INPUT_EXTENSION, OUTPUT_EXTENSION),'r')
    print('')
    for line in output:
        print(line.rstrip())
    output.close() 

if __name__ == '__main__':
    read(file())
