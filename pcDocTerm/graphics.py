# pcDocTerm/graphics.py
# This module contains the graphical user interface (GUI) for the pcDocTerm application
# This project is under the GNU General Public License v3.0 (GPL-3.0).

from tkinter import *
from tkinter.font import Font
from PCInfo import *

window = None
mainFrame = None
mainText = None
pcInfo = None

def createGraphics(windowPassed):
    global window, mainFrame, mainText, pcInfo

    window = windowPassed

    mainFrame = Frame(window, bg="black")
    mainFrame.pack(fill=BOTH, expand=True)

    mainText = Text(mainFrame, bg="black", fg="#16c60c", font=("Consolas", 12), wrap=WORD, state=DISABLED)
    mainText.pack(fill=BOTH, expand=True)

    try:
        pcInfo = PCInfo()  # Initialize the PCInfo object
    except Exception as e:
        writeText(f"Error initializing PCInfo: {e}")
        return

def destroyGraphics():
    global mainFrame, mainText

    if mainText:
        mainText.destroy()
        mainText = None
    if mainFrame:
        mainFrame.destroy()
        mainFrame = None

def writeText(text):
    global mainText

    if mainText:
        mainText.configure(state=NORMAL)
        mainText.insert(END, text)
        mainText.configure(state=DISABLED)
        mainText.see(END)  # Scroll to the end

def writeLine(text):
    global mainText

    if mainText:
        mainText.configure(state=NORMAL)
        mainText.insert(END, text+"\n")
        mainText.configure(state=DISABLED)
        mainText.see(END)  # Scroll to the end

def clearText():
    global mainText

    if mainText:
        mainText.configure(state=NORMAL)
        mainText.delete(1.0, END)
        mainText.configure(state=DISABLED)

def updateGraphics():
    global pcInfo, window

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    clearText()

    font = Font(family="Consolas", size=12)
    char_width = font.measure("A")
    line_height = font.metrics("linespace")

    num_chars = max(5, (window.winfo_width() // char_width)-1)
    num_lines = max(3, (window.winfo_height() // line_height))
    
    for h in range(num_lines):
        line = ""

        for w in range(num_chars):
            if (h == 0 and w == 0) or (h == num_lines - 1 and w == num_chars - 1) or (h == num_lines - 1 and w == 0) or (h == 0 and w == num_chars - 1):
               line += "+"
            elif h == 0 or h == num_lines - 1:
                line += "-"
            elif w == 0 or w == num_chars - 1:
                line += "|"
            else:
                line += " "
        
        if h != num_lines-1:
            writeLine(line)
        else:
            writeText(line)