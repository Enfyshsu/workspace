#!/usr/bin/python3
import docker
import re
import os
import colorama
import sshtunnel
from colorama import Fore, Back, Style
from tabulate import tabulate
from time import sleep



class SGHelper():

    def __init__(self):
        colorama.init(autoreset=True)
        self.docker_client = docker.from_env()
        self.container_ifces, self.SG_VPN_hosts = self.__container_network_parser()
        

    def is_SG_host(self, container_name):
        return re.match(r'^mn\.[a-zA-Z0-9]*$', container_name) is not None

    def __container_network_parser(self):
        res_container_ifces = {} # {container_name:{ifce_name:ip}}
        res_SG_VPN_hosts = {} #{container_name: docker_bridge_ip}
        for container in self.docker_client.containers.list():
            ip_a = container.exec_run(cmd='ip a').output.decode('utf-8')
            ifces = re.findall(r': (.*)@.*\n.*\n.*inet (.*)/', ip_a)
            res_container_ifces[container.name] = ifces
            
            # if the container has bridge and it's a SG host, then it's a SG VPN host
            if 'bridge' in container.attrs["NetworkSettings"]["Networks"] and self.is_SG_host(container.name):
                res_SG_VPN_hosts[container.name] = container.attrs["NetworkSettings"]["Networks"]["bridge"]["IPAddress"]

        return res_container_ifces, res_SG_VPN_hosts


    def __SG_forwarder(self, vpn_container, target_container, local_port, remote_port):
        with sshtunnel.open_tunnel(
            ssh_address_or_host = (self.SG_VPN_hosts[vpn_container], 22),
            ssh_username = 'root',
            ssh_password = 'test',
            remote_bind_address = (self.container_ifces[target_container][0][1], remote_port),
            local_bind_address = ('0.0.0.0', local_port)
        ) as server:
            print('Forwarding', target_container + '('+ self.container_ifces[target_container][0][1] +'):' + str(remote_port) + ' to localhost:' + str(local_port) + ' by ' + vpn_container + '(' + self.SG_VPN_hosts[vpn_container] + ') ...')
            print('Please press Ctrl + C to exit.')
            try:
                while True:
                    sleep(1)
            except KeyboardInterrupt:
                pass

    def list_containers(self):
        container_ifces = self.container_ifces
        
        SGcons = []
        othercons = []
        for name in container_ifces:
            ifces_str = ""
            for ifce in container_ifces[name]:
                ifces_str += '{:10}'.format(ifce[0]) # interface name
                ifces_str += '{:15}'.format(ifce[1]) # interface ip
                ifces_str += '\n'
            ifces_str = ifces_str[:-1]

            # Is SG host or not
            if self.is_SG_host(name):
                # Is VPN host or not
                if name in self.SG_VPN_hosts:
                    SGcons.append([name, ifces_str, u'\u2705'])
                else:
                    SGcons.append([name, ifces_str, u'\u274C'])
            else:
                othercons.append([name, ifces_str])

        print(Fore.GREEN + 'Found SG Containernet Hosts:')
        SG_headers = ['Container', 'Interfaces & IP Addr', 'VPN Host']
        print(tabulate(SGcons, SG_headers, tablefmt='rounded_grid'))
        
        print(Fore.BLUE + 'Found Another Containers:')
        other_headers = ['Container', 'Interfaces & IP Addr']
        print(tabulate(othercons, other_headers, tablefmt='rounded_grid'))

                

    def SG_wireshark_forwarder(self, vpn_container, target_container, local_port):
        self.__SG_forwarder(vpn_container, target_container, local_port, remote_port = 3000)

    def SG_ssh_forwarder(self, vpn_container, target_container, local_port):
        self.__SG_forwarder(vpn_container, target_container, local_port, remote_port = 22)
    
    
 

if __name__ == '__main__':
    helper = SGHelper()
    #helper.list_containers()
    #helper.SG_ssh_forwarder('mn.vpn', 'mn.d2', 3000)
    while True:
        os.system('clear')
        print(Fore.GREEN + 'Wellcome to SG Container Helper!!!')
        print('1. List SG containers.')
        print('2. Forward SG Host\'s SSH service to local port.')
        print('3. Forward SG Host\'s Wireshark GUI to local port.')
        print('4. Exit.')
        
        option = int(input(">> "))
        
        if option == 1:
            helper.list_containers()
            input("Press anykey to go menu.")

        elif option == 2:
            vpn_container = input('Select VPN container: ')
            while vpn_container not in helper.SG_VPN_hosts:
                print('Please select a VPN container in', list(helper.SG_VPN_hosts.keys()))
                vpn_container = input('Select VPN container: ')

            target_container = input('Select target container: ')
            while target_container not in helper.container_ifces:
                print('Container not found.')
                target_container = input('Select target container: ')
            
            while not helper.is_SG_host(target_container):
                print('The container is not a SG host.')
                target_container = input('Select target container: ')

            local_port = int(input('Select local binding port: '))

            os.system('clear')
            helper.SG_ssh_forwarder(vpn_container, target_container, local_port)

        elif option == 3:
            vpn_container = input('Select VPN container: ')
            while vpn_container not in helper.SG_VPN_hosts:
                print('Please select a VPN container in', list(helper.SG_VPN_hosts.keys()))
                vpn_container = input('Select VPN container: ')

            target_container = input('Select target container: ')
            while target_container not in helper.container_ifces:
                print('Container not found.')
                target_container = input('Select target container: ')
            
            while not helper.is_SG_host(target_container):
                print('The container is not a SG host.')
                target_container = input('Select target container: ')

            local_port = int(input('Select local binding port: '))

            os.system('clear')
            helper.SG_wireshark_forwarder(vpn_container, target_container, local_port)

        else:
            print('Bye.')
            break
