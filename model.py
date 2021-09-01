import json

dnevna_omejitev = 50

class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, potni_stroski):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.potni_stroski = potni_stroski

    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Napačno geslo!')

    def shrani_porabo(self, ime_datoteke):
        slovar_porabe = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'geslo': self.zasifrirano_geslo,
            'potni_stroski':self.potni_stroski.slovar_s_porabo(),
        }
        with open(ime_datoteke, 'w', encoding="UTF-8") as datoteka:
            json.dump(slovar_porabe, datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_porabo(cls, ime_datoteke):
        with open(ime_datoteke, encoding="UTF-8") as datoteka:
            slovar_porabe = json.load(datoteka)
        uporabnisko_ime = slovar_porabe['uporabnisko_ime']
        zasifrirano_geslo = slovar_porabe['geslo']
        potni_stroski = Potni_stroski.nalozi_iz_slovarja(slovar_porabe['potni_stroski'])
        return cls(uporabnisko_ime, zasifrirano_geslo, potni_stroski)

class Potni_stroski:
    def __init__(self):
        self.potovanja = []
        self._potovanja_po_imenih = {}
        self.dnevi = []
        self._dnevi_po_datumih = {}
        self.kategorije = []
        self._kategorije_po_imenih = {}
        self.izdatki = []

    def novo_potovanje(self, ime):
        for potovanje in self.potovanja:
            if potovanje.ime == ime:
                raise ValueError('POTOVANJE S TAKIM IMENOM ŽE OBSTAJA')
        novo = Potovanje(ime, self)
        self.potovanja.append(novo)
        self._potovanja_po_imenih[ime] = novo
        return novo

    def nov_dan(self, potovanje, datum):
        if datum in self._dnevi_po_datumih:
                raise ValueError('TA DAN ŽE OBSTAJA!')
        nov = Dan(potovanje, datum, self)
        self.dnevi.append(nov)
        self._dnevi_po_datumih[datum] = nov
        return nov

    def nova_kategorija(self, potovanje, ime):
        if ime in self._kategorije_po_imenih:
                raise ValueError('TA KATEGORIJA ŽE OBSTAJA!')
        nova = Kategorija(potovanje, ime, self)
        self.kategorije.append(nova)
        self._kategorije_po_imenih[ime] = nova
        return nova

    def odstrani_kategorijo(self, kategorija):
        self._preveri_kategorijo(kategorija)
        for znesek in kategorija.izdatki():
            if znesek.kategorija != None:
                raise ValueError('KATEGORIJE NE MORATE IZBRISATI DOKLER NI PRAZNA')
        self.kategorije.remove(kategorija)
 
    def nov_izdatek(self, potovanje, dan, lokacija, znesek, kategorija):
        self._preveri_potovanje(potovanje)
        self._preveri_dan(dan)
        self._preveri_kategorijo(kategorija)
        nov = Izdatek(potovanje, dan, lokacija, znesek, kategorija)
        self.izdatki.append(nov)
        return nov

    def poisci_potovanje(self, ime):
        return self._potovanja_po_imenih[ime]

    def poisci_dan(self, datum):
        return self._dnevi_po_datumih[datum]

    def poisci_kategorijo(self, ime):
        return self._kategorije_po_imenih[ime]

    def izdatki_potovanja(self, potovanje):
        for izdatek in self.izdatki:
            if izdatek.potovanje == potovanje:
                yield izdatek

    def izdatki_dneva(self, dan):
        for izdatek in self.izdatki:
            if izdatek.dan == dan:
                yield izdatek

    def izdatki_kategorije(self, kategorija):
        for izdatek in self.izdatki:
            if izdatek.kategorija == kategorija:
                yield izdatek

    def _preveri_potovanje(self, potovanje):
        if potovanje.potni_stroski != self:
            raise ValueError(f'Potovanje {potovanje} ne spada v tvoje potne stroške!')

    def _preveri_dan(self, dan):
        if dan.potni_stroski != self:
            raise ValueError(f'Dan {dan} ne spada v tvoje potne stroške!')

    def _preveri_kategorijo(self, kategorija):
        if kategorija is not None and kategorija.potni_stroski != self:
            raise ValueError(f'Kategorija {kategorija} ne spada v tvoje potne stroške!')

    def slovar_s_porabo(self):
        return {
            'potovanja': [{
                'ime': potovanje.ime ,
            } for potovanje in self.potovanja],
            'dnevi': [{
                'potovanje': dan.potovanje.ime,
                'datum': str(dan.datum),
            } for dan in self.dnevi],
            'kategorije': [{
                'potovanje': kategorija.potovanje.ime,
                'ime': kategorija.ime,
            } for kategorija in self.kategorije],
            'izdatki': [{
                'potovanje': izdatek.potovanje.ime,
                'dan': str(izdatek.dan.datum),
                'lokacija': izdatek.lokacija,
                'znesek': izdatek.znesek,
                'kategorija': None if izdatek.kategorija is None else izdatek.kategorija.ime,
            } for izdatek in self.izdatki],
        }

    @classmethod
    def nalozi_iz_slovarja(cls, slovar_s_porabo):
        potni_stroski = cls()
        for potovanje in slovar_s_porabo['potovanja']:
            potni_stroski.novo_potovanje(potovanje['ime'])
        for dan in slovar_s_porabo['dnevi']:
            potni_stroski.nov_dan(
                potni_stroski._potovanja_po_imenih[dan['potovanje']],
                dan['datum'])
        for kategorija in slovar_s_porabo['kategorije']:
            potni_stroski.nova_kategorija(
                potni_stroski._potovanja_po_imenih[kategorija['potovanje']],
                kategorija['ime'])
        for izdatek in slovar_s_porabo['izdatki']:
            potni_stroski.nov_izdatek(
                potni_stroski._potovanja_po_imenih[izdatek['potovanje']],
                potni_stroski._dnevi_po_datumih[izdatek['dan']],
                izdatek['lokacija'],
                izdatek['znesek'],
                potni_stroski._kategorije_po_imenih[izdatek['kategorija']],
            )
        return potni_stroski

    def shrani_porabo(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_s_porabo(), datoteka, ensure_ascii=False, indent=4)

    
    @classmethod
    def nalozi_porabo(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_s_porabo = json.load(datoteka)
        return cls.nalozi_iz_slovarja(slovar_s_porabo)

    #@staticmethod
    #def nalozi_porabo(ime_datoteke):
    #    with open(ime_datoteke) as datoteka:
    #        slovar_s_porabo = json.load(datoteka)
    #    potni_stroski = Potni_stroski()
    #    dnevi_po_datumu = {}
    #    kategorije_po_imenu = {None: None}
    #    for dan in slovar_s_porabo['dnevi']:
    #        nov_dan = potni_stroski.nov_dan(dan['datum'])
    #        dnevi_po_datumu[dan['datum']] = nov_dan
    #    for kategorija in slovar_s_porabo['kategorije']:
    #        nova_kategorija = potni_stroski.nova_kategorija(kategorija['ime'])
    #        kategorije_po_imenu[kategorija['ime']] = nova_kategorija
    #    for izdatek in slovar_s_porabo['izdatki']:
    #        potni_stroski.nov_izdatek(
    #            dnevi_po_datumu[izdatek['dan']],
    #            izdatek['lokacija'],
    #            izdatek['znesek'],
    #            kategorije_po_imenu[izdatek['kategorija']],
    #        )
    #    return potni_stroski  

    #def __str__(self):
    #    return f'Dnevi: {self.dnevi}'
#
    #def v_slovar(self):
    #    return { 
    #        'dnevi' : [dan.v_slovar() for dan in self.dnevi],
    #        'kategorije' : [kategorija.v_slovar() for kategorija in self.kategorije],
    #        'izdatki' : [izdatek.v_slovar() for izdatek in self.izdatki],
    #    }

class Potovanje:
    def __init__(self, ime, potni_stroski):
        self.ime = ime
        self.potni_stroski = potni_stroski

    def celotna_poraba(self):
        return sum([izdatek.znesek for izdatek in self.izdatki()])

    def izdatki(self):
        yield from self.potni_stroski.izdatki_potovanja(self)

class Dan:
    def __init__(self, potovanje, datum, potni_stroski):
        self.potovanje = potovanje
        self.datum = datum
        self.potni_stroski = potni_stroski
        
    
    #def __str__(self):
    #    return f'{self.datum}: {self.dnevna_poraba()}€'
#
    #def __repr__(self):
    #    return f'<Dan: {self}>'

    def dnevna_poraba(self):
        return sum([izdatek.znesek for izdatek in self.izdatki()])

    def izdatki(self):
        yield from self.potni_stroski.izdatki_dneva(self)

    #def v_slovar(self):
    #    return {
    #        'datum' : str(self.datum),
    #    }
    

class Kategorija:
    def __init__(self, potovanje,  ime, potni_stroski):
        self.potovanje = potovanje
        self.ime = ime
        self.potni_stroski = potni_stroski

    #def __str__(self):
    #    return f'{self.ime}: {self.kategoricna_poraba()}€'

    def kategoricna_poraba(self):
        return sum([izdatek.znesek for izdatek in self.izdatki()])

    def izdatki(self):
        yield from self.potni_stroski.izdatki_kategorije(self)

    #def v_slovar(self):
    #    return {
    #        'ime' : self.ime,
    #    }


class Izdatek:
    def __init__(self, potovanje, dan, lokacija, znesek, kategorija):
        self.potovanje = potovanje
        self.dan = dan
        self.lokacija = lokacija
        self.znesek = znesek
        self.kategorija = kategorija

    #def v_slovar(self):
    #    return {
    #        'dan' : str(self.dan.datum),
    #        'lokacija' : self.lokacija,
    #        'znesek' : self.znesek,
    #        'kategorija' : self.kategorija.ime,
    #    }
        
    def __lt__(self, other):
        return self.dan.datum < other.dan.datum
