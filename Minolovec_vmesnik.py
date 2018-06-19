# Uporabniški vmesnik

import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import Minolovec_model as model
import time

SIRINA_KVADRATKA = 2
VISINA_KVADRATKA = 1
MINA = '●'
ZASTAVA = '?'
BARVA_GUMBA = 'gainsboro'
BARVE = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']
FONT = ('times', 10, 'bold')

class Minolovec:
    def __init__(self):
        self.okno = tk.Tk()
        self.okno.title('Minolovec')

        # Spremenljivke ##
        self.konec_igre = False
        self.zacetek_igre = False
        self.win = False
        self.minsko_polje = None
        #self.zastava = tk.PhotoImage(file='zastava.gif')
        #self.mina = tk.PhotoImage(file='bomba.gif')

        self.vrstice = None
        self.stolpci = None
        self.stevilo_min = None
        self.vrednost_casa = 0
        ## Spremenljivke ##

        ## Meni ##
        meni = tk.Menu(self.okno)
        podmeni = tk.Menu(meni, tearoff=0)
        podmeni.add_command(label='Lahka', command=self.nastavi_lahka)
        podmeni.add_command(label='Srednja', command=self.nastavi_srednja)
        podmeni.add_command(label='Težka', command=self.nastavi_tezka)
        podmeni.add_command(label='Po meri', command=self.nastavi_po_meri)
        meni.add_cascade(label='Zahtevnost', menu=podmeni)

        meni.add_command(label='Nova igra', command=self.nova_igra)
        self.okno.configure(menu=meni)
        ## Meni ##
        
        self.prikaz_casa = tk.Label(self.okno, text=str(self.vrednost_casa))
        self.prikaz_casa.pack()

        #self.okno.bind('r', self.nova_igra)

        self.nastavi_lahka()
        self.nova_igra()
        self.okno.mainloop()
    
    def nastavi_zahtevnost(self, vrstice, stolpci, mine):
        self.vrstice = vrstice
        self.stolpci = stolpci
        self.stevilo_min = mine
        self.nova_igra()
    def nastavi_lahka(self):
        self.nastavi_zahtevnost(7, 7, 7)
    def nastavi_srednja(self):
        self.nastavi_zahtevnost(14, 14, 40)
    def nastavi_tezka(self):
        self.nastavi_zahtevnost(21, 21, 120)
    def nastavi_po_meri(self):
        vrstice = simpledialog.askinteger('Vrstice', 'Izberi število vrstic.', parent=self.okno, minvalue=1, maxvalue=30)
        stolpci = simpledialog.askinteger('Stolpci', 'Izberi število stolpcev.', parent=self.okno, minvalue=1, maxvalue=30)
        stevilo_polj = vrstice * stolpci
        mine = simpledialog.askinteger('Mine', 'Izberi število min.', parent=self.okno, minvalue=1, maxvalue=stevilo_polj)
        self.nastavi_zahtevnost(vrstice, stolpci, mine)
        
        
    def nova_igra(self):
        self.polje = model.Polje(self.vrstice, self.stolpci, self.stevilo_min)
        self.matrika = self.polje.postavi_mine()
        self.vrednost_casa = 0
        self.prikaz_casa.configure(text='0')
        self.konec_igre = False
        self.zacetek_igre = False

        if self.minsko_polje is not None:
            self.minsko_polje.pack_forget()
            
        self.minsko_polje = tk.Frame(self.okno)
        self.minsko_polje.pack()

        self.gumbi = []
        for i in range(self.vrstice):
            vrstica = []
            for j in range(self.stolpci):
                gumb = tk.Button(self.minsko_polje, text=' ', height=VISINA_KVADRATKA, width=SIRINA_KVADRATKA, background=BARVA_GUMBA, command=lambda i=i, j=j: self.levi_klik(i, j))
                gumb.bind('<Button-3>', lambda e, i=i, j=j: self.desni_klik(i, j))
                gumb.grid(row=i+2, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                vrstica.append(gumb)
            self.gumbi.append(vrstica)

    def levi_klik(self, i, j):
        if not self.zacetek_igre:
            self.zacetek_igre = True
            self.osvezi_cas()
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
        if not self.zacetek_igre:
            self.zacetek_igre = True
            self.osvezi_cas()
        if self.gumbi[i][j]['text'] == ZASTAVA:
            self.gumbi[i][j]['text'] = ' '
            self.gumbi[i][j]['state'] = 'normal'
        elif self.gumbi[i][j]['text'] == ' ' and self.gumbi[i][j]['state'] == 'normal':
            self.gumbi[i][j]['text'] = ZASTAVA
            self.gumbi[i][j].configure(font=FONT)
            self.gumbi[i][j]['state'] = 'disabled'

    def pokazi_cifro(self, i, j):
        cifra = self.polje.sosede(i, j, self.matrika)
        self.gumbi[i][j].configure(relief=tk.SUNKEN, disabledforeground=BARVE[cifra], font=FONT)
        self.gumbi[i][j]['text'] = str(cifra)
        self.gumbi[i][j]['state'] = 'disabled'
        self.zmaga()

    def pokazi_mino(self, i, j):
        self.gumbi[i][j]['text'] = MINA
        self.gumbi[i][j].configure(background='red', disabledforeground='black', font=FONT)
        self.zakleni_gumbe()
        self.pokazi_vse()
        self.konec_igre = True
        tk.messagebox.showinfo('Konec Igre', 'Žal vam ni uspelo. Poskusite ponovno.', icon='warning')

    def pokazi_prazno_polje(self, i, j):
        self.gumbi[i][j]['text'] = ' '
        self.gumbi[i][j]['state'] = 'disabled'
        self.gumbi[i][j].configure(relief=tk.SUNKEN)
        self.zmaga()

    def pokazi_vse(self):
        for i in range(len(self.gumbi)):
            for j in range(len(self.gumbi[i])):
                if self.matrika[i][j] == 1 and self.gumbi[i][j]['text'] != ZASTAVA:
                    self.gumbi[i][j]['text'] = MINA
                    self.gumbi[i][j].configure(disabledforeground='black', font=FONT)
                elif self.matrika[i][j] == 1 and self.gumbi[i][j]['text'] == ZASTAVA:
                    continue
                elif self.matrika[i][j] == 0:
                    if self.polje.sosede(i, j, self.matrika) == 0:
                        self.gumbi[i][j]['text'] = ' '
                        self.gumbi[i][j]['state'] = 'disabled'
                        self.gumbi[i][j].configure(relief=tk.SUNKEN)
                    else:
                        cifra = self.polje.sosede(i, j, self.matrika)
                        self.gumbi[i][j].configure(relief=tk.SUNKEN, disabledforeground=BARVE[cifra], font=FONT)
                        self.gumbi[i][j]['text'] = str(cifra)                     

    def pokazi_zastave(self):
        for i in range(len(self.gumbi)):
            for j in range(len(self.gumbi[i])):
                if self.matrika[i][j] == 1:
                    self.gumbi[i][j]['text'] = ZASTAVA
                    self.gumbi[i][j].configure(font=FONT)

    def zakleni_gumbe(self):
            for i in range(len(self.gumbi)):
                for j in range(len(self.gumbi[i])):
                    self.gumbi[i][j]['state'] = 'disabled'        

    def zmaga(self):
        self.win = True
        for i in range(len(self.gumbi)):
            for j in range(len(self.gumbi[i])):
                if self.matrika[i][j] == 0 and (self.gumbi[i][j]['state'] == 'normal' or self.gumbi[i][j]['text'] == ZASTAVA):
                    self.win = False
        if self.win:
            self.pokazi_zastave()
            self.konec_igre = True
            tk.messagebox.showinfo('Zmaga', 'Čestitke, uspelo vam je!')
            self.zapisi_cas()
            self.zakleni_gumbe()
            
    def dodaj_sekundo(self):
        if self.zacetek_igre:
            cas = int(self.prikaz_casa.cget('text'))
            self.vrednost_casa = cas + 1
            self.prikaz_casa.configure(text=str(self.vrednost_casa))

    def osvezi_cas(self):
        if not self.konec_igre:
            self.dodaj_sekundo()
            self.okno.after(1000, self.osvezi_cas)

    def zapisi_cas(self):
        with open('rezultati.txt', 'a') as rezultati:
            print(('Minolovca s {0} vrsticami, {1} stolpci in {2} minami, vam je uspelo koncati v {3} sekundah.'.format(
                self.vrstice, self.stolpci, self.stevilo_min, self.vrednost_casa)), file=rezultati)

        
Minolovec()
