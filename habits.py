from db import add_habit, habits_details, overview_all_habits, streak_ongoing, habit_details_single
from datetime import date


class Habit:
    
    def __init__(self, name:str, description: str, period: str, creation_date = str):
        self.name = name
        self.description = description
        self.period = period
        self.creation_date = str(date.today())
        
    
    def show(self):
        print({self.name}, {self.description}, {self.period})
    
        
    def __str__(self):
        return "Habit {0}, Description {1}, Period {2}.".format(self.name, self.description, self.period)
    
    
    def store(self, db):
        """
        store object in DB
        Parameters:
            db : initialized sqlite3 database from db.py
        Returns:
            no return
        """
        add_habit(db, self.name, self.description, self.period)
        
    def add_check(self, db, checkdate: str = None):
        """
        add entry to check table with habit name and current date
        Paramters:
            name of habit, if no extra date is selected then date is current day
        Returns:
            no return
        """
        checkdate = date.today()
        streak = "1"
        cur = db.cursor()
        cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (self.name, self.period, checkdate, streak))
        db.commit()
        
        
    def add_habit(self, db):
        add_habit(db, self.name, self.description, self.period)
        
    
def choose_period():       
    stop = False  
    choice = input("Periodicity: (d) for daily or (w) for weekly: ")     
    
    while not stop:
    
        if choice == "w":            
            period = "weekly"
            print(period)
            stop = True
            return period
            
        
        elif choice == "d":            
            period = "daily"
            print(period)
            stop = True
            return period
        
        else:
            print("Invalid entry, please try again: ")
            choice = input("Periodicity: (d) for daily or (w) for weekly: ") 
    
def create_habit(db):
    """
    creates new habit via user input and add to defined table for habits.
    Parameters:
        db where new habit is stored
        name, description and period of new habit via user input
    """
    try:
        print("Creating a new habit: ")
        habitlist = overview_all_habits(db)
        name = input("Name of habit: ")
        while name in habitlist:
            name = input("habitname already in list. Please enter other habitname: ")
        description= input("Description: ")
        period = choose_period()
        habit = Habit(name, description, period)
        habit.add_habit(db)
        habit.add_check(db)
        
    except Exception as e:
        print("Something went wrong while testing: " + e)

def modify_habit(db): #enter check if name is existing habit
    print("Lets modify an existing habit: ")
    data = overview_all_habits(db)
    name = input("Which habit do you want do change?: ")
    while name not in data:
        name = input("habitname NOT in list. Please enter correct habitname: ")
    habit_details_single(db, name)
    choice = input("What do you want to change from " + name + "? name (n), description (d) or periodicity (p)?")
        
    
    if choice == "n":
        try:
            new_name = input("Change " + name + " to: ")
            while new_name in data:
                new_name = input("habitname already in list. Please enter other habitname: ")
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
            new_period = choose_period()
            cur = db.cursor()
            cur.execute("""UPDATE habits SET period = ? WHERE name = ?""", [new_period, name])
            db.commit()
            print("Periodicity of Habit " + name + " was changed to "+ new_period + ".")
        
        except Exception as e:
            print("Something went wrong while changing the periodicity of: " + name, e)
            db.close()
    
    else:
        print("no valid attribute entered")

def delete_habit(db): 
    overview_all_habits(db)
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
           print("Checks from habit " + name + " were deleted from database.")
           db.commit()
            
    except Exception as e:
        print("Something went wrong while deleting: " + name, e)
        db.close()



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

