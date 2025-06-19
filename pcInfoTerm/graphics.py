# pcInfoTerm/graphics.py
# This module contains the graphical user interface (GUI) for the pcInfoTerm application
# This project is under the GNU General Public License v3.0 (GPL-3.0).

from tkinter import *
from tkinter.font import Font
from PCInfo import *
import threading
import queue
import time

window = None
mainFrame = None
mainText = None
pcInfo = None
data_queue = queue.Queue()
data_queue_backup = None
MINNUMLINES = 10
MAXNUMLINES = 30
MINNUMCHARS = 65
MAXNUMCHARS = 152

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
    global pcInfo, window, mainText, data_queue, data_queue_backup, MINNUMLINES, MINNUMCHARS, MAXNUMLINES, MAXNUMCHARS

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    clearText()

    font = Font(family="Consolas", size=12)
    char_width = font.measure("A")
    line_height = font.metrics("linespace")

    num_chars = max(5, (window.winfo_width() // char_width)-1)
    num_lines = max(3, (window.winfo_height() // line_height))

    try:
        data = data_queue.get_nowait()
    except queue.Empty:
        data = None
    
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
        
        # Add system information to the lines
        if h != num_lines-1: # Do not add system information to the last line and do not print \n
            if h != 0 and h != num_lines-1: # Do not add system information to the first and last line
                if h == 1:
                    strToAdd = "PCInfo - System Information Terminal"
                    paddingLeftChars = 2
                    writeLine(rewriteLine(line, strToAdd, paddingLeftChars))

                elif num_lines >= MAXNUMLINES and num_chars >= MAXNUMCHARS: # Big terminal, all information
                    if h <= 20: # Print static system information
                        line = (printSystemStaticInfo(h, line))

                        writeLine(printBarsInPile(h, data, line, paddingLeftChars=90))
                    else: # Print dynamic system information
                        writeLine(printPileOfData(h, line, 21))

                elif num_lines >= MAXNUMLINES and (num_chars >= MINNUMCHARS and num_chars < MAXNUMCHARS): # Medium terminal (height), some information
                    if h < 11:
                        writeLine(printSystemStaticInfo(h, line))
                    else:
                        writeLine(printBarsInPile(h, data, line, 11))

                elif num_chars >= MAXNUMCHARS and (num_lines >= MINNUMLINES and num_lines < MAXNUMLINES): # Medium terminal (width), some information
                    line = (printSystemStaticInfo(h, line))

                    writeLine(printBarsInPile(h, data, line, paddingLeftChars=80))

                elif (num_lines >= MINNUMLINES and num_lines < MAXNUMLINES) and (num_chars >= MINNUMCHARS and num_chars < MAXNUMCHARS): # Only add system information if the terminal is big enough
                    writeLine(printSystemStaticInfo(h, line))

                elif num_lines < MINNUMLINES or num_chars < MINNUMCHARS: # Small terminal, essential information only
                    writeLine(printBarsInPile(h, data, line, 3))

                else:
                    writeLine("ERR")
            else:
                writeLine(line)
        else:
            writeText(line)

    window.after(200, updateGraphics)  # Update the graphics in loop

def rewriteLine(line, text, paddingLeftChars=2):
    lineRet = line[:paddingLeftChars] + text + line[paddingLeftChars+len(text):]
    return lineRet

def printBarsInPile(h, data, line, firsth=2, paddingLeftChars=2):
    try:
        if h == firsth:
            dataDSK = (data["Disk"] if data and "Disk" in data else "N/A")
            if dataDSK != "N/A":
                data_queue_backup["Disk"] = dataDSK
            else:
                dataDSK = data_queue_backup["Disk"] if data_queue_backup["Disk"] else "N/A"

            strToAdd = "Disk: " + dataDSK
            linetowrite = (rewriteLine(line, strToAdd, paddingLeftChars))
        elif h == firsth+1:
            dataMEM = (data["Memory"] if data and "Memory" in data else "N/A")
            if dataMEM != "N/A":
                data_queue_backup["Memory"] = dataMEM
            else:
                dataMEM = data_queue_backup["Memory"] if data_queue_backup["Memory"] else "N/A"

            strToAdd = "Memory: " + dataMEM
            linetowrite = (rewriteLine(line, strToAdd, paddingLeftChars))
        elif h == firsth+2:
            dataBAT = (data["Battery"] if data and "Battery" in data else "N/A")
            if dataBAT != "N/A":
                data_queue_backup["Battery"] = dataBAT
            else:
                dataBAT = data_queue_backup["Battery"] if data_queue_backup["Battery"] else "N/A"

            strToAdd = "Battery: " + dataBAT
            linetowrite = (rewriteLine(line, strToAdd, paddingLeftChars))
        elif h >= firsth+3 and h < firsth+3 + int(pcInfo.system_info["CPU Cores"]):
            cpu_bars = (data["CPU"] if data and "CPU" in data else "N/A")

            if cpu_bars != "N/A":
                data_queue_backup["CPU"] = cpu_bars
            else:
                cpu_bars = data_queue_backup["CPU"] if data_queue_backup["CPU"] else ["▓"*20 for _ in range(int(pcInfo.system_info["CPU Cores"]))]

            if h-(firsth+3) < len(cpu_bars):
                strToAdd = f"CPU Core {h-(firsth+3)+1}: " + cpu_bars[h-(firsth+3)]
                linetowrite = (rewriteLine(line, strToAdd, paddingLeftChars))
        else:
            linetowrite = (line)

        return linetowrite
    except Exception as e:
        writeText(f"Error writing system information: {e}")

def printSystemStaticInfo(h, line):
    if h == 2:
        strToAdd = "Hostname: " + pcInfo.system_info["Hostname"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 3:
        strToAdd = "OS: " + pcInfo.system_info["OS"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 4:
        strToAdd = "OS Version: " + pcInfo.system_info["OS Version"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 5:
        strToAdd = "Architecture: " + pcInfo.system_info["Architecture"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 6:
        strToAdd = "Processor: " + pcInfo.system_info["Processor"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 7:
        strToAdd = "CPU Cores: " + pcInfo.system_info["CPU Cores"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 8:
        strToAdd = "Memory: " + pcInfo.system_info["Memory"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == 9:
        strToAdd = "Disk: " + pcInfo.system_info["Disk"]
        linetowrite = (rewriteLine(line, strToAdd))
    else:
        linetowrite = (line)

    return linetowrite

def printPileOfData(h, line, firsth=11):
    global pcInfo

    if h == firsth:
        strToAdd = "Disk usage: " + pcInfo.get_current_disk_usage()
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == firsth+1:
        strToAdd = "Disk read time: " + pcInfo.get_current_disk_read()
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == firsth+2:
        strToAdd = "Disk write time: " + pcInfo.get_current_disk_write()
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == firsth+3:
        strToAdd = "Memory usage: " + pcInfo.get_current_memory_usage()
        linetowrite = (rewriteLine(line, strToAdd))
    elif h == firsth+4:
        strToAdd = "Battery time: " + pcInfo.get_battery_info()["Time Left"]
        linetowrite = (rewriteLine(line, strToAdd))
    elif h >= firsth+6 and (h-firsth-6 < pcInfo.get_current_cpu_freq().__len__() or pcInfo.get_current_disk_partitions().__len__() > h-firsth-6):
        if pcInfo.get_current_disk_partitions() != None and pcInfo.get_current_disk_partitions().__len__() > h-firsth-6:
            diskPart = pcInfo.get_current_disk_partitions()[h-firsth-6]

        if pcInfo.get_current_cpu_freq() != None and pcInfo.get_current_cpu_freq().__len__() > h-firsth-6:
            coreFreq = pcInfo.get_current_cpu_freq()[h-firsth-6]
            strToAdd = "CPU Core " + str(h-firsth-6+1) + ": Frequency: " + coreFreq
            linetowrite = (rewriteLine(line, strToAdd))
        else:
            linetowrite = (line)

        linetowrite = rewriteLine(linetowrite, "Disk Partition " + str(h-firsth-6+1) + ": " + (diskPart if diskPart else "N/A"), (90))
    else:
        linetowrite = (line)

    #get_current_cpu_freq and get_current_disk_partitions lists

    return linetowrite

def start_data_thread():
    t = threading.Thread(target=getDataForQueue, daemon=True)
    t.start()

def getDataForQueue():
    global pcInfo, data_queue, data_queue_backup

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    data_queue_backup = {
                "Disk": "▓"*20,
                "Memory": "▓"*20,
                "CPU": ["▓"*20 for _ in range(int(pcInfo.system_info["CPU Cores"]))],
                "Battery": "▓"*20
            }
    
    while True:
        try:
            disk_bar = getDiskUsageBar()
            mem_bar = getMemoryUsageBar()
            cpu_bars = getCpuUsageBar()
            battery_bar = getBatteryBar()
            
            data_queue.put({
                "Disk": disk_bar,
                "Memory": mem_bar,
                "CPU": cpu_bars,
                "Battery": battery_bar
            })
        except Exception as e:
            data_queue.put({"error": str(e)})

        time.sleep(0.3)  # Sleep for a while to avoid busy waiting

def getDiskUsageBar(): # Returns a string representing the disk usage bar (length 20 characters)
    global pcInfo

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    try:
        used = float((pcInfo.get_current_disk_usage_percent().replace("%", "")))  # Get the used disk space percentage
        avable = 100.0-used  # Get the available disk space percentage

        used_bar = "█" * int(used / 5)
        avable_bar = "░" * int(avable / 5)
    except Exception as e:
        writeText(f"Error calculating disk usage: {e}")
        return
    
    bar = used_bar + avable_bar
    bar = bar.ljust(20, "░")  # Ensure the bar is 20

    return bar

def getMemoryUsageBar(): # Returns a string representing the memory usage bar (length 20 characters)
    global pcInfo

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    try:
        used = float((pcInfo.get_current_memory_usage_percent().replace("%", "")))  # Get the used disk space percentage
        avable = 100.0-used  # Get the available disk space percentage

        used_bar = "█" * int(used / 5)
        avable_bar = "░" * int(avable / 5)
    except Exception as e:
        writeText(f"Error calculating memory usage: {e}")
        return
    
    bar = used_bar + avable_bar
    bar = bar.ljust(20, "░")  # Ensure the bar is 20

    return bar

def getCpuUsageBar(): # Returns a list representing the CPUs usage bar (length 20 characters)
    global pcInfo

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    bar = []
    
    for core in pcInfo.get_current_cpu_usage():  # Get the CPU usage for each core
        try:
            used_bar = "█" * int(core / 5)
            avable_bar = "░" * int((100.0-core) / 5)
        except Exception as e:
            used_bar = "▓" * 20
            avable_bar = "░" * 0

        bar.append((used_bar + avable_bar).ljust(20, "░"))
    
    while len(bar) < int(pcInfo.system_info["CPU Cores"]):
        bar.append("▓" * 20)  # Fill with empty bars if not enough cores

    return bar

def getBatteryBar(): # Returns a string representing the battery bar (length 20 characters)
    global pcInfo

    if not pcInfo:
        writeText("PCInfo is not initialized.")
        return
    
    try:
        battery = pcInfo.get_battery_info()

        if battery == "Battery information not available.":
            return None
        
        percent = float(battery["Battery Percentage"].replace("%", ""))

        used_bar = "█" * int(percent / 5)
        avable_bar = "░" * int((100.0-percent) / 5)
    except Exception as e:
        writeText(f"Error calculating battery usage: {e}")
        return
    
    bar = used_bar + avable_bar
    bar = bar.ljust(20, "░")  # Ensure the bar is 20

    return bar