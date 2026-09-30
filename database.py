import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="gym_user",
    password="Gym@123",
    database="gym_management"
)

if connection.is_connected():
    print("Connected to Gym Management Database!")

connection.close()
