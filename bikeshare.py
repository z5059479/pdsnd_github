from datetime import datetime
import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
#1st line
#2nd line
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
    while True:
        city = input("Would you like to see data for Chicago, New York, or Washington?\n").lower()
        if city not in ['chicago', 'new york', 'washington']:
            print('There is something wrong with the input, please try again.\n')
            continue
        if city == 'new york':
            city = 'new york city'
        break
    #Ask if want to filter by day, month, both or none
    while True:
        filter_option = input("Would you like to filter the data by month, day, both, or not at all? type \"none\" for no time filter\n").lower()
        if filter_option not in ['month', 'day', 'both', 'none']:
            print('There is something wrong with the input, please try again.\n')
            continue
        break
    # TO DO: get user input for month (all, january, february, ... , june)
    #set month = None by default
    month = None
    if filter_option in ['both', 'month']:
        while True:
            month = input("Which month? January, February, March, April, May, or June?\n").lower()   
            if month not in ['january', 'february', 'march', 'april', 'may', 'june']:
                print('There is something wrong with the input, please try again.\n')
                continue
            break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    #set day = None by default
    day = None
    if filter_option in ['both', 'day']:
        while True:
            #input will be string stead of integer(is '1', not 1)
            day = input("Which day? Please type your response as an integer (e.g., 0=Sunday, 1=Monday).\n")
            #check input type before check value
            try:
                test_value = int(day)
            except ValueError:
                print('Input is not integer, try again\n')
                continue
            if not 0 <= int(day) < 7:
                print('There is something wrong with the input, please try again.\n')
                continue
            break

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
    #read the pd based on city first
    df = pd.read_csv(CITY_DATA[city])
    
    #filter month
    if month:
        #print(pd.to_datetime(df.head(1)['Start Time']))
        df = df[pd.to_datetime(df['Start Time']).dt.strftime("%B") == month.capitalize()]
        #print(df)
    
    #filter day:
    if day:
        #print(pd.to_datetime(df.head(1)['Start Time']))
        df = df[pd.to_datetime(df['Start Time']).dt.strftime("%w") == day]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_month = pd.to_datetime(df['Start Time']).dt.strftime("%B").mode()[0]
    print('Most Common Month: {}\n'.format(most_month))
    
    # TO DO: display the most common day of week
    most_day = pd.to_datetime(df['Start Time']).dt.strftime("%A").mode()[0]
    print('Most Common Day of the Week: {}\n'.format(most_day))
    
    # TO DO: display the most common start hour
    most_hour = pd.to_datetime(df['Start Time']).dt.strftime("%H").mode()[0]
    print('Most Common Start Hour: {}\n'.format(most_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start_station = df['Start Station'].mode()[0]
    print('Most Common used Start Station: ', most_start_station + '\n')
    
    # TO DO: display most commonly used end station
    most_end_station = df['End Station'].mode()[0]
    print('Most Common used End Station: ', most_end_station + '\n')
    print()
    # TO DO: display most frequent combination of start station and end station trip Ref:https://stackoverflow.com/questions/15222754/groupby-pandas-dataframe-and-select-most-common-value
    df['Stations'] = df['Start Station'] + ',' + df['End Station']
    most_stations  = df['Stations'].mode()[0]
    print('Most Frequent Combination of Start Station & End Station:')
    start_station, end_station = most_stations.split(',')
    print('Start Station: ', start_station)
    print('End Station: ', end_station)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print('Total Travel Time: {} seconds\n'.format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print('Mean Travel Time: {} seconds\n'.format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts().to_dict()
    print('User Types:')
    for key, value in user_types.items():
        print('{} : {}'.format(key, value))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        genders = df['Gender'].value_counts().to_dict()
        print('\nGenders:')
        for key, value in genders.items():
            print('{} : {}'.format(key, value))    

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('\nYear of Birth')
    
        #Earliest
        #put int() as min() returns decimal
        earliest_yob = int(df['Birth Year'].min())
        print('Earliest: ', earliest_yob)
    
        #Most Recenct
        #put int() as min() returns decimal
        latest_yob = int(df['Birth Year'].max())
        print('Earliest: ', latest_yob)
    
        #Most Frequenst
        #put int() as min() returns decimal
        most_yob = int(df['Birth Year'].mode()[0])
        print('Earliest: ', most_yob)   
    
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)  
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
       

if __name__ == "__main__":
	main()
