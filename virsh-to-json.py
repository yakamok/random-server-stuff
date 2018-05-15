#!/usr/bin/python
import glob
import json
import sys
import os
import paramiko

username = 'root' #make sure the correct keys are available
cmd = 'virsh list --all'
for_json_dict = {}
failed_connections = []
hosts_file = "/path/to/host-list"

with open(host_file,"r") as handle:
	host_ip_list = [x.strip() for x in handle.readlines()]

for x in host_ip_list:
	#establish ssh connection
	try:
		ssh = paramiko.SSHClient()
		ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
		ssh.connect(x,username=username)
		ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)#command being sent

		data = [f.strip() for f in ssh_stdout.readlines()[2:]]
		data.pop(len(data) -1)

		state_dict = {}
		for d in data:
			state_dict[d.split()[1]] = d.split()[2]

		temp_dict = {}

		#sort states and calculate the number of stats and assign to host, also preparing to dump into a json file
		for key,value in state_dict.iteritems():
			if value not in temp_dict:
				temp_dict[value] = 1
			else:
				temp_dict[value] += 1
			for_json_dict[x] = temp_dict
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
