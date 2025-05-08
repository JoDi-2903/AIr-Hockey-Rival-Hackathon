import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import queue

class App(tk.Tk):
    running: bool = False

    def __init__(self):
        super().__init__()
        self.title("AIr-Hockey - Team Awesome Aquajellies")
        self.geometry("500x500")

        tk.Label(self, text="Log:").pack(anchor=tk.W, padx=5, pady=5)
        self.text_area = ScrolledText(self, state='disabled', width=60, height=10, wrap=tk.WORD)
        self.text_area.pack(pady=5, padx=5)

        tk.Button(self, text="Start", command=self.start_running, bg="lightgreen").pack(padx=5, pady=5)
        tk.Button(self, text="Stop", command=self.stop_running, bg="#F77B7B").pack(padx=5, pady=5)

        self.log_queue = queue.Queue()

        self.after(100, self.process_log_queue)

    def start_running(self):
        self.running = True

    def stop_running(self):
        self.running = False

    def process_log_queue(self):
        while not self.log_queue.empty():
            msg = self.log_queue.get()
            self.append_log(msg)
        self.after(100, self.process_log_queue)  # Check again after 100 ms

    def append_log(self, msg):
        self.text_area.configure(state='normal')
        self.text_area.insert(tk.END, msg + "\n")
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)  # Auto-scroll
