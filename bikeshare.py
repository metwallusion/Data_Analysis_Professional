import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

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
    i=0
    while(i==0):
        city=input("For which city (chicago, new york city, washington) ? Type 'exit' to close the program.\n")
        exit() if city.lower()=="exit" else 0
        #i=True if city.lower() in CITY_DATA else print("You entered {}. Please enter a valid data (city)".format(city))
        if city in CITY_DATA: i+=1
        else: print("You entered {}. Please enter a valid data (city)".format(city))

    months = ['all','january', 'february', 'march', 'april', 'may', 'june']
    # TO DO: get user input for month (all, january, february, ... june)
    i=0
    while(i==0):
        month=input("For which month i.e (january, february, ..., june)? Enter 'all' to get all months.\n")
        exit() if month.lower()=="exit" else 0
        if month.lower() in months: i+=1
        else: print("You entered {}. Please enter a valid data (month)".format(month))

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    weekDays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday","all"]
    i=0
    while(i==0):
        day=input("For which day i.e (monday, tuesday, ... sunday)? Enter 'all' to get all days.\n")
        exit() if day.lower()=="exit" else 0
        if day.lower() in weekDays: i+=1
        else: print("You entered {}. Please enter a valid data (day)".format(day))


    print('-'*40)
    return city.lower(), month.lower(), day.lower()

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
    df=pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time']=pd.to_datetime(df['End Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    df_copy=df.copy()

    if month.lower() != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        df = df[df['month'] == month]
    else:
        month='all'
    if day.lower() != 'all':
        df = df[df['day_of_week'] == day.title()]
    else:
        day='all'
    return df,df_copy,month,day

def time_stats(df,df_copy,month_num,day_entered):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    # TO DO: display the most common month
    print("The most common month of all is '{}'".format((months[(df_copy['month'].mode()[0])-1]).title()))

    # TO DO: display the most common day of week
    print("The most common day of the week within your selected month '{}' is '{}'".format((months[(df['month'].mode()[0])-1]).title(),\
    df_copy['day_of_week'][df_copy['month'] == month_num].mode()[0])) if month_num !='all' else print("The most common day of the week of all months is '{}'".\
    format(df_copy['day_of_week'].mode()[0]))

    # TO DO: display the most common start hour
    if month_num !='all' and day_entered !='all':
        print("The most common start hour within your selected day '{}' and month '{}' is '{}'".format(df['day_of_week'].mode()[0],\
        (months[(df['month'].mode()[0])-1]).title(),df['hour'].mode()[0]))
    elif month_num =='all' and day_entered !='all':
        print("The most common start hour within your selected day '{}' and all months is '{}'".format(df['day_of_week'].mode()[0],df_copy['hour']\
        [df_copy['day_of_week']==df['day_of_week'].mode()[0]].mode()[0]))
    elif month_num !='all' and day_entered =='all':
        print("The most common start hour within all days in month '{}' is '{}'".\
        format((months[(df['month'].mode()[0])-1]).title(),df_copy['hour'][df_copy['month']==df['month'].mode()[0]].mode()[0]))
    else:
        print("The most common hour of all months and days is '{}'".format(df_copy['hour'].mode()[0]))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df,df_copy):
    """Displays statistics on the most popular stations and trip."""
    #Each commented line containing df_copy can be used to get the output for all times
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    print("The most commonly used start station within your month/day selection is '{}'\n".format(df['Start Station'].mode()[0]))
    #print("The most commonly used start station of all times is '{}'\n".format(df_copy['Start Station'].mode()[0]))

    # TO DO: display most commonly used end station
    print("The most commonly used end station within your month/day selection is '{}'\n".format(df['End Station'].mode()[0]))
    #print("The most commonly used end station of all times is '{}'\n".format(df_copy['End Station'].mode()[0]))

    # TO DO: display most frequent combination of start station and end station trip
    print("The most frequent combination of start and end stations within your month/day selection is:\n{}\n".\
    format(df.groupby(['Start Station','End Station']).size().idxmax()))
    #print("The most frequent combination of start and end stations of all times selection is:\n{}\n".\
    #format(df_copy.groupby(['Start Station','End Station']).size().idxmax()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    print("Total travel time is '{}' seconds\n".format(df['Trip Duration'].sum()))

    # TO DO: display mean travel time
    print("Average travel time is '{}' seconds\n".format(df['Trip Duration'].mean()))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    #df.fillna(df.mean())
    # TO DO: Display counts of user types
    print("Counts of user types:\n{}\n".format(df['User Type'].value_counts()))


    # TO DO: Display counts of gender
    print("Counts of gender:\n{}\n".format(df['Gender'].value_counts()))


    # TO DO: Display earliest, most recent, and most common year of birth
    print("The year of birth:\n{} is the earliest\n{} is the most recent\n{} is the most common\n".\
    format(df['Birth Year'].min(),df['Birth Year'].max(),df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df,df_copy,month_num,day_entered = load_data(city, month, day)
        #df is the filtered data , df_copy is a copy for the unfiltered data
        time_stats(df,df_copy,month_num,day_entered)
        station_stats(df,df_copy)
        trip_duration_stats(df)
        user_stats(df)
        view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?: ")
        start_loc = 0
        i=0
        while (view_data.lower() == 'yes' and i<len(df.iloc[0:-1]) ):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            i+=1
            view_data = input("Do you wish to continue?: ").lower()
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
