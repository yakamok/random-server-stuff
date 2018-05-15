#!/usr/bin/python
import glob
import json
import sys
import os

host_results_dir = "" #put absolute path to output files here 

if os.path.exists(host_results_dir) == False:
	print "no dir path has been set"
	sys.exit(0)
#grabbing all the files in host_results_dir
hosts_list = [x.replace(host_results_dir,'') for x in glob.glob(host_results_dir + "*")]

#if nothing is found exit
if len(hosts_list) == 0:
	print "no files found"
	sys.exit(0)

for_json_dict = {}
failed_files = []

#everything happens here
for x in hosts_list:
	#open host file and clean it up, remove first 2 lines
	try:
		with open(host_results_dir + x,"r") as handle:
			data = [f.strip() for f in handle.readlines()[2:]]
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
		failed_files.append(x)

#write failed to parse files to file
if len(failed_files) > 0:
	print "some files failed to be parsed, please check: failed-files log"
	with open("failed-files","w") as handle:
		[handle.write(x + "\n") for x in failed_files]

#now dump everything into a json file
with open("host-stats.json","w") as handle:
	json.dump(for_json_dict,handle)
