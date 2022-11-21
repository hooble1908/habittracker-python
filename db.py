#all functions related to creating, storing and reading from database

import sqlite3
from datetime import date, datetime, timedelta 
import pandas as pd

def get_db(name="main.db"):
    """
    create SQL Database for storing habit data and check data
    Parameter:
        name of database, if no name given than defaultvalue
    Returns:
        db variable
    """
    try:
        db = sqlite3.connect(name)
        print("Database " + name + " ready.")
        return db
    except:
        print("Creating Database failed!")
        close_db(db)


def close_db(db):
    db.close()


def create_tables(db):
    """
    creates two tables  - habits (contains habits, their descriptions and period of validity for streak),
                        - checks (name of habit, period and checkdates and number of current streak)
    Parameters:
        db - database in which the tables will be created
    Returns:
        no return
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
    adds new habit to table habits with description and periodicity of habit
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
        if not adding_date:
            adding_date = str(date.today())
        cur.execute("""INSERT INTO habits (name, description, period, adding_date) VALUES (?,?,?,?) """, (name, description, period, adding_date))
        add_check(db, name, period, adding_date)
        db.commit()
        print("Habit " + name + " was added to database.")
    
    except Exception as e:
        print("Something went wrong while adding a habit: ", e)
        


def add_check(db, name, period, checkdate=None, streak=1):
    if not checkdate:
        checkdate = date.today()
    cur = db.cursor()
    cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (name, period, checkdate, streak))
    db.commit()



def get_check_data(db, name=None):
    """
    get all entries from table checks with selected habitname
    Parameter:
        db - database where table "checks" is
        name - name of habit
    Returns:
        all entries from the selected habit name
    """
    cur = db.cursor()
    if not name:
        name = input("checkdata for which habit?: ")
    #overview_all_habits(db)
    cur.execute("SELECT * FROM checks WHERE habit=?", (name,))
    print("CheckID, habit, period, checkdate")    
    for row in cur:
        print(row)
    
    return cur 
        
def get_period_check_data(db, period):
    """
    get all checkdata for all habits with selected period "daily" or "weekly"
    Parameter:
        db - database where table "checks" is
        period - "daily" or "weekly"
    Returns:
        all checkentries for habits of selected period row by row
    """
    cur = db.cursor()
    cur.execute("SELECT habit, period, checkdate FROM checks WHERE period=?", (period,))
    print("habit -- period -- checkdate")    
    for row in cur:
        print(row)        

     
def get_last_checkdate(db, name):
     """
     get last checkdate from table checks for selected habit
     Parameter:
         db - database where table "checks" is
         name - name of habit
     Returns:
         last checkdate for selected habit
     """
     try:
         cur = db.cursor()
         last_checkdate = cur.execute("SELECT MAX(checkdate) FROM checks WHERE habit=?", (name,))
         print("Last checkdate for Habit " + name + " was: ")
         last_checkdate = cur.fetchone()
         return last_checkdate
     
     except Exception as e:
         print("Something went wrong with checkdata from: " + name, e)


def get_last_streak(db, name):
    """
    get last streak from table checks for selected habit
    Parameter:
        db - database where table "checks" is
        name - name of habit
    Returns:
        last streakvalue for selected habit
    """
    try:
        cur = db.cursor()
        last_streak = cur.execute("SELECT streak FROM checks WHERE habit=? ORDER BY checkID DESC LIMIT 1", (name,))
        last_streak = cur.fetchone()
        return last_streak
    
    except Exception as e:
        print("Something went wrong with checkdata from: " + name, e)


def get_longest_streak(db, name):
    try:
        cur = db.cursor()
        longest_streak = cur.execute("SELECT streak FROM checks WHERE habit=? ORDER BY streak DESC LIMIT 1", (name,))
        longest_streak = cur.fetchone()
        print("Longest streak from habit: " + name + " is: ", longest_streak)
        return longest_streak
    
    except Exception as e:
        print("Something went wrong with checkdata from: " + name, e)


def get_last_checkdate_all(db):
     """
     get last checkdate from every habit from table , with pandas dataframe
     Parameter:
         db - database where table "checks" is
     Returns:
         pandas dataframe with habit, checkID, period and last checkdate
     """
     try:
         cur = db.cursor()
         cur.execute("SELECT DISTINCT habit, period, checkdate FROM checks")
         df = pd.DataFrame(cur.fetchall(), columns = ['habit', 'period', 'last checkdate'])
         print(df.groupby(["period", "habit"]).max())
     
     except Exception as e:
         print("Something went wrong with getting checkdata: ", e)    


def overview_all_habits(db):
    """
    select all names from table "habits" of current database.
    Parameters:
        db - database
    Returns:
        print of db-export row by row
    """
    print("Overview all Habits: ")
    cur = db.cursor()
    cur.execute("SELECT DISTINCT name, period FROM habits")
    for row in cur:
        print(row)

def overview_daily_habits(db):
    """
    select all habits from table "habits" of current database with period daily.
    Parameters:
        db - database
    Returns:
        print of db-export row by row
    """
    print("Overview all daily habits: ")
    period = "daily"
    cur = db.cursor()
    cur.execute("SELECT DISTINCT name FROM habits WHERE period=?", (period,))
    for row in cur:
        print(row)

def overview_weekly_habits(db):
    """
    select all habits from table "habits" of current database with period weekly.
    Parameters:
        db - database
    Returns:
        print of db-export
    """
    print("Overview all weekly habits: ")
    period = "weekly"
    cur = db.cursor()
    cur.execute("SELECT DISTINCT name FROM habits WHERE period=?", (period,))
    for row in cur:
        print(row)

def habits_details(db):
    """
    select habits and their details from table "habits" from current database
    Parameters:
        db - database
    Returns:
        print of db-export
    """
    print("Overview all Habits and their details. ")
    cur = db.cursor()
    cur.execute("SELECT DISTINCT * FROM habits")
    print("habit, description, period, creationdate")
    for row in cur:
        print(row)

def delete_habit_data(db, name):
    """
    deletes all entries from the selected habit from tables "habits" and "checks"
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
    
