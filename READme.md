# Employee Management System

## Overview

As a software engineer, I created this comprehensive Employee Management System to practice database operations, CRUD functionality, and data analysis with Python and SQLite. This project demonstrates my ability to build functional database-driven applications with meaningful data analytics capabilities.

The software is a full-featured employee directory application that stores, manages, and analyzes employee information including contact details, departments, and employment history. The system provides insights into workforce metrics and retention patterns.

**Key Features:**
- Complete CRUD operations for employee records
- SQLite database with proper schema design
- Data analytics with SQL aggregate functions
- Department statistics and workforce analysis
- Employee tenure tracking and retention metrics

https://youtu.be/IHJz29Kwiag

## Development Environment

This project was developed using:
- **Operating System**: Windows
- **IDE**: Visual Studio Code
- **Programming Language**: Python 3
- **Database**: SQLite3
- **Key Libraries**: datetime, dateutil.relativedelta
- **Version Control**: Git with GitHub

## Database Design

The application uses a single SQLite database with the following schema:

```sql
CREATE TABLE employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    address TEXT NOT NULL,
    phone_number TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    department TEXT,
    entry_date DATE NOT NULL,
    departure_date DATE
)