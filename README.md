# Automated Daily Maximum/Average Climograph Trend Analysis Pipeline for the National Oceanic and Atmospheric Administration's Local Climatological Database

Standalone program for creating and analyzing climographs for every day of the calendar year using historical synoptic data from the National Oceanic and Atmospheric Administration's (NOAA's) Local Climatological Database (LCD). By borrowing scripts from the Novel-Metrics-for-Analyzing-Extreme-Heat-Patterns-Across-US-Cities repository, it operates as a robust ETL (extract, transform, load) pipeline for converting long-term hourly weather data into daily maximum/average quantities useful for atmospheric inquiries and then displays the readings in a time series and histogram based on a selected calendar day. This is useful for determining the range for a given city on a particular day in terms temperature/heat index/etc., as well as if those values have changed substantially with time. The statistical analysis performs best if given at least 30 years of data for a particular station, though obviously performs better given an even larger time span.

# Technical Information:

Language: Python 3.11+

Libraries: Pandas (Dataframes), NumPy (Matrix Math), MetPy (Atmospheric calcs), Scipy (Stats), Matplotlib (Visualization).

Infrastructure: Logging (System monitoring).

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

