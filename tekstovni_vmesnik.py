import json
from datetime import date
from model import Potni_stroski
 
#moji_potni_stroski = Potni_stroski()

#feb2 = moji_potni_stroski.nov_dan(date(2021, 2, 2))
#feb3 = moji_potni_stroski.nov_dan(date(2021, 2, 3))
#feb5 = moji_potni_stroski.nov_dan(date(2021, 2, 5))
#mar15 = moji_potni_stroski.nov_dan(date(2021, 3, 15))
#nastanitev = moji_potni_stroski.nova_kategorija('nastanitev')
#hrana = moji_potni_stroski.nova_kategorija('hrana')
#prevoz = moji_potni_stroski.nova_kategorija('prevoz')
#aktivnost =moji_potni_stroski.nova_kategorija('aktivnost') 
#
#moji_potni_stroski.nov_izdatek(feb2, 'Bled', 30, nastanitev)
#moji_potni_stroski.nov_izdatek(feb2, 'LJ', 7, hrana)
#moji_potni_stroski.nov_izdatek(feb3, 'LJ', 14, hrana)
#moji_potni_stroski.nov_izdatek(feb5, 'Bali', 35, prevoz)
#moji_potni_stroski.nov_izdatek(mar15,'Pokljuka', 40, nastanitev)
#moji_potni_stroski.nov_izdatek(mar15, 'Bali', 20, aktivnost)

LOGO = '''
______  ____    ____  __ __    ___  _                ___  __ __  ____   ___  ____   _____   ___          __  _    ___    ___  ____   ___  ____  
|      ||    \  /    ||  |  |  /  _]| |              /  _]|  |  ||    \ /  _]|    \ / ___/  /  _]        |  |/ ]  /  _]  /  _]|    \ /  _]|    \ 
|      ||  D  )|  o  ||  |  | /  [_ | |             /  [_ |  |  ||  o  )  [_ |  _  (   \_  /  [_         |  ' /  /  [_  /  [_ |  o  )  [_ |  D  )
|_|  |_||    / |     ||  |  ||    _]| |___         |    _]|_   _||   _/    _]|  |  |\__  ||    _]        |    \ |    _]|    _]|   _/    _]|    / 
  |  |  |    \ |  _  ||  :  ||   [_ |     |        |   [_ |     ||  | |   [_ |  |  |/  \ ||   [_         |     \|   [_ |   [_ |  | |   [_ |    \ 
  |  |  |  .  \|  |  | \   / |     ||     |        |     ||  |  ||  | |     ||  |  |\    ||     |        |  .  ||     ||     ||  | |     ||  .  \
  |__|  |__|\_||__|__|  \_/  |_____||_____|        |_____||__|__||__| |_____||__|__| \___||_____|        |__|\_||_____||_____||__| |_____||__|\_|
                                                                                                                                                 
'''
DATOTEKA_S_PORABO = 'poraba1.json' 

try:
    moji_potni_stroski = Potni_stroski.nalozi_porabo(DATOTEKA_S_PORABO)
except FileNotFoundError:
    moji_potni_stroski = Potni_stroski()

def krepko(niz):
    return f'\033[1m{niz}\033[0m'

def napaka(niz):
    return f'\033[1;91m{niz}\033[0m'

def uspeh(niz):
    return f'\033[1;94m{niz}\033[0m'

def prikaz_zneska(ime, stanje):
    if stanje > 0:
        return f'{ime}: {uspeh(stanje)} €'
    else:
        return f'{ime}: 0 €'

def prikaz_potovanja(potovanje):
    return prikaz_zneska(potovanje.ime, potovanje.celotna_poraba())

def prikaz_dneva(dan):
    return prikaz_zneska(dan.datum, dan.dnevna_poraba())

def prikaz_kategorije(kategorija):
    return prikaz_zneska(kategorija.ime, kategorija.kategoricna_poraba())

def vnesi_stevilo(pozdrav):
    while True: 
        try:
            stevilo = input(pozdrav)
            return int(stevilo)
        except ValueError:
            print(napaka(f'Prosim vnesite stevilo'))
            

#def check_month(vnos):
#    while True:
#        try:
#            month = input(vnos)
#        if 1 <= int(month) <= 12 :
#            return int(month)
#        else:
#            print(f'Vnesi število med 1 in 12')

#def število_dni(y, m):
#      leap = 0
#      if y% 400 == 0:
#         leap = 1
#      elif y % 100 == 0:
#         leap = 0
#      elif y% 4 == 0:
#         leap = 1
#      if m==2:
#         return 28 + leap
#      list = [1,3,5,7,8,10,12]
#      if m in list:
#         return 31
#      return 30
#
#def preveri(vnos1):
#    while True:
#        if vnos1 <= število_dni():
#            return vnos1
#        else:
#            print('ERROR: Dan ne obstaja. Vnesite pravilen dan!')


