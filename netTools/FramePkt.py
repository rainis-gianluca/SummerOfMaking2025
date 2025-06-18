# netTools/FramePkt.py
# This module defines the FramePkt class, which is responsible for preparing and sending ARP frames over a network.
# This project is under the GNU General Public License v3.0 (GPL-3.0).

from scapy.all import Ether, ARP, srp
from ipaddress import ip_address
from socket import gethostbyname
import ipaddress

class FramePkt:
    networkIp = None  # Network IP
    destinationIp = None  # Destination IP
    subnetMask = None  # Subnet mask
    arp = None  # ARP layer
    ether = None  # Ethernet layer
    frame = None  # Frame to send
    stopProcess = False  # Flag to stop the process

    def __init__(self):
        self.networkIp = None
        self.destinationIp = None
        self.subnetMask = None
        self.arp = None
        self.ether = None
        self.frame = None
        self.stopProcess = False

    @staticmethod
    def is_valid_ip(ip_str):
        try:
            ip_address(ip_str)
            return True
        except ValueError:
            return False
        
    @staticmethod
    def is_valid_DNS(name):
        try:
            gethostbyname(name)
            return True
        except Exception:
            return False

    def prepare_frame(self):
        try:
            if self.networkIp is None:
                raise Exception("Error: Network IP is not set.")
            
            if self.subnetMask is None:
                raise Exception("Error: Subnet mask is not set.")
            else:
                subnet = sum(bin(int(i)).count('1') for i in self.subnetMask.split('.'))
                net = ipaddress.ip_network(f"{self.networkIp}/{subnet}", strict=False)
                
                if ipaddress.ip_address(self.networkIp) != net.network_address:
                    self.networkIp = str(net.network_address)
                else:
                    self.networkIp = self.networkIp
            
            if self.destinationIp is None:
                self.destinationIp = self.networkIp
            
            self.arp = ARP(pdst=self.destinationIp)
            self.ether = Ether(dst="ff:ff:ff:ff:ff:ff")
            self.frame = self.ether / self.arp
        except Exception as e:
            raise Exception(f"Error preparing frame: {e}")

    def send_frame(self, log_callback=None, arp_callback=None):
        subnet = 0

        for i in (self.subnetMask).split('.'):
            subnet += bin(int(i)).count('1')

        network = ipaddress.ip_network(f"{self.networkIp}/{subnet}", strict=False)
        scanned_ips = set()

        log_callback(f"Network: {network}")

        for ip in network.hosts():
            if self.stopProcess:
                log_callback("Process stopped by user.")
                return

            if str(ip) not in scanned_ips:
                try:
                    self.set_destinationIp(str(ip))
                    self.prepare_frame()
                except Exception as e:
                    if log_callback:
                        log_callback(f"Error preparing frame for {ip}: {e}")
                    else:
                        raise Exception(f"Error preparing frame for {ip}: {e}")

                try:
                    answered, unanswered = srp(self.frame, timeout=1, verbose=0)

                    if answered:
                        for sent, received in answered:
                            if arp_callback:
                                arp_callback(f"IP: {received.psrc} | MAC: {received.hwsrc}")
                    else:
                        if arp_callback:
                            arp_callback(f"IP: {self.get_destinationIp()} | MAC: NULL")
                except Exception as e:
                    if log_callback:
                        log_callback(f"Error sending frame: {e}")
                    else:
                        raise Exception(f"Error sending frame: {e}")
                    
                scanned_ips.add(str(ip))

        if log_callback and arp_callback: # log_callback to print logs on a Text label, arp_callback to print the arp response on a Text label. You can use print() instead.
            log_callback("Frame sending completed.")
        else:
            raise Exception("Frame sending completed without log/arp callback.")

    # GETTERS AND SETTERS
    def get_networkIp(self):
        return self.networkIp
    
    def get_destinationIp(self):
        return self.destinationIp
    
    def get_subnetMask(self):
        return self.subnetMask
    
    def get_arp(self):
        return self.arp
    
    def get_ether(self):
        return self.ether
    
    def get_frame(self):
        return self.frame
    
    def get_stopProcess(self):
        return self.stopProcess
    
    def set_networkIp(self, networkIp):
        if self.is_valid_ip(networkIp):
            self.networkIp = networkIp
        elif self.is_valid_DNS(networkIp):
            self.networkIp = gethostbyname(networkIp)
        else:
            raise ValueError("Invalid IP address or DNS name.")

    def set_destinationIp(self, destinationIp):
        if self.is_valid_ip(destinationIp):
            self.destinationIp = destinationIp
        elif self.is_valid_DNS(destinationIp):
            self.destinationIp = gethostbyname(destinationIp)
        else:
            raise ValueError("Invalid IP address or DNS name.")
        
    def set_subnetMask(self, subnetMask):
        if self.is_valid_ip(subnetMask):
            # Validate subnet mask
            try:
                foundZero = False

                for i in subnetMask.split('.'):
                    for bit in str(bin(int(i))[2:].zfill(8)):
                        if bit == '1':
                            if foundZero:
                                raise ValueError("Invalid subnet mask: 1s must be contiguous.")
                        else:
                            foundZero = True

                self.subnetMask = subnetMask
            except Exception as e:
                raise ValueError(f"Invalid subnet mask: {e}")
        else:
            raise ValueError("Invalid subnet mask.")
        
    def set_arp(self, arp):
        if isinstance(arp, ARP):
            self.arp = arp
        else:
            raise ValueError("Invalid ARP layer.")
        
    def set_ether(self, ether):
        if isinstance(ether, Ether):
            self.ether = ether
        else:
            raise ValueError("Invalid Ethernet layer.")
        
    def set_frame(self, frame):
        if isinstance(frame, Ether):
            self.frame = frame
        else:
            raise ValueError("Invalid frame.")
        
    def set_stopProcess(self, stopProcess):
        if isinstance(stopProcess, bool):
            self.stopProcess = stopProcess
        else:
            raise ValueError("stopProcess must be a boolean value.")