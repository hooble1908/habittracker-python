#all functions regarding the analysepart of habits
import pandas as pd
from db import overview_daily_habits, overview_weekly_habits
from datetime import datetime

def count_checks_total(db):
    """
    total number of checks per habit without duplicates
    -----------------------------
    Parameters:
        db - database where table checks is 
    Returns:
        pandas dataframe with total number of checks per habit without duplicates; duplicate=two checks with same date
    """
    cur = db.cursor()
    cur.execute("SELECT habit, period, checkdate, streak FROM checks")
    df = pd.DataFrame(cur.fetchall(), columns = ["habit", "period", "last checkdate", "streak"])
    df = df.drop_duplicates()
    df = df["habit"].value_counts()
    print("Total checks per habit (without duplicates): ")
    print(df)


def count_checks_single(db, name=None):
    """
    total number of checks for specific habit without duplicates, if habit not given user can enter
    -----------------------------
    Parameters:
        db - database where table checks is 
    Returns:
        pandas dataframe with total number of checks per habit without duplicates; duplicate=two checks with same date
    """
    if not name:
        name = input("checkdata for which habit?: ")
    cur = db.cursor()
    cur.execute("SELECT habit, period, checkdate, streak FROM checks WHERE habit=?", (name,))
    df = pd.DataFrame(cur.fetchall(), columns = ["habit", "period", "last checkdate", "streak"])
    df = df.drop_duplicates()
    df = df["habit"].value_counts()
    print("Total checks (without duplicates): ", df.to_string())
    return df


def checkrate_single(db, name=None):
    """
    number of checkdates to days/calendarweeks since creation of habit, depends on period of habit
    Parameters:
        db : name of database where checkinformation and habitinformation is
        name : name of habit
    Returns:
    print with number checks and days/weeks since adding of the habit
    """
    if not name:
        name = input("checkdata for which habit?: ")
    checks = count_checks_single(db, name)
    cur = db.cursor()
    addingdate = cur.execute("SELECT adding_date FROM habits WHERE name=?", (name,))
    addingdate = str(cur.fetchone())
    addingdate = addingdate[2:-3]
    print("Addingdate for habit ", name, " was: ",addingdate)    
    addingdate = datetime.strptime(addingdate, '%Y-%m-%d') #datetimeobject
    addingdate.replace(minute=0, hour=0, second=0, microsecond=0) #set date to begin of day to work with calendarday
    now = datetime.now()
    now.replace(minute=0, hour=0, second=0, microsecond=0) #set date to begin so calculation is correct with calendarday
    print("Today is: ", now.date())
    period = cur.execute("""SELECT DISTINCT period FROM habits WHERE name=?""", (name,))
    period = str(cur.fetchone())
    period = period[2:-3] #remove unnecessary strings from export
    
    if period == "daily":
        difference_check = now - addingdate
        print("You have accomplished at habit ",checks.to_string(), " checks in the last ",difference_check.days, " days.") #alternative way to convert to string in print
        print("---------------------------")
        
    elif period == "weekly":
        difference_check = now.isocalendar().week - addingdate.isocalendar().week #datetime objects with calendarweek
        print("You have accomplished at habit ",checks.to_string(), " checks in the last ",difference_check, " weeks.")
        print("---------------------------")
        
    else:
        print("Please check period. Invalid value!") #if period is neither daily or weekly

    
def checkrate_period(db, period=None):
    """
    number of checkdates to days/calendarweeks since creation of all habits of given period
    Parameters:
        db : name of database where checkinformation and habitinformation is
        period : period of habits
    Returns:
    print with number checks and days/weeks since adding of habits of given period
    """
    if not period:
        period = input("checkdata for which period?:")
    
    if period == "daily":
        data = overview_daily_habits(db)
        for i in data: #run function for every item of return
            checkrate_single(db, i)
    elif period == "weekly":
        data = overview_weekly_habits(db)
        for i in data:
            checkrate_single(db, i)
    else:
        print("Please check period. Invalid value!")
        

def get_all_checkdata_single(db, name=None):
    """
    get all entries from table checks with selected habitname
    if no habitname is given user can choose which he wants to see
    Parameter:
        db - database where table "checks" is
        name - name of habit
    Returns:
        all check entries from the selected habit name
    """
    cur = db.cursor()
    if not name:
        name = input("checkdata for which habit?: ")
    cur.execute("SELECT * FROM checks WHERE habit=?", (name,))
    print("CheckID, habit, period, checkdate")    
    for row in cur:
        print(row) #print export row by row
    print("------------------------------------------")
    return cur 


def get_all_checkdata_period(db, period=None):
    """
    get all checkdata for all habits with selected period "daily" or "weekly"
    Parameter:
        db - database where table "checks" is
        period - "daily" or "weekly"
    Returns:
        all checkentries for habits of selected period row by row
    """
    if not period:
        period = input("checkdata for which period? daily or weekly?: ")
    cur = db.cursor()
    cur.execute("SELECT habit, period, checkdate FROM checks WHERE period=?", (period,))
    print("habit -- period -- checkdate")    
    for row in cur:
        print(row)        


def get_longest_streak_habit(db, name=None):
    """
    get longest streakvalue from db for chosen habit, if no habitname given than user can entry
    Parameters
        db - database where table "checks" is
        name : name of habit
    Returns
    print with name and longest streak value
    longest_streak: value for further functions
    """
    if not name:
        name = input("For which habit you want to see the longest streak?: ")
        
    try:
        cur = db.cursor()
        longest_streak = cur.execute("SELECT habit, streak FROM checks WHERE habit=? ORDER BY streak DESC LIMIT 1", (name,))
        longest_streak = cur.fetchone()
        print("Longest streak from habit " + name + " is: ", longest_streak)
        return longest_streak
    
    except Exception as e:
        print("Something went wrong with checkdata from: " + name, e)


def get_longest_streak_period(db, period=None):
    """
    get longest streakvalue from db for chosen period, if no periodname given than user can entry
    Parameters
        db - database where table "checks" is
        period : period of habits
    Returns
    print with name and longest streak value for given period
    longest_streak: value for further functions
    """
    if not period:
        period = input("For which period you want to see the longest streaks?: ")
        
    try:
        cur = db.cursor()
        longest_streak = cur.execute("SELECT habit, streak FROM checks WHERE period=? ORDER BY streak DESC LIMIT 1", (period,))
        longest_streak = cur.fetchone()
        print("Longest streak from period " +period + " is: ", longest_streak)
        return longest_streak
    
    except Exception as e:
        print("Something went wrong with checkdata from: " + period, e)


def get_longest_streak_from_all(db):
    """
    get longest streakvalue from all habits from db
    Parameters
        db - database where table "checks" is
    Returns
    print with name and longest streak value from all habits
    longest_streak: value for further functions
    """        
    try:
        cur = db.cursor()
        longest_streak = cur.execute("SELECT habit, streak FROM checks ORDER BY streak DESC LIMIT 1")
        longest_streak = cur.fetchone()
        print("Longest streak from all habits is: ", longest_streak)
        return longest_streak
    
    except Exception as e:
        print("Something went wrong with checkdata from: ", e)
