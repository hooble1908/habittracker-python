from db import get_db, create_tables, overview_all_habits, habits_details, check_habit, habit_details_single, \
actual_streak_today_single, actual_streak_today_period, habit_details_period, get_last_checkdate_all, defaultdata_db
from habits import create_habit, modify_habit, delete_habit
from analyse import checkrate_single, checkrate_period, get_all_checkdata_single, \
get_longest_streak_habit, get_longest_streak_period, get_longest_streak_from_all

def main_cli():
    """
    main program of habittracker application.
    exposes all the options and functions of the application to the user
    via an CLI with input-function
    """
    db = get_db() #"main.db" by default, can give other name for testpurposes
    create_tables(db)
    testdata = input("Want to create testdata in database? (y) for YES, (any key) for NO: ") 
    if testdata == "y": #of no measn user wants to start fresh or already data from last usage in db
       defaultdata_db(db) 
    
    stop = False
    
    while not stop:
    #main menu is while-loop aslong as variable "stop" is not TRUE, same for branch-menu-points    
        print("--------------------------------------------------------------------")
        choice = input("What do you want to do? \n Overview (1) \n Check Habit (2) \n Create Habit (3) \n" \
                       " Modify Habit (4) \n Delete Habit (5) \n Analysemodul (6) \n Exit (e): ")
        
        if choice == "1":
            stop_sub = False          
            
            while not stop_sub:
                proceed = input("Proceed with Overview with (any key) -- Exit to main with (e): ")
                print("XXXXXXXXXXXXXXXXXXXX   OVERVIEW   XXXXXXXXXXXXXXX")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    habits_details(db)
                    print("XXXXXXXXXXXXXXXXXX   END OVERVIEW   XXXXXXXXXXXXXXXXXX")
                    stop_sub = True
                   
        elif choice == "2":            
            stop_sub = False
            
            while not stop_sub:
                proceed = input("Proceed with checking a habit with (any key) -- Exit to main with (e): ")
                print("XXXXXXXXXXXXXXX   CHECKING HABIT   XXXXXXXXXXXXXXXXXXXXXXXX")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    overview_all_habits(db)
                    name = input("Which habit do you want to check?: ")
                    check_habit(db, name)
                    print("XXXXXXXXXXXXXXXXX   END CHECKING HABIT   XXXXXXXXXXXXXXXXXXXX")
                
        elif choice == "3":
            stop_sub = False
            
            while not stop_sub:
                proceed = input("Proceed with creating a habit with (any key) -- Exit to main with (e): ")
                print("XXXXXXXXXXXXXXXXXXXX   CREATING HABIT   XXXXXXXXXXXXXXXXXXXXXXXX")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    create_habit(db)
                    print("XXXXXXXXXXXXXXXXX   END OF CREATING HABIT   XXXXXXXXXXXXXXXXXXXX")
    
        elif choice == "4":
            stop_sub = False
            
            while not stop_sub:
                proceed = input("Proceed with modifying a habit with (any key) -- Exit to main with (e): ")
                print("XXXXXXXXXXXXXXXXXXXXXX   MODIFYING HABIT   XXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    modify_habit(db)
                    print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXX   END MODIFYING HABIT   XXXXXXXXXXXXXXXXXXXX")
        
        elif choice == "5":
            stop_sub = False
            
            while not stop_sub:
                proceed = input("Proceed with deleting a habit with (any key) -- Exit to main with (e): ")
                print("XXXXXXXXXXXXXXXXXXX   DELETING HABIT   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    delete_habit(db)
                    print("XXXXXXXXXXXXXXXXXXXX   END DELETING HABIT   XXXXXXXXXXXXXXXXXXXXXX")
            
        elif choice == "6":
            stop_sub = False
            
            while not stop_sub:
                proceed = input("Proceed to analyze habits with (any key) -- Exit to main with (e): ")
                
                if proceed == "e":
                    stop_sub = True
                                    
                else:
                    proceed = input("What do you want to analyze?: \n Specific Habit (1) \n Specific Period (2) \n All Habits (3) \n" \
                          " Exit to last menu with (any left key) ")
                    
                    if proceed == "1":
                        print("XXXXXXXXXXXXXXXXXXXX   ANALYSE ONE HABIT   XXXXXXXXXXXXXXXXXXX")
                        overview_all_habits(db)
                        name = input("Which habit do you want to analyze?: ")
                        habit_details_single(db, name)
                        checkrate_single(db, name)
                        get_all_checkdata_single(db, name)
                        actual_streak_today_single(db, name)
                        get_longest_streak_habit(db, name)
                        print("XXXXXXXXXXXXX   END OF ANALYSING ", name, "   XXXXXXXXXXXXXXXXXX" )
                        
                    
                    elif proceed == "2":
                        print("XXXXXXXXXXXXXXXXX ANALYSE PERIOD   XXXXXXXXXXXXXXXXXXXXX")
                        period = input("Habits of which PERIOD do you want to analyze? (daily) or (weekly): ")
                        habit_details_period(db, period)
                        checkrate_period(db, period)
                        actual_streak_today_period(db, period)
                        get_longest_streak_period(db, period)
                        print("XXXXXXXXXXXXXXXXXXX   END OF ANALYSING ", period, "   XXXXXXXXXXXXXXXXXXXXXXXXXX" )

                    
                    
                    elif proceed == "3":
                        print("XXXXXXXXXXXXXXXXXX   ANALYSING ALL HABITS   XXXXXXXXXXXXXXXXXXXX")
                        habits_details(db)
                        get_last_checkdate_all(db)
                        data = overview_all_habits(db)
                        for i in data:
                            actual_streak_today_single(db, i)
                            get_longest_streak_habit(db, i)
                        get_longest_streak_from_all(db)
                        print("For more details please try specific or period analysis.")
                        print("XXXXXXXXXXXXXXXXXXXXXXXXX   END OF ANALYSING ALL HABITS   XXXXXXXXXXXXXXXXXXXXXXXX")
                    
                    else:
                        stop_sub = True
            
        elif choice == "e":
            proceed = input("Exit program via (e): ")
                
            if proceed == "e":
                print("Bye")
                print("XXXXXXXXXXXXXXX END OF APPLICATION   XXXXXXXXXXXXXXXXXXX")
                db.commit() #safe changes and close database connection at end of application
                db.close()
                stop = True
                    
if __name__ == "main_cli":
    main_cli()

main_cli()
