# Created by Ethan Johnson for use at Core Scientific
# Python 3.9
from operator import itemgetter
import shutil
import os
import pandas as pd
from pathlib import Path
import datetime
import os
import numpy as np
from tabulate import tabulate
                
def dateplaceholder(n):
    if len(n) == 1:
        n = "0" + n
    return(n)

def Timestamp():        #create output string based on current date and time
    x = datetime.datetime.now()
    xyear = str(x.year)
    xmonth = dateplaceholder(str(x.month))
    xday = dateplaceholder(str(x.day))
    xhour = dateplaceholder(str(x.hour))
    xminute = dateplaceholder(str(x.minute))
    xsecond = dateplaceholder(str(x.second))

    time = xyear + "_" + xmonth + "_" +xday + "_" + xhour + xminute + xsecond
    return time

def getList():
    csvFiles = Path("./CSV Files/").rglob("*.csv")      #Checks all csv files in /CSV Files/ folder
    all_csvs = [pd.read_csv(file) for file in csvFiles]
    df = pd.concat(all_csvs) 
    return df
def help():
    print('''
    Common Shortcuts:
    'c' = 'company'     | Counts by company, globs all GEM together
    'l' = 'location'    | Counts by Building
    'm' = 'minertype'   | Counts by Miner Type
    't' = 'temp'        | Counts by Temperature, sorts by Good Temp (< 80), Over Temp(> 80), and Fans(= 255)
    's' = 'status'      | Counts by Status
    'ss' = 'substatus'  | Counts by Substatus
    
    For anything that is not a shortcut, exactly match the name of the column you want to count.
    ''')

def main():
    while True:
        item = input("What column would you like to count? (Type '-s' for list of shortcuts)")
        
        if str(item).lower().strip() == "exit" or str(item).lower().strip() == "quit":
            quit()
        if item.lower().strip() == '-s':
            help()
            continue

        df = getList()
        counts = []

        if item.lower().strip() == 'l':
            item = 'location'
        elif item.lower().strip() == 'c':
            item = 'company'
        elif item.lower().strip() == 'm':
            item = 'minertype'
        elif item.lower().strip() == 't':
            item = 'temp'
        elif item.lower().strip() == 's':
            item = 'status'
        elif item.lower().strip() == 'ss':
            item = 'substatus'

        df = df.sort_values(item)
        try:
            if str(item) == 'location':
                df['location'].replace(to_replace="-A.*", value=r"-A Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-B.*", value=r"-B Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-C.*", value=r"-C Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-D.*", value=r"-D Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-E.*", value=r"-E Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-F.*", value=r"-F Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-G.*", value=r"-G Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-H.*", value=r"-H Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-I.*", value=r"-I Building", regex=True, inplace=True)
                df['location'].replace(to_replace="-R.*", value=r"-Repair Location", regex=True, inplace=True)   

            elif str(item) == 'company':
                df['company'].replace(to_replace="GEM.*", value=r"GEM", regex=True, inplace=True)

            elif item == 'temp':
                try:
                    df['temp'] = np.where(df['temp'] < 80, 'Good Temp', np.where(df['temp'] == 0, 'Failed to pull', np.where(df['temp'] == 255, 'Fans', np.where(df['temp'] > 80,'Over Temp', 'Failed to Pull'))))
                except Exception as e:
                    print(e)
            
            counts = df.value_counts(item).sort_index()
            counts = counts.reset_index()
            counts.columns = [str(item).capitalize(),'Counts']
            post_file = "Counts_" + Timestamp() + ".csv"
            outFile = "Output/" + post_file
            cols = counts.columns
            counts.loc['Total', cols[0]] = "Total"
            counts.loc['Total','Counts'] = counts['Counts'].sum()
            
            
            print("\n\n")
            print(tabulate(counts,tablefmt="fancy_grid", headers="keys",showindex=False))
            print("\n\n")

            counts.to_csv(outFile,header=cols, index=False)

        except Exception as e:
            print("Value invalid, try again. (Exactly match the name of the column you want to count.)")
            print(e)
            continue

        i = input("Are you finished? (y/N)")
        try:
            if i[0].lower() == "y":
                break
            if i.lower == '-s':
                help()
        except Exception as e:
            continue
        
        
    sc_folder = "./CSV Files/"      
    dn_folder = "./Archive/"

    for file_name in os.listdir(sc_folder):         #Moves all csv files to Archive folder
        source = sc_folder + file_name
        destination = dn_folder + "Counts_" + Timestamp() + ".csv"

    if os.path.isfile(source):
        shutil.move(source, destination)
main()


os.system("pause")
