__author__ = 'cheikh'

from fractions import gcd
from functools import reduce

# List of basic functions
# ================================================================================
def iter_frames(img):
    try:
        i= 0
        while 1:
            img.seek(i)
            imframe = img.copy()
            if i == 0:
                palette = imframe.getpalette()
            else:
                imframe.putpalette(palette)
            yield imframe
            i += 1
    except EOFError:
        pass

# ================================================================================
def fgcd(vala,valb):
    val = gcd(vala,valb)
    factors = reduce(list.__add__, ([i, val//i] for i in range(1, int(val**0.5) + 1) if val % i == 0))
    factors.sort()
    if len(factors) > 1:
        del factors[0] # first factor is always 1

    return factors

# ================================================================================
def choose_factor(a,b):
    ## Ask user to provide a pixellization factor
    list_factor = fgcd(a,b)
    while len(list_factor) < 2:
        a -= 1
        list_factor = fgcd(a,b)

    factor = inputint('Veuillez choisir la taille de votre pixel : ', list_factor)

    return factor


#================================================================================
def inputint(text, list_choice = None, min=None,max=None,strict=False):
    test = False

    while not test:
        if list_choice:
            print(text,str(list_choice))
            try:
                ma_valeur = int(input())
                test = (ma_valeur in list_choice)
                if not test:
                    print("cette valeur n'est pas dans la liste")
            except ValueError:
                print("Ceci n'est pas une entrée valide")
            pass
        #elif min or max:
        else:
            print(text)
            try:
                ma_valeur = int(input())
                test = True
            except ValueError:
                print("Ceci n'est pas une entrée valide")
            pass

    return ma_valeur

#================================================================================
if __name__ == 'main':
    my_val = 50
    my_list = [0,2,4,6,8]

    my_test1 = inputint('choisissez où commence la bande [0 - {}]:'.format(my_val))

    print(my_list)
    my_test2 = inputint('choisissez une valeur dans la liste:',my_list)

    print(my_test1,' - ', type(my_test1))
    print(my_test2,' - ', type(my_test2))
