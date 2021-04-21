import regex as re
import datetime as dt

def check_birthday(birthday):
    birthday = re.findall(r"[\w']+", birthday)

    birthday = list(map(int, birthday))

    if(len(birthday)<=1):
        return False,None

    if(len(birthday)==2):
        birthday.append(1) #If birthday don't have year, we set the year to 1

    try:
        birthday = dt.datetime(birthday[2],birthday[1],birthday[0])
    except ValueError:
        return False,None

    return True,birthday

def check_name(full_name):

    if(len(full_name)<=0):
        return False,None

    for name in full_name:
        if not (re.search('[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+', name)):
            return False,None

    return True,full_name