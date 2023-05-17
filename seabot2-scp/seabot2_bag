#!/bin/zsh

DIRECTORY=`pwd`
SEABOT=$1
USER=pi
IP=192.168.0.10

FILES=($(ssh $USER@$IP$SEABOT ls /home/$USER/log))

COUNTER=0
for f in $FILES; do
        echo $COUNTER $f
        ((COUNTER++))
done

echo -n "Enter file number (default 0) : "
read USERINPUT

if [[ $USERINPUT == "" ]]; then
	USERINPUT=0
fi

((USERINPUT++))
FILE=($FILES[$USERINPUT])
echo "Download " $FILE " from Seabot" $SEABOT 

scp -r $USER@$IP$SEABOT:~/log/$FILE $DIRECTORY
