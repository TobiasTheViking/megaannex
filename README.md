megaannex
=========

Hook program for gitannex to use mega.co.nz as backend

# Requirements:

    requests>=0.10
    pycrypto

Credit for the mega api interface goes to: https://github.com/richardasaurus/mega.py 

## Install
Clone the git repository in your home folder.

    git clone git://github.com/TobiasTheViking/megaannex.git 

This should make a ~/megannex folder

## Setup
Run the program once to make an empty config file

    cd ~/megaannex; python2 megaannex.py

Edit the megaannex.conf file. Add your mega.co.nz username and password

Note: The folder option in the megaannex.conf file isn't yet used. 

## Commands for gitannex:

    git config annex.mega-store-hook '/usr/bin/python2 ~/megaannex/megaannex.py store --subject $ANNEX_KEY --file $ANNEX_FILE'
    git config annex.mega-retrieve-hook '/usr/bin/python2 ~/megaannex/megaannex.py  getfile --subject $ANNEX_KEY --file $ANNEX_FILE'
    git config annex.mega-checkpresent-hook '/usr/bin/python2 ~/megaannex/megaannex.py fileexists --subject $ANNEX_KEY'
    git config annex.mega-remove-hook '/usr/bin/python2 ~/megaannex/megaannex.py delete --subject $ANNEX_KEY'
    git annex initremote mega type=hook hooktype=mega encryption=shared
    git annex describe mega "the mega.co.nz library"
