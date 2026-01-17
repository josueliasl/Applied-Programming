# Imports for SQLITE database connection and operations

import sqlite3
from datetime import date, datetime
from dateutil.relativedelta import relativedelta

# Setup and Initialize Database

def get_connection(db_name):
    try: 
        return sqlite3.connect(db_name)
    except Exception as e:
        print(f'Error: {e}')
        raise

# Create a table in the database

def create_table(connection):
    query = """
    CREATE TABLE IF NOT EXISTS employees(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          full_name TEXT NOT NULL,
          address TEXT NOT NULL,
          phone_number TEXT NOT NULL,
          email TEXT NOT NULL UNIQUE,
          department TEXT,
          entry_date DATE NOT NULL,
          departure_date DATE
    )
    """
    try:
        with connection:
            connection.execute(query)
        print("Table was created!")
    except Exception as e:
        print(e)

# Add employee to database

def insert_employee(connection, 
                    full_name:str, 
                    address:str, 
                    phone_number:str, 
                    email:str, 
                    department:str,
                    entry_date:str, 
                    departure_date:str | None):
        query = """
        INSERT INTO employees(full_name, address, phone_number, email, department, entry_date, departure_date)
        VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        try:
            with connection :
                connection.execute(query, (full_name, address, phone_number, email, department, entry_date, departure_date))
            print(f"{full_name} was added to our list of employees!")
        except Exception as e:
            print(e)     

# Update employee information (contact details only):

# Delete employee when departing

def delete_employee(connection, id:int):
    query = "DELETE FROM employees WHERE id = ?"
    try: 
        with connection:
            connection.execute(query,(id,)) 
        print(f'USER ID: {id} was deleted!')
    except Exception as e:
        print(e)

# Update employee's email

def update_email(connection, id:int, email:str):
    query = "UPDATE employees SET email = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query,(email, id))
        print(f"User ID {id} has new email of {email}")
    except Exception as e:
        print(e)

# Update employee's address

def update_address(connection, id:int, address:str):
    query = "UPDATE employees SET address = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query,(address, id))
        print(f"User ID {id} has new address of {address}")
    except Exception as e:
        print(e)

# Update employee's phone number

def update_phone_number(connection, id:int, phone_number:str):
    query = "UPDATE employees SET phone_number = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query,(phone_number, id))
        print(f"User ID {id} has new phone_number of {phone_number}")
    except Exception as e:
        print(e)

# Update employee's department

def update_department(connection, id:int, department:str):
    query = "UPDATE employees SET department = ? WHERE id = ?"
    try:
        with connection:
            connection.execute(query,(department, id))
        print(f"User ID {id} has new department of {department}")
    except Exception as e:
        print(e)

# Summary of average time each worker has been working for us !!!

def average_worker_retention(connection):
    results = []
    query = "SELECT entry_date, departure_date FROM employees "
    try:
        with connection:
            data = connection.execute(query).fetchall()
    except Exception as e:
        print(e)
        

    today = datetime.today()
    for entry_date, departure_date in data:
        entry_date = datetime.strptime(entry_date, '%Y-%m-%d')
        
        if departure_date:
            departure_date = datetime.strptime(departure_date, '%Y-%m-%d')
            end_date = departure_date

        else:
            end_date = today

        delta = end_date - entry_date
        days_worked = delta.days

        rd = relativedelta(end_date, entry_date)

        years = rd.years
        months = rd.months
        remaining_days = rd.days
        years_worked = days_worked / 365.25

        results.append({ 
        'years_worked': round(years_worked, 2),
        'formatted': f"{years} years, {months} months, {remaining_days} days"
        })
    return results



# Summary of total number of employees in our history !!!

def count_total_employees(connection):
    """
    Count total number of employees in the database
    """
    query = "SELECT COUNT(*) FROM EMPLOYEES"
    try: 
        with connection: 
            cursor = connection.execute(query)
            total = cursor.fetchone()[0]
        return total
    except Exception as e:
        print(f"Error counting employees: {e}")
        return 0
    
# Summary of current VS former employees
def count_employees_by_status(connection):
    """
    Count current and former number of employees in the database
    """
    query = """ 
    SELECT 
    COUNT(*) as total,
    COUNT(CASE WHEN departure_date IS NULL THEN 1 END) as current_employees,
    COUNT(CASE WHEN departure_date IS NOT NULL THEN 1 END) as former_employees
    FROM employees
     """
    try:
        with connection:
            cursor = connection.execute(query)
            total, current, former = cursor.fetchone()

        current_pct = (current / total * 100) if total > 0 else 0
        former_pct = (former / total * 100) if total > 0 else 0 
        return{
            'total': total,
            'current': current,
            'former': former,
            'current_pct': round(current_pct, 1),
            'former_pct': round(former_pct, 1)
        }
    except Exception as e:
        print(f"Error counting employees by status: {e}")
        return{'total': 0,
               'current':0, 
               'former': 0,
               'current_pct':0,
               'former_pct': 0
               }

# Add many employees at once 
def insert_employees(connection, employees:list[tuple]):
    query = """INSERT INTO employees(full_name, address, phone_number, email, department, entry_date, departure_date)
    VALUES  (?, ?, ?, ?, ?, ?, ?)
    """
    try:
        with connection:
            connection.executemany(query, employees)
        print(f"{len(employees)} collaborators were added to the database!")
    except Exception as e:
        print(e)

# Retrieves and displays all employees

def fetch_users(connection, condition: str = None) -> list[tuple]:
    query = "SELECT * FROM employees"
    if condition:
        query += f" WHERE {condition}"
    try:
        with connection:
            rows = connection.execute(query).fetchall()
        return rows
    except Exception as e:
        print(e)
        return []

def get_department_stats(connection):
     """Use SQL GROUP BY and COUNT() aggregate function"""
     query="""
     SELECT department, COUNT(*) as num_employees
     FROM employees
     GROUP BY department
     ORDER BY num_employees DESC 
     """
     try:
         cursor = connection.cursor()
         cursor.execute(query)
         return cursor.fetchall()
     except Exception as e:
        print(f"Error: {e}")
        return []
# Main function: executes menu & user functionality

def main():
    connection = get_connection("employees.db")
    
    # Create table
    try:

        create_table(connection)
        
        while True:

            start = (input(
    """Enter your Option:
        1. Add
        2. Delete
        3. Update
        4. Search
        5. Average worker retention
        6. Number of workers
        7. Department statistics
        8. Exit): 
        """)).strip().lower()
        
            if start in ('add', '1'):
              while True:
                full_name = input('Enter full name: ')
                address = input('Enter address: ')
                phone_number = input('Enter phone number: ')
                email = input('Enter email: ')
                department = input('Enter department: ')
                entry_date = input('Enter entry date (YYYY-MM-DD): ')
                departure_date = input('Enter departure date (YYYY-MM-DD): ')
                
            
                if departure_date.strip() == "":
                        departure_date = None
                insert_employee(connection,
                                full_name, 
                                address, 
                                phone_number, 
                                email, 
                                department, 
                                entry_date, 
                                departure_date)
                repeat = input("Would you like to add another employee? (yes/no): ").strip().lower()
                if repeat not in ('yes', 'y', '1'):
                    print('Finished adding employees.')
                    break

            elif start in ("delete", "2"):
                try:
                    user_id = int(input("Enter User ID: "))
                except ValueError:
                   print("Invalid ID.")
                   continue
                delete_employee(connection, user_id)

            elif start in ("update", "3"):
                user_id = int(input("Enter the employee's id for changing information: "))
                data_change = (input("""What piece of data do you want to update? 
        1. Email
        2. Address
        3. Phone number
        4. Department
        5. None): """)).strip().lower()
                if data_change in ('email', '1'):
                        email = input('Enter new email: ')
                        update_email(connection, user_id, email)

                elif data_change in ('address', '2'):
                        address = input('Enter new address: ')
                        update_address(connection, user_id, address)

                elif data_change in ('phone number', 'phone', '3'):
                        phone_number = input('Enter new phone number: ')
                        update_phone_number(connection, user_id, phone_number)

                elif data_change in ('department', '4'):
                        department = input('Enter new department: ')
                        update_department(connection, user_id, department)

                elif data_change in ('none', '5'):
                         print('Thanks for letting us know, please go back to the main menu!')

                else:
                        print('Invalid option.')

            elif start in ('search', '4'):
                print("All users: ")
                for user in fetch_users(connection):
                   print(user)
                   
            elif start in ('average', 'Average worker retention', '5'):
                results = average_worker_retention(connection)
                if not results:
                    print("No employees found or an error ocurred.")
                else: 
                    print("Average time each employee has been working:")
                    for emp in results[:5]:
                        print(f"{emp['formatted']} ({emp['years_worked']} years)")

            elif start in ('number', 'Number of workers', '6'):
                total = count_total_employees(connection)
                print(f"\n{'='*60}")
                print('EMPLOYEE COUNT SUMMARY')
                print(f"{'='*60}")
                print(f"Total employees in database: {total}")

                counts = count_employees_by_status(connection)
                if counts['total'] > 0:
                    print(f"\nCurrent employees: {counts['current']} ({counts['current_pct']}%)")
                    print(f"Former employees: {counts['former']} ({counts['former_pct']}%)")
                    print(f"Active workforce: {counts['current_pct']:.1f}%")
                    print(f"{'='*60}\n")

            elif start in ('department', 'Department statistics', 'stats', '7'):
                dept_stats = get_department_stats(connection)
                if dept_stats:
                    print(f"\n{'Department':<25} {'Employees':<10} {'% of Total':<10}")
                    print("-" * 45)

                    total_employees = sum(count for _, count in dept_stats)
                    for department, count in dept_stats:
                        percentage = (count / total_employees * 100) if total_employees > 0 else 0
                        print(f"{department: <25} {count:<10} {percentage:.1f}%")
                        print("-" * 45)
                        print(f"{'TOTAL':<25} {total_employees:<10} {100:.1f}%")
                else:
                    print("No department data available.")

                print("="*60)



            elif start in ('exit', '8'):
                 print('Thank you, goodbye!')
                 break

    finally:
            connection.close()

if __name__ =="__main__":
 main()    