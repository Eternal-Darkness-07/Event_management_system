from pywebio.input import *
from pywebio.output import *
import os
import csv
import pandas as pd
import pyautogui


def see_booking():
    info = input_group("Enter blow information:",inputs=[
        input("Event name", name="Event_name", type=TEXT, required= True, placeholder="Enter event name"),
        input("starting date", name="start", type=DATE, required=True, placeholder="Enter the date"),
    ])
    
    time = str(info['start'])
    name = str(info["Event_name"]).strip().replace(" ","_")
    file_path = os.path.join("csv_files", name + time + "_booking.csv")
    
    df = pd.read_csv(file_path)
    put_scrollable(put_table(df.to_dict(orient='records')), height=400)
    go_to_login = actions("Do you want to login again?", ['Yes'])
    
    if go_to_login == 'Yes':
        pyautogui.hotkey('f5')
    


def create():
    info = input_group("Enter blow information:",inputs=[
        input("Event name", name="Event_name", type=TEXT, required= True, placeholder="Enter event name"),
        input("Event place", name="Event_place", type=TEXT, required=True, placeholder="Enter place name"),
        input("Space available", name="people", type=NUMBER, required=True, placeholder="Enter the number of people can attend the event"),
        input("starting date & time", name="start", type=DATETIME, required=True, placeholder="Enter the date and time"),
        input("Ending date & time", name="end", type=DATETIME, required=True, placeholder="Enter the date and time"),
        input("Price of a ticket", name="price", type=NUMBER, required=True, placeholder="Enter the price of ticket")
    ])
    file_path = os.path.join("csv_files","event_data.csv")
    with open(file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "0",
            info['Event_name'],
            info['Event_place'],
            str(info['people']),
            "0",
            str(info['start']).replace('T',' Time:- '),
            str(info['end']).replace('T', ' Time:- '),
            info['price']
        ])
    file.close()
    
    df = pd.read_csv(file_path)
    df.loc[df.index[-1], 'ID'] = str(len(df))
    df.to_csv(file_path, index=False)
    
    time = str(info['start']).replace(' Time:- ', 'T').split("T")[0]
    name = str(info["Event_name"]).strip().replace(" ","_")
    file_path = os.path.join("csv_files", name + time + "_booking.csv")
    
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([
            "ID",
            "Name",
            "email",
            "Number-of-tickets",
        ])
    file.close()
    
    put_markdown('<span style="color: green;"> Event: ' + info["Event_name"] + ' has been added</span>')
    go_to_login = actions("Do you want to login again?", ['Yes'])
    
    if go_to_login == 'Yes':
        pyautogui.hotkey('f5')
        
    