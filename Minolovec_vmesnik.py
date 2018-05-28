# Uporabniški vmesnik

import tkinter as tk
from tkinter import messagebox
import Minolovec_model as model
import time

VRSTICE = 15
STOLPCI = 15
STEVILO_MIN = 60
SIRINA_KVADRATKA = 2
VISINA_KVADRATKA = 1
MINA = '*'
ZASTAVA = '?'
BARVA_GUMBA = '#D3D3D3'
BARVE = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']


class Minolovec:
    def __init__(self):
        okno = tk.Tk()
        okno.title('Minolovec')
        
        self.cas = 0
        self.konec_igre = False

        self.gumbi = []
        for i in range(VRSTICE):
            vrstica = []
            for j in range(STOLPCI):
                gumb = tk.Button(okno, text=' ', width=SIRINA_KVADRATKA, command=lambda i=i, j=j: self.levi_klik(i, j))
                gumb.bind('<Button-3>', lambda e, i=i, j=j: self.desni_klik(i, j))
                gumb.grid(row=i+2, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                vrstica.append(gumb)
            self.gumbi.append(vrstica)
            
        self.nova_igra()
        
        cas = tk.Label(okno, text=str(self.cas))
        restart = tk.Button(okno, text='Restart', command=self.nova_igra)
        cas.grid(row=1, column=STOLPCI // 2)
        restart.grid(row=0, column=0, columnspan=STOLPCI, sticky=tk.N+tk.W+tk.S+tk.E)
        
        okno.mainloop()
    
        
    def nova_igra(self):
        self.polje = model.Polje(VRSTICE, STOLPCI, STEVILO_MIN)
        self.matrika = self.polje.postavi_mine()
        self.konec_igre = False

        for vrstica in range(len(self.gumbi)):
            for stolpec in range(len(self.gumbi[vrstica])):
                self.gumbi[vrstica][stolpec].config(relief=tk.RAISED)
                self.gumbi[vrstica][stolpec]['state'] = 'normal'
                self.gumbi[vrstica][stolpec]['text'] = ' '
                self.gumbi[vrstica][stolpec].config(background=BARVA_GUMBA)


    def osvezi_cas(self):
        self.cas += 1
        self.cas.after(1000, self.osvezi_cas)
        return self.cas

    def levi_klik(self, i, j):
        if self.konec_igre:
            return None
        elif self.matrika[i][j] == 1:
            self.gumbi[i][j]['text'] = MINA
            self.gumbi[i][j].config(background='red', disabledforeground='black')
            self.konec_igre = True
            tk.messagebox.showinfo('Game Over', 'You have lost.')
            #pokazi vse mine
            for _i in range(0, VRSTICE):
                    for _j in range(STOLPCI):
                        if self.matrika[_i][_j] == 1:
                            self.gumbi[_i][_j]['text'] = MINA

        elif self.polje.sosede(i, j, self.matrika) == 0:
            self.gumbi[i][j]['text'] = ' '
            #sedaj še za vsa polja, ki nimajo sosed
            self.auto_klik(i, j)
            self.gumbi[i][j]['state'] = 'disabled'
            self.gumbi[i][j].config(relief=tk.SUNKEN)
            self.zmaga()
       
        else: #self.polje[i][j] == cifra
            cifra = self.polje.sosede(i, j, self.matrika)
            self.gumbi[i][j]['text'] = str(cifra)
            self.gumbi[i][j].config(disabledforeground=BARVE[cifra])
            self.gumbi[i][j]['state'] = 'disabled'
            self.zmaga()
       
    def auto_klik(self, i, j):
        if self.gumbi[i][j]['state'] == 'disabled':
            return None
        elif self.polje.sosede(i, j, self.matrika) == 0:
            self.gumbi[i][j]['text'] = ' '
            self.gumbi[i][j].config(relief=tk.SUNKEN)
            self.gumbi[i][j]['state'] = 'disabled'
            for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                            if (x == i) and (y == j):
                                continue
                            elif (x < 0) or (x > VRSTICE-1) or (y < 0) or (y > STOLPCI-1):
                                continue
                            else:
                                self.auto_klik(x, y)
        else: #self.polje[i][j] == cifra
            cifra = self.polje.sosede(i, j, self.matrika)
            self.gumbi[i][j]['text'] = str(cifra)
            self.gumbi[i][j].config(disabledforeground=BARVE[cifra])
            self.gumbi[i][j]['state'] = 'disabled'

    def desni_klik(self, i, j):
        if self.konec_igre:
           return None
        elif self.gumbi[i][j]['text'] == ZASTAVA:
            self.gumbi[i][j]['text'] = ' '
            self.gumbi[i][j]['state'] = 'normal'
        elif self.gumbi[i][j]['text'] == ' ' and self.gumbi[i][j]['state'] == 'normal':
            self.gumbi[i][j]['text'] = ZASTAVA
            self.gumbi[i][j]['state'] = 'disabled'

    def zmaga(self):
        win = True
        for i in range(0, VRSTICE):
            for j in range(0, STOLPCI):
                if self.matrika[i][j] != 1 and self.gumbi[i][j]['state'] == 'normal':
                    win = False
        if win:
            tk.messagebox.showinfo('Game Over', 'You have won.')

        

Minolovec()
