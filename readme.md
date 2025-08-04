# XIQ CSV Rename - UPDATE IN PROGRESS
### XIQ_CSV_rename.py
## Purpose
This script will rename the Hostname of devices from a CSV file. The CSV file will need to have a column labeled ***'serialnumber'*** that contains a list of serial numbers and a column labeled ***'new_name'*** with the new hostname for the device. 

Enhanced verion:  This script will also change the description field of a specified device using the same CSV file.  A column must have the label ***'new_description'***.

Any hostname or description cell that is blank will be skipped.
## Information
The script will perform API calls to check that those serial numbers exist in the VIQ, if not, it will log a message that the device doesn't exist. 

## Needed files
The XIQ_CSV_rename.py script uses several other files. If these files are missing the script will not function.
In the same folder as the XIQ_CSV_rename.py script there should be an /app/ folder. Inside this folder should be a logger.py file and a xiq_api.py file. After running the script a new file 'csv_rename_log.log' will be created.

The script requires a CSV file to be entered when ran. This CSV file should be added to the same folder as the script.

The log file that is created when running will show any errors that the script might run into. It is a great place to look when troubleshooting any issues.

## Running the script
open the terminal to the location of the script and run this command.

```
python XIQ_CSV_rename.py
```
### Logging in
The script will prompt the user for XIQ credentials.
>Note: your password will not show on the screen as you type

### Entering the csv file
The script will prompt to enter the CSV file.
```
Make sure the csv file is in the same folder as the python script.
Please enter csv filename:
```
Enter the name of the file that is located in the same folder as the script and press enter.

### flags
There is an optional flag that can be added to the script when running.
```
--external
```
This flag will enable you to execute this script on an XIQ account where you are an external user. After logging in with your XIQ credentials, the script will give you a numeric option of each of the XIQ instances you have access to. Choose the one you would like to use.

You can add the flag when running the script.
```
python XIQ_CSV_rename.py --external
```
## requirements
There are additional modules that need to be installed in order for this script to function. They are listed in the requirements.txt file and can be installed with the command 'pip install -r requirements.txt' if using pip.
