# XIQ CSV Rename

|  _The software is provided as-is and [Extreme Networks](http://www.extremenetworks.com/) has no obligation to provide maintenance, support, updates, enhancements, or modifications. Any support provided by [Extreme Networks](http://www.extremenetworks.com/) is at its sole discretion._

_Issues and/or bug fixes may be reported on in the Issues for this repository._  |

## Purpose
This script will rename the Hostname and Description of devices from a CSV file. A CSV template example has been provided.

>Note: Use a combination of hostname and/or descriptions but the serial number is required.  Serial numbers should be unique per CSV.  Any blank hostname or description cell will be skipped.

Device List CSV Options:

| Serial Number | new_hostname | new_description |
| ------------ | ------------ | --------------- |
| 01234567891234 | Change-Hostname | <blank> | 
| ABCDEFGHIJKLMN | <blank> | Change device description |
| ABCDEFG0123456 | Change-Hostname | Change device description | 

## Information
The script will perform API calls to check if serial numbers exist in the VIQ, if not, it will log a message that the device doesn't exist. 

## Needed files
The `XIQ_CSV_rename.py` script uses several other files. If these files are missing the script will not function.

In the same folder as the `XIQ_CSV_rename.py` script there should be an /app/ folder. Inside this folder should be a `logger.py` file and a `xiq_api.py` file. After running the script a new file `csv_rename_log.log` will be created in the main directory of your CSV script.

The script requires a CSV file to be entered when ran. An example CSV file is provided named: `device_list.csv`

The log file that is created when running will show any errors that the script might run into. It is a great place to look when troubleshooting any issues.

## Running the script
Open the terminal to the location of the script and run this command.

```
python XIQ_CSV_rename.py
```
### Logging in
The script will prompt the user for XIQ credentials.  You can alternatively provide an API token in the script to bypass this requirement if desired.  See line # 17-18.

>Note: your password will not show on the screen as you type

### Entering the csv file
The script will prompt to enter the CSV file or you can press enter and accept the default name.
```
Make sure the CSV file is in the same folder as the python script if using the default name.
Please enter csv filename including "CSV" extension [default: device_list.csv <- press enter]:
```
Enter the name of the file and press enter.

### Optional Flags
There is an optional flag that can be added to the script when running.
```
--external
```
This flag will enable you to execute this script on an XIQ account where you are an external user. After logging in with your XIQ credentials, the script will give you a numeric option of each of the XIQ instances you have access to. Choose the one you would like to use.

You can add the flag when running the script.
```
python XIQ_CSV_rename.py --external
```
## Requirements
There are additional modules that need to be installed in order for this script to function. They're listed in the `requirements.txt` file and can be installed with this command if using pip.
```
pip install -r requirements.txt
```