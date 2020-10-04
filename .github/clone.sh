#!/bin/bash

# Copyright (C) 2020 by sandy1709

echo "
                    :'######:::::'###::::'########::::
                    '##... ##:::'## ##:::... ##..:::::
                     ##:::..:::'##:. ##::::: ##:::::::
                     ##:::::::'##:::. ##:::: ##:::::::
                     ##::::::: #########:::: ##:::::::
                     ##::: ##: ##.... ##:::: ##:::::::
                    . ######:: ##:::: ##:::: ##:::::::
                    :......:::..:::::..:::::..::::::::
"

echo "
'##::::'##::'######::'########:'########::'########:::'#######::'########:
 ##:::: ##:'##... ##: ##.....:: ##.... ##: ##.... ##:'##.... ##:... ##..::
 ##:::: ##: ##:::..:: ##::::::: ##:::: ##: ##:::: ##: ##:::: ##:::: ##::::
 ##:::: ##:. ######:: ######::: ########:: ########:: ##:::: ##:::: ##::::
 ##:::: ##::..... ##: ##...:::: ##.. ##::: ##.... ##: ##:::: ##:::: ##::::
 ##:::: ##:'##::: ##: ##::::::: ##::. ##:: ##:::: ##: ##:::: ##:::: ##::::
. #######::. ######:: ########: ##:::. ##: ########::. #######::::: ##::::
:.......::::......:::........::..:::::..::........::::.......::::::..:::::
"

FILE=/app/.git

if [ -d "$FILE" ] ; then
    echo "$FILE directory exists already."
else
    git clone https://github.com/Jisan09/catuserbot cat_ub
    rm -rf userbot
    mv cat_ub/.git .
    mv cat_ub/userbot .
    mv cat_ub/requirements.txt .
    rm -rf cat_ub
    python ./.github/update.py
fi

FILE=/app/bin/

if [ -d "$FILE" ] ; then
    echo "$FILE directory exists already."
else
    mkdir /app/bin/
    # downloading bins
    wget -O /app/bin/megadown https://raw.githubusercontent.com/adekmaulana/megadown/master/megadown
    wget -O /app/bin/cmrudl https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py
    # changing bins permissions
    chmod 755 bin/megadown
    chmod 755 bin/cmrudl 
    echo "Succesfully bins are added"
fi

python -m userbot
