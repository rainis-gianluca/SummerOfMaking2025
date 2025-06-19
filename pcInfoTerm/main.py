# pcInfoTerm/main.py
# This project is a terminal PC management tool
# This project is under the GNU General Public License v3.0 (GPL-3.0).
# Original Author: Gianluca Rainis ( __grdev on summer.hackclub.com )

from tkinter import *
from graphics import createGraphics, updateGraphics, start_data_thread
from pathlib import Path

POSITIONIMAGES = str(Path(__file__).parent.absolute()) + "\\images\\"

window = Tk()
window.title("pcInfoTerm - System information - Summer of Making 2025 Edition")
window.geometry("810x400")
window.minsize(400, 250)
window.configure(background="black")
window.resizable(True, True)  # Allow resizing
window.iconbitmap(POSITIONIMAGES+"terminal.ico")  # Set the icon for the window

createGraphics(window)

try:
    start_data_thread()
except Exception as e:
    print(f"Error in data thread: {e}\n")

try:
    updateGraphics()
except Exception as e:
    print(f"Error updating graphics: {e}\n")

if __name__ == "__main__": #Start the program
    window.mainloop()