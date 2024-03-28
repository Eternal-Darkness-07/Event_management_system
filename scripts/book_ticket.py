from pywebio.input import *
from pywebio.output import *
import os
import csv
import pandas as pd
import pyautogui

def final_pay(info):
    file_path = os.path.join("csv_files", "event_data.csv")
    df = pd.read_csv(file_path)
    user_info = input_group("Enter info", inputs=[
        input("Name:", type=TEXT, required=True, name="name", placeholder="Enter your name"),
        input("Email", type=TEXT, required=True, name="email", placeholder="Enter your email")
    ])

    event_id = info['ID']
    prize = int(df.loc[df.index[event_id - 1], 'Price'])
    name = str(df.loc[df.index[event_id - 1], 'Events-name'])
    booked_seats = int(df.loc[df.index[event_id - 1], 'booked-seats']) + int(info['num'])

    put_markdown('<span style="color: green"> You want to book ' + str(info['num']) + " tickets of " + name +" </span>")
    put_markdown('<span style="color: red">Total price: ' + str(info['num'] * prize) + " </span>")

    choice = actions("Choose an action", ['final', 'cancel'])

    if choice == 'final':
        put_markdown('Your tickets are booked')
        df.loc[df.index[event_id - 1], 'booked-seats'] = booked_seats
        df.to_csv(file_path, index=False)

        time = str(df.loc[df.index[event_id - 1], 'Starting-date-&-time']).replace(" Time:- ", "T").split("T")[0]
        name = str(df.loc[df.index[event_id - 1], 'Events-name']).strip().replace(" ", "_")
        file_path = os.path.join("csv_files", name + time + "_booking.csv")
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                "0",
                user_info['name'],
                user_info['email'],
                info['num'],
            ])
        df = pd.read_csv(file_path)
        df.loc[df.index[-1], 'ID'] = str(len(df))
        df.to_csv(file_path, index=False)
    else:
        clear()
        select_event()

def is_avail(info):
    file_path = os.path.join("csv_files", "event_data.csv")
    df = pd.read_csv(file_path)
    event_id = info['ID']
    num_tickets = int(info['num'])

    total_seats = int(df.loc[df.index[event_id - 1], 'Total-seats'])
    booked_seats = int(df.loc[df.index[event_id - 1], 'booked-seats'])
    if total_seats - booked_seats < num_tickets:
        return "num", "Not enough tickets available"

def select_event():
    file_path = os.path.join("csv_files", "event_data.csv")
    df = pd.read_csv(file_path)
    put_table(df.to_dict(orient='records'))
    info = input_group("Booking details:", inputs=[
        input("Event ID:", name='ID', type=NUMBER, required=True),
        input("Number of tickets", name='num', type=NUMBER, required=True)
    ], validate=is_avail)

    final_pay(info)

def book():
    select_event()
    go_to_login = actions("Do you want to login again?", ['Yes'])

    if go_to_login == 'Yes':
        pyautogui.hotkey('f5')
