# netTools/main.py
# This is the main entry point for the NetTools application, which initializes the GUI and sets up the menu.
# This project is a network analysis tool that provides various functionalities like packet generation and ARP analysis.
# This project is under the GNU General Public License v3.0 (GPL-3.0).
# EDUCATIONAL PURPOSES ONLY
# Original Author: Gianluca Rainis ( __grdev on summer.hackclub.com )

from graphics import createGraphics, menuGestor
from tkinter import Tk, Menu

window = Tk()
window.title("NetTools - Pro Network analyzer - Summer of Making 2025 Edition")
window.geometry("500x600")
window.resizable(False, False)
window.configure(background="black")

menu = Menu(window)
menu.add_command(label="Packet Generator", command=lambda: menuGestor("Packet Generator"))
menu.add_command(label="ARP Analyzer", command=lambda: menuGestor("ARP Analyzer"))
menu.add_command(label="DoS as DDoS", command=lambda: menuGestor("DoS as DDoS"))
menu.add_command(label="Port Scan", command=lambda: menuGestor("Port Scan"))
menu.add_separator()
menu.add_command(label="About", command=lambda: menuGestor("About"))
window.config(menu=menu)

createGraphics(window)

if __name__ == "__main__": #Start the program
    window.mainloop()