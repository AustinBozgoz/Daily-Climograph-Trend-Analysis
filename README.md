# Automated Daily Maximum/Average Climograph Trend Analysis Pipeline for the National Oceanic and Atmospheric Administration's Local Climatological Database

Standalone program for creating and analyzing climographs for every day of the calendar year using historical synoptic data from the National Oceanic and Atmospheric Administration's (NOAA's) Local Climatological Database (LCD). By borrowing scripts from the Novel-Metrics-for-Analyzing-Extreme-Heat-Patterns-Across-US-Cities repository, it operates as a robust ETL (extract, transform, load) pipeline for converting long-term hourly weather data into daily maximum/average quantities useful for atmospheric inquiries and then displays the readings in a time series and histogram based on a selected calendar day. This is useful for determining the range for a given city on a particular day in terms temperature/heat index/etc., as well as if those values have changed substantially with time. The statistical analysis performs best if given at least 30 years of data for a particular station, though obviously performs better given an even larger time span.

# Technical Information:

Language: Python 3.11+

Libraries: Pandas (Dataframes), NumPy (Matrix Math), MetPy (Atmospheric calcs), Scipy (Stats), Matplotlib (Visualization).

Infrastructure: Logging (System monitoring).

# Project Architecture:

