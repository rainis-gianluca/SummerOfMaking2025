# Summer of Making 2025 projects
This is the readme file for all the projects.

Author: Gianluca Rainis ( __grdev on summer.hackclub.com )
License: GNU General Public License v3.0

## Projects
### netTools 
A network analizer tool that can send personalized packets, scan the LAN with ARP to found for all IPs the MAC and the DNS, simulate a DDoS sending packets to a host with random public source IP and scan the ports in a given range of a host to search which are open.
#### Libraries
-tkinter
-pathlib
-socket
-threading
-random
-scapy
-ipaddress
#### Installation
To install the tool first you need to download the source code from github, then download and intall python on your PC (https://www.python.org/downloads/), then you need to install the libraries, to install the libraries run the following commands:

```bash
pip install pathlib
```
```bash
pip install socket.py
```
```bash
pip install random2
```
```bash
pip install scapy
```
```bash
pip install ipaddress
```

The other libraries can be installed when you install python. The commands to install the libraries may be different for other OS.
The tool was written for Windows, but it may work also for linux.

To run the tool open the terminal in the project folder and run
```bash
python main.py
```

### pcDocTerm
A simple terminal that show you info about your pc status.
#### Libraries
-tkinter
-pathlib
-queue
-threading
-time
-socket
-psutil
-platform
#### Installation
To install the tool first you need to download the source code from github, then download and intall python on your PC (https://www.python.org/downloads/), then you need to install the libraries, to install the libraries run the following commands:

```bash
pip install pathlib
```
```bash
pip install socket.py
```
```bash
pip install psutil
```

The other libraries can be installed when you install python. The commands to install the libraries may be different for other OS.
The tool was written for Windows, but it may work also for linux.

To run the tool open the terminal in the project folder and run
```bash
python main.py
```

## AI Disclaimer
In all the project is used GitHub Copilot just as assistant to the coding, so the logic operations and the ideas of all the projects are of the developer. The AI helped just to write code fast (for example when it is repetitive), to write the comments (the less important) and helped to learn how to use some libraries (for example for a project I'd used psutil, the AI helped me to study the docs of the library).