def check_habit(db, name, checkdate=None):
    """
    adds new checkentry to table checks with habitname, period, checkdate and if streak is ongoing or not
    Parameters:
        db - database where table is
        name - name of habit added
        checkdate - current day of checking
    Returns:
        print that check was added to table checks
    """
    try:
        cur = db.cursor()
        if not checkdate:
            checkdate = date.today()
        period = cur.execute("""SELECT DISTINCT period FROM habits WHERE name=?""", (name,))
        period = str(cur.fetchone())
        period = period[2:-3]
        streak = streak_ongoing(db, name, period)
        cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (name, period, checkdate, streak))
        db.commit()
        print("Habit " + name + " was checked successfully.")
    
    except Exception as e:
        print("Something went wrong while checking: " + name, e)
        #close_db(db)


def streak_ongoing(db, name, period):
    """
    Parameters:
        db - name database checkinformation is stored
        name - name of habit that is checked if streak is still actice
    Returns
    if the difference of last checkdate and todays check is within period than value "True" is added to checkentry, if not "False"
    value used to calculate length of streak
    """
    try:
        try:
            last_checkdate = str(get_last_checkdate(db, name))
            last_checkdate = last_checkdate[2:-3]
            print(last_checkdate)
            last_checkdate = datetime.strptime(last_checkdate, '%Y-%m-%d')
            now = datetime.now()
            now.replace(minute=0, hour=0, second=0, microsecond=0)
            print("Today is: ")
            print(now.date())
            difference_check = now - last_checkdate
            last_streak = get_last_streak(db, name)
            last_streak = str(last_streak)
            last_streak = last_streak[1:-2]
            streak = int(last_streak)
            print("Last Streak: ", streak)
       
            if period == "daily":
                print(period + " difference is: " + str(difference_check.days))
                
                if difference_check <= timedelta(days=1):                    
                    print("already checked in current period")
                    print("Actual Streak is now: ", streak)
                    print("Streak for " + name + " continues.")
                
                elif difference_check <= timedelta(days=2):
                    streak += 1
                    print("Actual Streak is now: ", streak)
                    print("Streak for " + name + " continues.")
                
                else:
                    streak = 1
                    print("Actual Streak is now: ", streak)
                    print("New streak for " + name + " starts today. Keep going!")
                
            elif period == "weekly":
                
                difference_weekly = now.isocalendar().week - last_checkdate.isocalendar().week
                print(period + " difference is: " + str(difference_weekly) + " calendarweeks.")

                if difference_weekly == 1:
                    streak += 1
                    print("Actual Streak is: ", streak)
                    print("Streak for " + name + " continues.")
                
                elif difference_weekly == 0:
                    print("Actual Streak is: ", streak)
                    print("Streak for " + name + " continues.")
                
                else:
                    streak = 1
                    print("Actual Streak is: ", streak)
                    print("New streak for " + name + " starts today. Keep going!")
            else:
                streak = 1
                print("There is a problem with streakdata. Please check entry in db.")
        
            return streak
        
        except Exception as e:
            print("Something went wrong while checking streakdata: ",e)
            streak = 1
            
    except Exception as e:
        streak = 1
        print("Streakvalue 1 by default. Please check data in db." + e)
    
    finally:
        return streak


