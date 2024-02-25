import PySimpleGUI as sg
import calendar
import json
import os
import pygame

def load_messages():
    try:
        with open("savedmessages.json", "r") as file:
            try:
                messages = json.load(file)
            except json.JSONDecodeError:
                messages = {}
    except FileNotFoundError:
        messages = {}
    return messages

def save_messages(messages):
    with open("savedmessages.json", "w") as file:
        json.dump(messages, file)

def check_unchecked_messages(messages, current_date):
    if current_date in messages:
        unchecked_messages = [msg for msg in messages[current_date] if not msg.startswith("√")]
        if unchecked_messages:
            file = "sound1.mp3"
            pygame.mixer.init()
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            sg.popup(
                f"Unchecked Messages for {current_date}:\n" + "\n".join(unchecked_messages),
                title="Unchecked Messages"
            )
            
pygame.init()

messages = load_messages()

current_date = calendar.datetime.datetime.now().strftime("%Y-%m-%d")

check_unchecked_messages(messages, current_date)

layout = [
    [sg.CalendarButton('Choose Date', target='date', key='cal_button'), sg.InputText('', key='date', disabled=True)],
    [sg.Text("Write message here:")],
    [sg.Multiline(key='message', size=(50, 10))],
    [sg.Button('Save Message'), sg.Button('View Messages')],
    [sg.Button('Quit')]
]

window = sg.Window('Calendar notes', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Quit':
        print("Shutting Down...")
        save_messages(messages)
        break

    if event == 'Save Message':
        date = values['date'].split()[0]  
        message = values['message'].strip()

        if date in messages:
            messages[date].append(message)
        else:
            messages[date] = [message]

        sg.popup("Message saved successfully!", title="Message Saved")

    if event == 'View Messages':
        date = values['date'].split()[0]  
        
        if date in messages:
            message_window_layout = [
                [sg.Text(f"Messages for {date}:")],
                [sg.Listbox(values=messages[date], size=(50, 10), key='message_list')],
                [sg.Button('Delete Message')]  
            ]
            
            message_window = sg.Window('View Messages', message_window_layout)
            
            while True:
                event, values = message_window.read()
                
                if event == sg.WIN_CLOSED:
                    break
                
                if event == 'Delete Message':
                    selected_messages = values['message_list']
                    if selected_messages:
                        selected_message = selected_messages[0]
                        messages[date].remove(selected_message)
                        sg.popup("Message deleted successfully!", title="Message Deleted")
                        message_window['message_list'].update(values=messages[date])
                                                
            message_window.close()

        else:
            sg.popup("No messages saved for this date", title="No Messages Found")

save_messages(messages)
window.close()
