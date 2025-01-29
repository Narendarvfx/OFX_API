#!/bin/bash

#
# Copyright (c) 2023.
# Designed & Developed by Narendar Reddy G, OscarFX Private Limited
# All rights reserved.
#

if [ $# -gt 0 ]
  then
    if [ $1 != "compiled" ]
      then
         echo
         echo "Invalid argument passed. Call './test.sh compiled' if don't want to compile the source before."
         echo
         exit 1
    fi
else
  grunt
fi
./node_modules/mocha-phantomjs/bin/mocha-phantomjs test/test.html
