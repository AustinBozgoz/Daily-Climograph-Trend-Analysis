import os

#for the sake of the atmospheric scientists not that versed in python
cwd=os.path.dirname(os.path.abspath(__file__))#locate directory with scripts
os.chdir(cwd) #change directory to where scripts are located

##################################################################################

import sys
import checkpoint_maker
import LCD_hourly_daily_max
import logging
import daily_climograph_trend_analysis
import LCD_API_download
import calendar


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    force=True,
    handlers=[
        logging.FileHandler("Daily Climograph.log",mode='a',encoding='utf-8',delay=False), # Saves to a file
        #logging.StreamHandler()              # Also prints to your terminal
    ]
)

def main(cwd):
    print('Working in path %s \n \n'%cwd)
    finish=0
    
    while finish==0:
        print('\n \nThis code runs in a 3 step sequence')
        print('(1) Download hourly weather data from a particular station')
        print('(2) Analyze hourly weather data and convert it into daily max/avgs')
        print('(3) Create Daily Trend Climographs for a specific calendar day')
        print('Please select a step using a number')
        
        selection=input()

        if '1' in selection:
            logging.info('Beginning API Data Pull...')
            LCD_API_download.LCD_API_Pull(cwd)
            logging.info('Successfully pulled data from API')
            finish=1
    
        elif '2' in selection:
            logging.info('Beginning Daily Max/Avg conversion...')
            print('\n \n Please select a function')
            print('(1) Convert daily max/avg for one city within \\NOAA_LCD_CSVs\\')
            print('(2) Convert daily max/avg for all cities within \\NOAA_LCD_CSVs\\')
            selection=input()
        
            if '1' in selection:
                guard=0
                while guard==0:
                    print('\n \n Input the city, state exactly as its listed in the \\NOAA_LCD_CSVs\\ folder')
                    print('e.g. Austin, TX or Atlanta, GA; mind the capitalization and space')
                    city=input()
                    if os.path.exists(cwd+'\\NOAA_LCD_CSVs\\'+city)==True:guard=1
                    else: 
                        print('Error no directory %s'%(cwd+'\\NOAA_LCD_CSVs\\'+city))
                        print('Check capitalization and syntax')
            
                guard=0
                while guard==0:
                    print('\n \n Input the 3 letter designator exactly as its listed in the \\NOAA_LCD_CSVs\\ %s folder'%city)
                    print('Only the 3 letter designator, do not include the LCD')
                    ID=input()
                    if os.path.exists(cwd+'\\NOAA_LCD_CSVs\\'+city+'\\'+ID+' LCD')==True:guard=1
                    else: 
                        print('Error no directory %s'%(cwd+'\\NOAA_LCD_CSVs\\'+city+'\\'+ID+' LCD'))
                        print('Check capitalization and syntax')
                logging.info('Converting daily max/avg for one city %s %s LCD ...'%(city,ID))
                LCD_hourly_daily_max.LCD_hourly_daily_max(cwd+'\\NOAA_LCD_CSVs\\',oneCity=city,oneStation=ID)
                logging.info('Completed conversion for %s %s LCD'%(city,ID))
                finish=1
            
            elif '2' in selection:
                guard=0
                while guard==0:
                    print('\n \n Please select a function')
                    print('(1) Start a new conversion for all cities within \\NOAA_LCD_CSVs\\')
                    print('(2) Continue an interrupted conversion for all cities within \\NOAA_LCD_CSVs\\')
                    selection=input()
            
                    if '1' in selection:
                        guard=1
                        logging.info("Making Checkpoint....")  
                        checkpoint_maker.checkpoint_maker('new',cwd+'\\NOAA_LCD_CSVs\\')
                        logging.info('Beginning LCD Analysis....')
                        LCD_hourly_daily_max.LCD_hourly_daily_max(cwd+'\\NOAA_LCD_CSVs\\')
                        logging.info('Completed LCD Analysis for all cities')
                        finish=1
                
                    elif ('2' in selection) and (os.path.isfile(cwd+'\\NOAA_LCD_CSVs\\checkpoint.csv')==False):
                        print('Error, missing checkpoint file within \\NOAA_LCD_CSVs\\, please choose 1 as your selection')
                    elif ('2' in selection):
                        guard=1
                        logging.info('Beginning LCD Analysis....')
                        LCD_hourly_daily_max.LCD_hourly_daily_max(cwd+'\\NOAA_LCD_CSVs\\')
                        logging.info('Completed LCD Analysis for all cities')
                        finish=1
                    else: print('\n \n Please make a selection 1-2 \n \n')
                    
        elif '3' in selection:
            guard=0
            while guard==0:
                print('\n \n Please select a function')
                print('(1) Analyze all calendar days')
                print('(2) Analyze a specific calendar day')
                selection=input()
                    
                if '1' in selection:
                    guard=1
                    date='annual'
                    
                elif '2' in selection:
                    guard=1
                    guard1=0
                    while guard1==0:
                        print('\n \nEnter the number of the month for analysis (e.g. April would be 4)')
                        month=input()
                        if (month.isnumeric()==True): 
                            if (float(month).is_integer()==True):
                                if (int(month)>0) and (int(month)<13):guard1=1
                                else: print('Month should be between 1 and 12 for the months of the year')
                            else: print('Month should be an integer')
                        else: print('Month should be an integer')
                    month=int(month)
                    
                    maxDay=daily_climograph_trend_analysis.month_day_range(month)[-1]
                    guard1=0
                    while guard1==0:
                        print('\n \nEnter the day of the month for analysis')
                        day=input()
                        if (day.isnumeric()==True): 
                            if (float(day).is_integer()==True):
                                if (int(day)>0) and (int(day)<=maxDay):guard1=1
                                else:
                                    print('Only %i days in month %i'%(maxDay,month))
                                    print('Day of the month should be between 1 and %i'%maxDay)
                            else: print('Day should be an integer')
                        else: print('Day should be an integer')
                    date=[int(month),int(day)]
                        
                else: print('\n \n Please make a selection 1-2')
                
            guard=0
            while guard==0:
                print('\n \n Please select a function')
                print('(1) Analyze for all available years')
                print('(2) Analyze for a specific year range')
                print('Note accurate statistical analysis needs at least a 30 year period')
                selection=input()
                    
                if '2' in selection:
                    guard2=0
                    while guard2==0:
                        guard1=0
                        while guard1==0:
                            print('\n \nEnter the starting year')
                            startYear=input()
                            if (startYear.isnumeric()==True): 
                                if (float(startYear).is_integer()==True):
                                    if (int(startYear)>1900) and (int(startYear)<2100):guard1=1
                                    else: print('Starting Year should be between 1900 and 2100')
                                else: print('Starting Year should be an integer')
                            else: print('Starting Year should be an integer')
                        guard1=0
                        while guard1==0:
                            print('\n \nEnter the ending year')
                            endYear=input()
                            if (endYear.isnumeric()==True):
                                if (float(endYear).is_integer()==True):
                                    if (int(endYear)>1900) and (int(endYear)<2100):guard1=1
                                    else: print('Ending Year should be between 1900 and 2100')
                                else: print('Ending month should be an integer')
                            else: print('Ending month should be an integer')
                        if endYear<startYear:print('End year should be after start year')
                        else:guard2=1
                    years=[int(startYear),int(endYear)]
                    guard=1
                    
                elif '1' in selection:
                    guard=1
                    years='all'
                    
                else: print('\n \n Please make a selection 1-2')
                    
            guard=0
            while guard==0:
                print('\n \n Please select a function')
                print('(1) Analyze for all cities in \\NOAA_LCD_CSVs\\')
                print('(2) Analyze for a specific city')
                selection=input()
                    
                if '1' in selection:
                    guard=1
                    logging.info('Clearing Checkpoint graphs...')
                    checkpoint_maker.checkpoint_maker('clear graphs',cwd+'\\NOAA_LCD_CSVs\\')
                    logging.info('Creating Climographs for all cities....')
                    daily_climograph_trend_analysis.daily_climograph_trend_analysis(date=date,city='all',years=years,quantity='all',base=cwd+'\\NOAA_LCD_CSVs\\')
                    logging.info('Completed Analysis of all Cities')
                    finish=1
                    
                if '2' in selection:
                    guard=1
                        
                    guard1=0
                    while guard1==0:
                        print('\n \n Input the city, state exactly as its listed in the \\NOAA_LCD_CSVs\\ folder')
                        print('e.g. Austin, TX or Atlanta, GA; mind the capitalization and space')
                        city=input()
                        if os.path.exists(cwd+'\\NOAA_LCD_CSVs\\'+city)==True:guard1=1
                        else: 
                            print('Error no directory %s'%(cwd+'\\NOAA_LCD_CSVs\\'+city))
                            print('Check capitalization and syntax')
                                
                    guard1=0
                    while guard1==0:
                        print('\n \n Input the 3 letter designator exactly as its listed in the \\NOAA_LCD_CSVs\\ %s folder'%city)
                        print('Only the 3 letter designator, do not include the LCD')
                        ID=input()
                        if os.path.exists(cwd+'\\NOAA_LCD_CSVs\\'+city+'\\'+ID+' LCD')==True:guard1=1
                        else: 
                            print('Error no directory %s'%(cwd+'\\NOAA_LCD_CSVs\\'+city+'\\'+ID+' LCD'))
                            print('Check capitalization and syntax')
                        
                    logging.info('Creating Climographs for %s'%city)
                    daily_climograph_trend_analysis.daily_climograph_trend_analysis(date=date,city=city,stationID=ID+' LCD',years=years,quantity='all',base=cwd+'\\NOAA_LCD_CSVs\\')
                    logging.info('Completed Analysis of %s'%city)
                    finish=1
    return


if __name__ == "__main__":
    main(cwd)
    
