#!/bin/bash

if [ -d "env" ]
then
  echo "Python Virtual env exists"
else
  python3 -m venv env
fi

exho $PWD
source env/bin/activate

pip3 install -r requirements.txt

if [ -d "logs" ]
then
  echo "Log Folder Exists "
else
  mkdir logs
  touch logs/error.log logs/access.log
fi

sudo chmod -R 777 logs
echo "env setup finished"