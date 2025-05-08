import tkinter as tk
from tkinter import messagebox, scrolledtext
from PIL import Image, ImageTk

# Platzhalter-Funktionen
def start_camera():
    log_message("Kamera gestartet (simuliert).")

def stop_camera():
    log_message("Kamera gestoppt (simuliert).")

def start_tracking():
    log_message("Puck-Tracking aktiviert (simuliert).")

def start_algorithm():
    log_message("Spiel-Algorithmus läuft (simuliert).")

def start_control():
    log_message("Robotersteuerung aktiv (simuliert).")

def log_message(msg):
    log_box.insert(tk.END, msg + "\n")
    log_box.see(tk.END)

# Fenster erstellen
root = tk.Tk()
root.title("AIr-Hockey - Team Awesome Aquajellies")
root.geometry("500x550")

# Qualle-Bild laden und anzeigen
try:
    qualle_img = Image.open("qualle.png")
    qualle_img = qualle_img.resize((150, 150))  # ggf. anpassen
    qualle_photo = ImageTk.PhotoImage(qualle_img)
    qualle_label = tk.Label(root, image=qualle_photo)
    qualle_label.pack(pady=10)
except Exception as e:
    tk.Label(root, text="⚠️ Qualle-Bild nicht gefunden").pack(pady=10)

# Buttons
tk.Button(root, text="Kamera starten", command=start_camera, width=25, bg="#28a745", fg="white").pack(pady=5)
tk.Button(root, text="Kamera stoppen", command=stop_camera, width=25, bg="#dc3545", fg="white").pack(pady=5)
tk.Button(root, text="Puck-Tracking starten", command=start_tracking, width=25).pack(pady=5)
tk.Button(root, text="Algorithmus starten", command=start_algorithm, width=25).pack(pady=5)
tk.Button(root, text="Robotersteuerung starten", command=start_control, width=25).pack(pady=5)

# Logs
tk.Label(root, text="System-Logs:").pack()
log_box = scrolledtext.ScrolledText(root, width=60, height=10, wrap=tk.WORD)
log_box.pack(pady=10)

# GUI starten
root.mainloop()
