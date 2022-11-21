#all functions regarding the analysepart of habits
from db import get_last_checkdate, get_db, overview_all_habits, create_tables, add_habit, check_habit, delete_habit_data
from datetime import datetime, timedelta, date
from testing_stuff import fuelle_test
from habits import Habit
import time

"""def streak_ongoing(db, name, period):
    
    Parameters:
        db - name database checkinformation is stored
        name - name of habit that is checked if streak is still actice
    Returns
    if the difference of last checkdate and todays check is within period than value "True" is added to checkentry, if not "False"
    value used to calculate length of streak
    
    try:
        last_checkdate = str(get_last_checkdate(db, name))
        last_checkdate = last_checkdate[2:-3]
        print(last_checkdate)
        last_checkdate = datetime.strptime(last_checkdate, '%Y-%m-%d')
        today = datetime.today()    
        print("Today is: ")
        print(today.date())
        #print(today.isocalendar())
        difference_check = today - last_checkdate
        print(period + " difference is: " + str(difference_check.days))
   
        if period == "daily":
            if difference_check <= timedelta(days=1):
                streak = "True"
            else:
                streak = "False"
            
        elif period == "weekly":
            if difference_check <= timedelta(weeks=1):
                streak = "True"
            else:
                streak = "False"
        else:
            streak = "Invalid data"
    
        print(streak)
        return streak
    
    except Exception as e:
        print("Something went wrong while checking streakdata: ",e)
        streak = "Invalid data"
        """
    
def fuelle_test_db():    
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

db = get_db("test.db")
fuelle_test(db)
overview_all_habits(db)
#streak_ongoing(db, "Singing", "weekly")