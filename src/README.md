**Functionality**: Identify directory having small number of PCHR log files. and move those files into few hourly directories which 
comes into log processing later. e.g directories like "9-0", "9-n". Reduces the number folders having fragmented files.


Logs> .\dist\reorganize_fragmented_hourly_logs\reorganize_fragmented_hourly_logs.exe -h

-------------------------------------------------------------------------------------------
usage: reorganize_fragmented_hourly_logs.exe [-h] [--datedir DATEDIR] base_path

positional arguments:
  base_path          Please provide the path cache\...\log under network-element directory

optional arguments:
  -h, --help         show this help message and exit
  --datedir DATEDIR  Please provide a date (YYYYMMDD) you want to work on, if not provided it will work on sysdate
  
------------------------------------------------------------------------------------------
**Usage clarification:**
Considering, no/less frequent files insertion into past dated directory. This process by default work for sysdate directory.
However we can run this process for past date manually using optional argument "--dirdate"

Thereby, It can be executed in the following two way.

1) To run this in scheduler, to perform multiple execution for sysdate, you can use this like:
--> reorganize_fragmented_hourly_logs.exe <base_path>

2) To run this manually one time for past date:
--> reorganize_fragmented_hourly_logs.exe <base_path> --dirdate YYYYMMDD
  
