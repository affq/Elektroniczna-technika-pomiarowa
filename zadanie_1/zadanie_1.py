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
        self.master.configure(background='#dfd6eb')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.focus_force()

        self.create_buttons()

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
    
    def create_buttons(self):
        self.label = tk.Label(self.master, text="Wybierz zakładkę:", font=(font, 15, 'bold'), bg="#dfd6eb")
        self.label.pack(pady=10)

        self.button1 = tk.Button(self.master, text="Wykres zależności współczynników od długości fali", command=self.zakladka_1, font=(font, 12), bg="white")
        self.button1.pack(pady=10)

        self.button2 = tk.Button(self.master, text="Obliczenie poprawki atmosferycznej", command=self.zakladka_2, font=(font, 12), bg="white")
        self.button2.pack(pady=10)

        self.button3 = tk.Button(self.master, text="Różnica między łukiem a cięciwą", command=self.zakladka_3, font=(font, 12), bg="white")
        self.button3.pack(pady=10)


class Zakladka_1():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Wykres zależności współczynników od długości fali")
        self.master.geometry("750x570")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.focus_force()

        self.data = self.ng0()
        self.create_table()
        self.create_canvas()
        self.section_buttons()

    
    def create_table(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(font, 10, 'bold'))

        tree = ttk.Treeview(self.master, style="Treeview")
        tree["columns"] = ("Długość fali", "Ng")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Długość fali", anchor=tk.W, width=120)
        tree.column("Ng", anchor=tk.W, width=80)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Długość fali", text="Długość fali [nm]", anchor=tk.W)
        tree.heading("Ng", text="Ng", anchor=tk.W)

        for i in range(len(self.data)):
            if i % 2 == 0:
                tree.insert("", i, text="", values=(int(self.data[i][0] * 1000), "{:.2f}".format(self.data[i][1])), tags=('evenrow',))
            else:
                tree.insert("", i, text="", values=(int(self.data[i][0] * 1000), "{:.2f}".format(self.data[i][1])))

        tree.tag_configure('evenrow', background='#dfd6eb')

        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=tree.yview)
        scrollbar.place(x=204, y=75, height=460)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.place(x=20, y=50, height=500)

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
        ax.plot([i[0]*1000 for i in self.data], [i[1] for i in self.data], color="#402f60")
        ax.set_xlabel("Długość fali [nm]")
        ax.set_ylabel("Ng")
        ax.grid(color="#dfd6eb")\

        ax.title.set_text("Zależność wartości Ng od długości fali")

        ax.tick_params(axis='x', colors='#402f60')
        ax.tick_params(axis='y', colors='#402f60')
        return fig
    
    def create_canvas(self):
        fig = self.create_plot()
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().place(x=250, y=20)
        canvas.draw()

    def close(self, event=None):
        self.master.destroy()

    # dodaj na samej górze 3 przyciski oznaczające konkretne zakładki, wyróżnij ten, który jest aktualnie wybrany
    def section_buttons(self):
        self.button1 = tk.Button(self.master, text="Zakładka 1", font=(font, 12, 'bold'), bg="#dfd6eb")
        self.button1.place(x=0, y=0, width=100, height=30)
        self.button1.configure(state='disabled')
        self.button1.config(relief=tk.SUNKEN)

        self.button2 = tk.Button(self.master, text="Zakładka 2", command=self.zakladka_2, font=(font, 12), bg="white")
        self.button2.place(x=100, y=0, width=100, height=30)

        self.button3 = tk.Button(self.master, text="Zakładka 3", command=self.zakladka_3, font=(font, 12), bg="white")
        self.button3.place(x=200, y=0, width=100, height=30)
    
    def zakladka_2(self):
        self.master.destroy()
        Zakladka_2()
    
    def zakladka_3(self):
        self.master.destroy()
        Zakladka_3()
    
