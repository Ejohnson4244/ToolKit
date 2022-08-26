import os
from pathlib import Path
import pandas as pd
import datetime
from requests.auth import HTTPDigestAuth
import subprocess
import csv
from tabulate import tabulate
import shutil
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed

def Scan(IP):
    print("Scanning " + IP + "...")
    loc = get_location(IP)
    status = Ping(IP)

    scanList = [IP, loc, status]
    return scanList

def Ping(IP):
    
    r = subprocess.Popen('ping ' + IP, stdout=subprocess.PIPE)
    r.wait()
    if r.poll():
        status = "DOWN"
    else:
        status = "UP"
    return status

def get_location(IP):
    machine_location = ""
    try:
        for location in pod_locations:
            if location['ip'] == IP:
                machine_location = location['site-bay-shelf-position']
        return machine_location
    except Exception as e: 
        print(e)
        machine_location = "Failed to pull"
    print(machine_location)

def getIP():    
    ipList = []
    csvFiles = Path("./CSV Files/").rglob("*.csv")      #Checks all csv files in /CSV Files/ folder
    all_csvs = [pd.read_csv(file) for file in csvFiles]
    ip_df = pd.concat(all_csvs) 
    ipList = ip_df['ip']
    return ipList


def dateplaceholder(n):
    if len(n) == 1:
        n = "0" + n
    return(n)

def Timestamp():        #create output string based on current date and time
    x=datetime.datetime.now()
    xyear = str(x.year)
    xmonth = dateplaceholder(str(x.month))
    xday = dateplaceholder(str(x.day))
    xhour = dateplaceholder(str(x.hour))
    xminute = dateplaceholder(str(x.minute))
    xsecond = dateplaceholder(str(x.second))

    time = xyear + "_" + xmonth + "_" +xday + "_" + xhour + xminute + xsecond
    return time


ip = getIP()

pod_csv = "locations/DNN3_Locations.csv"
pod_locations_df = pd.read_csv(pod_csv)
pod_locations = pod_locations_df.to_dict(orient='records')

with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
    futures = []
    pingList = []
    for i in ip:
        futures.append(executor.submit(Scan, i))
    for future in as_completed(futures):
        pingList.append(future.result())
    print(tabulate(pingList,tablefmt="fancy_grid",showindex="never",))

post_file = "Scan_" + Timestamp() + ".csv"
outFile = "Output/" + post_file
cols = ['IP','Location',"Status"]

with open(outFile, 'w',newline = "") as csvwfile:
    writer = csv.writer(csvwfile)
    try:
        writer.writerow(cols)
        writer.writerows(pingList)
    except Exception as e:
        print("")

sc_folder = "./CSV Files/"      
dn_folder = "./Archive/"

for file_name in os.listdir(sc_folder):         #Moves all csv files to Archive folder
    source = sc_folder + file_name
    destination = dn_folder + "Scanned_" + Timestamp() + ".csv"

    if os.path.isfile(source):
        shutil.move(source, destination)

os.system("pause")
