import threading
import tkinter as tk
from tkinter import messagebox
from capture.sniffer import ServerSniffer
from network.packet_sender import PacketSender
from config import PACKETS_THRESHOLD, UDP_PORT_RANGE
from utils.logger import logger

class RocketGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Rocket League Server Tool")
        self.root.geometry("400x250")
        self.server_ip = None
        self.server_port = None

        self.label = tk.Label(self.root, text="Press 'Scan' to find server")
        self.label.pack(pady=10)

        self.scan_button = tk.Button(self.root, text="Scan Server", command=self.scan_server)
        self.scan_button.pack(pady=5)

        self.packet_label = tk.Label(self.root, text="Packets to send:")
        self.packet_label.pack(pady=5)

        self.packet_entry = tk.Entry(self.root)
        self.packet_entry.insert(0, "1000")
        self.packet_entry.pack(pady=5)

        self.send_button = tk.Button(self.root, text="Send Packets", state=tk.DISABLED, command=self.send_packets)
        self.send_button.pack(pady=10)

    def scan_server(self):
        self.label.config(text="Scanning for server...")
        self.scan_button.config(state=tk.DISABLED)

        def scan():
            sniffer = ServerSniffer(port_range=UDP_PORT_RANGE, threshold=PACKETS_THRESHOLD)
            ip, port = sniffer.start_sniffing()
            if ip and port:
                self.server_ip = ip
                self.server_port = port
                self.label.config(text=f"Server: {ip}:{port}")
                self.send_button.config(state=tk.NORMAL)
            else:
                self.label.config(text="No server detected.")
            self.scan_button.config(state=tk.NORMAL)

        threading.Thread(target=scan, daemon=True).start()

    def send_packets(self):
        try:
            count = int(self.packet_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid number of packets")
            return

        def send():
            sender = PacketSender(self.server_ip, self.server_port)
            sender.send_packets(count=count)
            messagebox.showinfo("Done", f"Sent {count} packets.")

        threading.Thread(target=send, daemon=True).start()

    def run(self):
        self.root.mainloop()

