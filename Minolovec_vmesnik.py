# Uporabniški vmesnik

import tkinter as tk
from tkinter import messagebox
import Minolovec_model as model
import time

VRSTICE = 15
STOLPCI = 15
STEVILO_MIN = 30
SIRINA_KVADRATKA = 2
VISINA_KVADRATKA = 1
MINA = '●'
ZASTAVA = '?'
BARVA_GUMBA = '#D3D3D3'
BARVE = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']


class Minolovec:
    def __init__(self):
        okno = tk.Tk()
        okno.title('Minolovec')
        
        self.konec_igre = False
        self.prvi_klik = False

        self.vrstice = VRSTICE
        self.stolpci = STOLPCI
        self.stevilo_min = STEVILO_MIN
        self.mina = MINA
        self.zastava = ZASTAVA
        self.barva_gumba = BARVA_GUMBA
        self.barve = BARVE
        self.font = ('times', 10, 'bold')
        
        ## Igralno Polje ##
        self.gumbi = []
        for i in range(self.vrstice):
            vrstica = []
            for j in range(self.stolpci):
                gumb = tk.Button(okno, text=' ', width=SIRINA_KVADRATKA, command=lambda i=i, j=j: self.levi_klik(i, j))
                gumb.bind('<Button-3>', lambda e, i=i, j=j: self.desni_klik(i, j))
                gumb.grid(row=i+2, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                vrstica.append(gumb)
            self.gumbi.append(vrstica)

        meni = tk.Menu(okno)
        okno.config(menu=meni)
        meni.add_cascade(label='Velikost polja')
            
        self.nova_igra()
        
        self.vrednost_casa = 0
        self.prikaz_casa = tk.Label(okno, text=str(self.vrednost_casa))
        self.prikaz_casa.grid(row=1, column=0, columnspan=self.stolpci)

        restart = tk.Button(okno, text='Nova igra', command=self.nova_igra)
        restart.grid(row=0, column=0, columnspan=self.stolpci, sticky=tk.N+tk.W+tk.S+tk.E)
        
        okno.mainloop()
    
        
    def nova_igra(self):
        self.polje = model.Polje(self.vrstice, self.stolpci, self.stevilo_min)
        self.matrika = self.polje.postavi_mine()
        self.konec_igre = False
        self.prvi_klik = False
        self.vrednost_casa = 0

        for i in range(len(self.gumbi)):
            for j in range(len(self.gumbi[i])):
                self.gumbi[i][j].config(relief=tk.RAISED)
                self.gumbi[i][j]['state'] = 'normal'
                self.gumbi[i][j]['text'] = ' '
                self.gumbi[i][j].config(background=self.barva_gumba)

    def levi_klik(self, i, j):
        self.prvi_klik = True
        #self.osvezi_cas()
        if self.matrika[i][j] == 1:
            self.pokazi_mino(i, j)                            
        elif self.polje.sosede(i, j, self.matrika) == 0:
            self.auto_klik(i, j)       
        else: #self.polje[i][j] == cifra
            self.pokazi_cifro(i, j)

    def auto_klik(self, i, j):
        if self.gumbi[i][j]['state'] == 'disabled':
            return None
        elif self.polje.sosede(i, j, self.matrika) == 0:
            self.pokazi_prazno_polje(i, j)
            for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                            if (x == i) and (y == j):
                                continue
                            elif (x < 0) or (x > self.vrstice-1) or (y < 0) or (y > self.stolpci-1):
                                continue
                            else:
                                self.auto_klik(x, y)
        else: #self.polje[i][j] == cifra
            self.pokazi_cifro(i, j)

    def desni_klik(self, i, j):
        self.prvi_klik = True
        #self.osvezi_cas()
        if self.konec_igre:
            return None
        elif self.gumbi[i][j]['text'] == self.zastava:
            self.gumbi[i][j]['text'] = ' '
            self.gumbi[i][j]['state'] = 'normal'
            #self.osvezi_cas()
        elif self.gumbi[i][j]['text'] == ' ' and self.gumbi[i][j]['state'] == 'normal':
            self.gumbi[i][j]['text'] = self.zastava
            self.gumbi[i][j].config(font=self.font)
            self.gumbi[i][j]['state'] = 'disabled'
            #self.osvezi_cas()

    def zmaga(self):
        win = True
        for i in range(len(self.gumbi)):
            for j in range(len(self.gumbi[i])):
                if self.matrika[i][j] != 1 and self.gumbi[i][j]['state'] == 'normal':
                    win = False
        if win:
            tk.messagebox.showinfo('Konec igre', 'Čestitke, uspelo vam je!')
            self.konec_igre = True
            self.zakleni_gumbe()

    def zakleni_gumbe(self):
            for i in range(len(self.gumbi)):
                for j in range(len(self.gumbi[i])):
                    self.gumbi[i][j]['state'] = 'disabled'        

    def pokazi_cifro(self, i, j):
        cifra = self.polje.sosede(i, j, self.matrika)
        self.gumbi[i][j].config(relief=tk.SUNKEN, disabledforeground=self.barve[cifra], font=self.font)
        self.gumbi[i][j]['text'] = str(cifra)
        self.gumbi[i][j]['state'] = 'disabled'
        self.zmaga()

    def pokazi_mino(self, i, j):
        self.gumbi[i][j]['text'] = self.mina
        self.gumbi[i][j].config(background='red', disabledforeground='black', font=self.font)
        self.zakleni_gumbe()
        self.pokazi_vse()
        self.konec_igre = True
        tk.messagebox.showinfo('Konec Igre', 'Žal vam ni uspelo. Poskusite ponovno.')

    def pokazi_prazno_polje(self, i, j):
        self.gumbi[i][j]['text'] = ' '
        self.gumbi[i][j]['state'] = 'disabled'
        self.gumbi[i][j].config(relief=tk.SUNKEN)
        self.zmaga()

    def pokazi_vse(self):
        for i in range(len(self.gumbi)):
            for j in range(len(self.gumbi[i])):
                if self.matrika[i][j] == 1:
                    self.gumbi[i][j]['text'] = self.mina
                    self.gumbi[i][j].config(disabledforeground='black', font=self.font)
                elif self.polje.sosede(i, j, self.matrika) == 0:
                    self.gumbi[i][j]['text'] = ' '
                    self.gumbi[i][j].config(relief=tk.SUNKEN)      
                else: #self.polje[i][j] == cifra
                    cifra = self.polje.sosede(i, j, self.matrika)
                    self.gumbi[i][j].config(relief=tk.SUNKEN, disabledforeground=self.barve[cifra], font=self.font)
                    self.gumbi[i][j]['text'] = str(cifra)                    

    def osvezi_cas(self):
        while not self.konec_igre:
            self.dodaj_sekundo()
            okno.after(1000, self.osvezi_cas)

    def dodaj_sekundo(self):
        if self.prvi_klik:
            cas = int(self.prikaz_casa.cget('text'))
            self.prikaz_casa.configure(text=str(cas + 1))
        
Minolovec()
