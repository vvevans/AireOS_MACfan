# AireOS_MACfan
**Required from customer**
* "ap_inventory.csv" - an inventory file of customer's APs, with (at min.) the following columns:
  * "ap_number"
  * "mac_address"
  
Customers often provide a spreadsheet with AP mac addresses in various formats.    
The Cisco AireOS WLC works with Expanded Unix format, which is colon-delimited between bytes.   
There are two parts to this 'app'; 'sanimacs.py' can be used by itself to parse    
any mac format, from customer file named 'ap_inventory.csv'. It strips delimiters  
and outputs bare mac-addresses.                                                     
'Sanimacs.py' also removes any rows with empty fields or invalid mac-addrs based on
length (too short / long) or some typos (invalid characters).                      
                                                                                   
The script, 'AireOS_MACfan.py' uses output from previous script (sanimacs.py) to format macs for
AireOS and create AP naming commands, which are output to text file, 'ap_naming.txt'.
The naming convention here is just a site code and AP number. Can be adapted to fit
your customer's naming convention.                                                 
                                                                                   
Save customer's spreadsheet to CSV format, ensuring that the AP name/number and    
mac-address columns are named "ap_number" and "mac_address", respectively.

"requirements.txt" PIP file is included for necessary modules.
