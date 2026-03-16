# Automated Daily Maximum/Average Climograph Trend Analysis Pipeline for the National Oceanic and Atmospheric Administration's Local Climatological Database

Standalone program for creating and analyzing climographs for any day of the calendar year using historical synoptic data from the National Oceanic and Atmospheric Administration's (NOAA's) Local Climatological Database (LCD). By borrowing modules from the LCD-Daily-Max-Avg-Downloader-and-Converter repository, it both downloads and operates as a robust ETL (extract, transform, load) pipeline for converting long-term hourly weather data into daily maximum/average quantities useful for atmospheric inquiries. These quantities are then displayed in a time series and histogram based on a selected calendar day. This is useful for determining the range of the synoptic values a city experiences for a particular day, as well as if those values have changed substantially with time. The statistical analysis performs best if given at least 30 years of data for a particular station, though obviously is more accurate if given an even larger span of time.

# Technical Information:

Language: Python 3.11+

Libraries: Pandas (Dataframes), NumPy (Matrix Math), MetPy (Atmospheric calcs), Scipy (Stats), Matplotlib (Visualization), Requests (API HTTP Integration)

Infrastructure: Logging (System monitoring).

# Pipeline Architecture:

Ingest: requests fetches raw CSV from NOAA.

Clean: Pandas and NumPy handle the ETL process.

Compute: MetPy and SciPy derive advanced metrics like Wet Bulb and heat Index.

Visualize: Matplotlib generates timeseries and histograms. NumPy and SciPy perform regression techniques on the data to create a line of best fit and analysis on the histograms.

# Getting Started

## Clone the repo
git clone https://github.com/AustinBozgoz/LCD-Daily-Max-Avg-Downloader-and-Converter

## Install dependencies
pip install -r requirements.txt

## Run the pipeline
python src/main.py

## Operation
This program operates in a 3 step sequence as directed by user input:

1) Downloads the hourly LCD information for a given station
   * To find the correct station, navigate to https://www.ncei.noaa.gov/cdo-web/datatools/lcd and find the station you want to use. Record the 5 digit WBAN for the station (for example, Atlanta Hartsfield Airport is 13874). Then navigate to https://infosys.ars.usda.gov/svn/code/windgen/doc/USAF-WBAN.txt and, using ctrl-F, input the WBAN to locate the full station ID. The 11 digit station identifier is the combination of the first two columns listed beside your station (for example, Atlanta Hartsfield airport would be 72219013874)
   * The LCD data will be saved in a directory labelled NOAA_LCD_CSVs within the same folder the python scripts are located in
   * Input the name of the city, state exactly as its listed on the NOAA website
   * Input a 3 letter designator for the particular station (for example, Atlanta Hartsfield Airport might be ATL)
   * The CSVs are downloaded in batches of ten years to reduce the chances of the server request timing out
2) Converts the hourly weather data into daily maximum/average values
   * Can convert one city at a time, in which case input the city, state exactly as the directory is written inside the NOAA_LCD_CSVs folder and give the same 3 letter designator as the station
   * Can also convert all cities located within the NOAA_LCD_CSVs folder, in which case an extra file titled checkpoint.csv is saved to prevent redoing completed cities if the process is interrupted
3) Organizes daily maximums/averages by calendar day to create timeseries graphs and histograms of synoptic values
   * All plots are saved within the directories for their respective cities, in a folder called climographs
   * Creates a timeseries plot to show how the daily value changes over the years. Plots a line of best fit over the timeseries and displays values related to the LOBF, including the p-value for the fit. The alternative hypothesis for the linear regression analysis is that the slope is nonzero.
   * Creates a histogram of the values to show the occurance for each value.
   * The statistical features (average, skewness, standard deviation) for the histogram are then used to create a theoretical histogram describing the range and probability of occurance for a particular synoptic value. This estimation obviously assumes the synoptic value is constant with time

# Project Architecture:

