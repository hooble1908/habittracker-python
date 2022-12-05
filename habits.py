from db import add_habit, overview_all_habits, streak_ongoing, habit_details_single
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
        checkdate = date.today() #checkdate for adding check is alwys current day, so there is no cheating :)
        streak = "1" #streak starts always at 1 for first entry
        cur = db.cursor()
        cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (self.name, self.period, checkdate, streak))
        db.commit()
        
        
    def add_habit(self, db):
        add_habit(db, self.name, self.description, self.period)
        #call function with properties of current habitobject
    
def choose_period():       
    """
    gives user opportunity to choose period, can only choose between two options to make shure value for period is correct for further use
    Paramters:
        name of habit, if no extra date is selected then date is current day
    Returns:
        no return
    """
    stop = False  
    choice = input("Periodicity: (d) for daily or (w) for weekly: ")     
    
    while not stop: #to make shure userentry is one of two correct values
    
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
        
        else: #quasi exception that userentry is invalid value
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
        while name in habitlist: #catch exception that habitname is already taken
            name = input("habitname already in list. Please enter other habitname: ")
        description= input("enter description: ")
        period = choose_period() #call function that user can only enter correct period-values
        habit = Habit(name, description, period)
        habit.add_habit(db) 
        habit.add_check(db)
        
    except Exception as e:
        print("Something went wrong while creating the habit: " + e) #show message and exception to user

def modify_habit(db): 
    """
    show user details of all habits and let him choose which details from whoch habit he wants to edit
    Parameters:
        db where habits and details are stored
        name - name of habit 
        description - description of habit
        period - period of habit
    Return:
        print of status at end
    """
    
    print("Lets modify an existing habit: ")
    data = overview_all_habits(db)
    name = input("Which habit do you want do change?: ")
    while name not in data: #to catch exception that user enters a NON-existing habit
        name = input("habitname NOT in list. Please enter correct habitname: ")
    habit_details_single(db, name)
    choice = input("What do you want to change from habit " + name + "? name (n), description (d) or periodicity (p)?")
        
    
    if choice == "n":
        try:
            new_name = input("Change name of habit " + name + " to: ")
            while new_name in data: #catch exception that new name is not already an existing habit
                new_name = input("habitname already in list. Please enter other habitname: ")
            cur = db.cursor()
            cur.execute("""UPDATE habits SET name = ? WHERE name = ?""", [new_name, name]) #updates existing values in database with new values from userinput
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
            new_period = choose_period() #call function to make shure user can only change period to correct values
            cur = db.cursor()
            cur.execute("""UPDATE habits SET period = ? WHERE name = ?""", [new_period, name])
            db.commit()
            print("Periodicity of Habit " + name + " was changed to "+ new_period + ".")
        
        except Exception as e:
            print("Something went wrong while changing the periodicity of: " + name, e)
            db.close()
    
    else: #catch invalid userinput
        print("no valid attribute entered")

def delete_habit(db): 
    """
    delete habit, and if user wants to also checkdata from habit, from database
    Parameters:
        db where habit and  checks are stored
        name - name of habit 
    Return:
        
    """
    overview_all_habits(db)
    name = input("Which habit do you want do delete?: ")
    try:
        cur = db.cursor()
        cur.execute("""DELETE FROM habits WHERE name = ?""", [name])
        db.commit()
        print("Habit " + name + " was deleted from active habits.")
        
        also_checks = input("Do you also want to delete checks from deleted habit? If YES enter (y): ")#option to keep checks
        if also_checks == "y": #to only accept correct user input
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
        checkdate - default current day of checking
    Returns:
        print that check was added to table checks
    """
    try:
        cur = db.cursor()
        if not checkdate: #quasi default TODAY
            checkdate = date.today()
        period = cur.execute("""SELECT DISTINCT period FROM habits WHERE name=?""", (name,))
        period = str(cur.fetchone())
        period = period[2:-3]    #to remove parts of string at beginning and end of value so input is correct for function
        streak = streak_ongoing(db, name, period) #check if streak continues or new streak begins
        cur.execute("""INSERT INTO checks (habit, period, checkdate, streak) VALUES (?,?,?, ?) """, (name, period, checkdate, streak))
        db.commit()
        print("Habit " + name + " was checked successfully.")
    
    except Exception as e:
        print("Something went wrong while checking: " + name, e)

