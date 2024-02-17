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
    [sg.Text("Write message here:")],
    [sg.Multiline(key='message', size=(50, 10))],
    [sg.Button('Save Message'), sg.Button('View Messages')],
    [sg.Button('Quit')]
]

window = sg.Window('Message', layout)

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == 'Quit':
        print("Shutting Down...")
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
                         messages[date].remove(selected_message)  # Remove the selected message from the list
                         sg.popup("Message deleted successfully!")
                         message_window['message_list'].update(values=messages[date])  # Update the listbox
                                                 
                
            message_window.close()

        else:
            sg.popup("No messages saved for this date")

save_messages(messages)
window.close()
