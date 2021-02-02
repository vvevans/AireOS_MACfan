import pandas as pd
from netaddr import *

#######################################################################################
#################################### Sanitize MAC Addresses ###########################
#######################################################################################
### Input from customer should either be spreadsheet with ap info or csv. Create csv###
### and name it 'ap_inventory.csv', as this is what script looks for. Column header ###
### for mac-addresses should be named 'mac_address'.                                ###
### This script can be used exclusively and also feeds into 'aireos_macfan'         ###
### to create mac-addrs in Unix-expanded format and ap naming commands for AireOS.  ###
#######################################################################################
################################### written by Virgil Evans ###########################
#######################################################################################

field = ['mac_address']
df = pd.read_csv('ap_inventory.csv', usecols=field)
# print summary of all columns / rows
print(df)

# modify dataframe to drop empty fields
modified_df = df.dropna()
# print new summary, minus empty fields
print(modified_df.isnull().sum())

bare_mac_list = []
def sanitize_mac(macs):
    valid_macs = [mac for mac in macs['mac_address'] if valid_mac(mac)]
    for mac in valid_macs:
        bare = EUI(mac)
        bare.dialect = mac_bare
        bare_mac_list.append(bare)
    return bare_mac_list


sanimacs = sanitize_mac(modified_df)
print(sanimacs)