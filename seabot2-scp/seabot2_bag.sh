#!/bin/zsh

DIRECTORY=`pwd`
FILE=$1
SEABOT=$2

echo "Get" $1 "from seabot"$SEABOT

scp -r pi@192.168.0.10$SEABOT:~/log/$FILE $DIRECTORY
