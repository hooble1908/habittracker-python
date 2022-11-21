# functions for testing the application

from habits import Habit
from db import get_db, add_habit, check_habit, create_tables, close_db, check_habit2
from analyse import count_checks, get_habit_data
from datetime import date

class TestHabit:
    
    def __init__(self, name:str, description: str, period: str, creation_date = str):
        self.name = name
        self.description = description
        self.period = period
        self.creation_date = str(date.today())
    
     
    def add_test_habit_manual(self, db, name, description, period):
        name = input("Enter Habitname: ")
        description = input("Enter Description: ")
        period = ("Enter Period (daily oder weekly): ")                  
        test_habit = Habit(name, description, period)
        test_habit.store(self.db)
        test_habit.add_check()
        test_habit.store()
    
  
    def test_analyse_functions(self):
        """
        Test if there are six testentries in test database as in setup_method implemented
        """
        data = get_habit_data(self.db, "test_habit")
        assert len(data) == 6
        
        count = count_checks(self.db, "test_habit")
        assert count == 6
    
    def teardown_method(self):
        """
        sequence at the end of pytest
        deletes test.db
        """
        import os
        os.remove("test.db")

def setup_method(name = "test", description = "description123", period = "Daily", creation_date = str(date.today())):
    """
    creates testdata in test.db for testing application and analysefunctions
    testdata contains some testhabits and some checkdata
    """
    test = TestHabit("test_object", "description_object1", "daily", "2021-01-01")
    add_habit(db, "test_habit1", "test_description", "daily")
    add_habit(db, "test_habit2", "test_description", "daily")
    add_habit(db, "test_habit3", "test_description", "daily")
    add_habit(db, "test_habit4", "test_description", "weekly")
    add_habit(db, "test_habit5", "test_description", "weekly")
    add_habit(db, "test_habit6", "test_description", "weekly")
    check_habit(db, "test_habit1")
    check_habit(db, "test_habit2")
    check_habit(db, "test_habit3", "2022-07-01")
    check_habit(db, "test_habit4", "2022-07-01")
    check_habit(db, "test_habit5", "2022-07-01")
    check_habit(db, "test_habit6", "2022-07-01")
    #test.add_test_habit_manual(db, name, description, period)
    print("Testdata created successfully.")

#print("Class TestHabit created successfully.")
#get_db("test.db")
db = get_db("test.db")
create_tables(db)
add_habit(db, "testhabit1", "testdescription1", "daily")
check_habit2(db, "oink1", "daily")
check_habit2(db, "oink2", "daily")
check_habit2(db, "oink3", "weekly")
#setup_method()
close_db(db)
#print("setup erfolgreich")
"""test.add_test_habit("testhabit2", "TESTdescription2", "daily")
print("add test erfolgreich")
test.test_analyse_functions()
print("analyse testen")
close_db()
test.teardown_method()
print("Test beendet")"""
