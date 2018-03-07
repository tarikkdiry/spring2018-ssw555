def us10(marriage_date, husband_birth, wife_birth): #MikeBug
    """List all couples who were married when the older spouse was more than twice as old as the younger spouse
"""
    if not marriage_date:
        return False
    test = True
    md = datetime(int(marriage_date[2]) - 14, int(MONTHS[marriage_date[1]]), int(marriage_date[0]))
    if(husband_birth):
        hb = datetime(int(husband_birth[2]), int(MONTHS[husband_birth[1]]), int(husband_birth[0]))
    if(wife_birth):
        wb = datetime(int(wife_birth[2]), int(MONTHS[wife_birth[1]]), int(wife_birth[0]))
    if (((wife_birth*2) >= husband_birth) || (((wife_birth) <= husband_birth*2))
        return True
