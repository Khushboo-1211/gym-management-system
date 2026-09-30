import tkinter as tk
from tkinter import ttk
import mysql.connector

import members
import trainers
import payments
import attendance


# ---------- DATABASE CONNECTION ----------

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="gym_user",
        password="Gym@123",
        database="gym_management"
    )


# ---------- OPEN MODULES ----------

def open_members():
    members.open_members()


def open_trainers():
    trainers.open_trainers()


def open_payments():
    payments.open_payments()


def open_attendance():
    attendance.open_attendance()


# ---------- DASHBOARD STATS ----------

def get_count(query):
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(query)
        result = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return result

    except Exception:
        return 0


def update_dashboard():

    members_count.set(
        get_count("SELECT COUNT(*) FROM members")
    )

    trainers_count.set(
        get_count("SELECT COUNT(*) FROM trainers")
    )

    payments_count.set(
        get_count("SELECT COUNT(*) FROM payments")
    )

    attendance_count.set(
        get_count(
            "SELECT COUNT(*) FROM attendance "
            "WHERE attendance_date = CURDATE()"
        )
    )


# ---------- MAIN WINDOW ----------

root = tk.Tk()

root.title("Gym Management System")
root.geometry("1000x650")
root.resizable(False, False)


# ---------- TITLE ----------

title = tk.Label(
    root,
    text="GYM MANAGEMENT SYSTEM",
    font=("Arial", 28, "bold")
)

title.pack(pady=25)


subtitle = tk.Label(
    root,
    text="Management Dashboard",
    font=("Arial", 14)
)

subtitle.pack()


# ---------- STAT VARIABLES ----------

members_count = tk.StringVar()
trainers_count = tk.StringVar()
payments_count = tk.StringVar()
attendance_count = tk.StringVar()


# ---------- STAT CARDS ----------

stats_frame = tk.Frame(root)
stats_frame.pack(pady=30)


def create_card(parent, title, variable):
    frame = tk.Frame(
        parent,
        width=200,
        height=110,
        relief="ridge",
        borderwidth=2
    )

    frame.pack_propagate(False)

    tk.Label(
        frame,
        text=title,
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    tk.Label(
        frame,
        textvariable=variable,
        font=("Arial", 24, "bold")
    ).pack()

    frame.pack(side=tk.LEFT, padx=10)


create_card(
    stats_frame,
    "Total Members",
    members_count
)

create_card(
    stats_frame,
    "Total Trainers",
    trainers_count
)

create_card(
    stats_frame,
    "Total Payments",
    payments_count
)

create_card(
    stats_frame,
    "Today's Attendance",
    attendance_count
)


# ---------- MANAGEMENT BUTTONS ----------

management_frame = tk.Frame(root)
management_frame.pack(pady=20)


tk.Button(
    management_frame,
    text="Member Management",
    width=25,
    height=2,
    font=("Arial", 12),
    command=open_members
).grid(row=0, column=0, padx=10, pady=10)


tk.Button(
    management_frame,
    text="Trainer Management",
    width=25,
    height=2,
    font=("Arial", 12),
    command=open_trainers
).grid(row=0, column=1, padx=10, pady=10)


tk.Button(
    management_frame,
    text="Payment Management",
    width=25,
    height=2,
    font=("Arial", 12),
    command=open_payments
).grid(row=1, column=0, padx=10, pady=10)


tk.Button(
    management_frame,
    text="Attendance Management",
    width=25,
    height=2,
    font=("Arial", 12),
    command=open_attendance
).grid(row=1, column=1, padx=10, pady=10)


# ---------- REFRESH BUTTON ----------

tk.Button(
    root,
    text="Refresh Dashboard",
    width=25,
    height=2,
    font=("Arial", 11),
    command=update_dashboard
).pack(pady=10)


# ---------- EXIT BUTTON ----------

tk.Button(
    root,
    text="Exit",
    width=25,
    height=2,
    font=("Arial", 11),
    command=root.destroy
).pack(pady=5)


# ---------- LOAD STATS ----------

update_dashboard()


root.mainloop()