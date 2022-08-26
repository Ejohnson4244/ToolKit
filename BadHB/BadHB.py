from requests.auth import HTTPDigestAuth
from requests import get
import datetime
from pathlib import Path
import pandas as pd
import csv
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil
from tabulate import tabulate

def get_location(IP):
    machine_location = ""
    try:
        for location in pod_locations:
            if location['ip'] == IP:
                machine_location = location['site-bay-shelf-position']
        return(machine_location)
    except Exception as e: 
        machine_location = "Failed to pull"
def getPass(Ifile):
    List=[]
    iFile = open(Ifile, 'r')
    tList = iFile.readlines()
    for entry in tList:
        if entry:
            List.append(entry.rstrip('\n'))
    iFile.close()
    return List
def getIP():    
    ipList = []
    csvFiles = Path("./CSV Files/").rglob("*.csv")      #Checks all csv files in /CSV Files/ folder
    all_csvs = [pd.read_csv(file) for file in csvFiles]
    ip_df = pd.concat(all_csvs) 
    ipList = ip_df['ip']
    return ipList


def scan_stats(user,pwd,ip):
    for i in pwd:
        try:
            stats_json = get("http://" + ip + '/cgi-bin/stats.cgi', auth=HTTPDigestAuth(user, i))
            if stats_json.status_code == 200:
                stats = stats_json.json()
                stats_json.close()
            return stats
        except:
            stats = ''
def scan_system_info(user,pwd,ip): #Queries system info 
    for i in pwd:
        try:
            system_info_json = get('http://' + ip + '/cgi-bin/get_system_info.cgi',timeout=5, auth=HTTPDigestAuth(user, i))
            if system_info_json.status_code == 200:
                system_info = system_info_json.json()
                system_info_json.close()
                return system_info
        except Exception as e:
            system_info = ''
def scan_miner_conf(user,pwd,ip): #Queries miner configs
    for i in pwd:
        try:
            miner_config_json = get('http://'+ ip +'/cgi-bin/get_miner_conf.cgi',timeout=5, auth=HTTPDigestAuth(user, i))
            if miner_config_json.status_code == 200:
                miner_conf = miner_config_json.json()
                miner_config_json.close()
                return miner_conf
        except Exception as e:
            miner_conf = ''

def MachineScan(user,pwd,ip):
    location = get_location(ip)
    print("Scanning " + ip)
    stats = scan_stats(user,pwd,ip) 

    miner_conf = scan_miner_conf(user, pwd, ip)

    hbList = []
    try:
        hb0Index = stats["STATS"][0]["chain"][0]["index"]
        hbList.append(hb0Index)
    except Exception as e:
        pass
    try:
        hb1Index = stats["STATS"][0]["chain"][1]["index"]
        hbList.append(hb1Index)
    except Exception as e:
        pass
    try:
        hb2Index = stats["STATS"][0]["chain"][2]["index"]
        hbList.append(hb2Index)
    except Exception as e:
        pass

    bhbList = []

    if 0 not in hbList:
        # print("hb0 is not actve")
        bhbList.append(0)
    if 1 not in hbList:
        # print("hb1 is not actve")
        bhbList.append(1)
    if 2 not in hbList:
        # print("hb2 is not actve")
        bhbList.append(2)

    subworker = extract_workername(miner_conf)

    if subworker != 'Failed to pull':
        asset = subworker[-6:]
    else:
        asset = "Failed to pull"

    if len(bhbList) == 0:
        bhbList = "Could not find BHB"
    
    

    minerList = [ip,asset,location,bhbList]
    return minerList
def extract_workername(miner_conf):
    try:
        workername = miner_conf['pools'][0]['user']
        subworker = workername.split('.')[1]

    except Exception as e:
        subworker = "Failed to pull"
    return subworker

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

pod_csv = "locations/DNN3_Locations.csv"
pod_locations_df = pd.read_csv(pod_csv)
pod_locations = pod_locations_df.to_dict(orient='records')

pwd = getPass("pwd.txt") #Pulls pwd for machine
ip = getIP()   #Gets list of IPs

minerList = []

with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
    futures = []
    for i in ip:
        futures.append(executor.submit(MachineScan, 'root', pwd, i))
    for future in as_completed(futures):
        minerList.append(future.result())
cols = ['IP','Asset','Location','Bad Chain [0,1,2]']
post_file = "Scan_" + Timestamp() + ".csv"
outFile = "Output/" + post_file
print(tabulate(minerList,tablefmt="fancy_grid",showindex="never", headers=cols))

with open(outFile, 'w',newline = "") as csvwfile:
    writer = csv.writer(csvwfile)
    try:
        writer.writerow(cols)
        writer.writerows(minerList)
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
