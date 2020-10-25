#!/bin/bash

mkdir /app/bin/
# downloading bins
wget -q -O /app/bin/megadown https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown
wget -q -O /app/bin/cmrudl https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py
# changing bins permissions
chmod 755 bin/megadown
chmod 755 bin/cmrudl 
echo "Succesfully bins are added"