def izberi(seznam):
    for indeks, (oznaka,_) in enumerate(seznam, 1):
        print(f'{indeks}) {oznaka}')
    while True:
        izbira = vnesi_stevilo('> ')
        if 1 <= izbira <= len(seznam):
            _, element = seznam[izbira - 1]
            return element
        else:
            print(napaka(f'Izberi število med 1 in {len(seznam)}'))

def izberi_kategorijo(kategorije):
    return izberi([(prikaz_kategorije(kategorija), kategorija) for kategorija in kategorije])

def izberi_dan(dnevi):
    return izberi([(prikaz_dneva(dan), dan) for dan in dnevi])

def izberi_potovanje(potovanja):
    return izberi([(prikaz_potovanja(potovanje), potovanje) for potovanje in potovanja])



def glavni_meni():
    print(krepko(LOGO))
    print(krepko('Pozdravljeni v TRAVEL EXPENSE KEEPER'))
    print('Za izhod pritisnite Ctrl-C.')
    while True:
        try:
            print(80 * '=')
            #povzetek_porabe()
            print()
            print(krepko('Kaj bi radi naredili?'))
            moznosti = [
                ('dodal potovanje', dodaj_potovanje),
                ('dodal kategorijo', dodaj_kategorijo),
                ('odstranil kategorijo', odstrani_kategorijo),
                ('dodal dan', dodaj_dan),
                ('dodal izdatek', dodaj_izdatek),
                ('pogledal stanje', poglej_stanje)
            ]     
            izbira = izberi(moznosti)
            print(80 * '-')
            izbira()
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...\
            ')
            moji_potni_stroski.shrani_porabo(DATOTEKA_S_PORABO)
        except ValueError as e:
            print(napaka(e.args[0]))
        except KeyboardInterrupt:
            print()
            print('Nasvidenje!')
            return

#def povzetek_porabe():
#    for kategorija in moji_potni_stroski.kategorije:
#        poraba_kategorije = kategorija.kategoricna_poraba()
def dodaj_potovanje():
    ime_potovanja = input('Vnesi ime potovanja> ')
    moji_potni_stroski.novo_potovanje(ime_potovanja)
    print(uspeh('Potovanje je uspešno dodano!'))

def dodaj_kategorijo():
    print('Potovanje:')
    potovanje = izberi_potovanje(moji_potni_stroski.potovanja)
    ime_kategorije = input('Vnesi ime kategorije> ')
    moji_potni_stroski.nova_kategorija(potovanje, ime_kategorije)
    print(uspeh('Kategorija uspešno dodana!'))

def odstrani_kategorijo():
    print('Izberite kategorijo, ki bi jo radi izbrisali.')
    kategorija = izberi_kategorijo(moji_potni_stroski.kategorije)
    if input(f'Ste prepričani, de želite odstraniti kategorijo {kategorija.ime}? [da/NE]') == 'da':
        moji_potni_stroski.odstrani_kategorijo(kategorija)
        print(uspeh('Kategorija je bila uspešno odstranjena!'))
    else:
        print('Odstranitev kategorije je preklicana!')

def dodaj_dan():
    print('Potovanje:')
    potovanje = izberi_potovanje(moji_potni_stroski.potovanja)
    year = vnesi_stevilo('Vnesi leto> ')
    month = vnesi_stevilo('Vnesi mesec> ')
    #check_month(month)
    #št_razp_dni = število_dni(year, month)
    #print('Število razpoložljivih dni:' + str(št_razp_dni))
    day = vnesi_stevilo('Vnesi dan> ')
    datum = date(year, month, day)
    moji_potni_stroski.nov_dan(potovanje, datum)
    print(uspeh('Dan uspešno dodan!'))

def dodaj_izdatek():
    print('Potovanje:')
    potovanje = izberi_potovanje(moji_potni_stroski.potovanja)
    print('Dan:')
    dan = izberi_dan(moji_potni_stroski.dnevi)
    lokacija = input('Lokacija:> ')
    znesek = vnesi_stevilo('Znesek:> ')
    print('Kategorija:')
    kategorija = izberi_kategorijo(moji_potni_stroski.kategorije)
    moji_potni_stroski.nov_izdatek(potovanje, dan, lokacija, znesek, kategorija)
    print(uspeh('Izdatek uspešno dodan!'))

def poglej_stanje():
    print(krepko('POTOVANJA'))
    for potovanje in moji_potni_stroski.potovanja:
        print(f'- {prikaz_potovanja(potovanje)}')
    print(krepko('DNEVI:'))
    for dan in moji_potni_stroski.dnevi:
        print(f'- {prikaz_dneva(dan)}')
    print(krepko('KATEGORIJE:'))
    for kategorija in moji_potni_stroski.kategorije:
        print(f'-{prikaz_kategorije(kategorija)}')

glavni_meni()
