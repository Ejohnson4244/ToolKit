# Created by Ethan Johnson for use at Core Scientific
# Python 3.9
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.auth import HTTPDigestAuth
import requests
from pathlib import Path
import pandas as pd
import csv
import datetime
from tabulate import tabulate
import shutil
import os

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

def get_location(IP):
    machine_location = ""
    try:
        for location in pod_locations:
            if location['ip'] == IP:
                machine_location = location['site-bay-shelf-position']
        return(machine_location)
    except Exception as e: 
        machine_location = "Failed to pull"

def scan_system_info(user,pwd,ip): #Queries system info 
    for i in pwd:
        try:
            system_info_json = requests.get('http://' + ip + '/cgi-bin/get_system_info.cgi',timeout=5, auth=HTTPDigestAuth(user, i))
            if system_info_json.status_code == 200:
                system_info = system_info_json.json()
                system_info_json.close()
                return system_info
        except Exception as e:
            system_info = ''


def scan_miner_conf(user,pwd,ip): #Queries miner configs
    for i in pwd:
        try:
            miner_config_json = requests.get('http://'+ ip +'/cgi-bin/get_miner_conf.cgi',timeout=5, auth=HTTPDigestAuth(user, i))
            if miner_config_json.status_code == 200:
                miner_conf = miner_config_json.json()
                miner_config_json.close()
                return miner_conf
        except Exception as e:
            miner_conf = ''


def scan_miner_type(user, pwd, IP):
    for i in pwd:
        try:
            miner_type_json = requests.get('http://'+ IP +'/cgi-bin/miner_type.cgi',timeout=5, auth=HTTPDigestAuth(user, i))
            if miner_type_json.status_code == 200:
                miner_type = miner_type_json.json()
                miner_type_json.close()
                return miner_type
        except Exception as e:
            miner_type = ''

def extract_fan_perc(miner_conf):
    try:
        perc = miner_conf["bitmain-fan-pwm"]
    except Exception as E:
        perc = "Failed to pull"
    return perc

def extract_fan_ctrl(miner_conf):
    fan_ctrl =''
    try:
        f_ctrl = miner_conf["bitmain-fan-ctrl"]
        if f_ctrl == True:
            fan_ctrl = "On"
        elif f_ctrl == False:
            fan_ctrl = "Off"
    except Exception as e:
        fan_ctrl = "Failed to pull"
    return fan_ctrl

def extract_hostname(machine_info): #Pulls hostname/asset
    try:
        hostname = machine_info['hostname']
        hostname = str(hostname.split('-')[1])
        return hostname
    except Exception as e:
        hostname = "Failed to pull"

def extract_workername(miner_conf):
    try:
        workername = miner_conf['pools'][0]['user']
        subworker = workername.split('.')[1]

    except Exception as e:
        subworker = "Failed to pull"
    return subworker

def extract_workmode(miner_conf):
    workmode =''
    try:
        wm = miner_conf['bitmain-work-mode']
        if wm == '0':
            workmode = "Normal"
        elif wm == '1':
            workmode = "Sleep"
    except Exception as e:
        workmode = "Failed to pull"
    return workmode

def extract_type(machine_info):
    try:
        mtype = machine_info['minertype']
    except Exception as e:
        mtype = 'Failed to pull'
    return mtype
def extract_ctrlBoard(miner_type):
    try:
        ctrlBoard = miner_type['subtype']
    except Exception as e:
        ctrlBoard = 'May not be supported'
    return ctrlBoard

def extract_firmware(machine_info):
    try:
        fw = machine_info['system_filesystem_version']
    except Exception as e:
        fw = 'Failed to pull'
    return fw

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

def machine_scan(user, pwd, IP):	
    location = get_location(IP)
    print("Scanning " + IP)
    machine_info = scan_system_info(user, pwd, IP) 
    hostname = extract_hostname(machine_info)
    miner_conf = scan_miner_conf(user, pwd, IP)
    subworker = extract_workername(miner_conf)
    workmode = extract_workmode(miner_conf)
    miner_type = scan_miner_type(user, pwd, IP)
    mtype = extract_type(machine_info)
    ctrlBoard = extract_ctrlBoard(miner_type)
    fw = extract_firmware(machine_info)
    fan_ctrl = extract_fan_ctrl(miner_conf)
    perc = extract_fan_perc(miner_conf)
    asset = subworker[-6:]
    if asset != hostname and subworker != "Failed to pull":
        subworker = " XX " + subworker + " XX"
        asset = "Failed to pull"
    miner_list =[IP, asset, location, hostname, subworker, mtype, ctrlBoard, fan_ctrl, perc, workmode, fw]

    return miner_list

pod_csv = "locations/DNN3_Locations.csv"
pod_locations_df = pd.read_csv(pod_csv)
pod_locations = pod_locations_df.to_dict(orient='records')

pwd = getPass("pwd.txt") #Pulls pwd for machine
ip = getIP()   #Gets list of IPs
minerList = []

with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
    futures = []
    for i in ip:
        futures.append(executor.submit(machine_scan, 'root', pwd, i))
    for future in as_completed(futures):
        minerList.append(future.result())
    #print(minerList)
    
post_file = "Scan_" + Timestamp() + ".csv"
outFile = "Output/" + post_file
cols = ['IP','Possible Asset','Location','Hostname','Workername','Miner Type', 'Control Board','Fan CTRL','Fan %','Workmode', 'Firmware Version']

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
