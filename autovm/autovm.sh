#!/bin/bash
# This script allows the auto creation of multiple virtual machines with the least effort possible

USAGE="USAGE: ./autoclone.sh <vmtoclone> <numofvms> <nameofvm> <memory>"

if [[ $# -lt 1  ]]; then
	echo "not enough arguments entered"
	echo $USAGE
	exit 1
fi

#error checking the args

#check template exists
VMTOCLONE="` virsh list --all | sed '1,2d' | awk '{print $2}' | grep "$1" `"
if [[ $VMTOCLONE != $1 ]]; then
	echo "$1 does not exist or is tpyed incorrectly"
	exit 1
fi

#check numofvms arg input is an integer

CHECK="` echo $2 | sed 's/[0-9]*//g' `"
CHECK1=$( printf '%d' "'$CHECK" )
if [[ $CHECK1 != 0 ]]; then
	echo "please type a number for numofvms"
	echo $USAGE
	exit 1
fi

#check memory arg is an integer

MEMARG="` echo $4 | sed 's/[0-9]*//g' `"
MEMARG1=$( printf '%d' "'$CHECK" )
if [[ $MEMARG1 != 0 ]]; then
	echo "please type a number for memory"
	echo $USAGE
	exit 1
fi

#Check there is enough available memory

MFREE=$(sed '2!d' /proc/meminfo | awk '{print $2}')
CACHED=$(sed '3!d' /proc/meminfo | awk '{print $2}')
BUFF=$(sed '4!d' /proc/meminfo | awk '{print $2}')
FREEMEM=$(( $MFREE+$CACHED+$BUFF ))

FREEMEM2=$((FREEMEM/1024))
VMMEM=$(($4 * $2))

if [[ $FREEMEM2 -lt $VMMEM  ]];then
	echo "not enough available memory"
	exit 1
fi

#--end of memory check

i='0'
while [ $i -lt $2 ]
do

#grab and create variables here

TEMPLATE=$1
MACADDR="` grep -v '^#' mac-ip.txt | sed '1!d'  | awk '{print $1}' `"
VMNAME=$3

if [[ $2 -eq 1 ]]; then
	VMDOMAIN=$VMNAME
else
	VMDOMAIN=$VMNAME$i
fi
#check to see if name already exists
NAMEC="` virsh list --all | sed '1,2d' | awk '{print $2}' | grep "$VMDOMAIN" `"
if [[ $NAMEC == $VMDOMAIN ]]; then
	echo "Guest $VMDOMAIN already exists"
	exit 0
fi

VMDEST="set the destination for your virtual machines here"
MEM=$(($4 * 1024))

#create vm using collected variables

virt-clone -m $MACADDR --original $TEMPLATE --name $VMDOMAIN --file $VMDEST$VMDOMAIN.img

virt-sysprep --enable hostname --hostname $VMDOMAIN -d $VMDOMAIN

virsh setmaxmem $VMDOMAIN $MEM

virsh start $VMDOMAIN

#comment out maccaddr used as to not have duplicates
sed -i "s/$MACADDR/\#$MACADDR/g" mac-ip.txt

# dump the name of the vm and the ip address to file
VMIP="` grep "$MACADDR" mac-ip.txt | awk '{print $2}' `"
echo $VMDOMAIN " " $VMIP >> vm-ip.txt

i=$(($i + 1))
done
