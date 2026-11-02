import tkinter as tk
from tkinter import ttk
from database import create_connection
def get_report_data():
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        cursor.execute("select count(*)from customers")
        total_customers=cursor.fetchone()[0]
        cursor.execute("select count(*)from accounts")
        total_accounts=cursor.fetchone()[0]
        cursor.execute("select sum(balance)from accounts")
        total_balance=cursor.fetchone()[0]or 0
        cursor.execute("""select sum(amount)from transactions where transaction_type='Deposit'""")
        total_deposits=cursor.fetchone()[0]or 0
        cursor.execute("""select sum(amount)from transactions where transaction_type='Withdraw'""")
        total_withdrawals=cursor.fetchone()[0]or 0
        cursor.close()
        connection.close()
        return(total_customers,total_accounts,total_balance,total_deposits,total_withdrawals)
    return 0,0,0,0,0
def open_reports():
    window=tk.Toplevel()
    window.geometry("700x550")
    title=ttk.Label(window,text="BANK REPORTS",font=("Arial",22,"bold"))
    title.pack(pady=25)
    data=get_report_data()
    total_customers=data[0]
    total_accounts=data[1]
    total_balance=data[2]
    total_deposits=data[3]
    total_withdrawals=data[4]
    report_frame=ttk.Frame(window)
    report_frame.pack(pady=20)
    ttk.Label(report_frame,text="Total Customers",font=("Arial",13)).grid(row=0,column=0,padx=30,pady=15)
    ttk.Label(report_frame,text=str(total_customers),font=("Arial",13)).grid(row=0,column=1,padx=30)
    ttk.Label(report_frame,text="Total Accounts",font=("Arial",13)).grid(row=1,column=0,padx=30,pady=15)
    ttk.Label(report_frame,text=str(total_accounts),font=("Arial",13)).grid(row=1,column=1,padx=30,pady=15)
    ttk.Label(report_frame,text="Total Bank Balance",font=("Arial",13)).grid(row=2,column=0,padx=30,pady=15)
    ttk.Label(report_frame,text=f"${float(total_balance):,.2f}",font=("Arial",13)).grid(row=2,column=1,padx=30)
    ttk.Label(report_frame,text="Total Deposits",font=("Arial",13)).grid(row=3,column=0,padx=30,pady=15)
    ttk.Label(report_frame,text=f"${float(total_deposits):,.2f}",font=("Arial",13)).grid(row=3,column=1,padx=30)
    ttk.Label(report_frame,text="Total WithDrawals",font=("Arial",13)).grid(row=4,column=0,padx=30,pady=15)
    ttk.Label(report_frame,text=f"${float(total_withdrawals):,.2f}",font=("Arial",13)).grid(row=4,column=1,padx=30)
    
    

    