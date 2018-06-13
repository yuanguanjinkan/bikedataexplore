import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def convert_float_to_int(values):
    if values is np.nan:
        return 0
    else:
        return int(values)

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
    city_list = ('chicago','new york city','washington')
    while True:
      city = input("Enter name of city(chicago, new york city, washington): ").lower()
      if city in city_list :
          break

    # TO DO: get user input for month (all, january, february, ... , june)
    month_list = ('all','january','february','march','april','may','june','july','august','september','october','november','december')
    while True:
      month = input("Enter month(all, january, february, ... , june): ").lower()
      if month in month_list :
          break

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day_list = ('all','monday','tuesday','wednesday','thursday','friday','saturday','sunday')
    while True:
      day = input("Enter month(all, monday, tuesday, ... sunday): ").lower()
      if day in day_list:
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
    """
    first load the file 
    """
    df = pd.read_csv(CITY_DATA[city])
	
    #filter the  month and day data
    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june','july','august','september ','october ','november','december']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
        
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    most_common_month = ''
    if not df['month'].mode().empty:
        most_common_month = df['month'].mode()[0]
    print("\nThe most common month:", most_common_month)

    # TO DO: display the most common day of weekm
    most_common_dayofweek = ''
    if not df['day_of_week'].mode().empty:
        most_common_dayofweek = df['day_of_week'].mode()[0]
    print("\nThe most common day of week:", most_common_dayofweek)
    
    # TO DO: display the most common start hour    
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour
    most_common_start_hour = ''
    if not df['hour'].mode().empty:
        most_common_start_hour = df['hour'].mode()[0]
    print("\nThe most common start hour:", most_common_start_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    most_start_station = ''
    if len(df['Start Station'].mode()) > 0:
        most_start_station = df['Start Station'].mode()[0]
    print("\nThe most start station:", most_start_station)
    

    # TO DO: display most commonly used end station
    most_end_station = ''
    if len(df['End Station'].mode()) > 0:
        most_end_station = df['End Station'].mode()[0]
        
    print("\nThe most end station:", most_end_station)
    
    # TO DO: display most frequent combination of start station and end station trip
    tmp_count = df.groupby(['Start Station','End Station'])['Start Time'].count()
    most_start_end_station = ''
    if not tmp_count.empty:
        most_start_end_station = df.groupby(['Start Station','End Station'])['Start Time'].count().idxmax()
    print("\nThe  most frequent combination of start station and end station trip:", most_start_end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_tavel_time = df['Trip Duration'].sum()
    print("\nThe  total travel time:", total_tavel_time)


    # TO DO: display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    if total_tavel_time == 0:
        mean_travel_time = 0
        
    print("\nThe mean travel time:", mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    # TO DO: Display counts of user types
    counts_of_user_types = df['User Type'].count()
    print('counts_of_user_types \n',counts_of_user_types)

    # TO DO: Display counts of gender
    counts_of_gender = ''
    if df.columns.str.lower().contains('gender'):
        counts_of_gender = df['Gender'].count()
    print('counts_of_gender \n',counts_of_gender)

    # TO DO: Display earliest, most recent, and most common year of birth    if df.columns.str.lower().contains('gender'):
    earliest_birthday = np.nan
    most_recent_birthday = np.nan
    most_common_year_of_birthday = np.array([])
    if df.columns.str.lower().contains('birth year'):
        earliest_birthday = df['Birth Year'].min()
        most_recent_birthday = df['Birth Year'].max()
        most_common_year_of_birthday = df['Birth Year'].mode()
    
    if len(most_common_year_of_birthday) > 0:
        most_common_year_of_birthday = most_common_year_of_birthday[0]
    else:
        most_common_year_of_birthday = np.nan
    
    print('earliest_birthday \n',convert_float_to_int(earliest_birthday))
    print('most_recent_birthday\n',convert_float_to_int(most_recent_birthday))
    print('most_common_year_of_birthday\n',convert_float_to_int(most_common_year_of_birthday))

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
