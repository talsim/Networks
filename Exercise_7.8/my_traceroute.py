from scapy.all import IP, sr1, ICMP
from time import sleep
import sys

MAX_TTL = 255  # by standard


def main():
    print("\t\t\t\tHello! This is a traceroute that was made by Tal. AKA Bugamer :]")
    sleep(1)

    if len(sys.argv) < 2:
        print("\nPlease provide the target domain.")
        return
    target = sys.argv[1]
    routers = []

    for ttl in range(1, MAX_TTL):
        packet = IP(ttl=ttl, dst=target) / ICMP()
        response = sr1(packet, timeout=3)

        if response is not None:
            delta_time = round((response.time - packet.sent_time) * 1000.0, 3)
            routers.append(f'{delta_time} ms  {response[IP].src}')
            if response[ICMP].type == 0:  # if it's a ICMP reply (which means we reached target)
                routers[len(routers) - 1] += f" -> {target}"  # adding the domain when we reach target
                break
        else:
            routers.append("Unreachable")

    i = 1
    for addr in routers:
        if i < 10:
            print(f'  {i}   {addr}')
        elif i < 100:
            print(f' {i}   {addr}')
        else:
            print(f'{i}   {addr}')
        i += 1


if __name__ == '__main__':
    main()
