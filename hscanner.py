#!/usr/bin/env python3

import socket
import platform
import subprocess
from termcolor import colored
import netifaces as ni
from collections import Counter
import time
import argparse
from rich.progress import track
from rich import print as print2
import socket
import ipaddress
from sys import platform as platform2
import os


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
        
        interface = ni.gateways()['default'][ni.AF_INET][1]
        masque_cidr = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']
    except:
        ip = '127.0.0.1'
    finally:
        s.close()
    return ip, masque_cidr

def convert_decimal_to_binary(ip):
    octets = ip.split(".")
    ipConverted = []
    for octet in octets:
        binaire = bin(int(octet))[2:].zfill(8)
        octetIP = ""
        for i in range(0, len(binaire), 4):
            octetIP += binaire[i:i+4] + " "
        ipConverted.append(binaire)
    
    return ''.join(ipConverted)


def generate_ips(ipv4, mask):
    ipv4 = convert_decimal_to_binary(ipv4)
    mask = convert_decimal_to_binary(mask)

    etlogique = []
    for i in range(8*4):
        if ipv4[i] == "1" and mask[i] == "1":
            etlogique.append("1")
        else:
            etlogique.append("0")

    res = mask.count("0")
    res = 2 ** res

    print(f"Network ip ({colored('Binary', attrs=['bold'])}):", colored("".join(etlogique), "red", attrs=['bold']))
    print(f"Network ip ({colored('Decimal', attrs=['bold'])}):", colored(socket.inet_ntoa(bytes(int("".join(etlogique)[i:i+8], 2) for i in range(0, 32, 8))), "red", attrs=['bold']))
    print("Available ip:",res)
    print(colored('='*50, "grey", attrs=['bold']))

    network_ip_decimal = str(socket.inet_ntoa(bytes(int("".join(etlogique)[i:i+8], 2) for i in range(0, 32, 8))))

    num_available_ips = res

    network_ip_octets = [int(octet) for octet in network_ip_decimal.split('.')]

    arrayresult.append("127.0.0.1")

    for i in range(num_available_ips):
        generated_ip_octets = [network_ip_octets[j] + (i >> (24 - j * 8) & 255) for j in range(4)]
        
        generated_ip_decimal = ".".join(map(str, generated_ip_octets))
        
        arrayresult.append(generated_ip_decimal)

def ping_ip(ip, timeout):
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    timeout = str(timeout)
    command = ['ping', param, '1', '-W', timeout, ip]

    if platform.system().lower() == 'windows':
        output_file = 'NUL'
    else:
        output_file = '/dev/null'

    time_counter = time.time()
    p = subprocess.call(command, stdout=open(output_file, 'w'), stderr=open(output_file, 'w'))
    time_counter = time.time() - time_counter

    return p, time_counter

def main(ip, timeout):
    p, timec = ping_ip(ip, timeout)

    if(p == 0):
        try:
            getHostName = socket.gethostbyaddr(ip)[0]
            output = (
                '[bold green][+][/bold green]'
                f'[italic green] [{timec:.3f}s][/italic green]'
                f'[bold white] {str(ip)} [/bold white]'
                ' Host is up'
                f'[yellow] {str(getHostName)}[/yellow]'
            )
        except:
            output = (
                '[bold yellow][\][/bold yellow]'
                f'[bold white] {str(ip)} [/bold white]'
                ' Host is up'
                f'[yellow] ~UNKNOW~[/yellow]'
            )
        print2(output, '[bold bright_black] (YOU)[/bold bright_black]' if str(ip) == str(iphost) else '')
        res = "up"
    else:
        res = "down"

    return res

