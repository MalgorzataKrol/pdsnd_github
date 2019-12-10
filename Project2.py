# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 14:23:37 2019

@author: USER
"""


import time
import pandas as pd
#import numpy as np
from matplotlib import pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = {1: 'january',
          2: 'february',
          3: 'march',
          4: 'april',
          5: 'may',
          6: 'june',
          7: 'all'}
WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

# function to return key for any value (val) from dictionary dictionary
def get_key_val(dictionary, val): 
    for key, value in dictionary.items(): 
         if val == value: 
             return key 

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = None
    while city not in CITY_DATA.keys():
        city = input("Choose the city (chicago, new york city, washington):")
        city = city.lower()


    # TO DO: get user input for month (all, january, february, ... , june)
    month = None
    while month not in MONTHS.values():
        month = input("Choose month of the analysis from: {}:".format(MONTHS.values()))
        month = month.lower()

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = None
    while day not in WEEKDAYS:
        day = input("Choose day from {}:".format(WEEKDAYS))
        day = day.lower()

    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    #print(df.head())
    # convert the Start Time and End Time column to datetime, create col. Travel Time
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
    df['Travel Time'] = df['End Time'] - df['Start Time']

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = get_key_val(MONTHS, month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        week_day = WEEKDAYS.index(day)
        df = df[df['day_of_week'] == week_day]
    
    return df

#filters_output = get_filters()
#dff = load_data(filters_output[0], filters_output[1], filters_output[2])

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    month_mode = df['month'].mode()[0]
    print("\n The most common month: ", MONTHS[month_mode])

    # TO DO: display the most common day of week
    day_mode = df['day_of_week'].mode()[0]
    print("\n The most common day of week: ", WEEKDAYS[day_mode])

    # TO DO: display the most common start hour
    start_hour_mode = df['Start Time'].dt.hour.mode()[0]
    print("\n The most common start hour: ", start_hour_mode)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station_mode = df['Start Station'].mode()[0]
    print("\n The most common start station: ", start_station_mode)  

    # TO DO: display most commonly used end station
    end_station_mode = df['End Station'].mode()[0]
    print("\n The most common end station: ", end_station_mode)  

    # TO DO: display most frequent combination of start station and end station trip
    df['Start - End Station'] = df['Start Station'] + ' - ' + df['End Station']
    print("\n The most common start - end station trip: ", df['Start - End Station'].mode()[0])  

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("\nTotal travel time: ", df['Travel Time'].sum())

    # TO DO: display mean travel time
    print("\nMean travel time: ", df['Travel Time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
def trip_duration_histo(df):
    """ Plots 2 histograms - for number of rentals for 1.months, 2.day of week"""
    """ Plots histograms only if 1.'all' months were selected, 2. 'all' days of week were selected"""
    
    print('\nCreating histogram...\n')
    

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize = (12,4))
    
    #print the histogram only if df contains data for all months
    if df['month'].max() - df['month'].min() > 0:
        ax1.set_xlabel('month')
        ax1.set_ylabel('number of rentals')
        ax1.hist(df['month'], bins = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], rwidth = 0.95)
        Months2=["nothing"] + list(MONTHS.values())
        ax1.set_xticklabels(Months2[:7], rotation=45)
    else:
        ax1.remove()
        
    #print the histogram only if df contains data for all days of week
    if df['day_of_week'].max() - df['day_of_week'].min() > 0:
        ax2.set_xlabel('day of week')
        ax2.set_ylabel('number of rentals')
        ax2.hist(df['day_of_week'], bins = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5], rwidth = 0.95)
        ax2.set_xticklabels(['nothing'] + WEEKDAYS[:7], rotation=45)
    else:
        ax2.remove()
        
    plt.show()


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    print("\nUser Types\' count:\n", df['User Type'].value_counts())

    # TO DO: Display counts of gender
    try:
        print("\nGender count:\n", df['Gender'].value_counts())
        print("The earliest year of birth: ", df['Birth Year'].min())
        print("The most recent year of birth: ", df['Birth Year'].max())
        print("The most common year of birth: ", df['Birth Year'].mode()[0])
    except:
        print("\nChoose Chicago or NYC to get more statistics!")
    
    # TO DO: Display earliest, most recent, and most common year of birth


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        trip_duration_histo(df)
        user_stats(df)
        

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()

    