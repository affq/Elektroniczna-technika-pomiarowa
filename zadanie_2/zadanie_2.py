import tkinter as tk
from tkinter import ttk
import serial
import time
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox

PORT = None
BAUD = None 
DATABITS = None
STOPBITS = None
PARITY = None 
XONXOFF = None
RTSCTS = None
DTRDSR = None

SERIAL = None # serial.Serial
SETTINGS_WINDOW = None # tk.Toplevel
ROOT = None # tk.Tk

parity_map = {
    "brak": "N",
    "parzysta": "E",
    "nieparzysta": "O",
    "mark": "M",
    "space": "S"
}

def save_settings(port_dropdown, baud_dropdown, data_bits_dropdown, stop_bits_dropdown, parity_dropdown, dtr_dropdown) -> None:
    global PORT, BAUD, DATABITS, STOPBITS, PARITY, XONXOFF, RTSCTS, DTRDSR

    if dtr_dropdown.get() == "none":
        XONXOFF = False
        RTSCTS = False
        DTRDSR = False
    elif dtr_dropdown.get() == "RTS/CTS":
        XONXOFF = False
        RTSCTS = True
        DTRDSR = False
    elif dtr_dropdown.get() == "DTR/DSR":
        XONXOFF = False
        RTSCTS = False
        DTRDSR = True
    elif dtr_dropdown.get() == "XON/XOFF":
        XONXOFF = True
        RTSCTS = False
        DTRDSR = False

    try:
        PORT = port_dropdown.get()
        BAUD = baud_dropdown.get()
        DATABITS = int(data_bits_dropdown.get())
        STOPBITS = int(stop_bits_dropdown.get())
        PARITY = parity_map[parity_dropdown.get()]
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawne dane")
        SETTINGS_WINDOW.focus_set()
        return None
    SETTINGS_WINDOW.destroy()

def settings_window() -> None:
    global SETTINGS_WINDOW
    SETTINGS_WINDOW = tk.Toplevel()
    SETTINGS_WINDOW.title("Ustawienia")
    SETTINGS_WINDOW.geometry("400x250")
    SETTINGS_WINDOW.resizable(False, False)

    port_frame = tk.LabelFrame(SETTINGS_WINDOW, text="Konfiguracja portu")
    port_frame.pack(padx=10, pady=10, anchor=tk.NW)

    # port
    port_label = tk.Label(port_frame, text="Port")
    port_label.grid(row=0, column=0, padx=10, pady=10)

    port_dropdown = ttk.Combobox(port_frame, width=10, values=["COM1", "COM2", "COM3", "COM4"])
    port_dropdown.grid(row=0, column=1, padx=10, pady=10)

    # baud rate
    baud_label = tk.Label(port_frame, text="Baud rate")
    baud_label.grid(row=1, column=0, padx=10, pady=10)

    baud_dropdown = ttk.Combobox(port_frame, width=10, values=["1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200", "230400"], textvariable=BAUD)
    baud_dropdown.grid(row=1, column=1, padx=10, pady=10)

    # bity danych
    data_bits_label = tk.Label(port_frame, text="Bity danych")
    data_bits_label.grid(row=2, column=0, padx=10, pady=10)

    data_bits_dropdown = ttk.Combobox(port_frame, width=10, values=["5", "6", "7", "8"], state="readonly")
    data_bits_dropdown.grid(row=2, column=1, padx=10, pady=10)

    # bity stopu
    stop_bits_label = tk.Label(port_frame, text="Bity stopu")
    stop_bits_label.grid(row=0, column=2, padx=10, pady=10)

    stop_bits_dropdown = ttk.Combobox(port_frame, width=10, values=["1", "2"], state="readonly")
    stop_bits_dropdown.grid(row=0, column=3, padx=10, pady=10)

    # parzystość
    parity_label = tk.Label(port_frame, text="Parzystość")
    parity_label.grid(row=1, column=2, padx=10, pady=10)

    parity_dropdown = ttk.Combobox(port_frame, width=10, values=["brak", "parzysta", "nieparzysta", "mark", "space"], state="readonly")
    parity_dropdown.grid(row=1, column=3, padx=10, pady=10)

    dtr_label = tk.Label(port_frame, text="Sterowanie")
    dtr_label.grid(row=2, column=2, padx=10, pady=10)

    dtr_dropdown = ttk.Combobox(port_frame, width=10, values=["none", "RTS/CTS", "DTR/DSR", "XON/XOFF"], state="readonly")
    dtr_dropdown.grid(row=2, column=3, padx=10, pady=10)

    save_button = tk.Button(SETTINGS_WINDOW, text="Zapisz", width=10, height=2, command = lambda: save_settings(port_dropdown, baud_dropdown, data_bits_dropdown, stop_bits_dropdown, parity_dropdown, dtr_dropdown))
    save_button.pack(padx=10, pady=10, anchor=tk.NE)

    SETTINGS_WINDOW.mainloop()