def ipScanner(host, value, timeout):
    global arrayresult
    total = 0
    up = 0
    down = 0

    arrayresult = []
    w = value

    arrayresult = []
    generate_ips(host, value)

    prog_bar = len(arrayresult)

    try:
        if(not args.ip):
            for ip in track(arrayresult, description="Scanning..."):
                func = main(ip, timeout)
                total = total+1
                if(func == "up"):
                    up = up+1
                    if args.p:
                        a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        # a_socket.settimeout(0.1)
                        for i in range(65535):
                            location = (ip, i)
                            try:
                                result_of_check = a_socket.connect_ex(location)
                            
                                if result_of_check == 0:
                                    print2(f"[bright_black]↪ Port {i} is open.[/bright_black]")
                            except socket.error as e:
                                print(f"Connection failed :/ : {e}")
                                a_socket.close()
                            
                        a_socket.close()
                elif(func == "down"):
                    down = down+1
        else:
            a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            a_socket.settimeout(2)
            for i in track(range(65535), description="Processing"):
                location = (args.ip, i)
                total = total + 1
                try:
                    result_of_check = a_socket.connect_ex(location)
                
                    if result_of_check == 0:
                        output = (
                            '[bold green][+][/bold green]'
                            ' Port'
                            f'[bold white] {int(i)} [/bold white]'
                            'is opened on'
                            f'[yellow] {str(args.ip)}[/yellow]'
                        )
                        print2(output)
                        up = up + 1
                    else:
                        down = down + 1
                except socket.error as e:
                    print(f"Connection failed :/ : {e}")  
                    a_socket.close()
                      
            a_socket.close()

    except KeyboardInterrupt:
        print("\nScript interrupted by user.")

    return up, down, total

if "__main__" == __name__:
    print("""██╗  ██╗███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ \n██║  ██║██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗\n███████║███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝\n██╔══██║╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗\n██║  ██║███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║\n╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
""")
    print(colored("Made by Hoag.", "green", attrs=['bold']))
    print(colored("Version: 1.2.1", "yellow", attrs=['bold']))
    print(colored('='*50, "grey", attrs=['bold']))

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, default=0.2, help='Time-out in seconds per ip tested. (Default: 0.2)')
    parser.add_argument('-p', action='store_true', help='Scan open ports on hosts (BETA)')
    parser.add_argument('--ip', type=str, help='Scan open ports of machine')
    args = parser.parse_args()
    
    if args.ip and not args.p:
        parser.error("--ip requires -p")
    elif args.ip and args.p:
       args.ip = str(ipaddress.ip_address(args.ip))

    print(colored("SELECTED ARGUMENTS:", attrs=['bold']))
    if args.t != 0.2:
        print(f"{colored('[+]', 'green', attrs=['bold'])} Custom timeout: {args.t}s")
    if args.p:
        print(f"{colored('[+]', 'green', attrs=['bold'])} Scan open ports on hosts")
    if args.ip:
        print(f"{colored('[+]', 'green', attrs=['bold'])} Scan open ports on {args.ip}")
    if not args.p and args.t == 0.2 and not args.ip:
        print(f"{colored('[-]', 'red', attrs=['bold'])} NONE")

    print("\n")

    try:
        ping_ip("https://google.com", 0.2)
    except:
        if platform2 == "linux" or platform2 == "linux2":
            exit(f"{colored('[-]', 'red', attrs=['bold'])} The ping command doesn't work. Try: {colored('sudo apt-get install -y iputils-ping', attrs=['bold'])}")

    iphost, mask = get_local_ip()
    print(f"IpV4 ({colored('Binary', attrs=['bold'])}): ",colored(convert_decimal_to_binary(iphost), "green", attrs=['bold']))
    print(f"IpV4 ({colored('Decimal', attrs=['bold'])}): ",colored(iphost, "green", attrs=['bold']))
    print(f"Subnet mask ({colored('Binary', attrs=['bold'])}): ",colored(convert_decimal_to_binary(mask), "yellow", attrs=['bold']))
    print(f"Subnet mask ({colored('Decimal', attrs=['bold'])}): ",colored(mask, "yellow", attrs=['bold']),"\n")

    n255 = Counter(list(str(mask).replace(".", " ").split(" ")))['255']
    n0 = Counter(list(str(mask).replace(".", " ").split(" ")))['0']
    
    ip2 = list(str(iphost).replace(".", " ").split(" "))
    ip2 = ip2[:-n0]
    ip2 = ".".join(ip2)
    
    start_time = time.time()
    result = ipScanner(iphost, mask, args.t)

    print(colored('='*50, "grey", attrs=['bold']))
    print('RESULT :')
    print(colored(result[2], "cyan", attrs=['bold']), f"{'hosts' if not args.p else 'ports'} were tested in {colored(time.time() - start_time, 'white', attrs=['bold'])} seconds.")
    print(colored(result[0], "green", attrs=['bold']), f"{'hosts' if not args.p else 'ports'} {'are' if result[0] > 1 else 'is'} up.")
    print(colored(result[1], "red", attrs=['bold']), f"{'hosts' if not args.p else 'ports'} {'are' if result[1] > 1 else 'is'} down.")
    exit()
