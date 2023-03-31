import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sgpacket
import time
import cmd
import re
from subprocess import check_output

# example transmitter
class SGPacketHelper(cmd.Cmd):
    intro = 'Use the helper to send packets. Type help or ? to list commands.\n'
    prompt = '<Cmd> '

    def do_TCP(self, arg):
        '''*************************************\nSend TCP packets: TCP [IP] [number]\nE.g., TCP 10.0.1.201 5\n*************************************'''
        send_TCP(*parse(arg))
    
    def do_UDP(self, arg):
        '''*************************************\nSend UDP packets: UDP [IP] [number]\nE.g., UDP 10.0.1.201 10\n*************************************'''
        send_UDP(*parse(arg))

    def do_MMS(self, arg):
        '''*************************************\nSend MMS packets: MMS [IP] [number]\nE.g., MMS 10.0.1.201 15\n*************************************'''
        send_MMS(*parse(arg))

    def do_GOOSE(self, arg):
        '''*************************************\nSend GOOSE packets: GOOSE [mac addr] [number]\nE.g., GOOSE 000000000011 20\n*************************************'''
        send_GOOSE(*parse(arg))

    def do_SV(self, arg):
        '''*************************************\nSend SV packets: SV [mac addr] [number]\nE.g., SV 000000000011 25\n*************************************'''
        send_SV(*parse(arg))

    def do_DNP3(self, arg):
        '''*************************************\nSend DNP3 packets: DNP3 [IP] [number]\nE.g., DNP3 10.0.1.201 15\n*************************************'''
        send_DNP3(*parse(arg))

    def do_XMPP(self, arg):
        '''*************************************\nSend XMPP packets: XMPP [IP] [number]\nE.g., XMPP 10.0.1.201 20\n*************************************'''
        send_XMPP(*parse(arg))
    
    def do_bye(self, arg):
        'Exit the helper:  bye'
        print('Bye.')
        return True
        
def send_TCP(ip, num, port=7000):
    t = sgpacket.Transmitter(sgpacket.PacketType.TCP, server_ip = ip, server_port = port)
    send_packets(t, num, 'TCP', ip, port)

def send_UDP(ip, num, port=7001):
    t = sgpacket.Transmitter(sgpacket.PacketType.UDP, server_ip = ip, server_port = port)
    send_packets(t, num, 'UDP', ip, port)

def send_MMS(ip, num, port=102):
    t = sgpacket.Transmitter(sgpacket.PacketType.MMS, server_ip = ip, server_port = port)
    send_packets(t, num, 'MMS', ip, port)

def send_GOOSE(mac, num):
    ipa = check_output(['ip', 'a']).decode('utf-8')
    ifce = re.findall(r': (.*eth0)@.*\n.*\n.*inet', ipa)[0]
    t = sgpacket.Transmitter(sgpacket.PacketType.GOOSE, ifce=ifce, dst_mac = mac)
    send_packets(t, num, 'GOOSE', mac)

def send_SV(mac, num):
    ipa = check_output(['ip', 'a']).decode('utf-8')
    ifce = re.findall(r': (.*eth0)@.*\n.*\n.*inet', ipa)[0]
    t = sgpacket.Transmitter(sgpacket.PacketType.SV, ifce=ifce, dst_mac = mac)
    send_packets(t, num, 'SV', mac)

def send_DNP3(ip, num, port=20000):
    t = sgpacket.Transmitter(sgpacket.PacketType.DNP3, server_ip = ip, server_port = port)
    # t = sgpacket.Transmitter(sgpacket.PacketType.TCP, server_ip = ip, server_port = port)
    send_packets(t, num, 'DNP3', ip, port)

def send_XMPP(ip, num, port=5222):
    t = sgpacket.Transmitter(sgpacket.PacketType.XMPP, server_ip = ip, server_port = port)
    send_packets(t, num, 'XMPP', ip, port)

def send_packets(t, num, pkt_type, addr, port=None):
    try:
        t.run()
        if pkt_type == 'DNP3':
            time.sleep(3)
            for i in range(num):
                t.send_one()
                time.sleep(3)
            time.sleep(3)
        else:
            for i in range(num):
                t.send_one()
                time.sleep(0.05)
        t.stop()
        t.join()
        sent_success(pkt_type, num, addr, port)
    except:
        t.stop()
        print('Transmitter stopped.')

def sent_success(pkt_type, num, addr, port=None):
    if port:
        print('Sent %d %s packets to %s:%s.' %(num, pkt_type, addr, port))
    else:
        print('Sent %d %s packets to %s.' %(num, pkt_type, addr))

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    addr, num = arg.split()
    return (addr, int(num))

if __name__ == '__main__':
    SGPacketHelper().cmdloop()
