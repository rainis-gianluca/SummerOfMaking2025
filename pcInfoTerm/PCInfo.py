# pcInfoTerm/PCInfo.py
# This module contains the backend logic for the pcInfoTerm application
# This project is under the GNU General Public License v3.0 (GPL-3.0).

import socket
import psutil
import platform

class PCInfo:
    def __init__(self):
        self.system_info = { # Static information about the system
            "Hostname": platform.node(),
            "OS": platform.system(),
            "OS Version": platform.version(),
            "Architecture": platform.architecture()[0],
            "Processor": platform.processor(),
            "CPU Cores": str(psutil.cpu_count(logical=True)),
            "Memory": self.get_memory_info(),
            "Disk": self.get_disk_info()
        }

    #Internal methods to get constant system information
    def get_memory_info(self): # Returns total memory in GB of RAM
        mem = psutil.virtual_memory()
        return f"{mem.total / (1024 ** 3):.2f} GB"

    def get_disk_info(self): # Returns total disk space in GB
        disk = psutil.disk_usage('/')
        return f"{disk.total / (1024 ** 3):.2f} GB"
    
    # Main methods to get system information
    
    def get_current_disk_usage(self): # Returns the current disk usage in GB
        disk = psutil.disk_usage('/')
        return f"{disk.used / (1024 ** 3):.2f} GB"
    
    def get_current_disk_usage_percent(self): # Returns the current disk usage in %
        disk = psutil.disk_usage('/')
        return f"{disk.percent}%"
    
    def get_current_disk_avable(self): # Returns the current disk avable in GB
        disk = psutil.disk_usage('/')
        return f"{disk.free / (1024 ** 3):.2f} GB"
    
    def get_current_disk_avable_percent(self): # Returns the current disk avable in %
        disk = psutil.disk_usage('/')
        return f"{100.0-disk.percent}%"
    
    def get_current_disk_read(self): # Returns the current disk read time
        return str(psutil.disk_io_counters().read_time)+"ms"
    
    def get_current_disk_write(self): # Returns the current disk write time
        return str(psutil.disk_io_counters().write_time)+"ms"
    
    def get_current_disk_partitions(self): # Returns the current disk partitions info (device, mountpoint, filesystem type)
        partitions = psutil.disk_partitions()
        partition_info = []

        for partition in partitions:
            partition_info.append(f"Device: {partition.device}, Mountpoint: {partition.mountpoint}, Fstype: {partition.fstype}")

        return partition_info
    
    def get_current_cpu_usage(self): # Returns the current CPU usage as a list of percentages (float) for each core
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)

        return cpu_usage
    
    def get_current_cpu_freq(self): # Returns the current CPU frequency in MHz as a list
        cpu = psutil.cpu_freq(percpu=True)
        
        cpuFreq = []

        for i in cpu:
            cpuFreq.append(str(i.current)+" MHz")

        return cpuFreq
    
    def get_current_memory_usage(self): # Returns the current memory usage in GB
        mem = psutil.virtual_memory()
        return f"{mem.used / (1024 ** 3):.2f} GB"
    
    def get_current_memory_usage_percent(self): # Returns the current memory usage in %
        mem = psutil.virtual_memory()
        return f"{mem.percent}%"
    
    def get_current_memory_avable(self): # Returns the current memory avable in GB
        mem = psutil.virtual_memory()
        return f"{mem.available / (1024 ** 3):.2f} GB"
    
    def get_current_memory_avable_percent(self): # Returns the current memory avable in %
        mem = psutil.virtual_memory()
        return f"{100.0-mem.percent}%"
    
    def get_battery_info(self): # Returns the battery information if available (Battery Percentage, Power Plugged, Time Left)
        if not psutil.sensors_battery():
            return "Battery information not available."
        else:
            battery = psutil.sensors_battery()

            battery_info = {
                "Battery Percentage": f"{battery.percent}%",
                "Power Plugged": battery.power_plugged,
                "Time Left": f"{battery.secsleft // 60} minutes" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Charging"
            }

            return battery_info
    
    def get_network_info(self): # Returns the network information (IP Address, MAC Address, Network Speed)
        network_info = psutil.net_if_addrs()
        interfacesInfo = []

        interfaceNames = network_info.keys()

        for interface in interfaceNames:
            if network_info[interface]:
                ip_address = "N/A"
                mac_address = "N/A"
                ipv6_address = "N/A"
            
                for setData in network_info[interface]:
                    if socket.AF_INET == setData.family:
                        # If the interface has an IP address
                        ip_address = setData.address
                    elif setData.family == getattr(socket, "AF_LINK", None) or \
                        setData.family == getattr(psutil, "AF_LINK", None) or \
                        setData.family == 17:
                        # If the interface has a MAC address
                        mac_address = setData.address
                    elif socket.AF_INET6 == setData.family:
                        # If the interface has an IPv6 address
                        ipv6_address = setData.address

                interfacesInfo.append([
                    str(interface),
                    "IP: "+str(ip_address),
                    "MAC: "+str(mac_address),
                    "IPv6: "+str(ipv6_address)
                ])

        return interfacesInfo if interfacesInfo else "No network interfaces found."