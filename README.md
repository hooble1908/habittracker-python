# My Habittracker Application by Michael Huber

Welcome to application of habittracker 1.0
This is first application ever from me in any programming language, so this was reaaaally challenging.

created with Spyder Python 3.9
database with sqlite3
menu with simple main- and subloops

## Installation

```shell
pip install -r requirements.txt
```
contains required packages
- sqlite3, datetime, pandas, numpy, pytest

## Usage

Start

```shell
python main.py
```

and follow instructions in application menu.
Control over user input via command line interface

option to create testdata in database for tests of functionality

two possible periods:
- daily: for daily tasks or goals, daily means one calendarday (not24h)
- weekly: for tasks for a whole week or once a week - calendarweek, start Monday

user can create new habits, change existing habits or delete habits with or without corresponding checkdata
and of course check habits - for current day only, not possible for past or future to ensure no cheating,
see checking your habits correctly also as a habit ;)

view of main menu:


1) Overview returns all current habits and their period

2) Check habit: user has to enter name of habit he wants to add a chekcentry. new streakvalue is calculated from last checkentry in database
    and current day and new entry in imported in database

3) Create Habit: user can entry name of habit, description and choose period. Than a new entry in list table with habits and first checkentry is created.
    check implemented if name of habit is already taken.
    
4) Modify habit: user can enter which habit and which detail (name, description, period) he wants to change. First check if chosen habit exists, 
    than check if new name is not already taken.
    
5) Delete Habit: User can delete a habit and if he likes alsl all checkdata from this habit from database.

6) Analyzemodul: User can see details from habits, checkdata and actual and longest streak of a single habit, all habits from a period or some, but
    not all details and values from all habits. 



## Tests

```shell
pytest und beschreiben wie man den Test durchführt
# open task:
- pytest
- installationguide

