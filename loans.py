import sqlite3
import os.path


"""
Defines the queries used
"""
CREATE_LOAN_TABLE = '''CREATE TABLE loans(loan_number, name, application_file, loan_date date, 
                amount_loaned, age, gender, business_type, location)'''
CREATE_SCHEDULE_TABLE = '''CREATE TABLE payment_schedules
                              (loan_number, scheduled_date date, amount)'''
CREATE_PAYMENT_TABLE = '''CREATE TABLE payments(loan_number, payment_date date, amount, reciept)'''

ADD_LOAN = '''INSERT INTO loans(loan_number, name, application_file, loan_date, 
                amount_loaned, age, gender, business_type, location)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
ADD_SCHEDULED_PAYMENT = '''INSERT INTO payment_schedules(loan_number, scheduled_date, amount)
                 VALUES (?, ?, ?)'''
ADD_PAYMENT = '''INSERT INTO payments(loan_number, payment_date, amount, reciept) 
                            VALUES (?, ?, ?, ?)'''

GET_LOAN_NUMBERS = '''SELECT loan_number FROM loans ORDER BY loan_number ASC'''
GET_LOAN = '''SELECT loan_number, name, application_file, loan_date as "loan_date [date]", 
                amount_loaned, age, gender, business_type, location
                FROM loans WHERE loan_number = ?'''
GET_LOAN_SCHEDULE = '''SELECT loan_number, scheduled_date as "d [date]", amount from 
                          payment_schedules WHERE loan_number = ? ORDER BY
                          date(scheduled_date) ASC'''
GET_LOAN_PAYMENTS = '''SELECT loan_number, payment_date as "d [date]", amount, reciept 
                          from payments WHERE loan_number = ? ORDER BY date(payment_date) ASC'''


db = None
cursor = None

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connect():
    global db, cursor
    init = False
    if not os.path.isfile('loan.db'):
        init = True
    db = sqlite3.connect('loan.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    db.row_factory = dict_factory
    cursor = db.cursor()
    if init:
        initial_setup()

def initial_setup():
    global db, cursor
    cursor.execute(CREATE_LOAN_TABLE)
    cursor.execute(CREATE_SCHEDULE_TABLE)
    cursor.execute(CREATE_PAYMENT_TABLE)
    db.commit()

"""
ADD FUNCTIONS
"""

def add_loan(loan_number, name, application_file, loan_date, amount_loaned, 
             age, gender, business_type, location):
    """
    Adds a loan to the database
    """
    global db, cursor
    loan_data = (loan_number, name, application_file, loan_date, amount_loaned, 
                 age, gender, business_type, location)
    cursor.execute(ADD_LOAN, loan_data)
    db.commit()

def add_scheduled_payment(loan_number, date, amount):
    global db, cursor
    data = (loan_number, date, amount)
    cursor.execute(ADD_SCHEDULED_PAYMENT, data)
    db.commit()

def add_payment(loan_number, date, amount, reciept):
    global db, cursor
    data = (loan_number, date, amount, reciept)
    cursor.execute(ADD_PAYMENT, data)
    db.commit()



"""
GET FUNCTIONS
"""
def get_loan(loan_number):
    data = (loan_number,)
    # get the main loan information
    cursor.execute(GET_LOAN, data)
    loan_info = cursor.fetchone()

    # get the scheduled payments
    schedule = []
    # builds a sorted list of all the scheduled payment dates
    amount = int(loan_info['amount_loaned'])
    for row in cursor.execute(GET_LOAN_SCHEDULE, data):
        amount -= int(row['amount'])
        schedule.append({'date':row['d'], 'amount':row['amount'], 'owed':amount}) 
        # remove loan number because we don't care about it
    

    # get the actual payments
    payments = []
    owed = int(loan_info['amount_loaned'])
    for row in cursor.execute(GET_LOAN_PAYMENTS, data):
        owed -= int(row['amount'])
        payments.append({'date':row['d'], 'amount':row['amount'], 'owed':owed,
                         'receipt':row['reciept']})

    return {'loan_info':loan_info, 'schedule':schedule, 'payments':payments}

def get_all_loans():
    loans = []
    cursor.execute(GET_LOAN_NUMBERS)
    loan_numbers = cursor.fetchall()
    for loan_number in loan_numbers:
        loans.append(get_loan(loan_number['loan_number']))
    return loans
