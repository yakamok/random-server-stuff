#collect DB host, name, user, pass from wp-config.php files

echo "searching for database details for collection"
WPCONFIG=($(find -name 'wp-config.php' | sed 's/^.\///'))
echo "finished collecting databse details"

i='0'
while [ $i -lt ${#WPCONFIG[@]} ]
do
    dbHost[$i]=$(grep 'DB_HOST' ${WPCONFIG[$i]} | awk '{print $2}' | sed "s/[()';]//g")
    echo ${dbHost[$i]}
    dbName[$i]=$(grep 'DB_NAME' ${WPCONFIG[$i]} | awk '{print $2}' | sed "s/[()';]//g")
    dbUser[$i]=$(grep 'DB_USER' ${WPCONFIG[$i]} | awk '{print $2}' | sed "s/[()';]//g")
    dbPass[$i]=$(grep 'DB_PASSWORD' ${WPCONFIG[$i]} | awk '{print $2}' | sed "s/[()';]//g")

    i=$(($i + 1))
done

echo "Database Details have been collected"

backupDirectory="dbbackup"

Date=$(date +"%m-%d-%y")

backupDirectory="$backupDirectory/$Date"

if [ ! -d "$HOME/$backupDirectory" ]
then
    mkdir -p $HOME/$backupDirectory/
    echo "Directory Created"
fi

echo "dumping databases to file now"
i='0'

while [ $i -lt ${#dbHost[@]}  ]
do
    echo ${dbHost[$i]}
    filename[i]="$HOME/$backupDirectory/${dbName[$i]}_$Date.sql"
    mysqldump -v -h ${dbHost[$i]} -u ${dbUser[$i]} -p${dbPass[$i]} ${dbName[$i]} > ${filename[i]}
    sleep 3
    i=$(($i + 1))
done
    echo "done dumping databases"
fi
