import bottle
import random 
import os 
import hashlib
from model import Potni_stroski, Uporabnik

uporabniki = {}
skrivnost = 'ZELO DOBRO ME ZAVARUJ'


for ime_datoteke in os.listdir('uporabniki'):
    uporabnik = Uporabnik.nalozi_porabo(os.path.join('uporabniki', ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik


def poisci_potovanje(ime_polja):
    ime_potovanja = bottle.request.forms.getunicode(ime_polja)
    moji_potni_stroski = potni_stroski_uporabnika()
    return moji_potni_stroski.poisci_potovanje(ime_potovanja)

def poisci_kategorijo(ime_polja):
    ime_kategorije = bottle.request.forms.getunicode(ime_polja)
    moji_potni_stroski = potni_stroski_uporabnika()
    return moji_potni_stroski.poisci_kategorijo(ime_kategorije)

def poisci_dan(datum_polja):
    datum_dneva = bottle.request.forms.get(datum_polja)
    moji_potni_stroski = potni_stroski_uporabnika()
    return moji_potni_stroski.poisci_dan(datum_dneva)

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return uporabniki[uporabnisko_ime]

def potni_stroski_uporabnika():
    return trenutni_uporabnik().potni_stroski

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_porabo(os.path.join('uporabniki', f'{uporabnik.uporabnisko_ime}.json'))

@bottle.get('/')
def zacetna_stran():
    bottle.redirect('/zacetna/')

@bottle.get('/zacetna/')
def zacetna():
    moji_potni_stroski = potni_stroski_uporabnika()
    return bottle.template('zacetna_stran.html', moji_potni_stroski=moji_potni_stroski)

@bottle.get('/pomoc/')
def pomoc():
    return bottle.template('pomoc.html')

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='UTF-8'))
    zasifrirano_geslo = h.hexdigest()
    if 'nov_racun' in bottle.request.forms and uporabnisko_ime not in uporabniki:
        uporabnik = Uporabnik(uporabnisko_ime, zasifrirano_geslo, Potni_stroski())
        uporabniki[uporabnisko_ime] = uporabnik
    else:
        uporabnik = uporabniki[uporabnisko_ime]
        uporabnik.preveri_geslo(zasifrirano_geslo)
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/')

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/')

@bottle.post('/dodaj-potovanje/')
def dodaj_potovanje():
    moji_potni_stroski = potni_stroski_uporabnika()
    moji_potni_stroski.novo_potovanje(bottle.request.forms.getunicode('ime'))
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/dodaj-kategorijo/')
def dodaj_kategorijo():
    moji_potni_stroski = potni_stroski_uporabnika()
    potovanje = poisci_potovanje('potovanje')
    ime = bottle.request.forms.getunicode('ime')
    moji_potni_stroski.nova_kategorija(potovanje, ime)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/dodaj-dan/')
def dodaj_dan():
    moji_potni_stroski = potni_stroski_uporabnika()
    potovanje = poisci_potovanje('potovanje')
    datum = bottle.request.forms['datum']
    moji_potni_stroski.nov_dan(potovanje, datum)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/dodaj-izdatek/')
def dodaj_izdatek():
    moji_potni_stroski = potni_stroski_uporabnika()
    potovanje = poisci_potovanje('potovanje')
    dan = poisci_dan('dan')
    lokacija = bottle.request.forms.getunicode('lokacija')
    znesek = int(bottle.request.forms['znesek'])
    kategorija = poisci_kategorijo('kategorija')
    moji_potni_stroski.nov_izdatek(potovanje, dan, lokacija, znesek, kategorija)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

@bottle.post('/odstrani-kategorijo/')
def odstrani_kategorijo():
    moji_potni_stroski = potni_stroski_uporabnika()
    kategorija = poisci_kategorijo('kategorija')
    moji_potni_stroski.odstrani_kategorijo(kategorija)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/')

bottle.run(debug=True, realoder=True)
