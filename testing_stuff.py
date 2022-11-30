# -*- coding: utf-8 -*-
"""
Created on Mon Oct 17 10:56:58 2022

@author: hooble
"""

from db import get_db, add_habit, check_habit, delete_habit_data, create_tables, overview_all_habits
from db import habits_details, overview_daily_habits, overview_weekly_habits, get_last_checkdate
from datetime import date, datetime, timedelta
from habits import Habit
import time

def test_add_habit():
    """FUNKTIONIERT!!!"""
    #db = get_db("test.db")
    name = input("Name of new habit:")
    description = input("Description:")
    period = input(("Periodicity:"))
    def add_habit_inner(db, name, description, period, adding_date=None):
        try:
            cur = db.cursor()
            if not adding_date:
                adding_date = str(date.today())
            cur.execute("""INSERT INTO habits (name, description, period, adding_date) VALUES (?,?,?,?) """, (name, description, period, adding_date))
            db.commit()
            print("Habit " + name + " was added to database.")
        
        except Exception as e:
            print("Something went wrong while adding a habit: ", e)
            db.close()
            
    add_habit_inner(db, name, description, period)

def test_modify_habit(db):
    """FUNKTIONIERT"""
    name = input("Which habit do you want do change?: ")
    choice = input("What do you want to change from " + name + "? name (n), description (d) or periodicity (p)?")
        
    
    if choice == "n":
        try:
            new_name = input("Change " + name + " to: ")
            cur = db.cursor()
            cur.execute("""UPDATE habits SET name = ? WHERE name = ?""", [new_name, name])
            db.commit()
            print("Habit " + name + " was changed to "+ new_name + ".")
        
        except Exception as e:
            print("Something went wrong while changing the name of: " + name, e)
            db.close()
    
    elif choice == "d":
        try:
            new_description = input("Change description to: ")
            cur = db.cursor()
            cur.execute("""UPDATE habits SET description = ? WHERE name = ?""", [new_description, name])
            db.commit()
            print("Description of Habit " + name + " was changed to "+ new_description + ".")
        
        except Exception as e:
            print("Something went wrong while changing the description of: " + name, e)
            db.close()
            
    elif choice == "p":
        try:
            new_period = input("Change period to: ")
            cur = db.cursor()
            cur.execute("""UPDATE habits SET period = ? WHERE name = ?""", [new_period, name])
            db.commit()
            print("Periodicity of Habit " + name + " was changed to "+ new_period + ".")
        
        except Exception as e:
            print("Something went wrong while changing the periodicity of: " + name, e)
            db.close()
    
    else:
        print("no valid attribute entered")

def test_delete_habit():
    #enter check if habit is existing
    name = input("Which habit do you want do delete?: ")
    try:
        cur = db.cursor()
        cur.execute("""DELETE FROM habits WHERE name = ?""", [name])
        db.commit()
        print("Habit " + name + " was deleted from active habits.")
        
        also_checks = input("Do you also want to delete checks from deleted habit? If YES enter (y): ")
        if also_checks == "y":
           cur = db.cursor()
           cur.execute("""DELETE FROM checks WHERE habit = ?""", [name])
           print("Checks from habit " + name + "were deleted from database.")
           db.commit()
            
    except Exception as e:
        print("Something went wrong while deleting: " + name, e)
        db.close()

def create_habit(db):
    """
    creates new habit via user input and add to defined table for habits.
    Parameters:
        db where new habit is stored
        name, description and period of new habit via user input
    """
    try:
        name = input("Name of habit: ")
        description= input("Description: ")
        period = input("Periodicity: ")
        habit = Habit(name, description, period)
        habit.add_habit(db)
        choice = input("Do you also want to add a check for " + name + "? (y) or (any) ")
        if choice == "y":
            habit.add_check(db)
        
    except Exception as e:
        print("Something went wrong while testing: " + e)

