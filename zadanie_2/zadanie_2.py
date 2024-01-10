import tkinter as tk
from tkinter import ttk
import serial
import time
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter.filedialog import asksaveasfilename
import threading


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

THREAD = None # threading.Thread

parity_map = {
    "brak": "N",
    "parzysta": "E",
    "nieparzysta": "O",
    "mark": "M",
    "space": "S"
}

def save_settings(port, baud, databits, stopbits, parity, xonxoff, rtscts, dtrdsr) -> None:
    global PORT, BAUD, DATABITS, STOPBITS, PARITY, XONXOFF, RTSCTS, DTRDSR
    try:
        PORT = port
        BAUD = baud
        DATABITS = int(databits)
        STOPBITS = int(stopbits)
        PARITY = parity_map[parity]
        XONXOFF = xonxoff
        RTSCTS = rtscts
        DTRDSR = dtrdsr
    except ValueError:
        messagebox.showerror("Błąd", "Niepoprawne dane")
        SETTINGS_WINDOW.focus_set()
        return None
    print(PORT, BAUD, DATABITS, STOPBITS, PARITY, XONXOFF, RTSCTS, DTRDSR)
    SETTINGS_WINDOW.destroy()

def settings_window() -> None:
    global SETTINGS_WINDOW
    SETTINGS_WINDOW = tk.Toplevel()
    SETTINGS_WINDOW.title("Ustawienia")
    SETTINGS_WINDOW.geometry("400x400")
    SETTINGS_WINDOW.resizable(False, False)

    port_frame = tk.LabelFrame(SETTINGS_WINDOW, text="Konfiguracja portu")
    port_frame.pack(padx=10, pady=10, anchor=tk.NW)

    # port
    port_label = tk.Label(port_frame, text="Port")
    port_label.grid(row=0, column=0, padx=10, pady=10)

    port_dropdown = ttk.Combobox(port_frame, width=10, values=["COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8"])
    port_dropdown.grid(row=0, column=1, padx=10, pady=10)
    port_dropdown.set("COM4")

    # baud rate
    baud_label = tk.Label(port_frame, text="Baud rate")
    baud_label.grid(row=1, column=0, padx=10, pady=10)

    baud_dropdown = ttk.Combobox(port_frame, width=10, values=["1200", "2400", "4800", "9600", "14400", "19200", "28800", "38400", "57600", "115200", "230400"])
    baud_dropdown.grid(row=1, column=1, padx=10, pady=10)
    baud_dropdown.set("9600")

    # bity danych
    data_bits_label = tk.Label(port_frame, text="Bity danych")
    data_bits_label.grid(row=2, column=0, padx=10, pady=10)

    data_bits_dropdown = ttk.Combobox(port_frame, width=10, values=["5", "6", "7", "8"], state="readonly")
    data_bits_dropdown.grid(row=2, column=1, padx=10, pady=10)
    data_bits_dropdown.set("8")

    # bity stopu
    stop_bits_label = tk.Label(port_frame, text="Bity stopu")
    stop_bits_label.grid(row=0, column=2, padx=10, pady=10)

    stop_bits_dropdown = ttk.Combobox(port_frame, width=10, values=["1", "2"], state="readonly")
    stop_bits_dropdown.grid(row=0, column=3, padx=10, pady=10)
    stop_bits_dropdown.set("2")

    # parzystość
    parity_label = tk.Label(port_frame, text="Parzystość")
    parity_label.grid(row=1, column=2, padx=10, pady=10)

    parity_dropdown = ttk.Combobox(port_frame, width=10, values=["brak", "parzysta", "nieparzysta", "mark", "space"], state="readonly")
    parity_dropdown.grid(row=1, column=3, padx=10, pady=10)
    parity_dropdown.set("brak")

    #flow control frame
    flow_control_frame = tk.LabelFrame(SETTINGS_WINDOW, text="Flow control")
    flow_control_frame.pack(padx=10, pady=10, anchor=tk.NW)

    # XON/XOFF checkbox
    xonxoff_var = tk.BooleanVar()
    xonxoff_checkbox = tk.Checkbutton(flow_control_frame, text="XON/XOFF", variable=xonxoff_var)
    xonxoff_checkbox.grid(row=0, column=0, padx=10, pady=10)

    # RTS/CTS checkbox
    rtscts_var = tk.BooleanVar()
    rtscts_checkbox = tk.Checkbutton(flow_control_frame, text="RTS/CTS", variable=rtscts_var)
    rtscts_checkbox.grid(row=0, column=1, padx=10, pady=10)

    # DTR/DSR checkbox
    dtrdsr_var = tk.BooleanVar()
    dtrdsr_checkbox = tk.Checkbutton(flow_control_frame, text="DTR/DSR", variable=dtrdsr_var)
    dtrdsr_checkbox.grid(row=0, column=2, padx=10, pady=10)

    save_button = tk.Button(SETTINGS_WINDOW, text="Zapisz", width=10, height=2, command = lambda: save_settings(port_dropdown.get(), baud_dropdown.get(), data_bits_dropdown.get(), stop_bits_dropdown.get(), parity_dropdown.get(), xonxoff_var.get(), rtscts_var.get(), dtrdsr_var.get()))
    save_button.pack(padx=10, pady=10, anchor=tk.NE)

    SETTINGS_WINDOW.mainloop()

