###########################################################################################
######################## AireOS MAC-Address format / AP Namer #############################
###########################################################################################
### Customers often provide a spreadsheet with AP mac addresses in various formats.     ###
### The WLC works with Expanded Unix format, which is colon-delimited between bytes.    ###
### There are two parts to this 'app'; 'sanimacs.py' can be used by itself to parse     ###
### any mac format, from customer file named 'ap_inventory.csv'. It strips delimiters   ###
### and output bare mac-addresses.                                                      ###
### 'Sanimacs.py' also removes any rows with empty fields or invalid mac-addrs based on ###
### length (too short / long) or some typos (invalid characters).                       ###
###                                                                                     ###
### This script, 'AireOS_MACfan.py' uses output from previous script to format macs for ###
### AireOS and create AP naming commands, which are output to text file, 'ap_naming.txt ###
### The naming convention here is just a site code and AP number. Can be adapted to fit ###
### your customer's naming convention.                                                  ###
###                                                                                     ###
### Save customer's spreadsheet to CSV format, ensuring that the AP name/number and     ###
### mac-address columns are named "ap_number" and "mac_address", respectively.          ###
###########################################################################################
################################### written by Virgil Evans ###############################
###########################################################################################

import pandas as pd
from netaddr import *
import sanimacs
from sanimacs import sanitize_mac

# column headings looked for in customer 'ap_inventory' file
fields = ['ap_number', 'mac_address']

# empty lists to be populated by script
mac_list = []
ap_nos = []
cisco_macs = []

# create dataframe object of read csv, only specified fields
# modify dataframe to drop empty fields
# below, data is output to terminal for a quick visual check
df = pd.read_csv('ap_inventory.csv', usecols=fields)
print(df)
print("==============================\n")
modified_df = df.dropna()
# create a new csv of clean data, two columns
# modified_df.to_csv('zonea_zonec_nonull.csv', index=False)

# review number of any remaining empty fields
print(modified_df)
print("==============================\n")
print(modified_df.isnull().sum())
print()


def get_ap_nos(ap_list):
    """
    Iterate the modified dataframe, reading 'ap_number' column entries only.
    From these, create a new list of ap-name entries.
    """
    for ap in ap_list['ap_number']:
        ap_nos.append(ap)
    return ap_nos


def convert_macs(macs):
    """
    Convert mac-addrs to format recognized by WLC (extended Unix).
    Then convert each mac to a string, for the command function later.
    The 'EUI' and 'dialect' options are taken from the 'netaddr' module
    """
    for mac in macs:
        formatted = EUI(mac)
        formatted.dialect = mac_unix_expanded
        cisco_macs.append(str(formatted))
    return cisco_macs

def ap_naming(ap_nos, macs):
    """
    Combine AP no. and mac-addr lists in order to write the ap-naming command
    to a file. Iterate over 'num_macs' to add ap number and mac addr to naming
    command.
    """
    with open('ap_naming.txt', 'w+') as f:
        num_macs = zip(ap_nos, macs)
        for ap, mac in num_macs:
            command = "config ap name AL207-" + ap + " " + mac
            f.write(command)
            f.write("\n")
        return f


sanimacs = sanitize_mac(modified_df)
get_aps = get_ap_nos(modified_df)
# get_macs = get_mac_addrs(modified_df)
converted = convert_macs(sanimacs)

print(get_aps)
print("\n=========================\n")
print(converted)
print("\n=========================\n")
commands = ap_naming(get_aps, converted)
