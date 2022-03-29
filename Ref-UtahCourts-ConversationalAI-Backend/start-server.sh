#!/bin/sh

PID1=$(lsof -t -i :5005)
PID2=$(lsof -t -i :5055)

if [[ ! -z $PID1 ]]
then
    kill -9 $PID1
    echo "Process: " $PID1 "terminated"
fi

if [[ ! -z $PID2 ]]
then
    kill -9 $PID2
    echo "Process: " $PID2 "terminated"
fi

python -m server run actions &
python -m server run --cors "*" --enable-api &
