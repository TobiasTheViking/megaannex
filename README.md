megaannex
=========

Hook program for gitannex to use mega.co.nz as backend

# Requirements:

    python2
    requests>=0.10
    pycrypto

Credit for the mega api interface goes to: https://github.com/richardasaurus/mega.py 

# Install
Clone the git repository in your home folder.

    git clone git://github.com/TobiasTheViking/megaannex.git 

This should make a ~/megaannex folder

# Setup
Run the program once to make an empty config file

    cd ~/megaannex; python2 megaannex.py

Edit the megaannex.conf file. Add your mega.co.nz username, password and folder name.

# Commands for gitannex:

    git config annex.mega-hook '/usr/bin/python2 ~/megaannex/megaannex.py'
    git annex initremote mega type=hook hooktype=mega encryption=shared
    git annex describe mega "the mega.co.nz library"
