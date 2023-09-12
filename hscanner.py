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


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Connexion à une adresse IP inexistante pour déterminer l'adresse IP locale
        s.connect(('10.255.255.255', 1))
        ip = s.getsockname()[0]
        
        # Obtenir les informations sur l'interface réseau associée à l'adresse IP
        interface = ni.gateways()['default'][ni.AF_INET][1]
        masque_cidr = ni.ifaddresses(interface)[ni.AF_INET][0]['netmask']
    except:
        ip = '127.0.0.1'  # Utilisez une valeur par défaut en cas d'échec
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
    print("="*50)

    # Adresse IP du réseau en décimal
    network_ip_decimal = str(socket.inet_ntoa(bytes(int("".join(etlogique)[i:i+8], 2) for i in range(0, 32, 8))))

    # Nombre d'adresses IP disponibles
    num_available_ips = res

    # Convertir l'adresse IP du réseau en une liste d'octets
    network_ip_octets = [int(octet) for octet in network_ip_decimal.split('.')]

    arrayresult.append("127.0.0.1")

    # Générer toutes les adresses IP possibles dans la plage
    for i in range(num_available_ips):
        # Ajouter l'indice actuel à chaque octet de l'adresse IP du réseau
        generated_ip_octets = [network_ip_octets[j] + (i >> (24 - j * 8) & 255) for j in range(4)]
        
        # Convertir les octets générés en format décimal
        generated_ip_decimal = ".".join(map(str, generated_ip_octets))
        
        arrayresult.append(generated_ip_decimal)


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
        for ip in track(arrayresult, description="Processing"):
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            timeout = str(timeout)
            command = ['ping', param, '1', '-W', timeout, ip]

            # Rediriger la sortie vers /dev/null ou NUL
            if platform.system().lower() == 'windows':
                output_file = 'NUL'
            else:
                output_file = '/dev/null'

            p = subprocess.call(command, stdout=open(output_file, 'w'), stderr=open(output_file, 'w'))
            
            if(p == 0):
                getHostName = socket.gethostbyaddr(ip)[0]
                output = (
                    '[bold green][+][/bold green]'
                    f'[bold white] {str(ip)} [/bold white]'
                    ' Host is up'
                    f'[yellow] {str(getHostName)}[/yellow]'
                )
                #print(colored("[+]", "green", attrs=['bold']), colored(ip, attrs=['bold']), " Host is up", colored(getHostName, "yellow", attrs=['dark', "bold"]), colored("(YOU)", "grey", attrs=['bold']) if str(ip) == str(iphost) else '')
                print2(output, '[bold bright_black] (YOU)[/bold bright_black]' if str(ip) == str(iphost) else '')
                up = up+1
            else:
                #print(colored("[-]", "red", attrs=['bold']), colored(ip, attrs=['bold']), " Host is down")
                down = down+1
            
            total = total+1

    except KeyboardInterrupt:
        print("\nScript interrupted by user.")

    return up, down, total

if "__main__" == __name__:
    print("""██╗  ██╗███████╗ ██████╗ █████╗ ███╗   ██╗███╗   ██╗███████╗██████╗ \n██║  ██║██╔════╝██╔════╝██╔══██╗████╗  ██║████╗  ██║██╔════╝██╔══██╗\n███████║███████╗██║     ███████║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝\n██╔══██║╚════██║██║     ██╔══██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗\n██║  ██║███████║╚██████╗██║  ██║██║ ╚████║██║ ╚████║███████╗██║  ██║\n╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝
""")
    print(colored("Made by Hoag.", "green", attrs=['bold']))
    print(colored("Version: 1.0", "yellow", attrs=['bold']))
    print("="*50)

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, default=0.2, help='Time-out in seconds per ip tested. (Default: 0.2)')
    args = parser.parse_args()

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

    print('='*50)
    print('RESULT :')
    print(colored(result[2], "cyan", attrs=['bold']), f"host{'s' if result[2] > 1 else ''} were tested in {colored(time.time() - start_time, 'white', attrs=['bold'])} seconds.")
    print(colored(result[0], "green", attrs=['bold']), f"host{'s' if result[0] > 1 else ''} {'are' if result[0] > 1 else 'is'} up.")
    print(colored(result[1], "red", attrs=['bold']), f"host{'s' if result[1] > 1 else ''} {'are' if result[1] > 1 else 'is'} down.")
    exit()
