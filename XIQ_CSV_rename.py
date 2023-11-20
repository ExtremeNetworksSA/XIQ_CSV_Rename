#!/usr/bin/env python3
import os
import inspect
import logging
import argparse
import sys
import math
import time
import getpass
import pandas as pd
import numpy as np
from app.logger import logger
from app.xiq_api import XIQ
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
logger = logging.getLogger('CSV_Rename.Main')


XIQ_API_token = ''

pageSize = 100

parser = argparse.ArgumentParser()
parser.add_argument('--external',action="store_true", help="Optional - adds External Account selection, to use an external VIQ")
args = parser.parse_args()

PATH = current_dir

# Git Shell Coloring - https://gist.github.com/vratiu/9780109
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
GREEN = "\033[0;32m"
YELLOW = "\033[0;33m"
RESET = "\033[0;0m"


totalExisting = 0
totalOnboard = 0 
totalFailed = 0

## XIQ API Setup
if XIQ_API_token:
    x = XIQ(token=XIQ_API_token)
else:
    print("Enter your XIQ login credentials")
    username = input("Email: ")
    password = getpass.getpass("Password: ")
    x = XIQ(user_name=username,password = password)
#OPTIONAL - use externally managed XIQ account
if args.external:
    accounts, viqName = x.selectManagedAccount()
    if accounts == 1:
        validResponse = False
        while validResponse != True:
            response = input("No External accounts found. Would you like to import data to your network?")
            if response == 'y':
                validResponse = True
            elif response =='n':
                sys.stdout.write(RED)
                sys.stdout.write("script is exiting....\n")
                sys.stdout.write(RESET)
                raise SystemExit
    elif accounts:
        validResponse = False
        while validResponse != True:
            print("\nWhich VIQ would you like to import the floor plan and APs too?")
            accounts_df = pd.DataFrame(accounts)
            count = 0
            for df_id, viq_info in accounts_df.iterrows():
                print(f"   {df_id}. {viq_info['name']}")
                count = df_id
            print(f"   {count+1}. {viqName} (This is Your main account)\n")
            selection = input(f"Please enter 0 - {count+1}: ")
            try:
                selection = int(selection)
            except:
                sys.stdout.write(YELLOW)
                sys.stdout.write("Please enter a valid response!!")
                sys.stdout.write(RESET)
                continue
            if 0 <= selection <= count+1:
                validResponse = True
                if selection != count+1:
                    newViqID = (accounts_df.loc[int(selection),'id'])
                    newViqName = (accounts_df.loc[int(selection),'name'])
                    x.switchAccount(newViqID, newViqName)



print("Make sure the csv file is in the same folder as the python script.")
filename = input("Please enter csv filename: ")

csv_df = pd.read_csv(filename,dtype=str)
csv_df['serialnumber'].replace('', np.nan, inplace=True)


# Check for duplicates in the CSV
duplicateSN = csv_df['serialnumber'].dropna().duplicated().any()
if duplicateSN:
    log_msg = ("Multiple APs have the same serial numbers in the CSV file. Please fix and try again.")
    logger.warning(log_msg)
    sys.stdout.write(RED)
    sys.stdout.write('\n' + log_msg + '\n')
    sys.stdout.write("script is exiting....")
    sys.stdout.write(RESET)
    raise SystemExit


# Check for rows on CSV file that are missing serial numbers
nanValues = csv_df[csv_df['serialnumber'].isna()]


listOfSN = list(csv_df['serialnumber'].dropna().unique())

if nanValues.serialnumber.size > 0 and len(listOfSN) == 0:
    log_msg = ("Serial numbers were not found for any AP in the CSV. Please check to make sure they are added correctly and try again.")
    logger.warning(log_msg)
    sys.stdout.write(YELLOW)
    sys.stdout.write("\n"+log_msg + '\n')
    print("script is exiting....")
    sys.stdout.write(RESET)
    raise SystemExit
elif nanValues.serialnumber.size > 0:
    totalFailed += nanValues.serialnumber.size
    sys.stdout.write(YELLOW)
    sys.stdout.write("\nSerial numbers were not found for these APs. Please correct and run the script again if you would like to add them.\n  ")
    sys.stdout.write(RESET)
    print(*nanValues.hostname.values, sep = "\n  ")
    logger.info("Serial numbers were not found for these APs: " + ",".join(nanValues.hostname.values))


# Batch serial numbers 
sizeofbatch = 100
if len(listOfSN) > sizeofbatch:
    sys.stdout.write(YELLOW)
    sys.stdout.write(f"\nThis script will work in batches of {sizeofbatch} APs.\n\n")
    sys.stdout.write(RESET)

count = 1
for i in range(0, len(listOfSN),sizeofbatch):
    print(f"Starting batch {count} of {math.ceil(len(listOfSN)/sizeofbatch)}")
    batch = listOfSN[i:i+sizeofbatch]
    cleanBatch = listOfSN[i:i+sizeofbatch]
    apSNFound = False
    # check if they exist 
    existingAps = x.checkApsBySerial(batch) 
    for ap in existingAps:
        batch = list(filter(lambda a: a != ap['serial_number'], batch))

    if batch:
        log_msg = (f"{len(batch)} out of {len(cleanBatch)} AP serial numbers were not found.")
        print(log_msg)
        logger.warning(log_msg)

    if existingAps:
        apSNFound = True
        for ap in existingAps:
            filt = csv_df["serialnumber"] == ap['serial_number']
            hostname = csv_df.loc[filt,'new name'].values[0].strip()
            response = x.renameAP(ap['serial_number'], hostname)
            if response != "Success":
                log_msg = f"Failed to change name of {hostname} on {ap['serial_number']}"
                sys.stdout.write(RED)
                sys.stdout.write(log_msg + '\n')
                sys.stdout.write(RESET)
                logger.error(log_msg)
            else:
                logger.info(f"Changed name of AP '{ap['serial_number']}' to {hostname}")
                
    print("Completed batch")
    
    count += 1

