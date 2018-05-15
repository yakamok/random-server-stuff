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

### RSS Feed Check & Stats - feed-check.py

This program used to check rss feeds from members of our IRC group and generate stats on how often we posted average word count ...etc, then it would determine if we were lazy or not.  

### Wordpress xml export to markdown - WP-post-2-md.py

Needed to convert the xml export of all posts from wordpress to markdown to use on my new site  

### Simple Stats showing invalid login attempts in auth.log - authlogs-ip-stats

Generate stats from failed auth attempts in /var/log/auth.log and fetching locations based on IP address  

### load average alert - loadavg-alert.py

Checks load average and notifys via email when its too high

### virsh-to-json.py

takes multiple files from "virsh list --all > hostname"  and parses them and counts the states per host then dumps to a json file. 
