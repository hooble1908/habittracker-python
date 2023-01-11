from db import get_db, streak_ongoing

#test calculation of new streakvalues - READ INSTRUCTIONS FOR CORRECT TESTING!!!

def test_add_one_to_streak_daily(mocker):
    #to run correctly set return_value for last_checkdate to the day before you are testing this actually
    #i was not able to mock datetime.datetime.now()
    db = get_db()
    mocker.patch("db.get_last_checkdate", return_value="('2023-01-10,')")
    mocker.patch("db.get_last_streak", return_value="(2,)")
    assert  streak_ongoing(db, "cigarettes", "daily") == 3  


def test_add_one_to_streak_weekly(mocker):
    #to run correctly set return_value for last_checkdate to a day of the last calendarweek you are testing this actually
    #i was not able to mock datetime.datetime.now()
    db = get_db()
    mocker.patch("db.get_last_checkdate", return_value="('2023-01-05,')")
    mocker.patch("db.get_last_streak", return_value="(4,)")
    assert  streak_ongoing(db, "swimming", "weekly") == 5  
    
    
def test_set_streak_to_one_daily(mocker):
    db = get_db()
    mocker.patch("db.get_last_checkdate", return_value="('2023-01-07,')")
    mocker.patch("db.get_last_streak", return_value="(2,)")
    assert  streak_ongoing(db, "cigarettes", "daily") == 1
    
    
def test_set_streak_to_one_weekly(mocker):
    db = get_db()
    mocker.patch("db.get_last_checkdate", return_value="('2023-01-01,')")
    mocker.patch("db.get_last_streak", return_value="(2,)")
    assert  streak_ongoing(db, "swimming", "weekly") == 1
    
    
def test_streak_two_checks_same_day_daily(mocker):
    #to run correctly set return_value for last_checkdate to the actual day you are testing this
    #i was not able to mock datetime.datetime.now()
    db = get_db()
    mocker.patch("db.get_last_checkdate", return_value="('2023-01-11,')")
    mocker.patch("db.get_last_streak", return_value="(2,)")
    assert  streak_ongoing(db, "cigarettes", "daily") == 2
       
    
def test_streak_two_checks_same_week_weekly(mocker):
    #to run correctly set return_value for last_checkdate to any day in the actual calendarweek you are testing this
    #i was not able to mock datetime.datetime.now()   
    db = get_db()
    mocker.patch("db.get_last_checkdate", return_value="('2023-01-10,')")
    mocker.patch("db.get_last_streak", return_value="(2,)")
    assert  streak_ongoing(db, "swimming", "weekly") == 2