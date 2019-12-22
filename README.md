# random-server-stuff
just a collection of random tools.  
Some of or most of these tools are unused now and old!  

### DNS Monitor - dns-monitor.py

I use this to see what my deivces are doing on the network.  

### AutoVM

simple automation of vm creation and deletion on KVM  

### DDNS

Poorly implemented experimental decentralised dns system for fun(do not use this code)  

### wp-db - wp-db.sh

quick script to find and backup wordpress databases, this could be done much better by just backing up the database its self.
was written to be used on a crappy godaddy host for a friend.  

### Simple Stats showing invalid login attempts in auth.log - authlogs-ip-stats

Generate stats from failed auth attempts in /var/log/auth.log and fetching locations based on IP address  

### load average alert - loadavg-alert.py

Checks load average and notifys via email when its too high

### virsh-to-json.py
Runs "virsh list --all" via ssh and parses the output and counts the states per host then dumps to a json file.  

### dnsmasq-blocklist.py

Simple program to accept piped lists of domains that need to be blocked and the added to blocklist.conf in /etc/dnsmasq.d/, Usage: cat list-of-domains.txt | python dnsmasq-blocklist.py  
