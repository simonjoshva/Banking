import tkinter as tk
from tkinter import ttk
from database import create_connection
from customer import open_customers
from accounts import open_accounts
from transaction import open_deposit,open_withdraw,open_transactions
from transfer import open_transfer
from statements import open_statement
from reports import open_reports
def get_count(table_name):
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        result=cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return result
    return 0

def get_total_balance():
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        cursor.execute("SELECT SUM(balance) FROM accounts")
        result=cursor.fetchone()[0]
        cursor.close()
        connection.close()
        return result if result is not None else 0
    return 0

def refresh_dashboard():
    total_customers=get_count("customers")
    total_accounts=get_count("accounts")
    total_balance=get_total_balance()
    customer_count_label.config(text=str(total_customers))
    account_count_label.config(text=str(total_accounts))
    balance_label.config(text=f"Rs.{total_balance:,.2f}")
        

def open_dashboard(username,role):
    d=tk.Tk()
    d.title('Bank Management System-Dashboard')
    d.geometry('900x600')
    title=ttk.Label(d,text='BANK MANAGEMENT SYSTEM',font=('Arial',22,'bold'))
    title.pack(pady=20)
    welcome=ttk.Label(d,text=f'Welcome,{username}({role})',font=('Arial',12))
    welcome.pack(pady=10)
    card_frame=ttk.Frame(d)
    card_frame.pack(pady=30)
    total_customers=get_count('customers')
    total_accounts=get_count('accounts')
    total_balance=get_total_balance()
    customer_frame=ttk.LabelFrame(card_frame,text='customers',padding=20)
    customer_frame.grid(row=0,column=0,padx=15)
    global customer_count_label
    customer_count_label=ttk.Label(customer_frame,text=str(total_customers),font=('Arial',20,'bold'))
    customer_count_label.pack()
    global account_count_label
    account_frame=ttk.LabelFrame(card_frame,text='Accounts',padding=20)
    account_frame.grid(row=0,column=1,padx=15)
    account_count_label=ttk.Label(account_frame,text=str(total_accounts),font=('Arial',20,'bold'))
    account_count_label.pack()
    balance_frame=ttk.LabelFrame(card_frame,text='Total Balance',padding=20)
    balance_frame.grid(row=0,column=2,padx=15)
    global balance_label
    balance_label=ttk.Label(balance_frame,text=f"{total_balance:,.2f}",font=('Arial',20,'bold'))
    balance_label.pack()
    button_frame=ttk.Frame(d)
    button_frame.pack(pady=30)
    ttk.Button(button_frame,text='Customers',width=20,command=open_customers).grid(row=0,column=0,padx=10,pady=10)
    ttk.Button(button_frame,text='Accounts',width=20,command=open_accounts).grid(row=0,column=1,padx=10,pady=10)
    ttk.Button(button_frame,text='Deposit',width=20,command=open_deposit).grid(row=1,column=0,padx=10,pady=10)
    ttk.Button(button_frame,text='Withdraw',width=20,command=open_withdraw).grid(row=1,column=1,padx=10,pady=10)
    ttk.Button(button_frame,text='Transfer',width=20,command=open_transfer).grid(row=2,column=0,padx=10,pady=10)
    ttk.Button(button_frame,text='Transactions',width=20,command=open_transactions).grid(row=2,column=1,padx=10,pady=10)
    ttk.Button(button_frame,text='Statements',width=20,command=open_statement).grid(row=3,column=0,padx=10,pady=10)
    ttk.Button(button_frame,text='Reports',width=20,command=open_reports).grid(row=3,column=1,padx=10,pady=10)
    ttk.Button(d,text="REFERESH DASHBOARD",command=refresh_dashboard).pack(pady=20)
    d.mainloop()
#open_dashboard("admin","Admin")
