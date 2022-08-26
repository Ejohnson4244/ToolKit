import datetime
from requests import post, get
from requests.auth import HTTPDigestAuth
from pathlib import Path
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
from time import sleep
import shutil
import os
import csv
from tabulate import tabulate

def dateplaceholder(n):
    if len(n) == 1:
        n = "0" + n
    return(n)
#create output string based on current date and time
def Timestamp():
    x=datetime.datetime.now()
    xyear = str(x.year)
    xmonth = dateplaceholder(str(x.month))
    xday = dateplaceholder(str(x.day))
    xhour = dateplaceholder(str(x.hour))
    xminute = dateplaceholder(str(x.minute))
    xsecond = dateplaceholder(str(x.second))

    y = xyear + xmonth + xday + "_" + xhour + xminute + xsecond
    return(y)
def getPass(Ifile): 
    List=[]
    iFile = open(Ifile, 'r')
    tList = iFile.readlines()
    for entry in tList:
        if entry:
            List.append(entry.rstrip('\n'))
    iFile.close()
    return List
def getIP():        #Reads 'ip' column in Minder export for IP addresses
    ipList = []
    
    csvFiles = Path("./CSV Files/").rglob("*.csv")      #Checks all csv files in /CSV Files/ folder
    all_csvs = [pd.read_csv(file) for file in csvFiles]
    ip_df = pd.concat(all_csvs) 
    ipList = ip_df['ip']
    return ipList


def x19Conf(user, password, IP, payload): #configing function for bitmain and vnish firmwares
    print("Waking " + IP + "...")
    for i in password:
        try:
            machine_conf = post("http://" + IP + '/cgi-bin/set_miner_conf.cgi', auth=HTTPDigestAuth(user, i), json = payload)
            if machine_conf.status_code == 200:
                machine_conf.close()
                return IP + " Success with: " + i
            else:
                print(IP + " may have failed.")
        except:
            return("")    

def machine_scan(user, pwd, IP):
    miner_conf = scan_miner_conf(user, pwd, IP)
    workmode = extract_workmode(miner_conf)
    subworker = extract_workername(miner_conf)
    asset = subworker[-6:]
    miner_list =[IP,asset,workmode]
    return miner_list


def scan_miner_conf(user,pwd,ip): #Queries miner configs
    for i in pwd:
        try:
            miner_config_json = post('http://'+ ip +'/cgi-bin/get_miner_conf.cgi',timeout=5, auth=HTTPDigestAuth(user, i))
            if miner_config_json.status_code == 200:
                miner_conf = miner_config_json.json()
                miner_config_json.close()
                return miner_conf
        except Exception as e:
            miner_conf = ''

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

def extract_workername(miner_conf):
    try:
        workername = miner_conf['pools'][0]['user']
        subworker = workername.split('.')[1]

    except Exception as e:
        subworker = "Failed to pull"
    return subworker

def main():
    payload = {

        "pools" : [
            {
                "url" : None,		        #pool1 URL
                "user" : None,  	        #pool1 user.worker
                "pass" : None		        #pool1 password
    },
            {
                "url" : None,		        #pool2 URL
                "user" : None,		        #pool2 user.worker
                "pass" : None		        #pool2 password
    },
            {
                "url" : None,		        #pool3 URL
                "user" : None,		        #pool3 user.worker
                "pass" : None		        #pool3 password
    }
            ]
        ,
        "api-listen" : None,		        #<-These 4 were set to fix an API access error on some argo T17s in a bugged firmware version of Vnish/minderOS
        "api-network" : None,		        #<-
        "api-groups" : None,		        #<-
        "api-allow" : None,		            #<-
        "bitmain-fan-ctrl" : None, 	#True = fan control enabled | False = Auto fan control
        "bitmain-fan-pwm" :None, 	    #fan speed percentage 100=5800-6100RPM | 50 = 3200-3400RPM | 20=2000-2300RPM 
        "bitmain-use-vil" : None,           #no observed effect when changed
        "bitmain-freq" : None, 		        #hashboard freq. modifying can cause hashboard corruption.
        "bitmain-voltage" : None,	        #hashboard voltage. modifying can cause hashboard corruption.
        "bitmain-ccdelay" : None,	        #power suppply delay. Not sure if it does anything on a production machine.
        "bitmain-pwth" : None,              #no observed effect when changed
        "bitmain-work-mode" : None,         #no observed effect when changed
        "bitmain-freq-level" : None,        #no observed effect when changed
        "miner-mode" : 0 		    #0=normal, 1=sleep, None=NoChange
    }

    password = getPass("pwd.txt")	#Gets a List of all passwords
    ip = getIP()

    with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor: #configs 10000 units at a time
        futures = []
        minerList = []
        for i in ip:
            futures.append(executor.submit(x19Conf, 'root', password, i, payload))
    print("Finished pushing configs.")
    sleep(10)
    print("Scanning Machines...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = []
        for i in ip:
            futures.append(executor.submit(machine_scan, 'root', password, i))
        for future in as_completed(futures):
            minerList.append(future.result())


    cols = ['IP','Asset','Workmode']
    df = pd.DataFrame(minerList)
    df.columns = cols
    
    counts = df['Workmode'].value_counts()
    counts = counts.reset_index()
    counts.columns = ['Workmode','Counts']
    print(tabulate(counts,tablefmt="fancy_grid",showindex="never", headers=['Workmode','Counts']))

    sc_folder = "./CSV Files/"      
    dn_folder = "./Archive/"
    post_file = "Scan_" + Timestamp() + ".csv"
    outFile = "Output/" + post_file
    with open(outFile, 'w',newline = "") as csvwfile:
        writer = csv.writer(csvwfile)
        try:
            writer.writerow(cols)
            writer.writerows(minerList)
        except Exception as e:
            print("")

    for file_name in os.listdir(sc_folder):         #Renames and moves all csv files to Archive folder, renaming according to operation
        source = sc_folder + file_name
        destination = dn_folder + post_file

        if os.path.isfile(source):
            shutil.move(source, destination)
            
main()
os.system("pause")