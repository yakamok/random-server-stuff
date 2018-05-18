import libvirt
import sys

username = "bob"
hostname = "hostypoo"

#connection made readonly, so no alteration of the system is possible
conn = libvirt.openReadOnly('qemu+ssh://' + username + '@' + hostname + '/system')
if conn == None:
    print 'Failed to open connection to the hypervisor'
    sys.exit(1)

#converting numerical value of state to human readable
states = {0:"nostate",1:"running",2:"blocked",3:"paused",4:"shutdown",5:"shut off",6:"crashed",7:"suspended",8:"last?"}

#test print all states from host
for x in conn.listDefinedDomains():
	myDom = conn.lookupByName(x)
	state, reason = myDom.state()
	print x + " " + states[state]

conn.close()
