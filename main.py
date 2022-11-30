from db import get_db, create_tables, overview_all_habits, habits_details, check_habit
from habits import Habit, create_habit, modify_habit, delete_habit

def main_cli():
    """
    main program of the habittracker application.
    exposes all the options and functions of the application to the user
    via an CLI with questionary package
    """
    db = get_db("test.db")
    create_tables(db)
        
    stop = False
    
    while not stop:
        
        choice = input("What do you want to do? \n Overview (1) \n Check Habit (2) \n Create Habit (3) \n" \
                       " Modify Habit (4) \n Delete Habit (5) \n Analysemodul (6) \n Exit (e): ")
        
        if choice == "1":
            stop_sub = False          
            while not stop_sub:
                proceed = input("Proceed with Overview? Exit type (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    habits_details(db)
                    stop_sub = True
                   
        elif choice == "2":            
            stop_sub = False
            while not stop_sub:
                proceed = input("Proceed with checking a habit? Exit type (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    overview_all_habits(db)
                    name = input("Which habit do you want to check?: ")
                    check_habit(db, name)
                
        elif choice == "3":
            stop_sub = False
            while not stop_sub:
                proceed = input("Proceed with creating a habit? Exit type (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    create_habit(db)
    
        elif choice == "4":
            stop_sub = False
            while not stop_sub:
                proceed = input("Proceed with modifying a habit? Exit type (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    modify_habit(db)
        
        elif choice == "5":
            stop_sub = False
            while not stop_sub:
                proceed = input("Proceed with deleting a habit? Exit type (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    delete_habit(db)
            
        elif choice == "6":
            stop_sub = False
            while not stop_sub:
                proceed = input("Proceed to analyze habits? Exit type (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    pass #erstellen
            
        elif choice == "e":
            proceed = input("Exit program via (e): ")
                
            if proceed == "e":
                print("Bye")
                stop = True

if __name__ == "main_cli":
    main_cli()

main_cli()
