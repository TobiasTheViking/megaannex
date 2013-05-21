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

if not os.path.exists(pwd + "/temp/"):
    os.mkdir(pwd + "/temp/")

def login(uname, pword):
    if dbglevel > 0:
        print("login: " + uname)
    global m
    m = mega.login(uname, pword)

    # get user details
    details = m.get_user()
    if dbglevel > 0:
        print("login: " + repr(details))
    # get account disk quota in MB
    if dbglevel > 0:
        print(m.get_quota())
    # get account storage space
    if dbglevel > 0:
        print(m.get_storage_space())

def postFile(subject, filename):
    if dbglevel > 0:
        print("postFile: " + subject)
    global m
    res = m.upload(filename)
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

    if file:
        print(subject)

def getFile(subject, filename):
    if dbglevel > 0:
        print("getFile: " + subject)
    global m

    file = m.find(subject)

    if file:
        res = m.download(file, pwd + "/temp/")
        if os.path.exists(pwd + "/temp/" + subject) or res:
            if dbglevel > 0:
                print("getFile Moving: " + repr(file))
            os.rename(pwd + "/temp/" + subject, filename)
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
            print(res)
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

    print("BLA: " + repr(conf) + " - " + repr(type(conf)))
    login(conf["uname"], conf["pword"])
    if "store" in sys.argv:
        postFile(sys.argv[sys.argv.index("--subject") + 1], sys.argv[sys.argv.index("--file") + 1])
    elif "fileexists" in sys.argv:
        checkFile(sys.argv[sys.argv.index("--subject") + 1])
    elif "getfile" in sys.argv:
        getFile(sys.argv[sys.argv.index("--subject") + 1], sys.argv[sys.argv.index("--file") + 1])
    elif "delete" in sys.argv:
        deleteFile(sys.argv[sys.argv.index("--subject") + 1])
    else:
        print("ERROR")

if __name__ == '__main__':
    main()
