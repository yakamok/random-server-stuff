# KVM related tools

### virsh-to-json.py
Runs "virsh list --all" via ssh and parses the output and counts the states per host then dumps to a json file.

### get-states.py

Uses the python-libvirt lib to make readonly connections to a list of hosts to collect the states of currently existing vm's, then organises the data into json format and saves to file.