class Zakladka_2():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Obliczenie poprawki atmosferycznej")
        self.master.geometry("420x300")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.focus_force()

        self.section_buttons()
        self.add_entries()

    def add_entries(self):
        self.label1 = tk.Label(self.master, text="Długość fali [nm]:", font=(font, 12), bg="white")
        self.label1.place(x=10, y=40)
        self.entry1 = tk.Entry(self.master, font=(font, 12), background="#dfd6eb")
        self.entry1.focus_set()
        self.entry1.place(x=200, y=40, width=200)

        self.label2 = tk.Label(self.master, text="Temperatura sucha [°C]:", font=(font, 12), bg="white")
        self.label2.place(x=10, y=80)
        self.entry2 = tk.Entry(self.master, font=(font, 12), background="#dfd6eb")
        self.entry2.place(x=200, y=80, width=200)

        self.label3 = tk.Label(self.master, text="Temperatura mokra [°C]:", font=(font, 12), bg="white")
        self.label3.place(x=10, y=120)
        self.entry3 = tk.Entry(self.master, font=(font, 12), background="#dfd6eb")
        self.entry3.place(x=200, y=120, width=200)

        self.label4 = tk.Label(self.master, text="Ciśnienie [hPa]:", font=(font, 12), bg="white")
        self.label4.place(x=10, y=160)
        self.entry4 = tk.Entry(self.master, font=(font, 12), background="#dfd6eb")
        self.entry4.place(x=200, y=160, width=200)

        self.label5 = tk.Label(self.master, text="Długość [m]:", font=(font, 12), bg="white")
        self.label5.place(x=10, y=200)
        self.entry5 = tk.Entry(self.master, font=(font, 12), background="#dfd6eb")
        self.entry5.place(x=200, y=200, width=200)

        self.button = tk.Button(self.master, text="Oblicz poprawkę", command=self.expand, font=(font, 12), bg="#402f60", fg="white")
        self.button.place(x=10, y=240, width=400)
    
    def section_buttons(self):
        self.button1 = tk.Button(self.master, text="Zakładka 1", command=self.zakladka_1, font=(font, 12), bg="white")
        self.button1.place(x=0, y=0, width=100, height=30)

        self.button2 = tk.Button(self.master, text="Zakładka 2", font=(font, 12, 'bold'), bg="#dfd6eb")
        self.button2.place(x=100, y=0, width=100, height=30)
        self.button2.configure(state='disabled')
        self.button2.config(relief=tk.SUNKEN)

        self.button3 = tk.Button(self.master, text="Zakładka 3", command=self.zakladka_3, font=(font, 12), bg="white")
        self.button3.place(x=200, y=0, width=100, height=30)

    def expand(self):
        try:
            self.results = self.correction()
        except:
            messagebox.showerror("Błąd", "Wprowadź poprawne dane")
            return

        self.master.geometry("500x400")

        self.label6 = tk.Label(self.master, text="Poprawka na km [mm]:", font=(font, 12), bg="white")
        self.label6.place(x=10, y=290)
        self.entry6 = tk.Entry(self.master, font=(font, 12, 'bold'), fg="#402f60")
        self.entry6.place(x=280, y=290, width=200)
        self.entry6.insert(0, str(self.results[0]))
        self.entry6.configure(state='readonly')

        self.label7 = tk.Label(self.master, text="Poprawka do mierzonej długości [mm]:", font=(font, 12), bg="white")
        self.label7.place(x=10, y=320)
        self.entry7 = tk.Entry(self.master, font=(font, 12, 'bold'), fg="#402f60")
        self.entry7.place(x=280, y=320, width=200)
        self.entry7.insert(0, str(self.results[1]))
        self.entry7.configure(state='readonly')

        self.label8 = tk.Label(self.master, text="Długość poprawiona [m]:", font=(font, 12), bg="white")
        self.label8.place(x=10, y=350)
        self.entry8 = tk.Entry(self.master, font=(font, 12, 'bold'), fg="#402f60")
        self.entry8.place(x=280, y=350, width=200)
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
    
    def zakladka_1(self):
        self.master.destroy()
        Zakladka_1()
    
    def zakladka_3(self):
        self.master.destroy()
        Zakladka_3()

