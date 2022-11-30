#all functions regarding the analysepart of habits
import pandas as pd
from db import get_db, overview_daily_habits, overview_weekly_habits, overview_all_habits

from datetime import datetime, timedelta, date
from numpy import array
from habits import Habit
import time

#db = get_db("test.db")

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
    print("Total checks (without duplicates): ", df)
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
    checks = int(checks)
    cur = db.cursor()
    addingdate = cur.execute("SELECT adding_date FROM habits WHERE name=?", (name,))
    addingdate = str(cur.fetchone())
    addingdate = addingdate[2:-3]
    print("Addingdate for habit ", name, " was: ",addingdate)    
    addingdate = datetime.strptime(addingdate, '%Y-%m-%d')
    addingdate.replace(minute=0, hour=0, second=0, microsecond=0)
    now = datetime.now()
    now.replace(minute=0, hour=0, second=0, microsecond=0)
    print("Today is: ", now.date())
    period = cur.execute("""SELECT DISTINCT period FROM habits WHERE name=?""", (name,))
    period = str(cur.fetchone())
    period = period[2:-3]
    
    if period == "daily":
        difference_check = now - addingdate
        print("You have accomplished ",checks, " checks in the last ",difference_check.days, " days.")
        print("---------------------------")
        
    elif period == "weekly":
        difference_check = now.isocalendar().week - addingdate.isocalendar().week
        print("You have accomplished ",checks, " checks in the last ",difference_check, " weeks.")
        print("---------------------------")
        
    else:
        print("Please check period. Invalid value!")

    
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
        for i in data:
            checkrate_single(db, i)
    elif period == "weekly":
        data = overview_weekly_habits(db)
        for i in data:
            checkrate_single(db, i)
    else:
        print("Please check period. Invalid value!")
        