def open_port() -> None:
    global SERIAL
    if SERIAL is not None:
        if SERIAL.isOpen():
            messagebox.showerror("Błąd", "Port jest już otwarty.")
            return None

    if PORT is None or BAUD is None or DATABITS is None or STOPBITS is None or PARITY is None or XONXOFF is None or RTSCTS is None or DTRDSR is None:
        messagebox.showerror("Błąd", "Nie ustawiono parametrów portu.")
        return None
    
    try:
        SERIAL = serial.Serial(PORT, BAUD, bytesize=DATABITS, stopbits=STOPBITS, parity=PARITY, xonxoff=XONXOFF, rtscts=RTSCTS, dsrdtr=DTRDSR)
    except serial.SerialException:
        messagebox.showerror("Błąd", "Nie można otworzyć portu.")
        return None
    global THREAD
    THREAD = threading.Thread(target=read_data, args=(SERIAL,), daemon=True)
    THREAD.start()
    print("Port otwarty.")

def close_port() -> None:
    global SERIAL
    if SERIAL is None:
        messagebox.showerror("Błąd", "Nie otwarto portu.")
        return None
    if not SERIAL.isOpen():
        messagebox.showerror("Błąd", "Port jest już zamknięty.")
        return None
    try:
        SERIAL.close()
        THREAD.join()
    except serial.SerialException:
        messagebox.showerror("Błąd", "Nie można zamknąć portu.")
        return None

def read_data(ser: serial.Serial) -> None:
    while True:
        try:
            data = ser.read(ser.inWaiting())
            if data:
                output_text.config(state="normal")
                output_text.insert(tk.END, data.decode("utf-8") + "\n")
                output_text.config(state="disabled")
            time.sleep(0.1)
        except serial.SerialException:
            messagebox.showerror("Błąd", "Nie można odczytać danych.")
            return None
    
    
def send_data() -> None:
    if input_text.get("1.0", tk.END) == "\n":
        messagebox.showerror("Błąd", "Nie wpisano danych.")
        return None
    try:
        SERIAL.write(input_text.get("1.0", tk.END).encode("utf-8"))
    except AttributeError:
        messagebox.showerror("Błąd", "Nie otwarto portu.")
        return None
    except serial.SerialException:
        messagebox.showerror("Błąd", "Nie można wysłać danych.")
        return None

def save_to_file() -> None:
    # if output_text.get("1.0", tk.END) == "\n":
    #     messagebox.showinfo("Informacja", "Brak danych do zapisania")
    #     return None
    try:
        file = asksaveasfilename(defaultextension=".txt", filetypes=[("Text file", "*.txt"), ("All files", "*.*")])
        if file:
            with open(file, "w") as f:
                f.write(output_text.get("1.0", tk.END))
        
    except FileNotFoundError as e:
        messagebox.showerror("Błąd", f"{e}")
        return None

def clear() -> None:
    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)
    output_text.config(state="disabled")

ROOT = tk.Tk()
ROOT.title("Terminálek")
ROOT.geometry("630x480")
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

output_text = ScrolledText(output_frame, width=70, height=10, state="disabled")
output_text.grid(row=0, column=0, padx=10, pady=10)

input_frame = tk.LabelFrame(ROOT, text="Pole komendy")
input_frame.grid(row=2, column=0, columnspan=5, padx=10, pady=10)

input_text = ScrolledText(input_frame, width=70, height=5)
input_text.grid(row=0, column=0, padx=10, pady=10)

send_button = tk.Button(input_frame, text="Wyślij", width=10, height=1, command=send_data)
send_button.grid(row=1, column=0, padx=10, pady=10)

ROOT.mainloop()