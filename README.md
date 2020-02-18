# CodeScrapper
Command line program that gets user solutions code from a leetcode.com website. 
Program is written in python and uses selenium framework. 
Currently it can be used only for scrapping C++ code.
Program is started by the console. 


usage: scrapper.py [-h] -e EMAIL -p PASSWORD -dr DRIVERPATH [-t WAITTIME]
                   [-o OUTPUTNAME]
CodeScrapper

required arguments:
  
  -e EMAIL, --email EMAIL
                        User email
                        
  -p PASSWORD, --password PASSWORD
                        User password
                        
  -dr DRIVERPATH, --driverpath DRIVERPATH
                        Absolute path to webdriver
                        
 optional arguments:
 
  -h, --help            show this help message and exit
                        
  -t WAITTIME, --waittime WAITTIME
                        Wait time for a website to load. When error occurs,
                        try add higher wait time (default=5)
                        
  -o OUTPUTNAME, --outputname OUTPUTNAME
                        Name of output folder (default=Problems)
