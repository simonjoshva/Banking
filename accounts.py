import tkinter as tk
from tkinter import ttk,messagebox
from database import create_connection
import random

def load_customers():
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select id,name from customers order by name"""
        cursor.execute(query)
        customers=cursor.fetchall()
        customer_combo["values"]=[f"{customer[0]}-{customer[1]}" for customer in customers]
        cursor.close()
        connection.close()
        
def generate_number():
    account_number=str(random.randint(1000000000,9999999999))
    account_number_entry.delete(0,tk.END)
    account_number_entry.insert(0,account_number)
    
def create_account():
    customer=customer_combo.get()
    account_type=account_type_combo.get()
    account_number=account_number_entry.get()
    if customer=="" or account_type=="" or account_number=="":
        messagebox.showwarning("warning","Please fill all fields")
        return
    customer_id=customer.split("-")[0]
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select id from accounts where account_number=%s"""
        cursor.execute(query,(account_number,))
        existing_account=cursor.fetchone()
        if existing_account:
            messagebox.showwarning("Warning","Account number already exists")
            return
        else:
            query="""insert into accounts (customer_id,account_number,account_type,balance) values(%s,%s,%s,%s)"""
            values=(customer_id,account_number,account_type,0.00)
            cursor.execute(query,values)
            connection.commit()
            cursor.close()
            connection.close()
            messagebox.showinfo("Success","Account created successfully")
            account_number_entry.delete(0,tk.END)
            account_type_combo.set("")
            customer_combo.set("")
            load_accounts()
def load_accounts():
    for item in account_tables.get_children():
        account_tables.delete(item)
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select accounts.id,customers.name,accounts.account_number,accounts.account_type,accounts.balance,accounts.status from accounts join customers on accounts.customer_id=customers.id order by accounts.id desc"""
        cursor.execute(query)
        accounts=cursor.fetchall()
        for account in accounts:
            account_tables.insert("",tk.END,values=account)
        cursor.close()
        connection.close()
                
    
def open_accounts():
    window=tk.Toplevel()
    window.title('Account Mangement')
    window.geometry('1000x600')
    global account_tables
    title=tk.Label(window,text='ACCOUNT MANAGEMENT',font=('Arial',20,'bold')).pack(pady=15)
    form_frame=ttk.Frame(window)
    form_frame.pack(pady=10)
    ttk.Label(form_frame,text='Customer').grid(row=0,column=0,padx=10,pady=10)
    global customer_combo
    customer_combo=ttk.Combobox(form_frame,width=30,state="readonly")
    customer_combo.grid(row=0,column=1,padx=10,pady=10)
    ttk.Label(form_frame,text='Account Type').grid(row=1,column=0,padx=10,pady=10)
    global account_type_combo
    account_type_combo=ttk.Combobox(form_frame,values=["saving","Current"],width=30,state="readonly")
    account_type_combo.grid(row=1,column=1,padx=10,pady=10)
    ttk.Label(form_frame,text="Account Number").grid(row=2,column=0,padx=10,pady=10)
    global account_number_entry
    account_number_entry=ttk.Entry(form_frame,width=30)
    account_number_entry.grid(row=2,column=1,padx=10,pady=10)
    ttk.Button(form_frame,text="GENERATE",command=generate_number).grid(row=2,column=2,padx=10)
    ttk.Button(window,text='CREATE ACCOUNT',command=create_account).pack(pady=15)
    table_frame=ttk.Frame(window)
    table_frame.pack(fill="both",expand=True,padx=20,pady=10)
    columns=("ID","Customer","Account Number","Account Type","Balance","Status")
    account_tables=ttk.Treeview(table_frame,columns=columns,show="headings",height=12)
    for column in columns:
        account_tables.heading(column,text=column)
        account_tables.column(column,width=150)
    account_tables.bind("<ButtonRelease-1>")
    account_tables.pack(side="left",fill="both",expand=True)
    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=account_tables.yview)
    scrollbar.pack(side="right",fill="y")
    account_tables.configure(yscrollcommand=scrollbar.set)
    load_accounts()
    load_customers()
