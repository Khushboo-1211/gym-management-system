# Gym Management System

## Project Overview

The **Gym Management System** is a Python-based desktop application developed to manage the daily operations of a gym.

The system uses **Python, Tkinter, and MySQL** to provide a simple graphical interface for managing gym members, trainers, payments, and attendance.

## Features

* Member Management

  * Add members
  * Update member details
  * Delete members
  * Search members
  * View all members
  * Input validation

* Trainer Management

  * Add trainers
  * Update trainer details
  * Delete trainers
  * Search and view trainers

* Payment Management

  * Record payments
  * Update payment details
  * Delete payments
  * View payment records
  * Payment validation

* Attendance Management

  * Mark member attendance
  * View attendance records
  * Update attendance
  * Delete attendance
  * Attendance validation

* Dashboard

  * Total members
  * Total trainers
  * Total payments
  * Today's attendance
  * Refresh dashboard

## Technologies Used

* Python
* Tkinter
* MySQL
* MySQL Connector/Python
* SQL

## Project Structure

```text
gym management system/
│
├── main.py
├── database.py
├── members.py
├── trainers.py
├── payments.py
├── attendance.py
├── gym_database.sql
└── README.md
```

## Database

The project uses a MySQL database named:

`gym_management`

The database contains the following tables:

* `members`
* `trainers`
* `payments`
* `attendance`

## Installation and Setup

### 1. Install Python

Install Python on your system.

### 2. Install MySQL

Install MySQL Server and MySQL Workbench.

### 3. Install Python MySQL Connector

Open the terminal and run:

```bash
pip install mysql-connector-python
```

### 4. Create the Database

Open MySQL Workbench and execute the SQL commands provided in:

`gym_database.sql`

### 5. Run the Application

Open the project folder in VS Code and run:

```bash
python main.py
```

## System Requirements

* Windows 10/11
* Python 3.x
* MySQL Server
* MySQL Workbench
* VS Code or any Python IDE

## Purpose of the Project

The purpose of this project is to demonstrate the use of **Python GUI programming, SQL database management, CRUD operations, validation, and database connectivity** in a real-world application.

## Future Scope

The system can be further improved by adding:

* Login and authentication
* Membership expiry notifications
* Automated payment reminders
* Trainer assignment to members
* Monthly revenue reports
* Graphs and analytics
* Backup and restore functionality


