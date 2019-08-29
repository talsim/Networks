from scapy.all import *
from scapy.layers.inet import *


def main():
    msg = ''
    for i in range(0, 2):
        for port in range(0, 256):
            print(f'sniffing at port: {port}')
            packet = sniff(filter=f"port {port}", timeout=0.000001)
            if (UDP in packet):
                msg += chr(port)
        print(f'The client sent: {msg}')


if __name__ == '__main__':
    main()
