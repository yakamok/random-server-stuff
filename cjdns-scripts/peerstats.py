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

with open("node-info","r") as handle:
	node_data = handle.readlines()

node_data_dict = {}

for x in node_data:
	node_data_dict[x.split()[0].replace('<br>','')] = x

for x in node_data_dict:
	print x

Title = "# Yakamo.org - Cjdns Peers\n"
date_stamp = "__Last Updated:__ " + time.strftime("%Y-%m-%d, %R")

with open("peerstats.md","w") as handle:
	handle.write(Title)
	handle.write(date_stamp + "  \n")
	handle.write("  \n")
	handle.write("### Current Peers:" + str(len(list_of_Nodes)) + "  \n")
	handle.write("  \n")

	for x in list_of_Nodes:
		if x in str(node_data_dict):
			handle.write(node_data_dict[x] + "\n")
		else:
			handle.write(x + "<br> _No data yet_  \n")
