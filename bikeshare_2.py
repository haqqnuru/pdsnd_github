import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

LIST_DAY = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}

LIST_MONTH = {'january': 1, 'february': 2, 'march': 3,'april': 4,'may': 5,'june': 6}

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Which of these cities would you like to see data from? Chicago, New York City, or Washington?\n')
        if city.lower() == 'chicago':
            print('You selected Chicago')
            break
        elif city.lower() == 'new york city':
            print('You selected New York City')
            break
        elif city.lower() == 'washington':
            print('You selected Washington')
            break
        else:
            print('You entered the wrong city. Please enter either Chicago, New York City or Washington')
           
    # filter data or no filter
    while True:
        filter = input('Do you want to filter the data or not? if yes, enter \'YES\'. if no filter, enter \'NO\'\n')
        if filter.lower() == 'yes':
            filter = True
        elif filter.lower() == 'no':
            filter = False
        else:
            print ('You entered the wrong input. Please enter \'YES\' or \'NO\'.')
            continue
        break

    # get user input for month (all, january, february, ... , june)
    while True:
        if filter:
            choice = input('How do you want to filter the data? by month or day?\n')
            if choice.lower() == 'month':
                month = input('Please enter a month between January to June.\n').lower()
                if month not in LIST_MONTH:
                    print ('You entered the wrong input. Please try again.')
                    continue
                month = LIST_MONTH[month]
                day ='all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
            elif choice.lower() == 'day':
                day = input('Please enter a day from Monday to Sunday.\n').lower()
                if day not in LIST_DAY:
                    print ('You entered the wrong input. Please try again.')
                    continue
                day = LIST_DAY[day]
                month ='all'
            else:
                print ('Please enter \'MONTH\' or \'DAY\'.')
                continue
            break
        else:
            day ='all'
            month ='all'
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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

     # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # filter by month if applicable
    if month != 'all':

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

        # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    
    return df



def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # extract month, day and hour of week from Start Time to create new columns
    df['hour']= df['Start Time'].dt.hour

    # display the most common month
    most_common_month = df['month'].mode()[0]
    for common in LIST_MONTH:
        if LIST_MONTH[common]==most_common_month:
            most_common_month = common.title()
    print('The most common month for traveling is', most_common_month)

    # display the most common day of week
    most_common_day = df['day_of_week'].mode()[0]
    for common in LIST_DAY:
        if LIST_DAY[common]==most_common_day:
            most_common_day = common.title()
    print('The most common day of week for traveling is', most_common_day)

    # display the most common start hour
    most_common_shour = df['hour'].mode()[0]
    print('The most common hour for travel is', most_common_shour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is', common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is', common_end_station)

    # display most frequent combination of start station and end station trip
    freq_combination = 'Start Station = ' + df['Start Station'] + ' and End Station = ' + df['End Station']
    print('The most frequent combination of start station and end station trip is', freq_combination.mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total travel time is', total_travel_time)

    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('The mean travel time is', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df.groupby('User Type',as_index=False).count()
    print('There are {} types of users in {}'.format(len(user_types), city.title()))
    for i in range(len(user_types)):
        print(user_types['User Type'][i], '=', user_types['Start Time'][i])

    # Display counts of gender
    print()
    if 'Gender' not in df:
        print('No gender information available in', city.title())
    else:
        gender = df.groupby('Gender',as_index=False).count()
        print('The counts of gender are:')
        for i in range(len(gender)):
            print(gender['Gender'][i], '=', gender['Start Time'][i])

    # Display earliest, most recent, and most common year of birth
    print()
    if 'Birth Year' not in df:
        print('No birth information available in', city.title())
    else:
        early_birth = int(df['Birth Year'].min())
        print('The earliest year of birth is', early_birth)
        recent_birth = int(df['Birth Year'].max())
        print('The most recent year of birth is', recent_birth)
        common_birth = int(df['Birth Year'].mode())
        print('The most common year of birth is', common_birth)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    """Displays raw data."""

    print('\nGetting the raw data...\n')

    raw_data = input('Would you like to see the raw data? if yes, enter \'YES\' to see raw data or enter any key to exit.\n').lower()
    raw=0
    while raw_data == 'yes':
        print(df[raw:raw+5])
        raw+=5
        raw_data = input('Would you like to see more raw data? if yes, enter \'YES\' to see more raw data or enter any key to exit.\n').lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? if yes, enter \'YES\' to restart or enter any key to exit program.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
