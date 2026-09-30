-- Gym Management System Database
-- Database: gym_management

CREATE DATABASE IF NOT EXISTS gym_management;
USE gym_management;

-- Members table
CREATE TABLE IF NOT EXISTS members (
    member_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(20),
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(100),
    membership_plan VARCHAR(50),
    join_date DATE,
    expiry_date DATE
);

-- Trainers table
CREATE TABLE IF NOT EXISTS trainers (
    trainer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    specialization VARCHAR(100),
    salary DECIMAL(10,2) NOT NULL
);

-- Payments table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date DATE NOT NULL,
    payment_method VARCHAR(50),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Attendance table
CREATE TABLE IF NOT EXISTS attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    member_id INT NOT NULL,
    attendance_date DATE NOT NULL,
    status VARCHAR(30),
    FOREIGN KEY (member_id) REFERENCES members(member_id)
);

-- Optional: create the MySQL user used by the Python program.
-- For GitHub, replace the password with your own local password and
-- keep real credentials out of the repository.
-- CREATE USER IF NOT EXISTS 'gym_user'@'localhost' IDENTIFIED BY 'YOUR_PASSWORD';
-- GRANT ALL PRIVILEGES ON gym_management.* TO 'gym_user'@'localhost';
-- FLUSH PRIVILEGES;
