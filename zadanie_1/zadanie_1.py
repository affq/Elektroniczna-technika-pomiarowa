# 1. Pierwsza zakładka: obliczenie  Ng dla długości fali od 400 do 1600 nm. Wykonanie wykresu zależności współczynników od długości fali, Wygenerowanie tabeli co 10 nm
# 2. druga zakładka: Obliczenie poprawki atmosferycznej: dane wprowadzane przez użytkownika: długośc fali w nm, temperatura sucha, temperatura mokra  (st C), ciśnienie w hPa, pomierzona długość [m]. Wyświetlanie: poprawka na km, poprawka do mierzonej długości, długość poprawiona [m]
# 3. trzecia zakładka: Obliczenie różnicy między łukiem a cięciwą [wynik w mm] dla przedziału od 1 km do 100 km. Zrobienie wykresu i wygenerowanie tabeli z wynikami (co 1 km) 

import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

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
        self.master.geometry("700x600")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.bind("<Escape>", self.close)
        self.master.bind("<Return>", self.close)
        self.master.focus_force()
        self.master.grab_set()

        self.data = self.ng0()
        self.create_table()
        self.create_canvas()

    
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

        tree.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    
    def ng0(self):
        ngs = []
        for i in range(400, 1601, 10):
            i = i/1000
            ng = 287.6155 + 4.8866/(i**2) + 0.0680/(i**4)
            ngs.append([i, ng])
        return ngs

    def create_plot(self):
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.plot([i[0] for i in self.data], [i[1] for i in self.data], color="black")
        ax.set_xlabel("Długość fali [nm]")
        ax.set_ylabel("Ng")
        ax.grid()
        return fig
    
    def create_canvas(self):
        fig = self.create_plot()
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().grid(row=0, column=1, sticky="nsew")
        canvas.draw()

    def close(self, event=None):
        self.master.destroy()


    
class Zakladka_2():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Obliczenie poprawki atmosferycznej")
        self.master.geometry("410x320")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.bind("<Escape>", self.close)
        self.master.bind("<Return>", self.close)
        self.master.focus_force()
        self.master.grab_set()

        self.add_entries()

    def add_entries(self):
        self.label1 = tk.Label(self.master, text="Długość fali [nm]:", font=(font, 12), bg="white")
        self.label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.entry1 = tk.Entry(self.master, font=(font, 12))
        self.entry1.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.label2 = tk.Label(self.master, text="Temperatura sucha [°C]:", font=(font, 12), bg="white")
        self.label2.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.entry2 = tk.Entry(self.master, font=(font, 12))
        self.entry2.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.label3 = tk.Label(self.master, text="Temperatura mokra [°C]:", font=(font, 12), bg="white")
        self.label3.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.entry3 = tk.Entry(self.master, font=(font, 12))
        self.entry3.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)

        self.label4 = tk.Label(self.master, text="Ciśnienie [hPa]:", font=(font, 12), bg="white")
        self.label4.grid(row=3, column=0, sticky="nsew", padx=10, pady=10)
        self.entry4 = tk.Entry(self.master, font=(font, 12))
        self.entry4.grid(row=3, column=1, sticky="nsew", padx=10, pady=10)

        self.label5 = tk.Label(self.master, text="Długość [m]:", font=(font, 12), bg="white")
        self.label5.grid(row=4, column=0, sticky="nsew", padx=10, pady=10)
        self.entry5 = tk.Entry(self.master, font=(font, 12))
        self.entry5.grid(row=4, column=1, sticky="nsew", padx=10, pady=10)

        self.button = tk.Button(self.master, text="Oblicz poprawkę", command=self.expand, font=(font, 12), bg="white")
        self.button.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)

    def expand(self):
        try:
            self.results = self.correction()
        except:
            messagebox.showerror("Błąd", "Wprowadź poprawne dane")
            return

        self.master.geometry("500x460")

        self.label6 = tk.Label(self.master, text="Poprawka na km [mm]:", font=(font, 12), bg="white")
        self.label6.grid(row=6, column=0, sticky="nsew", padx=10, pady=10)
        self.entry6 = tk.Entry(self.master, font=(font, 12))
        self.entry6.grid(row=6, column=1, sticky="nsew", padx=10, pady=10)
        self.entry6.insert(0, str(self.results[0]))
        self.entry6.configure(state='readonly')

        self.label7 = tk.Label(self.master, text="Poprawka do mierzonej długości [mm]:", font=(font, 12), bg="white")
        self.label7.grid(row=7, column=0, sticky="nsew", padx=10, pady=10)
        self.entry7 = tk.Entry(self.master, font=(font, 12))
        self.entry7.grid(row=7, column=1, sticky="nsew", padx=10, pady=10)
        self.entry7.insert(0, str(self.results[1]))
        self.entry7.configure(state='readonly')

        self.label8 = tk.Label(self.master, text="Długość poprawiona [m]:", font=(font, 12), bg="white")
        self.label8.grid(row=8, column=0, sticky="nsew", padx=10, pady=10)
        self.entry8 = tk.Entry(self.master, font=(font, 12))
        self.entry8.grid(row=8, column=1, sticky="nsew", padx=10, pady=10)
        self.entry8.insert(0, str(self.results[2]))
        self.entry8.configure(state='readonly')
    
    def get_data(self):
        wavelength = float(self.entry1.get())
        temperature_dry = float(self.entry2.get())
        temperature_wet = float(self.entry3.get())
        pressure = float(self.entry4.get())
        length = float(self.entry5.get())

        return wavelength, temperature_dry, temperature_wet, pressure, length
    
    def ng0(self, wavelength):
        wavelength = wavelength / 1000
        ng0 = 287.6155 + 4.8866/(wavelength**2) + 0.0680/(wavelength**4)
        return ng0
    
    def ng(self, wavelength, pressure, temperature_dry, humidity):
        celsius = temperature_dry + 273.15
        ng = self.ng0(wavelength) * 0.269578 * (pressure / celsius) - 11.27 * (humidity / celsius)
        return ng
    
    def ew(self, temperature_wet):
        ew = 6.1078 * np.exp((17.269 * temperature_wet) / (237.30 + temperature_wet))
        return ew
    
    def e(self, pressure, temperature_wet, temperature_dry, ew):
        e = ew - 0.000662 * pressure * (temperature_dry - temperature_wet)
        return e

    def correction(self):
        wavelength, temperature_dry, temperature_wet, pressure, length = self.get_data()
        ew = self.ew(temperature_wet)
        e = self.e(pressure, temperature_wet, temperature_dry, ew)
        ng = self.ng(wavelength, pressure, temperature_dry, e)
        ng0 = self.ng(wavelength, 1013.25, 15, 10.87)

        correction = ng0 - ng
        correction_to_length = correction * length / 1000000
        corrected_length = length + correction_to_length

        return "{:.2f}".format(correction), "{:.5f}".format(correction_to_length), "{:.5f}".format(corrected_length)


    def close(self, event=None):
        self.master.destroy()

class Zakladka_3():
    def __init__(self):
        return

root = tk.Tk()
app = StartScreen(root)
root.mainloop()

