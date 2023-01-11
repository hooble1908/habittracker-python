#all functions related to creating, storing and reading from database

import sqlite3
from datetime import date, datetime, timedelta 
import pandas as pd


def get_db(name="main.db"):
    """
    conncect to SQL Database for storing habit data and check data
    Parameter:
        name of database, if no name given than defaultvalue
    Returns:
        db as variable for other functions
    """
    try:
        db = sqlite3.connect(name)
        print("Database " + name + " ready.")
        return db
    except Exception as e:
        print("Connecting to Database failed!", e)
        close_db(db)


def close_db(db):
    """
    close connection to SQL Database
    Parameter:
        db variable
    Returns:
        print that db connection is closed
    """
    print("database connection closed!")
    db.close()


def create_tables(db):
    """
    creates two tables  - habits (contains habits, their descriptions and period of validity for streak),
                        - checks (name of habit, period and checkdates and number of current streak)
    if they already exist than nothing happens
    Parameters:
        db - database in which the tables will be created
    Returns:
        print if it was successful or not
    """
    try:
        cur = db.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS habits (
            name VARCHAR(50) PRIMARY KEY,
            description TEXT,
            period VARCHAR(10),
            adding_date TIMESTAMP
            );""")
    
        cur.execute("""CREATE TABLE IF NOT EXISTS checks (
            checkID INTEGER PRIMARY KEY,
            habit VARCHAR(50),      
            period VARCHAR(10),
            checkdate TIMESTAMP,
            streak INTEGER,
            FOREIGN KEY (habit) REFERENCES habits(name));""")
    
        db.commit()
        print("Tables successfully created in database.")
    
    except Exception as e:
        print("Something went wrong while creating tables: ",e)
        close_db(db)
    
    
def add_habit(db, name, description, period, adding_date=None):
    """
    adds new habit to table habits with description and periodicity of habit, used for creating testdata
    Parameters:
        db - database where table is
        name - name of habit added
        description - short description of habit
        period - intervall in which a habit must be checked to maintain the streak
        adding_date - date of creation habit, default current day
    Returns:
        print that habit was added to table
    """
    try:
        cur = db.cursor()
        if not adding_date: #default value is TODAY
            adding_date = str(date.today())
        cur.execute("""INSERT INTO habits (name, description, period, adding_date) VALUES (?,?,?,?) """, (name, description, period, adding_date))
        add_check(db, name, period, adding_date)
        db.commit()
        print("Habit " + name + " was added to database.")
        print("-----------------------------------------") #just for better visuability in CLI
    
    except Exception as e:
        print("Something went wrong while adding a habit: ", e)
        print("-----------------------------------------")


def add_check(db, name, period, checkdate=None, streak=1):
    """
    adds new check to table habits with habitname, period, checkdate and streakvalue, used for creating testdata
    Parameters:
        db - database where table is
        name - name of habit added
        period - intervall in which a habit must be checked to maintain the streak
        checkdatedate - date habit was checked for testdata
        streak - streakvalue for habit in regards of period
    Returns:
        print that check was added to table
    """    
    if not checkdate:
        checkdate = date.today()
    cur = db.cursor()
    cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (name, period, checkdate, streak))
    db.commit()

     
def get_last_checkdate(db, name=None):
     """
     get last checkdate from table checks for selected habit, if non given than user can entry
     Parameter:
         db - database where table "checks" is
         name - name of habit
     Returns:
         last_checkdate for selected habit as data for further functions         
     """
     if not name:
         data = overview_all_habits(db)
         name = input("for which habit you want to see last checkdate?: ")
         while name not in data: #to catch exception that user enters a NON-existing habit
             name = input("habitname NOT in list. Please enter correct habitname: ")
     try:
         cur = db.cursor()
         last_checkdate = cur.execute("SELECT MAX(checkdate) FROM checks WHERE habit=?", (name,)) #highest value for date is last date
         last_checkdate = cur.fetchone()
         return last_checkdate
     
     except Exception as e:
         print("Something went wrong with checkdata from: " + name, e)
         print("-----------------------------------------")


def get_last_checkdate_all(db):
     """
     get last checkdate from every habit from table, with pandas dataframe
     Parameter:
         db - database where table "checks" is
     Returns:
         pandas dataframe with habit, period, last checkdate, last streak
     """
     try:
         cur = db.cursor()
         cur.execute("SELECT DISTINCT habit, period, checkdate, streak FROM checks")
         df = pd.DataFrame(cur.fetchall(), columns = ['habit', 'period', 'last checkdate', 'last streak'])
         print(df.groupby(["period","habit",]).max()) #other way to get highest value with pandas, highest ID means last entry
         print("---------------------------------")
     
     except Exception as e:
         print("Something went wrong with getting checkdata: ", e)    
         

def get_last_checkdate_period(db, period=None):
     """
     get last checkdate from every habit with specific period, with pandas dataframe
     Parameter:
         db - database where table "checks" is
     Returns:
         pandas dataframe with habit, period and last checkdate
     """
     if not period:
         period = input("for which period you want to get last checkdates?: ")
     try:
         cur = db.cursor()
         cur.execute("SELECT DISTINCT habit, period, checkdate FROM checks WHERE period=?", (period,))
         df = pd.DataFrame(cur.fetchall(), columns = ['habit', 'period', 'last checkdate',])
         print(df.groupby(["period","habit",]).max()) #maximum from ID is latest entry
     
     except Exception as e:
         print("Something went wrong with getting checkdata: ", e) 


def overview_all_habits(db):
    """
    select all names and their period from table "habits" of current database.
    Parameters:
        db - database
    Returns:
        print of db-export row by row for user
        first dataobject (habitname) as tuple for further functions in analysis 
    """
    print("------------------------------------------")
    cur = db.cursor()
    data = cur.execute("SELECT DISTINCT name, period FROM habits")
    data = [i[0] for i in data]
    print("List of all habits: ",data)
    print("------------------------------") #just for visuability in CLI
    return data #for further use in functions
    
    
def overview_daily_habits(db):
    """
    select all habits from table "habits" of current database with period daily.
    Parameters:
        db - database
    Returns:
        print of db-export row by row
        habitnames as datatuple for use in other functions
    """
    period = "daily"
    cur = db.cursor()
    data = cur.execute("SELECT DISTINCT name FROM habits WHERE period=?", (period,))
    data = [i[0] for i in data]
    print("Overview all daily habits: ", data)
    return data
    print("-----------------------------------------")
    

def overview_weekly_habits(db):
    """
    select all habits from table "habits" of current database with period weekly.
    Parameters:
        db - database
    Returns:
        print of db-export
        habitnames as datatuple for use in other functions
    """
    period = "weekly"
    cur = db.cursor()
    data = cur.execute("SELECT DISTINCT name FROM habits WHERE period=?", (period,))
    data = [i[0] for i in data]
    print("Overview all weekly habits: ", data)
    return data
    print("-----------------------------------------")


def habits_details(db):
    """
    select habits and their details from table "habits" from current database
    Parameters:
        db - database
    Returns:
        print of db-export
        exportdata as datatuple for use in other functions
    """
    print("------------------------------------------------------------")
    print("Overview all Habits and their details. ")
    cur = db.cursor()
    data = cur.execute("SELECT DISTINCT * FROM habits")
    print("habit, description, period, creationdate")
    for row in cur:
        print(row)
    return data
    print("---------------------------------------")        

def habit_details_single(db, name=None):
    """
    select specific habit and its details from table "habits" from current database
    Parameters:
        db - database
    Returns:
        print of db-export in CLI
    """
    if not name: #if no name is given, but normally should from other calling function
        name = input("for which habit you want to get all details?: ")
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE name=?", (name,))
    print("habit, description, period, creationdate")
    for row in cur:
        print(row)   


def habit_details_period(db, period=None):
    """
    select habits and their details from table "habits" from current database for all habits of specific period
    Parameters:
        db - database
        period - habits of which period are chosen
    Returns:
        print of db-export
    """
    if not period:
        period = input("for which period you want to get all details?: ")
    cur = db.cursor()
    cur.execute("SELECT * FROM habits WHERE period=?", (period,))
    print("-------------------------------------------") # only for better visuability in CLI
    print("habit, description, period, creationdate")
    for row in cur:
        print(row)
    print("---------------------------------")   # only for better visuability in CLI 
        
        
def delete_habit_data(db, name):
    """
    deletes all entries from selected habit from tables "habits" and "checks"
    Parameters:
        db - database
        name - name of habit which should be deleted
    Returns:
        print
    """
    cur = db.cursor()
    cur.execute("DELETE * FROM habits WHERE habit_name=?", (name,))
    cur.execute("DELETE * FROM checks WHERE name=?", (name,))
    db.commit()
    db.close()
    print("Habit" + name + "and its checks deleted successfully.")
    print("--------------------------------------------------")
    
def check_habit(db, name, checkdate=None):
    """
    adds new checkentry to table "checks" with habitname, period, checkdate and value with current streak
    Parameters:
        db - database where table is
        name - name of habit added
        checkdate - current day of checking
    Returns:
        print that check was added to table checks
    """
    try:
        cur = db.cursor()
        if not checkdate: #define default if none is given
            checkdate = date.today()
        period = cur.execute("""SELECT DISTINCT period FROM habits WHERE name=?""", (name,))
        period = str(cur.fetchone())
        period = period[2:-3]    #prepare string so value for period is correct for input in function below
        streak = streak_ongoing(db, name, period)
        cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (name, period, checkdate, streak))
        db.commit()
        print("Habit " + name + " was checked successfully.")
    
    except Exception as e:
        print("Something went wrong while checking: " + name, e)
        print("-----------------------------------------")


def streak_ongoing(db, name, period):
    """
    calculates actual streakvalue for habit from last checkdate, last streakvalue and difference to today in regards of period
    Parameters:
        db - name database checkinformation is stored
        name - name of habit that is checked if streak is still active
        period - period of habit, needed to correctly calculate streak
    Returns:
    if the difference of last checkdate and todays check is within period than +1 to current streak value is added to checkentry, 
    if not within streakperiod than value for streak is 1
    """
    try:
        try:
            last_checkdate = str(get_last_checkdate(db, name))
            last_checkdate = last_checkdate[2:-3]
            print("Last Checkdate for habit " + name + " was: ",last_checkdate)
            last_checkdate = datetime.strptime(last_checkdate, '%Y-%m-%d') #change to datetimeobject so timedelta can be calculated
            now = datetime.now()
            now.replace(minute=0, hour=0, second=0, microsecond=0) #change timestamp so always calculate from same timepoint of day
            print("Today is: ", now.date())
            difference_check = now - last_checkdate # calculate difference from two datetime objects
            last_streak = get_last_streak(db, name)
            last_streak = str(last_streak)
            last_streak = last_streak[1:-2]
            streak = int(last_streak) #convert to integer so we can calculate new streakvalue
            print("Last Streak: ", streak)
       
            if period == "daily":
                print(period + " difference is: " + str(difference_check.days)) #print with difference in days
                
                if difference_check <= timedelta(days=1):   #if habit is checked multiple times on same day                 
                    print("already checked in current period")
                    print("Actual Streak is now: ", streak)
                    print("Streak for " + name + " continues.")
                
                elif difference_check <= timedelta(days=2): #correct timedelta, streakvalue +=1
                    streak += 1
                    print("Actual Streak is now: ", streak)
                    print("Streak for " + name + " continues.")
                
                else: #streak broken, new begins
                    streak = 1
                    print("Actual Streak is now: ", streak)
                    print("New streak for " + name + " starts today. Keep going!")
                
            elif period == "weekly": #=calendarweek
                
                difference_weekly = now.isocalendar().week - last_checkdate.isocalendar().week #timedelta from two dates in calendarweeks
                print(period + " difference is: " + str(difference_weekly) + " calendarweeks.")

                if difference_weekly == 1: #correct timedelta, current streak gets 1 more, other ways to check than days for learningpurposes
                    streak += 1
                    print("Actual Streak is: ", streak)
                    print("Streak for " + name + " continues.")
                
                elif difference_weekly == 0: #multiple checks in same calendarweek, to ashure no cheating in streakvalue
                    print("already checked in current period")
                    print("Actual Streak is: ", streak)
                    print("Streak for " + name + " continues.")
                
                else: #streak broken, new begins
                    streak = 1
                    print("Actual Streak is: ", streak)
                    print("New streak for " + name + " starts today. Keep going!")
            else: #to catch logical errors, set value to 1 
                streak = 1
                print("There is a problem with streakdata. Please check entry in db.")
            return streak #return new streakvalue for storing in database
        
        except Exception as e:
            print("Something went wrong while checking streakdata: ",e)
            streak = 1
            
    except Exception as e:
        streak = 1
        print("Streakvalue 1 by default. Please check data in db." + e)
    
    finally:
        print("------------------------------------------")
        return streak


def streakdata_single(db, name=None):
    """
    Parameters:
        db - database where table checks is
        name - optional, if not given user can choose which habit he wants to see streakinformation - normally value is given from other function
    Returns:
        pandas dataframe with all checkentries from specific habit without duplicates
    """
    cur = db.cursor()
    if not name:
        name = input("checkdata for which habit?: ")
    cur.execute("SELECT * FROM checks WHERE habit=?", (name,))
    df = pd.DataFrame(cur.fetchall(), columns = ["checkID", "habit", "period", "last checkdate", "streak"])
    df = df.drop_duplicates("last checkdate")
    print(df)


def get_last_streak(db, name):
    """
    get last streak from table checks for selected habit
    Parameter:
        db - database where table "checks" is
        name - name of habit
    Returns:
        last_streak: value for further functions
    """
    try:
        cur = db.cursor() #no check if name is valid habit because check is implemented in chain before already
        last_streak = cur.execute("SELECT streak FROM checks WHERE habit=? ORDER BY checkID DESC LIMIT 1", (name,))
        last_streak = cur.fetchone()
        return last_streak
    
    except Exception as e:
        print("Something went wrong with checkdata from: " + name, e)
    

def actual_streak_today_single(db, name=None):
    """
    calculates actual streakvalue from today, if there is no checkentry for current day in table
    -----------------------------
    Parameters:
        db - database where table checks is 
        name - name of habit, in not given than user can entry
    Returns:
        variable with actual streakvalue if there would be a checkentry for today
    """
    cur = db.cursor()    
    if not name:
        name = input("for which habit you want to see the actual streak from view TODAY?: ")
    period = cur.execute("""SELECT DISTINCT period FROM habits WHERE name=?""", (name,))
    period = str(cur.fetchone())
    period = period[2:-3]
    streak_ongoing(db, name, period)


def actual_streak_today_period(db, period=None):
    """
    calculates actual streakvalue from view = today, if there is no checkentry for current day in table
    -----------------------------
    Parameters:
        db - database where table checks is 
        period - period of habits are analysed, if not given than user can entry
    Returns:
        output of called function about actual streakvalue for each habit of period
    """   
    if not period:
        period = input("for which PERIOD you want to see the actual streaks from view TODAY? (daily) or (weekly): ")
    
    if period == "daily":
        data = overview_daily_habits(db)
        for i in data: #loop for every habit of choosen period
            streak_ongoing(db, i, period)
    elif period == "weekly":
        data = overview_weekly_habits(db)
        for i in data: #loop for every habit of choosen period
            streak_ongoing(db, i, period)
    else: #logical exception for incorrect periodvalue
        print("Please check value for period. Invalid value!")


def defaultdata_db(db):
    """
    creates testdata in database for testingpurposes of functionality, analysis and errorhandling
    -----------------------------
    Parameters:
        db - database where table checks is 
    Returns:
        print that data was created successfully or exception
    """   
    try: #for shure better way, but nooby :)
        add_habit(db, "jogging", "1x a week", "weekly", "2022-12-02")
        add_habit(db, "swimming", "1x a week", "weekly", "2022-11-30")
        add_habit(db, "stairs", "no elevator at home or work", "daily", "2022-11-30")
        add_habit(db, "cigarettes", "not even drunk", "daily", "2022-12-07")
        add_habit(db, "vitamins", "drink or tablette", "daily", "2022-12-04")
        add_habit(db, "no fastfood", "no pizza, kebap or mcdo/bk", "weekly", "2022-11-30")
        add_check(db, "jogging", "weekly", "2022-12-07", "2")
        add_check(db, "jogging", "weekly", "2022-12-18", "3")
        add_check(db, "jogging", "weekly", "2022-12-28", "1")
        add_check(db, "jogging", "weekly", "2023-01-03", "1")
        add_check(db, "swimming", "weekly", "2022-12-13", "1")
        add_check(db, "swimming", "weekly", "2022-12-19", "2")
        add_check(db, "swimming", "weekly", "2023-01-02", "1")
        add_check(db, "stairs", "daily", "2022-12-01", "2")
        add_check(db, "stairs", "daily", "2022-12-02", "3")
        add_check(db, "stairs", "daily", "2022-12-03", "3")
        add_check(db, "stairs", "daily", "2022-12-04", "4")
        add_check(db, "stairs", "daily", "2022-12-05", "5")
        add_check(db, "stairs", "daily", "2022-12-07", "1")
        add_check(db, "stairs", "daily", "2022-12-08", "2")
        add_check(db, "stairs", "daily", "2022-12-09", "3")
        add_check(db, "stairs", "daily", "2022-12-10", "4")
        add_check(db, "stairs", "daily", "2022-12-11", "5")
        add_check(db, "stairs", "daily", "2022-12-12", "6")
        add_check(db, "stairs", "daily", "2022-12-13", "7")
        add_check(db, "stairs", "daily", "2022-12-24", "1")
        add_check(db, "stairs", "daily", "2022-12-26", "1")
        add_check(db, "stairs", "daily", "2022-12-30", "1")
        add_check(db, "stairs", "daily", "2022-12-31", "2")
        add_check(db, "stairs", "daily", "2023-01-01", "3")
        add_check(db, "stairs", "daily", "2023-01-03", "1")
        add_check(db, "cigarettes", "daily", "2022-12-08", "2")
        add_check(db, "cigarettes", "daily", "2022-12-09", "3")
        add_check(db, "cigarettes", "daily", "2022-12-11", "1")
        add_check(db, "cigarettes", "daily", "2022-12-12", "2")
        add_check(db, "cigarettes", "daily", "2022-12-13", "3")
        add_check(db, "cigarettes", "daily", "2022-12-14", "4")
        add_check(db, "cigarettes", "daily", "2022-12-15", "5")
        add_check(db, "cigarettes", "daily", "2022-12-17", "1")
        add_check(db, "cigarettes", "daily", "2022-12-18", "2")
        add_check(db, "cigarettes", "daily", "2022-12-19", "3")
        add_check(db, "cigarettes", "daily", "2022-12-20", "4")
        add_check(db, "cigarettes", "daily", "2022-12-21", "5")
        add_check(db, "cigarettes", "daily", "2022-12-22", "6")
        add_check(db, "cigarettes", "daily", "2022-12-23", "7")
        add_check(db, "cigarettes", "daily", "2022-12-24", "8")
        add_check(db, "cigarettes", "daily", "2022-12-25", "9")
        add_check(db, "cigarettes", "daily", "2022-12-26", "10")
        add_check(db, "cigarettes", "daily", "2022-12-28", "1")
        add_check(db, "cigarettes", "daily", "2022-12-29", "2")
        add_check(db, "cigarettes", "daily", "2022-12-30", "3")
        add_check(db, "cigarettes", "daily", "2023-01-01", "1")
        add_check(db, "cigarettes", "daily", "2023-01-03", "1")
        add_check(db, "vitamins", "daily", "2022-12-05", "2")
        add_check(db, "vitamins", "daily", "2022-12-08", "1")
        add_check(db, "vitamins", "daily", "2022-12-09", "2")
        add_check(db, "vitamins", "daily", "2022-12-10", "3")
        add_check(db, "vitamins", "daily", "2022-12-13", "1")
        add_check(db, "vitamins", "daily", "2022-12-14", "2")
        add_check(db, "vitamins", "daily", "2022-12-15", "3")
        add_check(db, "vitamins", "daily", "2022-12-16", "4")
        add_check(db, "vitamins", "daily", "2022-12-17", "5")
        add_check(db, "vitamins", "daily", "2022-12-18", "6")
        add_check(db, "vitamins", "daily", "2022-12-19", "7")
        add_check(db, "vitamins", "daily", "2022-12-20", "8")
        add_check(db, "vitamins", "daily", "2022-12-21", "9")
        add_check(db, "vitamins", "daily", "2022-12-22", "10")
        add_check(db, "vitamins", "daily", "2022-12-23", "11")
        add_check(db, "vitamins", "daily", "2022-12-25", "1")
        add_check(db, "vitamins", "daily", "2022-12-27", "1")
        add_check(db, "vitamins", "daily", "2022-12-29", "1")
        add_check(db, "vitamins", "daily", "2022-12-30", "2")
        add_check(db, "vitamins", "daily", "2022-12-31", "3")
        add_check(db, "vitamins", "daily", "2023-01-02", "1")
        add_check(db, "no fastfood", "weekly", "2022-12-20", "1")
        add_check(db, "no fastfood", "weekly", "2022-12-26", "2")  
        print("Checkdata added to database.")
        db.commit()
        
    
    except Exception as e:
       print("Something went wrong with implementing testdata: ", e)
       close_db(db)
       