#!/bin/bash
#script to destroy 1 or more guests and return the id and maccaddress to the pool
# USAGE: ./delclones.sh guest1 guest2 guest 3 ....

#dump args into array
VMDOMAIN=("$@")

#extract the mac address from the Guest xml file and remove the # from the pool, freeing it up for use agian

i='0'
while [ $i -lt $# ]
do

virsh destroy ${VMDOMAIN[$i]}
sleep 5
echo "looking for mac address"
VMMAC=$(virsh dumpxml ${VMDOMAIN[$i]} | xml2 | grep 'address=' | sed -e 's/\/domain\/devices\/interface\/mac\/\@address\=//g')
echo "mac address found"

VMPATH=$(virsh dumpxml ${VMDOMAIN[$i]} | xml2 | grep 'disk/source/@file=' | sed -e 's/\/domain\/devices\/disk\/source\/\@file\=//g')
echo "location of ${VMDOMAIN[$i]} found"

sed -i "s/\#$VMMAC/$VMMAC/g" mac-ip.txt
echo "$VMMAC has been returned to pool"

virsh undefine ${VMDOMAIN[$i]}
echo "${VMDOMAIN[$i]} has been removed"
rm $VMPATH
echo "${VMDOMAIN[$i]}.img remove"

sed -i "/${VMDOMAIN[$i]}/d" vm-ip.txt
echo "vm-ip.txt - updated"
echo "FINISHED"
i=$((i + 1))
done
