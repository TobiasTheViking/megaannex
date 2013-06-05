#!/usr/bin/env python2
import os
import sys
import json
import time
import inspect

conf = False
m = False
version = "0.1.2"
plugin = "megaannex-" + version

pwd = os.path.dirname(__file__)
if not pwd:
    pwd = os.getcwd()
sys.path.append(pwd + '/lib')

if "--dbglevel" in sys.argv:
    dbglevel = int(sys.argv[sys.argv.index("--dbglevel") + 1])
else:
    dbglevel = 0

from mega import Mega
import errors

if dbglevel > 3:
    mega = Mega({'verbose': True})  # verbose option for print output
else:
    mega = Mega()

def log(description, level=0):
    if dbglevel > level:
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        try:
            data = " %s [%s] %s : '%s'" % (timestamp, plugin, inspect.stack()[1][3], description)
        except:
            data = " FALLBACK %s [%s] %s : '%s'" % (timestamp, plugin, inspect.stack()[1][3], repr(description))
        if "--stderr" in sys.argv:
            sys.stderr.write(data + "\n")
        else:
            print(data)

def login(uname, pword):
    log(uname)
    global m

    delay = 1
    while not m and delay < 10:
        try:
            m = mega.login(uname, pword)
        except errors.RequestError as e:
            if e[0] == -3:
                log("[%s] EAGAIN: Retrying with exponential backoff: %s " %( repr(e[0]), repr(delay)))
                time.sleep(delay)
                delay += 1
            else:
                log("errors.RequestError: " + repr(e))
                sys.exit(1)

    log("Done")

def postFile(subject, filename, folder):
    log("%s to %s - %s" % ( filename, folder[0], subject))
    global m
    
    file = findInFolder(subject, folder)
    if file:
        log("File already exists: " + repr(file))
        return True

    delay = 1
    res = False
    while not res and delay < 10:
        try:
            res = m.upload(filename, dest=folder[0], dest_filename=subject)
        except errors.RequestError as e:
            if e[0] == -3:
                log("[%s] EAGAIN: Retrying with exponential backoff: %s " %( repr(e[0]), repr(delay)))
                time.sleep(delay)
                delay += 1
            else:
                log("errors.RequestError: " + repr(e))
                sys.exit(1)

    if res:
        log("Done: " + repr(res["f"][0]["h"]))
    else:
        sys.exit(1)

def findInFolder(subject, folder):
    log("%s - %s" % (repr(subject), repr(folder)), 3)
    if isinstance(folder, int):
        folder = [folder]

    delay = 1
    while delay < 10:
        try:
            files = m.get_files_in_node(folder[0]).items()
            log("files: " + repr(len(files)))
            if len(files) == 0:
                log("Empty folder, breaking")
                break
            for file in files:
                if file[1]['a'] and file[1]['a']['n'] == subject:
                    log("found file: " + repr(file), 3)
                    return file
            if len(files) > 0:
                break
        except errors.RequestError as e:
            if e[0] == -3:
                log("[%s] EAGAIN: Retrying with exponential backoff: %s " %( repr(e[0]), repr(delay)))
                time.sleep(delay)
                delay += 1
            else:
                log("errors.RequestError: " + repr(e))
                sys.exit(1)
    log("Failure")

def checkFile(subject, folder):
    log(subject)
    global m

    file = findInFolder(subject, folder)
    if file:
        log("Found: " + repr(file))
        print(subject)
    else:
        log("Failure")

def getFile(subject, filename, folder):
    log(subject)
    global m

    file = findInFolder(subject, folder)
    if file:
        dest, dest_filename = os.path.split(filename)

        delay = 1
        res = False
        while not res and delay < 10:
            try:
                res = m.download(file, dest_path=dest, dest_filename=dest_filename)
            except errors.RequestError as e:
                if e[0] == -3:
                    log("[%s] EAGAIN: Retrying with exponential backoff: %s " %( repr(e[0]), repr(delay)))
                    time.sleep(delay)
                    delay += 1
                else:
                    log("errors.RequestError: " + repr(e))
                    sys.exit(1)

        log("Done: " + repr(res))
    else:
        log("Failure")


def deleteFile(subject, folder):
    log(subject)
    global m

    file = findInFolder(subject, folder)

    if file:
        delay = 1
        res = False
        while not res and delay < 10:
            try:
                res = m.destroy(file[0])
            except errors.RequestError as e:
                if e[0] == -3:
                    log("[%s] EAGAIN: Retrying with exponential backoff: %s " %( repr(e[0]), repr(delay)))
                    time.sleep(delay)
                    delay += 1
                else:
                    log("errors.RequestError: " + repr(e))
                    sys.exit(1)

        log("Done: " + repr(res))
    else:
        log("Failure")

def readFile(fname, flags="r"):
    log(repr(fname) + " - " + repr(flags))

    if not os.path.exists(fname):
        log("File doesn't exist")
        return False
    d = ""
    try:
        t = open(fname, flags)
        d = t.read()
        t.close()
    except Exception as e:
        log("Exception: " + repr(e), -1)

    log("Done")
    return d

