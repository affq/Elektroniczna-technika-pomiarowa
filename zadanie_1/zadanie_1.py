# 1. Pierwsza zakładka: obliczenie  Ng dla długości fali od 400 do 1600 nm. Wykonanie wykresu zależności współczynników od długości fali, Wygenerowanie tabeli co 10 nm
# 2. druga zakładka: Obliczenie poprawki atmosferycznej: dane wprowadzane przez użytkownika: długośc fali w nm, temperatura sucha, temperatura mokra  (st C), ciśnienie w hPa, pomierzona długość [m]. Wyświetlanie: poprawka na km, poprawka do mierzonej długości, długość poprawiona [m]
# 3. trzecia zakładka: Obliczenie różnicy między łukiem a cięciwą [wynik w mm] dla przedziału od 1 km do 100 km. Zrobienie wykresu i wygenerowanie tabeli z wynikami (co 1 km) 

import math
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

font = "Signika Negative"

class StartScreen:
    def __init__(self, master):
        self.master = master
        self.master.title("Zadanie 1")
        self.master.geometry("600x300")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.bind("<Escape>", self.close)
        self.master.bind("<Return>", self.close)
        self.master.focus_force()
        self.master.grab_set()

        self.label = tk.Label(self.master, text="Wybierz zakładkę:", font=(font, 12), bg="white")
        self.label.pack(pady=10)

        self.button1 = tk.Button(self.master, text="Wykres zależności współczynników od długości fali", command=self.zakladka_1, font=(font, 12), bg="white")
        self.button1.pack(pady=10)

        self.button2 = tk.Button(self.master, text="Obliczenie poprawki atmosferycznej", command=self.zakladka_2, font=(font, 12), bg="white")
        self.button2.pack(pady=10)

        self.button3 = tk.Button(self.master, text="Różnica między łukiem a cięciwą", command=self.zakladka_3, font=(font, 12), bg="white")
        self.button3.pack(pady=10)

    def close(self, event=None):
        self.master.destroy()
    
    def zakladka_1(self):
        self.master.destroy()
        Zakladka_1()
    
    def zakladka_2(self):
        self.master.destroy()
        Zakladka_2()
    
    def zakladka_3(self):
        self.master.destroy()
        Zakladka_3()

class Zakladka_1():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Wykres zależności współczynników od długości fali")
        self.master.geometry("600x300")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.bind("<Escape>", self.close)
        self.master.bind("<Return>", self.close)
        self.master.focus_force()
        self.master.grab_set()

        self.data = self.calculate_ng()
        self.create_table()
    
    def create_table(self):
        tree = ttk.Treeview(self.master)
        tree["columns"] = ("Długość fali", "Ng")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Długość fali", anchor=tk.W, width=100)
        tree.column("Ng", anchor=tk.W, width=100)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Długość fali", text="Długość fali [nm]", anchor=tk.W)
        tree.heading("Ng", text="Ng", anchor=tk.W)

        for i in range(len(self.data)):
            tree.insert("", i, text="", values=(self.data[i][0], self.data[i][1]))

        tree.grid(row=0, column=0, sticky="nsew")
    
    def calculate_ng(self):
        ngs = []
        for i in range(400, 1601, 10):
            i = i/1000
            ng = 287.6155 + 4.8866/(i**2) + 0.0680/(i**4)
            ngs.append([i, ng])
        return ngs

    def create_plot(self):
        return
    
    def close(self, event=None):
        self.master.destroy()


    
class Zakladka_2():
    def __init__(self):
        return

class Zakladka_3():
    def __init__(self):
        return

root = tk.Tk()
app = StartScreen(root)
root.mainloop()

