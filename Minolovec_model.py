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

    def sosede(self, i, j):
        polje = self.postavi_mine()
        sosede = 0
        for vrstica in range(i-1, i+2):
            for stolpec in range(j-1, j+2):
                if (vrstica == i) and (stolpec == j): # sama sebi ni sosed
                    continue
                if ((vrstica < 0) or (vrstica > self.vrstice-1) or (stolpec < 0) or (stolpec > self.stolpci-1)):
                # smo izven matrike
                    continue
                if polje[vrstica][stolpec] == 1: # mina!
                    sosede += 1 
        return sosede
        
                    

