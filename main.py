import PySimpleGUI as sg
import calendar
import json

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

messages = load_messages()

layout = [
    [sg.CalendarButton('Choose Date', target='date', key='cal_button'), sg.InputText('', key='date', disabled=True)],
    [sg.Multiline(key='message', size=(50, 10))],
    [sg.Button('Save Message'), sg.Button('View Messages')]
]

window = sg.Window('Calendar with Messages', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        save_messages(messages)
        break

    if event == 'Save Message':
        date = values['date'].split()[0]  # Remove the time component
        message = values['message'].strip()

        if date in messages:
            messages[date].append(message)
        else:
            messages[date] = [message]

        sg.popup("Message saved successfully!")

    if event == 'View Messages':
        date = values['date'].split()[0]  # Remove the time component
        
        if date in messages:
            message_window_layout = [
                [sg.Text(f"Messages for {date}:")],
                [sg.Listbox(values=messages[date], size=(50, 10), key='message_list')],
            ]
            
            message_window = sg.Window('View Messages', message_window_layout)
            
            while True:
                event, values = message_window.read()
                
                if event == sg.WIN_CLOSED:
                    break
                
                
            message_window.close()

        else:
            sg.popup("No messages saved for this date")

save_messages(messages)
window.close()