def open_port() -> None:
    global SERIAL
    try:
        SERIAL = serial.Serial(PORT, BAUD, bytesize=DATABITS, stopbits=STOPBITS, parity=PARITY, xonxoff=XONXOFF, rtscts=RTSCTS, dsrdtr=DTRDSR)
        read_data(SERIAL)
    except serial.SerialException:
        messagebox.showerror("Błąd", "Nie można otworzyć portu")
        return None
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawne dane")
        return None
    except AttributeError:
        messagebox.showerror("Błąd", "Niepoprawne dane")
        return None
    # open_button["text"] = "Zamknij port"

def read_data(ser: serial.Serial) -> None:
    line = ""
    while True:
        if ser.in_waiting > 0:
            data = ser.read(1)
            if data == b"\n":
                print(line)
                output_text.config(state="normal")
                output_text.insert(tk.END, line)
                output_text.config(state="disabled")
                line = ""
            else:
                line += data.decode("utf-8")
        else:
            time.sleep(0.1)
    
    
def send_data() -> None:
    if input_text.get("1.0", tk.END) == "\n":
        messagebox.showerror("Błąd", "Nie wpisano danych")
        return None
    try:
        data = input_text.get("1.0", tk.END)
        SERIAL.write(data.encode("utf-8"))
    except AttributeError:
        messagebox.showerror("Błąd", "Nie otwarto portu")
        return None
    except serial.SerialException:
        messagebox.showerror("Błąd", "Nie można wysłać danych")
        return None

def save_to_file() -> None:
    if output_text.get("1.0", tk.END) == "\n":
        return None
    try:
        data = output_text.get("1.0", tk.END)
        with open("output.txt", "w") as f:
            f.write(data)
    except:
        messagebox.showerror("Błąd", "Nie można zapisać do pliku")
        return None

def clear() -> None:
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

ROOT = tk.Tk()
ROOT.title("Terminálek")
ROOT.geometry("610x480")
ROOT.resizable(False, False)

settings_button = tk.Button(ROOT, text="Ustaw port", width=20, height=2, command = lambda: settings_window())
settings_button.grid(row=0, column=0, padx=10, pady=10)

open_button = tk.Button(ROOT, text="Otwórz port", width=10, height=2, command=open_port)
open_button.grid(row=0, column=1, padx=10, pady=10)

save_button = tk.Button(ROOT, text="Zapisz do pliku", width=13, height=2, command=save_to_file)
save_button.grid(row=0, column=2, padx=10, pady=10)

clear_button = tk.Button(ROOT, text="Wyczyść", width=10, height=2, command=clear)
clear_button.grid(row=0, column=3, padx=10, pady=10)

close_button = tk.Button(ROOT, text="X Zamknij", width=10, height=2, command=ROOT.destroy)
close_button.grid(row=0, column=4, padx=10, pady=10)

output_frame = tk.LabelFrame(ROOT, text="Odbiór")
output_frame.grid(row=1, column=0, columnspan=5, padx=10, pady=10)

output_text = tk.Text(output_frame, width=70, height=10, state="disabled")
output_text.grid(row=0, column=0, padx=10, pady=10)

input_frame = tk.LabelFrame(ROOT, text="Pole komendy")
input_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

input_text = tk.Text(input_frame, width=70, height=3)
input_text.grid(row=0, column=0, padx=10, pady=10)

send_button = tk.Button(input_frame, text="Wyślij", width=10, height=1, command=send_data)
send_button.grid(row=1, column=0, padx=10, pady=10)

ROOT.mainloop()