import sys

def Julian_date(day, month, year):
    if month == 1:
        month = 13
        year -= 1
    elif month == 2:
        month = 14
        year -= 1
    julian = (36525*year)//100 + (306001*(month+1))//10000 + day + 1720981
    return julian

date = input('Please enter the date: ')

day, month, year = map(int, date.split())

julian = Julian_date(day, month, year)

print(f'The Julian date of {day}/{month}/{year} is: {julian}')