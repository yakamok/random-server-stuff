#!/usr/bin/python
import glob
import json
import sys
import os
import paramiko

username = 'root' #this depends on the correct keys being available
cmd = 'virsh list --all'
for_json_dict = {}
failed_connections = []

with open("hostnames","r") as handle:
	host_ip_list = [x.strip() for x in handle.readlines()]

def parse_output(stdout_data):
	data = [f.strip() for f in stdout_data]
	data.pop(len(data) -1)
	#sort states and calculate the number of stats and assign to host, also preparing to dump into a json file
	state_dict = {}
	for d in data:
		state_dict[d.split()[1]] = d.split()[2]

	temp_dict = {}
	for key,value in state_dict.iteritems():
		if value not in temp_dict:
			temp_dict[value] = 1
		else:
			temp_dict[value] += 1
		for_json_dict[x] = temp_dict

for x in host_ip_list:
	#establish ssh connection
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(x,username=username,timeout=3)
		
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)#command being sent
	 	parse_output(ssh_stdout.readlines()[2:])
	
	except:
		failed_connections.append(x)

print for_json_dict 

#write failed to parse files to file
if len(failed_connections) > 0:
	print "failed to connect to host(s), please check fail-conns.log"
	with open("failed-conns.log","w") as handle:
		[handle.write(x + "\n") for x in failed_connections]

#now dump everything into a json file
with open("host-stats.json","w") as handle:
	json.dump(for_json_dict,handle)
