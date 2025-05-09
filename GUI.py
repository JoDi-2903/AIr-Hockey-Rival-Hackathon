import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from PIL import Image, ImageTk
import itertools
import queue
import threading


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AIr-Hockey - Team Awesome Aquajellies")
        self.geometry("600x700")
        self.configure(bg="white")

        self.running = False
        self.error_blinking = False
        self.running_blinking = False
        self.blink_state_error = itertools.cycle(["red", "white"])
        self.blink_state_run = itertools.cycle(["green", "white"])

        self.log_queue = queue.Queue()

        self._build_gui()
        self.after(100, self.process_log_queue)

    def _build_gui(self):
        # Status indicators
        status_frame = tk.Frame(self, bg="white")
        status_frame.pack(pady=10)

        self.error_circle = tk.Canvas(status_frame, width=30, height=30, highlightthickness=0, bg="white")
        self.error_circle.create_oval(5, 5, 25, 25, fill="white", tags="light")
        self.error_circle.grid(row=0, column=0, padx=40)
        tk.Label(status_frame, text="Error", bg="white").grid(row=1, column=0)

        self.run_circle = tk.Canvas(status_frame, width=30, height=30, highlightthickness=0, bg="white")
        self.run_circle.create_oval(5, 5, 25, 25, fill="white", tags="light")
        self.run_circle.grid(row=0, column=1, padx=40)
        tk.Label(status_frame, text="Running", bg="white").grid(row=1, column=1)

        # Image
        try:
            qualle_img = Image.open("qualle.png")
            qualle_img = qualle_img.resize((120, 120))
            self.qualle_photo = ImageTk.PhotoImage(qualle_img)
            tk.Label(self, image=self.qualle_photo, bg="white").pack(pady=(10, 30))
        except:
            tk.Label(self, text="(Qualle fehlt)", font=("Arial", 14), bg="white").pack(pady=(10, 30))

        # Buttons
        button_style = {"width": 20, "height": 2, "font": ("Arial", 12, "bold")}
        tk.Button(self, text="Play", command=self.start_running, bg="lightgreen", **button_style).pack(pady=5)
        tk.Button(self, text="Stop", command=self.stop_running, bg="tomato", **button_style).pack(pady=5)
        tk.Button(self, text="Acknowledge Error", command=self.acknowledge_error, bg="gold", **button_style).pack(pady=5)
        tk.Button(self, text="Exit", command=self.exit_program, bg="white", **button_style).pack(pady=20)

        # Log output
        tk.Label(self, text="Log:", bg="white").pack(anchor=tk.W, padx=5, pady=5)
        self.text_area = ScrolledText(self, state='disabled', width=70, height=10, wrap=tk.WORD)
        self.text_area.pack(pady=5, padx=5)

    def start_running(self):
        self.running = True
        self.error_blinking = False
        self.running_blinking = True
        self.log("System started.")
        self.error_circle.itemconfig("light", fill="white")
        self.blink_run()

        # Example: start a background thread
        threading.Thread(target=self.fake_worker, daemon=True).start()

    def stop_running(self):
        self.running = False
        self.running_blinking = False
        self.error_blinking = False
        self.run_circle.itemconfig("light", fill="white")
        self.error_circle.itemconfig("light", fill="white")
        self.log("System stopped.")

    def acknowledge_error(self):
        self.error_blinking = False
        self.error_circle.itemconfig("light", fill="white")
        self.log("Error acknowledged.")

    def exit_program(self):
        self.destroy()

    def blink_error(self):
        if self.error_blinking:
            color = next(self.blink_state_error)
            self.error_circle.itemconfig("light", fill=color)
            self.after(500, self.blink_error)

    def blink_run(self):
        if self.running_blinking:
            color = next(self.blink_state_run)
            self.run_circle.itemconfig("light", fill=color)
            self.after(500, self.blink_run)

    def log(self, msg: str):
        self.log_queue.put(msg)

    def process_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.append_log(msg)
        self.after(100, self.process_log_queue)

    def append_log(self, msg):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    def fake_worker(self):
        import time
        for i in range(5):
            if not self.running:
                break
            self.log(f"Running task step {i + 1}")
            time.sleep(1)
        if self.running:
            self.log("Task completed.")


if __name__ == "__main__":
    app = App()
    app.mainloop()