def saveFile(fname, content, flags="w"):
    log(fname + " - " + str(len(content)) + " - " + repr(flags))
    t = open(fname, flags)
    t.write(content)
    t.close()
    log("Done")

def createFolder(subject, folder):
    log("%s - %s" % (subject, folder))

    delay = 1
    res = False
    while not res and delay < 10:
        try:
            res = m.create_folder(subject, folder)
        except errors.RequestError as e:
            if e[0] == -3:
                log("[%s] EAGAIN: Retrying with exponential backoff: %s " %( repr(e[0]), repr(delay)))
                time.sleep(delay)
                delay += 1
            else:
                log("errors.RequestError: " + repr(e))
                sys.exit(1)
    if res:
        log("Done: " + repr(res))
        return res
    else:
        sys.exit(1)


def main():
    global conf
    args = sys.argv

    ANNEX_ACTION = os.getenv("ANNEX_ACTION")
    ANNEX_KEY = os.getenv("ANNEX_KEY")
    ANNEX_HASH_1 = os.getenv("ANNEX_HASH_1")
    ANNEX_HASH_2 = os.getenv("ANNEX_HASH_2")
    ANNEX_FILE = os.getenv("ANNEX_FILE")
    envargs = []
    if ANNEX_ACTION:
        envargs += ["ANNEX_ACTION=" + ANNEX_ACTION]
    if ANNEX_KEY:
        envargs += ["ANNEX_KEY=" + ANNEX_KEY]
    if ANNEX_HASH_1:
        envargs += ["ANNEX_HASH_1=" + ANNEX_HASH_1]
    if ANNEX_HASH_2:
        envargs += ["ANNEX_HASH_2=" + ANNEX_HASH_2]
    if ANNEX_FILE:
        envargs += ["ANNEX_FILE=" + ANNEX_FILE]
    log("ARGS: " + repr(" ".join(envargs + args)))

    if not os.path.exists(pwd + "/megaannex.conf"):
        saveFile(pwd + "/megaannex.conf", json.dumps({"uname": "", "folder": "gitannex", "pword": ""}))
        log("no megaannex.conf file found. Creating empty template")
        sys.exit(1)

    conf = readFile(pwd + "/megaannex.conf")
    try:
        conf = json.loads(conf)
    except Exception as e:
        log("Traceback EXCEPTION: " + repr(e))
        log("Couldn't parse conf: " + repr(conf))
        conf = {}

    log("Conf: " + repr(conf), 2)

    if "uname" not in conf or "pword" not in conf or ("uname" in conf and conf["uname"] == "") or ("pword" in conf and conf["pword"] == ""):
        log("No username or password found in config")
        sys.exit(1)

    login(conf["uname"], conf["pword"])
    if ANNEX_HASH_1 and ANNEX_HASH_2:
        folder = findInFolder(conf["folder"], 2)
        if folder:
            log("Using folder: " + repr(folder[0]))
            ANNEX_FOLDER = folder
        elif conf["folder"]:
            folder = createFolder(conf["folder"], 2)
            log("created folder0: " + repr(folder["f"][0]["h"]))
            ANNEX_FOLDER = [folder["f"][0]["h"]]
        
        folder = findInFolder(ANNEX_HASH_1, ANNEX_FOLDER)
        if folder:
            log("Using folder1: " + repr(folder[0]))
            ANNEX_FOLDER = folder
        elif ANNEX_HASH_1:
            folder = createFolder(ANNEX_HASH_1, ANNEX_FOLDER[0])
            log("created folder1: " + repr(folder["f"][0]["h"]))
            ANNEX_FOLDER = [folder["f"][0]["h"]]

        folder = findInFolder(ANNEX_HASH_2, ANNEX_FOLDER)
        if folder:
            log("Using folder2: " + repr(folder[0]))
            ANNEX_FOLDER = folder
        elif ANNEX_HASH_2:
            log("create folder2: " + repr(ANNEX_FOLDER))
            folder = createFolder(ANNEX_HASH_2, ANNEX_FOLDER[0])
            log("created folder2: " + repr(folder["f"][0]["h"]))
            ANNEX_FOLDER = [folder["f"][0]["h"]]

    if "store" == ANNEX_ACTION:
        postFile(ANNEX_KEY, ANNEX_FILE, ANNEX_FOLDER)
    elif "checkpresent" == ANNEX_ACTION:
        checkFile(ANNEX_KEY, ANNEX_FOLDER)
    elif "retrieve" == ANNEX_ACTION:
        getFile(ANNEX_KEY, ANNEX_FILE, ANNEX_FOLDER)
    elif "remove" == ANNEX_ACTION:
        deleteFile(ANNEX_KEY, ANNEX_FOLDER)
    else:
        setup = '''
Please run the following commands in your annex directory:

git config annex.mega-hook '/usr/bin/python2 %s/megaannex.py'
git annex initremote mega type=hook hooktype=mega encryption=%s
git annex describe mega "the mega library"
''' % (os.getcwd(), "shared")
        print setup
        sys.exit(1)

t = time.time()
if dbglevel > 0:
    if "--stderr" in sys.argv:
        sys.stderr.write("\n")
    else:
        print("")

log("START")
if __name__ == '__main__':
    main()
log("STOP: %ss" % int(time.time() - t))
