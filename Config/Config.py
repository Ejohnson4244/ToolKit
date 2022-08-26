# Created by Ethan Johnson for use at Core Scientific
# Python 3.9
from requests import post, get
from pathlib import Path
from requests.auth import HTTPDigestAuth
from concurrent.futures import ThreadPoolExecutor, as_completed
import concurrent.futures
import datetime
import pandas as pd
import shutil
import os
import csv
from tabulate import tabulate
from time import sleep
from json import *

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

def x19Conf(user, password, IP, payload): #configing function for bitmain and vnish firmwares
    print("Sending config to " + IP + "...")
    for i in password:
        try:
            machine_conf = post("http://" + IP + '/cgi-bin/set_miner_conf.cgi', auth=HTTPDigestAuth(user, i), json = payload)
            if machine_conf.status_code == 200:
                machine_conf.close()
                return IP+" Success with: " + i
            else:
                print("Bad password or empty IP")
        except:
            return("This machine caused an improperly handled exception! Most likely an empty IP")
            #pass            

def x19Reboot(user, password, IP ): 
    print("Rebooting " + IP + "..." )
    for i in password:
        try:
            respo = get("http://" + IP + '/cgi-bin/reboot.cgi', auth=HTTPDigestAuth(user, i))
            if respo.status_code == 200:
                respo.close()
                sleep(20) #General boot time for S19s with zynq based control boards.
                print("Reboot Complete for:" + str(IP))
            else:
                print("Rebooting " + IP + " May have failed...")
        except OSError: return "Rebooting " + IP + "...Failed..."

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

def machine_scan(user, pwd, IP):
    miner_conf = scan_miner_conf(user, pwd, IP)
    workmode = extract_workmode(miner_conf)
    subworker = extract_workername(miner_conf)
    fan_ctrl = extract_fan_ctrl(miner_conf)
    fan_perc = extract_fan_perc(miner_conf)
    asset = subworker[-6:]

    miner_list =[IP,asset,workmode,fan_ctrl,fan_perc]
    return miner_list

def extract_workername(miner_conf):
    try:
        workername = miner_conf['pools'][0]['user']
        subworker = workername.split('.')[1]

    except Exception as e:
        subworker = "Failed to pull"
    return subworker
def extract_fan_perc(miner_conf):
    try:
        perc = miner_conf["bitmain-fan-pwm"]
    except Exception as e:
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
def main():
    mode = input("1. Sleep Mode\n2. Wake up\n3. Fan control\nSelect an option: ")
    if str(mode) == "1":
        fan_control = True
        fan_pwm = 100
        miner_mode = 1
        
    elif str(mode) == "2":
        fan_control = None
        fan_pwm = None
        miner_mode = 0
    elif str(mode) == "3":
        fan_settings = input("Select a fan speed(Percentage 20\-100\ or auto:) ")
        if fan_settings == "auto":
            fan_control = False
            fan_pwm = None
        else:
            fan_control=True
            fan_pwm = fan_settings
        miner_mode = 0
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
        "bitmain-fan-ctrl" : fan_control, 	#True = fan control enabled | False = Auto fan control
        "bitmain-fan-pwm" : fan_pwm, 	    #fan speed percentage 100=5800-6100RPM | 50 = 3200-3400RPM | 20=2000-2300RPM 
        "bitmain-use-vil" : None,           #no observed effect when changed
        "bitmain-freq" : None, 		        #hashboard freq. modifying can cause hashboard corruption.
        "bitmain-voltage" : None,	        #hashboard voltage. modifying can cause hashboard corruption.
        "bitmain-ccdelay" : None,	        #power suppply delay. Not sure if it does anything on a production machine.
        "bitmain-pwth" : None,              #no observed effect when changed
        "bitmain-work-mode" : None,         #no observed effect when changed
        "bitmain-freq-level" : None,        #no observed effect when changed
        "miner-mode" : miner_mode 		    #0=normal, 1=sleep, None=NoChange
    }
    

    password = getPass("pwd.txt")	#Gets a List of all passwords
    ip = getIP()                    #Gets list of IPs

    #config
    results = [] 
    with concurrent.futures.ThreadPoolExecutor(max_workers=10000) as executor: #configs 10000 units at a time
        futures = []
        minerList = []
        for i in ip:
            futures.append(executor.submit(x19Conf, 'root', password, i, payload))
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())# for debugging issues
    
    #reboot. Only needed for fan modification.
    if str(mode) == '3':
        bresults = [] 
        with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
            futures = []
            for i in ip:
                futures.append(executor.submit(x19Reboot, 'root', password, i))
            for future in concurrent.futures.as_completed(futures):
                bresults.append(future.result())# for debugging
    sleep(10)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = []
        for i in ip:
            futures.append(executor.submit(machine_scan, 'root', password, i))
        for future in as_completed(futures):
            minerList.append(future.result())

    
    print("Finished pushing configs")

    cols = ['IP','Asset','Workmode','Fan Control','Fan %']

    df = pd.DataFrame(minerList)
    df.columns = cols
    
    counts = df['Workmode'].value_counts()
    counts = counts.reset_index()
    counts.columns = ['Workmode','Counts']
    # print(counts)
    print(tabulate(counts,tablefmt="fancy_grid",showindex="never", headers=['Workmode','Counts']))

    sc_folder = "./CSV Files/"      
    dn_folder = "./Archive/"
    copy_folder = "./Active Sleeping/"
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

        if miner_mode == 0:
            file_name1 = "Wake " + Timestamp() + ".csv"
        elif miner_mode == 1:
            file_name1 = "Sleep " + Timestamp() + ".csv"
        else:
            file_name1 = "Fan Config " + Timestamp() +".csv"
        source = sc_folder + file_name
        destination = dn_folder + file_name1

        if os.path.isfile(source):
            shutil.move(source, destination)
            if miner_mode == 1:
                shutil.copy(destination, copy_folder)
            
main()
os.system("pause")