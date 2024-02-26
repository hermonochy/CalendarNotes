import PySimpleGUI as sg
import calendar
import json
import ephem
import os
import pygame
from datetime import date, timedelta

DEFAULT_MESSAGES = {
    "christmas": "Merry Christmas!",
    "easter": "Happy Easter!",
    "halloween": "Happy Halloween!",
    "new years day": "Happy New Year's Day!",
    "new moon": "Happy New Moon!",
    "full moon": "Happy Full Moon!"
}

def load_messages():
    try:
        with open("savedmessages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = {}
    return messages

def save_messages(messages):
    with open("savedmessages.json", "w") as file:
        json.dump(messages, file)

def calculate_event_date(event_name, year):
    if event_name == 'christmas':
        return date(year, 12, 25)
    elif event_name == 'easter':
        return calculate_easter_date(year)
    elif event_name == 'halloween':
        return date(year, 10, 31)
    elif event_name == 'new years day':
        return date(year, 1, 1)
    elif event_name == 'new moon':
        return calculate_moon_phase_date('new', year)
    elif event_name == 'full moon':
        return calculate_moon_phase_date('full', year)
    
def calculate_easter_date(year):
    easter = ephem.Easter(year)
    easter_date = ephem.localtime(easter)
    return date(easter_date.year, easter_date.month, easter_date.day)

def calculate_moon_phase_date(phase, year):
    current_date = date(year, 1, 1)
    while True:
        if ephem.next_new_moon(current_date) < ephem.next_full_moon(current_date):
            next_new_moon = ephem.localtime(ephem.next_new_moon(current_date))
            if phase == 'new':
                return date(next_new_moon.year, next_new_moon.month, next_new_moon.day)
        else:
            next_full_moon = ephem.localtime(ephem.next_full_moon(current_date))
            if phase == 'full':
                return date(next_full_moon.year, next_full_moon.month, next_full_moon.day)
        current_date += timedelta(days=1)

# Input Dialog for Year Selection
layout = [[sg.Text('Enter a year to calculate event dates:'), sg.Input(key='year_input'), sg.Button('Calculate')]]
window = sg.Window('Year Selection Dialog', layout)

event_year = None
while True:
    event_year_data = window.read()
    if event_year_data[0] == 'Calculate':
        event_year = int(event_year_data[1]['year_input'])
        break

window.close()

messages = load_messages()
for event_name in DEFAULT_MESSAGES.keys():
    event_date = calculate_event_date(event_name, event_year)
    key = f"{calendar.month_name[event_date.month].lower()} {event_date.day}"
    messages[key] = DEFAULT_MESSAGES[event_name]

save_messages(messages)

# Rest of the code remains the same
