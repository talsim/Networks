from scapy.all import *
from scapy.layers.inet import *
import time

ip = '127.0.0.1'


def main():
    print('started')
    while True:
        msg = input('Please enter your message: ')
        for char in msg:
            send(IP(dst=ip) / UDP(dport=ord(char)) / Raw(load=' '))
            time.sleep(0.00001)


if __name__ == '__main__':
    main()
