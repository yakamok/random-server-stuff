#!/usr/bin/python
import json
import sys
import libvirt

username = 'bob'
for_json_dict = {}
failed_connections = []

#converting numerical value of state to human readable
states = {0:"nostate",1:"running",2:"blocked",3:"paused",4:"shutdown",5:"shut off",6:"crashed",7:"suspended",8:"last?"}

with open("hostnames","r") as handle:
	host_ip_list = [x.strip() for x in handle.readlines()]

for x in host_ip_list:
	try:
		temp_dict = {}
		#connection readonly
		conn = libvirt.openReadOnly('qemu+ssh://' + username + '@' + x + '/system')
		#get the list of stats for this host
		for d in conn.listDefinedDomains():
			state, _ = conn.lookupByName(d).state()
			if states[state] not in temp_dict:
				temp_dict[states[state]] = 1
			else:
				temp_dict[states[state]] += 1
		for_json_dict[x] = temp_dict
		conn.close()

	except:
		failed_connections.append(x)

print for_json_dict 

#log failed connections
if len(failed_connections) > 0:
	print "failed to connect to host(s), please check fail-conns.log"
	with open("failed-conns.log","w") as handle:
		[handle.write(x + "\n") for x in failed_connections]

# #now dump everything into a json file
with open("host-stats.json","w") as handle:
	json.dump(for_json_dict,handle)
