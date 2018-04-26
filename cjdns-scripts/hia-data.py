#!/usr/bin/python

import time
import urllib2
import sys
import json
sys.path.append("/opt/cjdns/contrib/python/")
import cjdnsadmin.adminTools as at
from cjdnsadmin.publicToIp6 import PublicToIp6_convert;

cjdns=at.anonConnect()
results = at.peerStats(cjdns,verbose=False,human_readable=True);
cjdns.disconnect()

with open("known-nodes","r") as handle:
	known_nodes = handle.readlines()
known_nodes_count = len(known_nodes)

list_of_Nodes = []
for x in results:
	if "UNRESPONSIVE" not in str(x):
		list_of_Nodes.append(PublicToIp6_convert(x['publicKey']))

for x in list_of_Nodes:
	if x not in str(known_nodes):
		known_nodes.append(x.strip())

if len(known_nodes) > known_nodes_count:
	with open("known-nodes","w") as handle:
		for x in known_nodes:
			handle.write(str(x.strip() + "\n"))

node_info = []

opener = urllib2.build_opener()
opener.addheaders = [('User-Agent', 'http://h.yakamo.org/index.php?p=pages/peerstats')]

for x in list_of_Nodes:
	time.sleep(1)
	try:
		handle = opener.open("http://api.hia.cjdns.ca/" + x.replace(':','') + "/")
		data_unclean = json.load(handle)
		if "URLs" in data_unclean:
			if len(data_unclean['URLs']) >= 1:
				node_info.append(x.strip() + " - __Peers:__ " + str(len(data_unclean['Peers'])) + " | __Open ports:__   " + str(len(data_unclean['OpenPortsTCP'])) + " | " + '[URL](' + data_unclean['URLs'][0] + ')')
			else:
				node_info.append(x.strip() + " - __Peers:__ " + str(len(data_unclean['Peers'])) + " | __Open 2ports:__   " + str(len(data_unclean['OpenPortsTCP'])))
	except:
		node_info.append(x.strip() + " - _No Data Found!_")

with open("node-info","w") as handle:
	for x in node_info:
		handle.write(x + "\n")
