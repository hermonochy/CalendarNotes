# Calendar Notes

This is a simple note management system built using PySimpleGUI. Users can select a date, write a message associated with that date, save the message, view messages for a specific date, and delete messages if needed.

## Features
- Users can select a date using the calendar button.
- Users can write a message in the provided text area.
- Users can save a message for a specific date.
- Users can view saved messages for a specific date.
- Users can delete messages for a specific date.

## How to Use
- Select a date using the calendar button.
- Write a message in the text area.
- Click on "Save Message" to save the message for the selected date.
- Click on "View Messages" to see saved messages for the selected date.
- In the "View Messages" window, you can select a message and click "Delete Message" to remove it.

## Files
- `savedmessages.json`: JSON file used to store the saved messages.

## Note
If you close the main window or click "Quit", the program will save the messages to `savedmessages.json` before shutting down.
It is advised to use PySimpleGUI 4.60.5 as 5.00.0 requires subscribtion

## Future Work
- More efficient system for viewing messages
- Sending messages to owners email
