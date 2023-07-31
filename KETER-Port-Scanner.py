import socket
import threading
import logging
from queue import Queue
from datetime import datetime
import argparse



print('''
KKKKKKKKK    KKKKKKEEEEEEEEEEEEEEEEEEEEETTTTTTTTTTTTTTTTTTTTTTEEEEEEEEEEEEEEEEEEEEERRRRRRRRRRRRRRRRR        
K:::::::K    K:::::E::::::::::::::::::::T:::::::::::::::::::::E::::::::::::::::::::R::::::::::::::::R       
K:::::::K    K:::::E::::::::::::::::::::T:::::::::::::::::::::E::::::::::::::::::::R::::::RRRRRR:::::R      
K:::::::K   K::::::EE::::::EEEEEEEEE::::T:::::TT:::::::TT:::::EE::::::EEEEEEEEE::::RR:::::R     R:::::R     
KK::::::K  K:::::KKK E:::::E       EEEEETTTTTT  T:::::T  TTTTTT E:::::E       EEEEEE R::::R     R:::::R     
  K:::::K K:::::K    E:::::E                    T:::::T         E:::::E              R::::R     R:::::R     
  K::::::K:::::K     E::::::EEEEEEEEEE          T:::::T         E::::::EEEEEEEEEE    R::::RRRRRR:::::R      
  K:::::::::::K      E:::::::::::::::E          T:::::T         E:::::::::::::::E    R:::::::::::::RR       
  K:::::::::::K      E:::::::::::::::E          T:::::T         E:::::::::::::::E    R::::RRRRRR:::::R      
  K::::::K:::::K     E::::::EEEEEEEEEE          T:::::T         E::::::EEEEEEEEEE    R::::R     R:::::R     
  K:::::K K:::::K    E:::::E                    T:::::T         E:::::E              R::::R     R:::::R     
KK::::::K  K:::::KKK E:::::E       EEEEEE       T:::::T         E:::::E       EEEEEE R::::R     R:::::R     
K:::::::K   K::::::EE::::::EEEEEEEE:::::E     TT:::::::TT     EE::::::EEEEEEEE:::::RR:::::R     R:::::R     
K:::::::K    K:::::E::::::::::::::::::::E     T:::::::::T     E::::::::::::::::::::R::::::R     R:::::R     
K:::::::K    K:::::E::::::::::::::::::::E     T:::::::::T     E::::::::::::::::::::R::::::R     R:::::R     
KKKKKKKKK    KKKKKKEEEEEEEEEEEEEEEEEEEEEE     TTTTTTTTTTT     EEEEEEEEEEEEEEEEEEEEERRRRRRRR     RRRRRRR     

Made by azor_4e / Azor#1100

Github: https://github.com/AzrDll


''')







def get_arguments():
    parser = argparse.ArgumentParser(description="Python Port Scanner")
    parser.add_argument("-H", "--host", type=str, required=True, help="Target host (IP or domain)")
    parser.add_argument("-m", "--mode", type=int, choices=[1, 2, 3], required=True, help="Scan mode (1: ports 1-1024, 2: ports 1-65535, 3: custom)")
    parser.add_argument("-s", "--start", type=int, help="Start port for custom scan")
    parser.add_argument("-e", "--end", type=int, help="End port for custom scan")
    return parser.parse_args()

def get_port_range(mode, start=None, end=None):
    if mode == 1:
        return 1, 1024
    elif mode == 2:
        return 1, 65535
    elif mode == 3:
        if start is None or end is None:
            raise ValueError("Start and end ports must be specified for custom scan")
        if start >= end:
            raise ValueError("Start port must be less than end port")
        return start, end

def scan(host, port):
    try:
        with socket.socket() as s:
            s.settimeout(5)
            result = s.connect_ex((host, port))
            if result == 0:
                return True
    except Exception as e:
        logging.error(f"Error scanning port {port}: {e}")
    return False

def worker(host, queue, open_ports, lock, completed, port_start, port_end):
    while True:
        port = queue.get()
        if port is None:
            break
        if scan(host, port):
            logging.info(f"Port {port} is open...")
            with lock:
                open_ports.append(port)
        with lock:
            completed[0] += 1
            print_progress_bar(completed[0], port_end - port_start + 1)
        queue.task_done()

def print_progress_bar(completed, total, length=50):
    fill = '█' * int(length * completed // total)
    empty = '-' * (length - len(fill))
    print(f'\rProgress: |{fill}{empty}| {completed}/{total} ports scanned', end='')

def run_scanner(host, port_start, port_end, threads):
    queue = Queue()
    open_ports = []
    lock = threading.Lock()
    completed = [0]

    for port in range(port_start, port_end+1):
        queue.put(port)

    for _ in range(threads):
        threading.Thread(target=worker, args=(host, queue, open_ports, lock, completed, port_start, port_end)).start()

    try:
        queue.join()
    except KeyboardInterrupt:
        print("\nInterrupted, stopping scan...")
    finally:
        # Insert sentinel tasks to stop the workers
        for _ in range(threads):
            queue.put(None)
        return open_ports

def main():
    args = get_arguments()
    host = socket.gethostbyname(args.host)
    port_start, port_end = get_port_range(args.mode, args.start, args.end)

    print(f"Target IP: {host}")
    print("Scanning started at:" + str(datetime.now()))

    open_ports = run_scanner(host, port_start, port_end, 200)

    print("\nScanning complete at:" + str(datetime.now()))
    print(f"Open ports: {open_ports}")

if __name__ == "__main__":
    main()
