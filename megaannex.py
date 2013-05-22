#!/usr/bin/env python2
import os
import sys
import json
conf = False

pwd = os.path.dirname(__file__)
if not pwd:
    pwd = os.getcwd()
sys.path.append(pwd + '/lib')

if "--dbglevel" in sys.argv:
    dbglevel = int(sys.argv[sys.argv.index("--dbglevel") + 1])
else:
    dbglevel = 0

from mega import Mega
if dbglevel > 3:
    mega = Mega({'verbose': True})  # verbose option for print output
else:
    mega = Mega()
m = False

def login(uname, pword):
    if dbglevel > 0:
        print("login: " + uname)
    global m
    m = mega.login(uname, pword)

    # get user details
    if dbglevel > 5:
        print("details: " + repr(m.get_user()))
    # get account disk quota in MB
    if dbglevel > 5:
        print("quota:" + str(m.get_quota()))
    # get account storage space
    if dbglevel > 5:
        print("space: " + str(m.get_storage_space()))

def postFile(subject, filename):
    if dbglevel > 0:
        print("postFile: " + subject)
    global m
    
    #def upload(self, filename, dest=None, dest_filename=None):
    res = m.upload(filename, dest=conf["folder"], dest_filename=subject)
    if res:
        if dbglevel > 0:
            print(res)
    else:
        sys.exit(1)

def checkFile(subject):
    if dbglevel > 0:
        print("checkFile: " + subject)
    global m

    file = m.find(subject)
    if dbglevel > 0:
        print("found: " + repr(file))

    if file:
        print(subject)

def getFile(subject, filename):
    if dbglevel > 0:
        print("getFile: " + subject)
    global m

    file = m.find(subject)
    if dbglevel > 0:
        print("found: " + repr(file))

    if file:
        dest, dest_filename = os.path.split(filename)
        res = m.download(file, dest_path=dest, dest_filename=dest_filename)
        if dbglevel > 0:
            print("getFile res: " + repr(res))


def deleteFile(subject):
    if dbglevel > 0:
        print("deleteFile: " + subject)
    global m

    file = m.find(subject)

    if file:
        #delete or destroy file. by id or url
        #print(m.delete(file[0]))
        res = m.destroy(file[0])
        if dbglevel > 0:
            print("res: " + repr(res))
        #print(m.delete_url(link))
        #print(m.destroy_url(link))

def readFile(fname, flags="r"):
    if dbglevel > 0:
        print(repr(fname) + " - " + repr(flags))

    if not os.path.exists(fname):
        print("File doesn't exist")
        return False
    d = ""
    try:
        t = open(fname, flags)
        d = t.read()
        t.close()
    except Exception as e:
        print("Exception: " + repr(e), -1)

    if dbglevel > 0:
        print("Done")
    return d

def saveFile(fname, content, flags="w"):
    if dbglevel > 0:
        print(fname + " - " + str(len(content)) + " - " + repr(flags))
    t = open(fname, flags)
    t.write(content)
    t.close()
    if dbglevel > 0:
        print("Done")

def main():
    global conf
    args = sys.argv
    if dbglevel > 0:
        print(repr(args))

    if not os.path.exists(pwd + "/megaannex.conf"):
        saveFile(pwd + "/megaannex.conf", json.dumps({"uname": "", "folder": "gitannex", "pword": ""}))
        print("no megaannex.conf file found. Creating empty template")
        sys.exit(1)

    conf = readFile(pwd + "/megaannex.conf")
    try:
        conf = json.loads(conf)
    except Exception as e:
        print("Traceback EXCEPTION: " + repr(e))
        print("Couldn't parse conf: " + repr(conf))
        conf = {}

    if dbglevel > 0:
        print("Conf: " + repr(conf))

    if "uname" not in conf or "pword" not in conf or ("uname" in conf and conf["uname"] == "") or ("pword" in conf and conf["pword"] == ""):
        print("No username or password found in config")
        sys.exit(1)

    login(conf["uname"], conf["pword"])
    if not m.find(conf["folder"]):
        d = m.create_folder(conf["folder"])
        if dbglevel > 0:
            print("CREATE_FOLDER: " + repr(d))


    act = os.getenv("ANNEX_ACTION")
    if "store" == act:
        postFile(os.getenv("ANNEX_HASH_1"), os.getenv("ANNEX_FILE"))
    elif "checkpresent" == act:
        checkFile(os.getenv("ANNEX_HASH_1"))
    elif "retrieve" == act:
        getFile(os.getenv("ANNEX_HASH_1"), os.getenv("ANNEX_FILE"))
    elif "remove" == act:
        deleteFile(os.getenv("ANNEX_HASH_1"))
    else:
        print("ERROR")
        sys.exit(1)

if __name__ == '__main__':
    main()
