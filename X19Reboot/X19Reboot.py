# Created by Ethan Johnson for use at Core Scientific
# Python 3.9
from requests.auth import HTTPDigestAuth
import concurrent.futures
from requests import get
from pathlib import Path
from time import sleep
import pandas as pd
import datetime
import shutil
import os

def x19Reboot(user,password, IP):
    print("Rebooting " + IP + "...")
    for i in password:
        try:
            respo = get("http://" + IP + '/cgi-bin/reboot.cgi', auth=HTTPDigestAuth(user, i)) #Send Reboot to IP
            if respo.status_code == 200:
                respo.close()
                sleep(20) #Boot time for S19s with zynq control boards.
                print("Reboot successful for " + str(IP))
            else:
                print("Rebooting " + IP + " May have failed...")

        except OSError: return "Failed to reboot " + IP

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

    y = xyear +"_"+ xmonth +"_"+ xday + "_" + xhour + xminute + xsecond
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

def main():
    password = getPass("pwd.txt")	#Gets a List of all passwords
    ip = getIP()                    #Gets list of IPs

    bresults = [] 
    with concurrent.futures.ThreadPoolExecutor(max_workers=1000) as executor:
        futures = []
        for i in ip:
            futures.append(executor.submit(x19Reboot, 'root', password, i))
        for future in concurrent.futures.as_completed(futures):
            bresults.append(future.result())
    
    sc_folder = "./CSV Files/"      
    dn_folder = "./Archive/"

    for file_name in os.listdir(sc_folder):         #Moves all csv files to Archive folder
        post_file = "Reboot " + Timestamp() + ".csv"
        source = sc_folder + file_name
        destination = dn_folder + post_file

        if os.path.isfile(source):
            shutil.move(source, destination)
main()