Data Input: Reads raw csv's from NOAA's LCD database (https://www.ncdc.noaa.gov/cdo-web/datatools/lcd). The database only permits data downloading one decade at a time, so you must download the information each decade starting at January 1st at the beginning of the decade (or whenever the sation first started collecting information) to the last day in the decade (as in December 31st, the 9th year of the decade). E.g. for the 1980s of a particular station, the csv should be dated from January 1st, 1980 to December 31st, 1989. If the station started in 1985, it is also acceptable to use a csv of [Any month] [Any day], 1985 to December 31st, 1989. Manual Adjustments to the code will need to be made in order to include csv's of more recent years (i.e. past 2019).

Data Formating: LCD data files should be saved in csv file extension and organized within a directory labelled NOAA_LCD_CSVs, saved within the source file. Within that folder should be another directory with the name of the city, and within that should be a 3 letter designation for the station the data was taken from, followed by a space and the letters LCD. Within that directory thee csv files should be saved as the 3 letter station ID_LCD_the starting year-the ending year for that batch of data. For example, the LCD data for Miami, Florida (station ID MIA) from 1980-1989 should be saved within the same directory as the source files as NOAA_LCD_CSVs/Miami, FL/ MIA LCD/MIA_LCD_1980-1989.csv  

Error Correction: Checks hourly readings and removes letters from entries, ignores blank entries, checks that values are reasonable (e.g. temperature is not in the thousands of degrees)

Processing: Uses MetPy for unit-aware calculations (e.g. Heat Index) and Scipy for probability distribution plot analysis as well as outlier detection.

Output: Generates cleaned data, turning hourly readings of daily maximum/average temperature, heat index, wet-bulb temperature, relative humidity; seperates that data based on calendar day to create a time series graph and a histogram graph for each data type. The time series graphs also include a line of best fit along with a p-value describing an alternate hypothesis of a non-zero slope.

# Key Features:

Statistical Analysis for Time Series' Line of Best Fit slope: The alternative hypothesis for the linear regression analysis is that the slope is nonzero, and the p-value for the null hypothesis is displayed on the graph. If the p-value is less than .05, that is strong statistical evidence that the slope is nonzero (i.e. the value is increasing or decreasing with time)

Theoretical Histogram generation: Alongside a timeseries graph for each calendar day, a histogram is also created displaying the frequency that each quantity occurs. This data is extrapoloted to calculate the average, standard deviation, and skewness of a normal distribution and those factors are used to create a theoretical histogram. This describes the probability distribution for that paticular synoptic quantity for that given calendar day (e.g. for january 1st our station's temperature has a 60% chance to be within 70 and 75 degrees farhenheit). This approximation makes the assumption that the synoptic quantity is constant with time, and should therefore be ignored if the p-value for the timeseries graphh was less than .05.
    
HIstogram value at percentile: An unused function within the daily_climograph_trend_analysis module will take the theoretical histogram inputs (avg,std,skew of the extrapolated normal distribution) and a random number between 0 and 1 to return the value of the histogram associated with that percentile. This has applications in monte-carlo simulations that have a dependence of synoptic values for a given calendar day and has been applied to other projects that utilize the rest of this script.

Modular Design: Every major step of the ETL pipeline is seperated into a different script and outputs its transformation into a seperate and meticulously labelled database. This allows for versatility of use for this project not only to find extreme heat values but to also utilize daily maximum values from any city within the LCD database. The error correction function is also cleanly seperated as a standalone function, allowing for any future programmer to easily clean and utilize the LCD database for any project.

Unit Based Calculations: Incorporated metpy in order to ensure consistent use of fahrenheit for all heat-index related calculations

Versatility: Utilized directory packages and organization to permit for a theoretically unlimited number of cities within the analysis. Also included simple controls for the sake of limiting the analysis timeframe to any month or year range as specified by the user.

Resilence: Implemeneted a global logging system in order to track which csv's or cities are corrupted.

Performance: Implemeneted a combination of numpy vectorization and standard python loops in order to optimize performance of high-volume datasets and ensure accuracy of calculations.

# Clone the repo
git clone https://github.com/AustinBozgoz/Daily-Climograph-Trend-Analysis

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python src/main.py

