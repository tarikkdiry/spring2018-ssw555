from datetime import datetime
MONTHS = {"JAN": "01", "FEB": "02", "MAR": "03", "APR": "04", "MAY": "05", "JUN": "06",
          "JUL": "07", "AUG": "08", "SEP" : "09", "OCT": "10", "NOV": "11", "DEC": "12"}

def us09(mother_death, father_death, child_birth):
    ''' Child born after mother deaths and before 9 months of fathers death'''
    if not child_birth or not (mother_death and father_death):
        return False
    cb = datetime(int(child_birth[2]), int(MONTHS[child_birth[1]]), int(child_birth[0]))
    md = datetime(int(mother_death[2]), int(MONTHS[mother_death[1]]), int(mother_death[0]))
    fd = datetime(int(father_death[2]), int(MONTHS[father_death[1]]), int(father_death[0]))
    if(father_death and not mother_death):
        return ((fd.year - cb.year) * 12 + fd.month - cb.month) >= 9
    elif(mother_death and not father_death):
        return md > cb
    return md > cb and ((fd.year - cb.year) * 12 + fd.month - cb.month) >= 9