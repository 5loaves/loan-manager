import loans as loansDB
from time import strftime
from datetime import date, datetime
import json

loansDB.connect()

def format_date(d):
    return d.strftime('%d-%b-%Y')

def deformat_date(string_date):
    return datetime.strptime(string_date, "%Y-%m-%d").date()

def get_last_payment(payments):
    return format_date(payments[-1]['date']) if len(payments) != 0 else 'Never'

def get_next_payment(schedule):
    for d in schedule:
        if d['date'] > date.today():
            return format_date(d['date'])

def amount_behind(payments, schedule):
    expected_paid = 0
    for d in schedule:
        if d['date'] <= date.today():
            expected_paid += int(d['amount'])
    paid = 0
    for p in payments:
        paid += int(p['amount'])
    return expected_paid - paid

def days_behind(payments, schedule):
    if amount_behind(payments, schedule) > 0:
        for d in schedule:
            if d['date'] <= date.today():
                return -(d['date'].day-date.today().day)
    return 0

def owed(loaned, payments):
    paid = 0
    for p in payments:
        paid += int(p['amount'])
    return int(loaned) - paid


def get_home_page_table():
    loans = loansDB.get_all_loans()
    loan_table = []
    for l in loans:
        loan = l['loan_info']
        loan_table.append({'loanNum':loan['loan_number'],
                           'amount':loan['amount_loaned'],
                           'owed':str(owed(loan['amount_loaned'], l['payments'])),
                           'lastPay': get_last_payment(l['payments']),
                           'nextPay': get_next_payment(l['schedule']),
                           'daysBehind': days_behind(l['payments'], l['schedule']),
                           'amountBehind':'$'+str(amount_behind(l['payments'], l['schedule']))})
    return json.dumps(loan_table)


def generate_kiva_report():
    loans = loansDB.get_all_loans()
    report = ''
    for l in loans:
        loan = l['loan_info']
        report += loan['loan_number'] + ',' + str(owed(loan['amount_loaned'], l['payments']))
        report += '\n'
    return json.dumps(report)

def get_loan(msg):
    loan_number = msg['loanNum']
    loan = loansDB.get_loan(loan_number)

    for p in loan:
        if type(loan[p]) == dict:
            for p2 in loan[p]:
                if type(loan[p][p2]) == date:
                    loan[p][p2] = format_date(loan[p][p2])
#        print '1',type(loan[p])
        if type(loan[p]) == list:
            for p2 in range(len(loan[p])):
 #               print '2',type(loan[p][p2]),loan[p][p2]
                if type(loan[p][p2]['date']) == date:
                    loan[p][p2]['date'] = format_date(loan[p][p2]['date'])
    return json.dumps(loan)

def add_loan(loan):
    print 'adding'
    loan_number = loan['loanNum']
    ln = loansDB.get_loan(loan_number)
    if ln:
        print 'error, loan already exists', loan_number
        return
    
    loansDB.add_loan(loan['loanNum'], loan['name'], loan['file'], deformat_date(loan['loanDate']), 
                loan['amount'], loan['age'], loan['gender'], loan['business'], loan['location'])

    for p in loan['payments']:
        loansDB.add_scheduled_payment(loan['loanNum'], deformat_date(p['date']), p['amount'])

def add_payment(payment):
    loansDB.add_payment(payment['loanNum'], payment['date'], payment['amount'], payment['reciept'])