def mainmenu():

    stop = False
    while not stop:
        print("Main Menu")
        choice = input("What do you want to do? \n Overview (1) \n Check Habit (2) \n Create Habit (3) \n" \
                   " Modify Habit (4) \n Delete Habit (5) \n Analysemodul (6) \n Exit (e): ")
        if choice == "1":
            print("continue sub")
        
        elif choice == "2":
            stop_sub = False
            while not stop_sub:
                print("SUB Menu")
                choice = input("What do you want to do? \n Overview (1) \n Check Habit (2) \n Create Habit (3) \n" \
                           " Modify Habit (4) \n Delete Habit (5) \n Analysemodul (6) \n Exit (e): ")
                if choice == "1":
                    print("continue sub")
                
                elif choice == "2":
                    print("continue sub") 
                
                elif choice == "3":
                    print("continue sub")
                    
                elif choice == "4":
                    print("continue sub")
                    
                elif choice == "5":
                    print("continue sub")
                    
                elif choice == "6":
                    print("continue sub")
                    
                elif choice == "e":
                    print("back to main")
                    stop_sub = True
 
        
        elif choice == "3":
            print("continue sub")
            
        elif choice == "4":
            print("continue sub")
            
        elif choice == "5":
            print("continue sub")
            
        elif choice == "6":
            print("continue sub")
            
        elif choice == "e":
            print("exit bye")
            stop = True



"""def fuelle_test_db():    
    db = get_db("test.db")
    create_tables(db)
    add_habit(db, "jogging", "2x a week", "weekly")
    add_habit(db, "swimming", "1h", "weekly")
    add_habit(db, "stairs", "no elevator at work", "daily")
    add_habit(db, "cigarettes", "not even drunk", "daily")
    add_habit(db, "vitamins", "drink or tablette", "daily")
    add_habit(db, "no fastfood", "not at all", "weekly")
    check_habit(db, "jogging", "weekly", "2022-11-01")
    check_habit(db, "jogging", "weekly", "2022-11-02")
    check_habit(db, "jogging", "weekly", "2022-11-05")
    check_habit(db, "jogging", "weekly", "2022-11-13")
    check_habit(db, "jogging", "weekly", "2022-11-15")
    check_habit(db, "swimming", "weekly", "2022-11-03")
    check_habit(db, "swimming", "weekly", "2022-11-13")
    check_habit(db, "stairs", "daily", "2022-11-13")
    check_habit(db, "stairs", "daily", "2022-11-14")
    check_habit(db, "cigarettes", "daily", "2022-11-01")
    check_habit(db, "cigarettes", "daily", "2022-11-02")
    check_habit(db, "cigarettes", "daily", "2022-11-04")
    check_habit(db, "vitamins", "daily", "2022-11-11")
    check_habit(db, "vitamins", "daily", "2022-11-12")
    check_habit(db, "vitamins", "daily", "2022-11-15")
    check_habit(db, "no fastfood", "weekly", "2022-11-01")
    check_habit(db, "no fastfood", "weekly", "2022-11-15")
    db.commit()
"""

#fuelle_test_db()
db = get_db("test.db")
"""
#overview_weekly_habits(db)
#habits_details(db)
#get_check_data(db)
last_checkdate = str(get_last_checkdate(db))
last_checkdate = last_checkdate[2:-3]
last_checkdate = datetime.strptime(last_checkdate, '%Y-%m-%d')
#last_date = time.strptime(last_checkdate, "%d/%m/%Y")
today = datetime.today()
#today_formatted = time.strptime(today, "%d/%m/%Y")
print(last_checkdate.date())
print(today.date())
Differenz = today - last_checkdate
#if Differenz <="1":
    #print("Streak +1")
#else:
    #print("Streak starts at 1")

print(Differenz.days)
Differenz_int = int(Differenz.days)
print(Differenz_int)
if Differenz_int <=30:
    print("YEP")
else:
    print("Depp")
"""

#testgit123