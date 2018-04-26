from scapy.all import *
import socket
import datetime

file_dump = "sniffy.dump"
if os.path.exists(file_dump) != True:
	open(file_dump,'w').close()

def find_dns_requests(pkt):
	if pkt.haslayer(DNS) and pkt.getlayer(DNS).qr == 0:
		with open(file_dump,"a") as handle:
			handle.write(str(datetime.datetime.now()) + " --- " + str(pkt.getlayer(DNS).qd.qname) + "\n")
		print str(pkt.getlayer(DNS).qd.qname)

sniff(iface="eth0", prn = find_dns_requests, filter = 'dst port 53 ',store=0)