def streak_actual(db, name=None):
    """
    Parameters:
        db - database where table checks is
        name - optional, if not given user can choose which habit he wants to see streakinformation
    Returns:
        pandas dataframe with actual streak number and longest streak for chosen habit
    """
    cur = db.cursor()
    if not name:
        name = input("checkdata for which habit?: ")
    cur.execute("SELECT * FROM checks WHERE habit=?", (name,))
    df = pd.DataFrame(cur.fetchall(), columns = ["checkID", "habit", "period", "last checkdate", "streak"])
    df = df.drop_duplicates("last checkdate")
    print(df)



def count_checks_total(db):
    """
    Parameters:
        db - database where table checks is 
    Returns:
        pandas dataframe with total number of checks per habit without duplicates
    """
    cur = db.cursor()
    cur.execute("SELECT habit, period, checkdate, streak FROM checks")
    df = pd.DataFrame(cur.fetchall(), columns = ["habit", "period", "last checkdate", "streak"])
    df = df.drop_duplicates()
    df = df["habit"].value_counts()
    print("Total checks per habit: ")
    print(df)

def fuelle_test_db():    
    db = get_db("test.db")
    create_tables(db)
    #add_habit(db, "jogging", "1x a week", "weekly", "2022-11-02")
    #add_habit(db, "swimming", "1x a week", "weekly", "2022-10-30")
    add_habit(db, "stairs", "no elevator at work", "daily", "2022-10-30")
    #add_habit(db, "cigarettes", "not even drunk", "daily", "2022-10-30")
    #add_habit(db, "vitamins", "drink or tablette", "daily", "2022-11-14")
    #add_habit(db, "no fastfood", "not at all", "weekly", "2022-10-30")
    #check_habit(db, "jogging")
    #check_habit(db, "jogging", "2022-11-02")
    #check_habit(db, "jogging", "2022-11-05")
    #check_habit(db, "jogging", "2022-11-13")
    #check_habit(db, "jogging", "2022-11-15")
    #check_habit(db, "swimming", "2022-11-03")
    #check_habit(db, "swimming", "2022-11-13")
    #check_habit(db, "stairs", "2022-11-13")
    #check_habit(db, "stairs", "2022-11-14")
    #check_habit(db, "cigarettes", "2022-11-01")
    #check_habit(db, "cigarettes", "2022-11-02")
    #check_habit(db, "cigarettes", "2022-11-04")
    #check_habit(db, "vitamins")
    #check_habit(db, "vitamins", "2022-11-12")
    #check_habit(db, "vitamins", "2022-11-15")
    #check_habit(db, "no fastfood", "2022-11-01")
    #check_habit(db, "no fastfood", "2022-11-15")
    #add_check(db, "swimming", "weekly", "2022-11-04", 2)
    #add_check(db, "swimming", "weekly", "2022-11-09", 3)
    add_check(db, "stairs", "daily", "2022-11-04", 1)
    add_check(db, "stairs", "daily", "2022-11-08", 1)
    add_check(db, "stairs", "daily", "2022-11-09", 2)
    add_check(db, "stairs", "daily", "2022-11-19", 1)
    #db.commit()


db = get_db("test.db")
#create_tables(db)
fuelle_test_db()
#overview_all_habits(db)
#add_habit(db, "swimming", "1x a week", "weekly", "2022-10-11")
#add_check(db, "swimming", "weekly", "2022-11-17", "True")
#add_check(db, "stairs", "daily", "2022-11-14", "True")
#check_habit(db, "swimming")
#db.commit()
#get_check_data(db, "stairs")
#get_period_check_data(db, "weekly")
#get_last_checkdate_all(db)
#streak_actual(db)
#get_last_streak(db, "swimming")
streak_ongoing(db, "stairs", "daily")