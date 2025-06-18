# netTools/Packet.py
# This is a Python module for creating and sending TCP packets using Scapy.
# This project is under the GNU General Public License v3.0 (GPL-3.0).

from scapy.all import IP, TCP, send, Raw, sr1, get_if_addr, conf
from ipaddress import ip_address
from socket import gethostbyname

class Packet():
    destinationIp = None #Destination IP
    destinationPort = None #Destination Port
    sourceIp = None #Source IP
    sourcePort = None #Source Port
    ttl = None #Time to live
    message = None #Message to send
    numberPackets = None #Number of packets to send
    payload_len = None #Message length
    syn_ack = None #SYN-ACK packet
    pkt = None #Packet to send
    ip = None #IP layer
    tcp = None #TCP layer
    data = None #Data layer

    def __init__(self):
        self.destinationIp = None
        self.destinationPort = None
        self.sourceIp = None
        self.sourcePort = None
        self.ttl = None
        self.message = None
        self.numberPackets = None
        self.payload_len = None
        self.syn_ack = None
        self.pkt = None
        self.ip = None
        self.tcp = None
        self.data = None

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
        
    def connect(self):
        if self.destinationIp is None or self.destinationPort is None or self.sourceIp is None or self.sourcePort is None:
            raise Exception("Error: Missing required parameters.")

        #SYN, SYN-ACK, ACK
        print("Sending SYN...")
        try:
            syn = IP(src=self.sourceIp, dst=self.destinationIp)/TCP(sport=self.sourcePort, dport=self.destinationPort, flags="S", seq=1000)
            self.syn_ack = sr1(syn, timeout=2)

            if self.sourceIp == get_if_addr(conf.iface).strip():
                if self.syn_ack is None or self.syn_ack[TCP].flags != "SA":
                    print("Connection failed.")
                    raise Exception()
                else:
                    print("Recived SYN-ACK")
            else:
                print("Warning: The source IP is not the same as the interface IP. This may cause issues with the connection.")
                print("Sended SYN, the destination may not respond correctly.")
        except Exception as e:
            raise Exception("Error: "+e.__str__())
        
        if self.sourceIp == get_if_addr(conf.iface).strip():
            try:
                seq_ack = self.syn_ack.seq+1
                ack = IP(src=self.sourceIp, dst=self.destinationIp) / TCP(sport=self.sourcePort, dport=self.destinationPort, flags="A", seq=syn.seq+1, ack=self.syn_ack.seq+1)

                print("Sending ACK...")
                send(ack)
            except Exception as e:
                print("Connection failed.")
                raise Exception("Error: "+e.__str__())

            print("Connected.")
        else:
            print("Warning: The source IP is not the same as the interface IP. This may cause issues with the connection.")
            print("Try to send the packet anyway.")

    def prepare_packet(self):
        if self.destinationIp is None or self.destinationPort is None or self.sourceIp is None or self.sourcePort is None or self.ttl is None or self.syn_ack is None:
            raise Exception("Error: Missing required parameters.")

        try:
            self.ip = IP()
            self.tcp = TCP()
        except Exception as e:
            raise Exception("Error: "+e.__str__())
    
        try:
            self.ip.src = self.sourceIp
            self.ip.dst = self.destinationIp
            self.ip.ttl = self.ttl

            self.tcp.sport = self.sourcePort
            self.tcp.dport = self.destinationPort
            self.tcp.flags = "PA"
            self.tcp.seq = 1001

            if self.sourceIp == get_if_addr(conf.iface).strip():
                self.tcp.ack = self.syn_ack.seq + 1
            else:
                self.tcp.ack = 1
        except Exception as e:
            raise Exception("Error: "+e.__str__())

        try:
            self.data = Raw(load=self.message)
        except Exception as e:
            raise Exception("Error: "+e.__str__())

        try:
            self.pkt = self.ip / self.tcp / self.data
        except Exception as e:
            raise Exception("Error: "+e.__str__())
        
    def send_packets(self):
        if self.destinationIp is None or self.destinationPort is None or self.numberPackets is None or self.payload_len is None or self.pkt is None or self.ip is None or self.tcp is None or self.data is None:
            raise Exception("Error: Missing required parameters.")

        tempPacketSended = 0

        try:
            while self.numberPackets != 0:
                resp = sr1(self.pkt, timeout=2, verbose=0)
                self.numberPackets -= 1
                tempPacketSended += 1
                print("Sent packet "+str(tempPacketSended)+" to "+str(self.destinationIp)+":"+str(self.destinationPort))
                print("Response: "+str(resp))

                self.tcp.seq += self.payload_len
                self.pkt = self.ip / self.tcp / self.data
        except Exception as e:
            raise Exception("Error: "+e.__str__())
        
    # GETTERS AND SETTERS
    def get_destination_ip(self):
        return self.destinationIp

    def get_destination_port(self):
        return self.destinationPort
    
    def get_source_ip(self):
        return self.sourceIp
    
    def get_source_port(self):
        return self.sourcePort
    
    def get_ttl(self):
        return self.ttl
    
    def get_message(self):
        return self.message
    
    def get_number_packets(self):
        return self.numberPackets
    
    def get_payload_length(self):
        return self.payload_len
    
    def get_syn_ack(self):
        return self.syn_ack
    
    def get_packet(self):
        return self.pkt
    
    def get_ip(self):
        return self.ip
    
    def get_tcp(self):
        return self.tcp
    
    def get_data(self):
        return self.data

    def set_destination_ip(self, ip):
        if self.is_valid_ip(ip):
            self.destinationIp = ip
        elif self.is_valid_DNS(ip):
            self.destinationIp = gethostbyname(ip)
        else:
            raise ValueError("Invalid IP address.")
    
    def set_destination_port(self, port):
        if port.isnumeric() and 0 < int(port) <= 65535:
            self.destinationPort = int(port)
        else:
            raise ValueError("Invalid port number.")
        
    def set_source_ip(self, ip):
        if self.is_valid_ip(ip):
            self.sourceIp = ip
        elif self.is_valid_DNS(ip):
            self.sourceIp = gethostbyname(ip)
        else:
            raise ValueError("Invalid IP address.")
    
    def set_source_port(self, port):
        if port.isnumeric() and 0 < int(port) <= 65535:
            self.sourcePort = int(port)
        else:
            raise ValueError("Invalid port number.")
        
    def set_ttl(self, ttl:int):
        if 0 < ttl <= 255:
            self.ttl = ttl
        else:
            raise ValueError("Invalid TTL.")
        
    def set_message(self, message:str):
        if isinstance(message, str):
            self.message = message
        else:
            raise ValueError("Message must be a string.")
    
    def set_number_packets(self, number:int):
        if number == -1 or number >= 0:
            self.numberPackets = int(number)
        else:
            raise ValueError("Invalid number of packets.")
        
    def set_payload_length(self, length:int):
        if isinstance(length, int) and length >= 0:
            self.payload_len = length
        else:
            raise ValueError("Payload length must be a non-negative integer.")
        
    def set_syn_ack(self, syn_ack):
        if syn_ack is not None:
            self.syn_ack = syn_ack
        else:
            raise ValueError("SYN-ACK packet cannot be None.")
        
    def set_packet(self, packet):
        if packet is not None:
            self.pkt = packet
        else:
            raise ValueError("Packet cannot be None.")
        
    def set_ip(self, ip):
        if isinstance(ip, IP):
            self.ip = ip
        else:
            raise ValueError("IP must be an instance of scapy.all.IP.")
        
    def set_tcp(self, tcp):
        if isinstance(tcp, TCP):
            self.tcp = tcp
        else:
            raise ValueError("TCP must be an instance of scapy.all.TCP.")
        
    def set_data(self, data):
        if isinstance(data, Raw):
            self.data = data
        else:
            raise ValueError("Data must be an instance of scapy.all.Raw.")