# 3. trzecia zakładka: Obliczenie różnicy między łukiem a cięciwą [wynik w mm] dla przedziału od 1 km do 100 km. Zrobienie wykresu i wygenerowanie tabeli z wynikami (co 1 km) 

class Zakladka_3():
    def __init__(self):
        self.master = tk.Tk()
        self.master.title("Różnica między łukiem a cięciwą")
        self.master.geometry("800x550")
        self.master.resizable(False, False)
        self.master.configure(background='white')
        self.master.protocol("WM_DELETE_WINDOW", self.master.destroy)
        self.master.focus_force()

        self.start = 1000
        self.stop = 100000
        self.step = 1000

        self.data = self.calculate_data()
        self.create_canvas()
        self.create_table()
        self.section_buttons()


    def close(self, event=None):
        self.master.destroy()
    
    def difference(self, length):
        radius = 6378000
        c = - (length**3) / (24 * (8*radius)**2)
        return c
    
    def create_canvas(self):
        fig = self.create_plot()
        canvas = FigureCanvasTkAgg(fig, master=self.master)
        canvas.get_tk_widget().place(x=280, y=20)
        canvas.draw()
        
    def create_plot(self):
        fig = plt.figure(figsize=(5, 5))
        ax = fig.add_subplot(111)
        ax.set_xlabel("Długość łuku [km]")
        ax.set_ylabel("Różnica między łukiem a cięciwą [mm]")
        ax.plot([i[0] for i in self.data], [i[1] for i in self.data], color="#402f60")
        ax.grid(color="#dfd6eb")

        ax.title.set_text("Różnica między łukiem a cięciwą dla przedziału 1-100 km")
    
        ax.tick_params(axis='x', colors='#402f60')
        ax.tick_params(axis='y', colors='#402f60')
        return fig
    
    def create_table(self):
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(font, 10, 'bold'))

        tree = ttk.Treeview(self.master, style="Treeview")
        tree["columns"] = ("Odległość", "Różnica")

        tree.column("#0", width=0, stretch=tk.NO)
        tree.column("Odległość", anchor=tk.W, width=100)
        tree.column("Różnica", anchor=tk.W, width=100)

        tree.heading("#0", text="", anchor=tk.W)
        tree.heading("Odległość", text="Odległość [km]", anchor=tk.W)
        tree.heading("Różnica", text="Różnica [mm]", anchor=tk.W)

        for i in range(len(self.data)):
            if i % 2 == 0:
                tree.insert("", i, text="", values=(int(self.data[i][0]), "{:.2f}".format(self.data[i][1])), tags=('evenrow',))
            else:
                tree.insert("", i, text="", values=(int(self.data[i][0]), "{:.2f}".format(self.data[i][1])))
        
        tree.tag_configure('evenrow', background='#dfd6eb')

        scrollbar = ttk.Scrollbar(self.master, orient="vertical", command=tree.yview)
        scrollbar.place(x=209, y=65, height=460)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.place(x=25, y=40, height=500)

    
    def calculate_data(self):
        data = []
        for i in range(self.start, self.stop + 1, self.step):
            data.append([i / 1000, self.difference(i)*1000])
        
        return data
    
    def section_buttons(self):
        self.button1 = tk.Button(self.master, text="Zakładka 1", command=self.zakladka_1, font=(font, 12), bg="white")
        self.button1.place(x=0, y=0, width=100, height=30)

        self.button2 = tk.Button(self.master, text="Zakładka 2", command=self.zakladka_2, font=(font, 12), bg="white")
        self.button2.place(x=100, y=0, width=100, height=30)

        self.button3 = tk.Button(self.master, text="Zakładka 3", font=(font, 12, 'bold'), bg="#dfd6eb")
        self.button3.place(x=200, y=0, width=100, height=30)
        self.button3.configure(state='disabled')
        self.button3.config(relief=tk.SUNKEN)
    
    def zakladka_1(self):
        self.master.destroy()
        Zakladka_1()
    
    def zakladka_2(self):
        self.master.destroy()
        Zakladka_2()
    

root = tk.Tk()
app = StartScreen(root)
root.mainloop()

