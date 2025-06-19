# pcDocTerm/main.py
# This project is a terminal PC management tool
# This project is under the GNU General Public License v3.0 (GPL-3.0).
# Original Author: Gianluca Rainis ( __grdev on summer.hackclub.com )

from tkinter import *
from graphics import createGraphics, updateGraphics
from pathlib import Path

POSITIONIMAGES = str(Path(__file__).parent.absolute()) + "\\images\\"

window = Tk()
window.title("pcDocTerm - System information - Summer of Making 2025 Edition")
window.geometry("810x400")
window.configure(background="black")
window.resizable(True, True)  # Allow resizing
window.iconbitmap(POSITIONIMAGES+"terminal.ico")  # Set the icon for the window

createGraphics(window)

def update():
    updateGraphics()
    window.after(100, update)  # Update in loop

if __name__ == "__main__": #Start the program
    update()
    window.mainloop()