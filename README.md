megaannex
=========

Hook program for gitannex to use mega.co.nz as backend

Requirements:
requests>=0.10
pycrypto
mega.py

The "megaapi" folder is a pull from https://github.com/richardasaurus/mega.py 

## Commands for gitannex:

    git config annex.mega-store-hook '/usr/bin/python2 ~/megaannex/megaannex.py store --subject $ANNEX_KEY --file $ANNEX_FILE'
    git config annex.mega-retrieve-hook '/usr/bin/python2 ~/megaannex/megaannex.py  getfile --subject $ANNEX_KEY --file $ANNEX_FILE'
    git config annex.mega-checkpresent-hook '/usr/bin/python2 ~/megaannex/megaannex.py fileexists --subject $ANNEX_KEY'
    git config annex.mega-remove-hook '/usr/bin/python2 ~/megaannex/megaannex.py delete --subject $ANNEX_KEY'
    git annex initremote mega type=hook hooktype=mega encryption=shared
    git annex describe mega "the mega.co.nz library"
