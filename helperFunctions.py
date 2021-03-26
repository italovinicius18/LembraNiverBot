import regex as re


def check_birthday(birthday):

    have_year = False

    if(len(birthday)<=1):
        return False,None

    if(len(birthday)==3):
        have_year = True

    if(have_year):
        birthday = {
            'day': birthday[0],
            'month': birthday[1],
            'year': birthday[2]
        }
    else:
        birthday = {
            'day': birthday[0],
            'month': birthday[1]
        }
    
    return True,birthday

def check_name(full_name):

    if(len(full_name)<=0):
        return False,None

    for name in full_name:
        if not (re.search('[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+', name)):
            return False,None

    return True,full_name