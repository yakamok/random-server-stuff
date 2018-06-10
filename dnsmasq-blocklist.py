#/usr/bin/python
#take file list of domains and add them to the block list in dnsmasq.d/blacklist.conf
#this program assumes you have setup dnsmasq as a router and is all installed and configured

import sys
import os
import getpass
import subprocess

#check if root
if getpass.getuser() == "root":
    #redirect page to this ip address
    point_To = "127.0.0.1"
    dnsmasq_config_dir = '/etc/dnsmasq.d/'
    config_file = 'blocklist.conf'

    #check if the blocklist config file exists and create it if not
    if not os.path.exists(dnsmasq_config_dir):
        print "Creating: " + dnsmasq_config_dir
        os.mkdir(dnsmasq_config_dir)

        if os.path.exists(dnsmasq_config_dir + config_file) != True:
            print "no config file found, creating now"
            open(dnsmasq_config_dir + config_file, 'w').close()

    #get the new list from stdin
    new_block_List = [x.strip() for x in sys.stdin.readlines()]
    print str(len(new_block_List)) + " entries found"

    #check theres actually a list
    if new_block_List:
        #get current list of blocks
        with open(dnsmasq_config_dir + config_file, "r") as handle:
            current_List = [x.strip().replace('address=/', '').replace("/" + point_To, '')\
                            for x in handle.readlines()]

        #compare lists and create a new list without dups
        final_List = list(set(current_List)|set(new_block_List))

        if (len(final_List) - len(current_List)) != 0:
            print str((len(final_List) - len(current_List))) + " new entries found"

        #write the final list to
            with open(dnsmasq_config_dir + config_file, "w") as handle:
                [handle.write("address=/" + x + "/" + point_To + "\n") for x in final_List]
                print str((len(final_List) - len(current_List)))\
                            + " original entries have been added"

                print str(len(final_List)) + " now in blocklist"

            #reload dnsmasq so it uses the updated list
            print "reloading dnsmasq..."

            process = subprocess.Popen("killall -s SIGHUP dnsmasq", shell=True,\
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = process.communicate()

            if err != None:
                print "error " + err
            else:
                print "reload complete"
        else:
            print "No new entries found"
    else:
        print "input was empty"
else:
    print "You are not Root!"
