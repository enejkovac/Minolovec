# Model

import random

class Polje:
    def __init__(self, vrstice, stolpci, stevilo_min):
        self.vrstice = vrstice
        self.stolpci = stolpci
        self.stevilo_min = stevilo_min
        
    def __repr__(self):
        vrstice, stolpci, stevilo_min = self.podatki()
        return ('{}(vrstice={}, stolpci={}, stevilo min={})'.format(self.__class__.__name__,
                                                                     vrstice, stolpci, stevilo_min))

    def podatki(self):
        return self.vrstice, self.stolpci, self.stevilo_min

    def matrika(self):
        matrika = [[0 for j in range(self.stolpci)] for i in range(self.vrstice)]
        return matrika

    def postavi_mine(self):
        stevilo_min = self.stevilo_min
        matrika_z_minami = self.matrika()
        if stevilo_min > self.vrstice * self.stolpci:
            return None # ko kličeš preveri, da ni NONE
        else:
            while stevilo_min > 0:
                nakljucna_vrstica = random.randint(0, self.vrstice - 1)
                nakljucen_stolpec = random.randint(0, self.stolpci - 1)
                if matrika_z_minami[nakljucna_vrstica][nakljucen_stolpec] == 0:
                    matrika_z_minami[nakljucna_vrstica][nakljucen_stolpec] = 1
                    stevilo_min -= 1
            return matrika_z_minami
        
                    

    




#class Bomba:
#
#    #polozaj() = vrstica, stolpec
#    
#    def __init__(self, vrstica, stolpec):
#        self.vrstica = vrstica
#        self.stolpec = stolpec
#
#    def __repr__(self):
#        vrstica, stolpec = self.polozaj()
#        return '{}(vrstica={}, stolpec={})'.format(self.__class__.__name__, vrstica, stolpec)
#
#    def polozaj(self):
#        return self.vrstica, self.stolpec
#
#
#class Stevilo:
#
#    #podatki() = vrstica, stolpec, cifra
#    
#    def __init__(self, vrstica, stolpec, cifra):
#        self.vrstica = vrstica
#        self.stolpec = stolpec
#        self.cifra = cifra
#
#    def __repr__(self):
#        vrstica, stolpec, cifra = self.podatki()
#        return ('{}(vrstica={}, stolpec={}, cifra={})'.format(self.__class__.__name__,
#                                                              vrstica, stolpec, cifra))
#    def podatki(self):
#        return self.vrstica, self.stolpec, self.cifra
    
