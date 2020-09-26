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

if [[ -n $HEROKU_API_KEY && -n $HEROKU_APP_NAME ]]; then
    herokuErr=$(python ./.github/herokugiturl.py)
    if [[ "$herokuErr" ]]; then 
        echo "$herokuErr"
    else
        HEROKU_GIT_URL="https://api:$HEROKU_API_KEY@git.heroku.com/$HEROKU_APP_NAME.git"
    fi
fi

FILE=/app/.git

if [ -d "$FILE" ] ; then
    echo "$FILE directory exists already."
else
    if [[ "$HEROKU_GIT_URL" ]]; then
        git clone "$HEROKU_GIT_URL" cat_ubh || git clone https://github.com/sandy1709/catuserbot cat_ubc
        mv cat_ubh/.git . || mv cat_ubc/.git .
        rm -rf cat_ubh || rm -rf cat_ubc
    else
        git clone https://github.com/sandy1709/catuserbot cat_ub
        mv cat_ub/.git .
        rm -rf cat_ub
    fi
fi

python -m userbot
