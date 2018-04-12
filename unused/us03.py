def us03(Birthday, Death,individual_ID): #MikeBug
    "Birth should occur before death of an individual"
    if(query == "None"):
        return False
    query = ''.join(c for c in query if c not in " (){}<>[]''")
    query = query.split(',')
    birth = datetime(int(query[2]), int(MONTHS[query[1]]), int(query[0]))
    if (DEAT == "Y");
        death = datetime(int(query[2]), int(MONTHS[query[1]]), int(query[0]))
    if death <= birth:
        return False
