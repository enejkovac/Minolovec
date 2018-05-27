# Uporabniški vmesnik

import tkinter as tk
import Minolovec_model as model
import time

VRSTICE = 15
STOLPCI = 15
STEVILO_MIN = 20
SIRINA_KVADRATKA = 2
VISINA_KVADRATKA = 1
BARVE = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']


class Minolovec:
    def __init__(self):
        okno = tk.Tk()
        okno.title('Minolovec')
        self.cas = 0

        #nastavimo model
        self.polje = model.Polje(VRSTICE, STOLPCI, STEVILO_MIN).postavi_mine()
        #self.gameover = tk.BooleanVar()
        #self.gameover.set(False)

    #def naredi_igro(self):
        cas = tk.Label(okno, text=str(self.cas))
        #osvezi_cas()
        cas.grid(row=1, column=STOLPCI // 2)
        tk.Button(okno, text="Restart").grid(row=0, column=0, columnspan=STOLPCI, sticky=tk.N+tk.W+tk.S+tk.E)
        #command=restart()
        self.gumbi = []
        for i in range(VRSTICE):
            vrstica = []
            for j in range(STOLPCI):
                gumb = tk.Button(okno, text=" ", width=SIRINA_KVADRATKA, command=lambda i=i, j=j: self.levi_klik(i, j))
                gumb.bind("<Button-3>", lambda e, i=i, j=j: self.desni_klik(i, j))
                gumb.grid(row=i+2, column=j, sticky=tk.N+tk.W+tk.S+tk.E)
                vrstica.append(gumb)
            self.gumbi.append(vrstica)

        okno.mainloop()

    def osvezi_cas(self):
        self.cas += 1
        self.cas.after(1000, self.osvezi_cas)
        return self.cas

    def levi_klik(self, i, j):
        #if self.gameover:
        #    return
        #gumbi[i][j]["text"] = str(self.polje.sosede(i, j))
        # kaj to sploh naredi????
        if self.polje[i][j] == 1:
            self.gumbi[i][j]["text"] = "*"
            self.gumbi[i][j].config(background='red', disabledforeground='black')
            self.gameover.set(True)
            tk.messagebox.showinfo("Game Over", "you have lost.")
            #pokazi vse mine
            for _i in range(0, VRSTICE):
                    for _j in range(STOLPCI):
                        if self.polje[_i][_j] == 1:
                            self.gumbi[_i][_j]["text"] = "*"

        elif self.polje.sosede(i, j) == 0:
            self.gumbi[i][j]["text"] = " "
            #sedaj še za vsa polja, ki nimajo sosed
            auto_klik(i, j)
            self.gumbi[i][j]['state'] = 'disabled'
            self.gumbi[i][j].config(relief=tk.SUNKEN)
            #checkWin()
       
        else: #self.polje[i][j] == cifra
            cifra = self.polje.sosede(i, j)
            self.gumbi[i][j]["text"] = str(cifra)
            self.gumbi[i][j].config(disabledforeground=BARVE[cifra])
            self.gumbi[i][j]['state'] = 'disabled'
       
    def auto_klik(self, i, j):
        if self.gumbi[i][j]["state"] == 'disabled':
            return None
        elif self.polje.sosede(i, j) == 0:
            self.gumbi[i][j]["text"] = " "
            self.gumbi[i][j].config(relief=tk.SUNKEN)
            self.gumbi[i][j]['state'] = 'disabled'
            for x in range(i-1, i+2):
                    for y in range(j-1, j+2):
                            if (x == i) and (y == j):
                                continue
                            elif (x < 0) or (x > VRSTICE-1) or (y < 0) or (y > STOLPCI-1):
                                continue
                            else:
                                auto_klik(x, y)
        else: #self.polje[i][j] == cifra
            cifra = self.polje.sosede(i, j)
            self.gumbi[i][j]["text"] = str(cifra)
            self.gumbi[i][j].config(disabledforeground=BARVE[cifra])
            self.gumbi[i][j]['state'] = 'disabled'

    def desni_klik(self, i, j):
        #if self.gameover:
        #   return
        if self.gumbi[i][j]["text"] == "?":
            self.gumbi[i][j]["text"] = " "
            self.gumbi[i][j]["state"] = "normal"
        elif self.gumbi[i][j]["text"] == " " and self.gumbi[i][j]["state"] == "normal":
            self.gumbi[i][j]["text"] = "?"
            self.gumbi[i][j]["state"] = "disabled"

    def zmaga(self):
        win = True
        for i in range(0, VRSTICE):
            for j in range(0, STOLPCI):
                if self.polje[i][j] != 1 and self.gumbi[i][j]["state"] == "normal":
                    win = False
        if win:
            tk.messagebox.showinfo("Game Over", "You have won.")
            
    def restart(self):
        self.gameover.set(False)
        naredi_igro()
        self.polje = model.Polje(VRSTICE, STOLPCI, STEVILO_MIN).postavi_mine()

    #def cas(self):
        

Minolovec()
