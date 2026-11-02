import tkinter as tk
from tkinter import ttk,messagebox
from database import create_connection

def load_accounts():
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select id,account_number from accounts where status='Active' order by account_number"""
        cursor.execute(query)
        accounts=cursor.fetchall()
        account_combo['values']=[f"{account[0]}-{account[1]}"for account in accounts]
        cursor.close()
        connection.close()
        
def deposit_money():
    account=account_combo.get()
    amount=amount_entry.get()
    if account=="" or amount=="":
        messagebox.showwarning("warning","please select an account and amount")
        return
    try:
        amount=float(amount)
        if amount<0:
            messagebox.showwarning("Warning","Amount must be greater than 0")
            return
    except ValueError:
        messagebox.showwarning("Warning","Please Enter a valid amount")
        return
    if amount>1000000:
        messagebox.showwarning("Warning","Amount is to large")
        return
    account_id=account.split("-")[0]
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select balance from accounts where id=%s"""
        cursor.execute(query,(account_id,))
        result=cursor.fetchone()
        if result is None:
            messagebox.showerror("Error","Account not found")
            cursor.close()
            connection.close()
            return
        current_balance=float(result[0])
        new_balance=current_balance+amount
        query="""update accounts set balance=%s where id=%s"""
        cursor.execute(query,(new_balance,account_id))
        query="""insert into transactions (account_id,transaction_type,amount,balance_after,description)values(%s,%s,%s,%s,%s)"""
        values=(account_id,"Deposit",amount,new_balance,"Cash deposit")
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success",f"₹{amount:,.2f} deposited successfully!")
        account_combo.set("")
        amount_entry.delete(0,tk.END)
        
def open_deposit():
    window=tk.Toplevel()
    window.title('Deposit Money')
    window.geometry('1000x600')
    title=ttk.Label(window,text='DEPOSIT MONEY',font=('Arial',20,'bold'))
    title.pack(pady=20)
    form_frame=ttk.Frame(window)
    form_frame.pack(pady=10)
    ttk.Label(form_frame,text='Account').grid(row=0,column=0,padx=10,pady=15)
    global account_combo
    account_combo=ttk.Combobox(form_frame,width=30,state="readonly")
    account_combo.grid(row=0,column=1,padx=10,pady=15)
    ttk.Label(form_frame,text='Amount').grid(row=1,column=0,padx=10,pady=15)
    global amount_entry
    amount_entry=ttk.Entry(form_frame,width=33)
    amount_entry.grid(row=1,column=1,padx=10,pady=15)
    ttk.Button(window,text='DEPOSIT MONEY',command=deposit_money).pack(pady=20)
    load_accounts()
    
def withdraw_money():
    account=account_combo.get()
    amount=amount_entry.get()
    if account=="" or amount=="":
        messagebox.showwarning("Warning","Please select an account and enter amount")
        return
    try:
        amount=float(amount)
        if amount<=0:
            messagebox.showwarning("Warning","Amount must be greater than 0")
            return
    except ValueError:
        messagebox.showwarning("Warning","Please enter a valid amount")
        return
    account_id=account.split("-")[0]
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select balance from accounts where id=%s"""
        cursor.execute(query,(account_id,))
        result=cursor.fetchone()
        if result is None:
            messagebox.showerror("Error","Account not found")
            cursor.close()
            connection.close()
            return
        current_balance=float(result[0])
        if amount>current_balance:
            messagebox.showwarning("Insufficient Balance","Not enough balance in this account")
            cursor.close()
            connection.close()
            return
        new_balance=current_balance-amount
        query="""update accounts set balance=%s where id=%s"""
        cursor.execute(query,(new_balance,account_id))
        query="""insert into transactions (account_id,transaction_type,amount,balance_after,description) values(%s,%s,%s,%s,%s)"""
        values=(account_id,"Withdraw",amount,new_balance,"Cash Withdraw")
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success",f"₹{amount:,.2f} withdrawn successfully!")
        account_combo.set("")
        amount_entry.delete(0,tk.END)

def open_withdraw():
    window=tk.Toplevel()
    window.geometry("500x350")
    
    title=ttk.Label(text="WITHDRAW MONEY",font=("Ariel",20,"bold"))
    title.pack(pady=20)
    form_frame=ttk.Frame(window)
    form_frame.pack(pady=10)
    ttk.Label(form_frame,text="Account").grid(row=0,column=0,padx=10,pady=15)
    global account_combo
    account_combo=ttk.Combobox(form_frame,width=30,)
    account_combo.grid(row=0,column=1,padx=10,pady=15)
    ttk.Label(form_frame,text="Amount").grid(row=1,column=0,padx=10,pady=15)
    global amount_entry
    amount_entry=ttk.Entry(form_frame,width=33)
    amount_entry.grid(row=1,column=1,padx=10,pady=15)
    ttk.Button(window,text="WITHDRAW MONEY",command=withdraw_money).pack(pady=20)
    load_accounts()
    
def load_transactions():
    for item in transaction_table.get_children():
        transaction_table.delete(item)
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select transactions.id,accounts.account_number,transactions.transaction_type,transactions.amount,transactions.balance_after,transactions.description,transactions.transaction_date from transactions join accounts on transactions.account_id=accounts.id order by transactions.id desc"""
        cursor.execute(query)
        transactions=cursor.fetchall()
        for transaction in transactions:
            transaction_table.insert("",tk.END,values=transaction)
            cursor.close()
            connection.close()
            
def open_transactions():
    window=tk.Toplevel()
    window.title("Transaction History")
    window.geometry("1100x600")
    title=ttk.Label(window,text="TRANSACTION HISTORY",font=('Arial',20,"bold"))
    title.pack(pady=20)
    table_frame=ttk.Frame(window)
    table_frame.pack(fill="both",expand=True,padx=20,pady=10)
    columns=("ID","Account Number","Type","Amount","Balance After","Description","Date")
    global transaction_table
    transaction_table=ttk.Treeview(table_frame,columns=columns,show="headings",height=18)
    for column in columns:
        transaction_table.heading(column,text=column)
        transaction_table.column(column,width=140)
    transaction_table.pack(side="left",fill="both",expand=True)
    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=transaction_table.yview)
    scrollbar.pack(side="right",fill="y")
    transaction_table.configure(yscrollcommand=scrollbar.set)
    load_transactions() 
        
    
    
    
