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
        account_values=[f"{account[0]}-{account[1]}" for account in accounts]
        sender_combo["value"]=account_values
        receiver_combo["value"]=account_values
        cursor.close()
        connection.close()
def transfer_money():
    sender=sender_combo.get()
    receiver=receiver_combo.get()
    amount=amount_entry.get()
    description=description_entry.get()
    if sender==""or receiver =="" or amount =="":
        messagebox.showwarning("Warning","Please Fill the all required fields")
        return
    if sender==receiver:
        messagebox.showwarning("Warning","Sender and receiver cannot be the same")
        return
    try:
        amount=float(amount)
        if amount<=0:
           messagebox.showwarning("Warning","Amount must be greater than 0")
           return
    except ValueError:
        messagebox.showwarning("Warning","Please enter a valid amount")
        return
    sender_id=sender.split("-")[0]
    receiver_id=receiver.split("-")[0]
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select balance from accounts where id=%s"""
        cursor.execute(query,(sender_id,))
        result=cursor.fetchone()
        if result is None:
            messagebox.showerror("Error","Sender Account not found")
            cursor.close()
            connection.close()
            return
        sender_balance=float(result[0])
        if amount>sender_balance:
            messagebox.showwarning("Insufficient Balance","Sender does not have enough balance")
            cursor.close()
            connection.close()
            return
        new_sender_balance=sender_balance-amount
        query="""select balance from accounts where id=%s"""
        cursor.execute(query,(receiver_id,))
        result=cursor.fetchone()
        if result is None:
            messagebox.showerror("Error","Receiver account not found")
            cursor.close()
            connection.colse()
            return
        receiver_balance=float(result[0])
        new_receiver_balance=receiver_balance+amount
        query="""update accounts set balance=%s where id=%s"""
        cursor.execute(query,(new_sender_balance,sender_id))
        cursor.execute(query,(new_receiver_balance,receiver_id))
        query="""insert into transfers (sender_account,receiver_account,amount,description)values(%s,%s,%s,%s)"""
        values=(sender,receiver,amount,description)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("success",f"₹{amount:,.2f} transferred successfully.")
        sender_combo.set("")
        receiver_combo.set("")
        amount_entry.delete(0,tk.END)
        description_entry.delete(0,tk.END)
        
def open_transfer():
    window=tk.Toplevel()
    window.title('Transfer Money')
    window.geometry('600x450')
    title=ttk.Label(window,text='TRANSFER MONEY',font=('Arial',20,'bold'))
    title.pack(pady=20)
    form_frame=ttk.Frame(window)
    form_frame.pack(pady=10)
    ttk.Label(form_frame,text='Sender Account').grid(row=0,column=0,padx=10,pady=15)
    global sender_combo
    sender_combo=ttk.Combobox(form_frame,width=30,state="readonly")
    sender_combo.grid(row=0,column=1,padx=10,pady=15)
    ttk.Label(form_frame,text='Receiver Account').grid(row=1,column=0,padx=10,pady=15)
    global receiver_combo
    receiver_combo=ttk.Combobox(form_frame,width=30,state="readonly")
    receiver_combo.grid(row=1,column=1,padx=10,pady=15)
    ttk.Label(form_frame,text='Amount').grid(row=2,column=0,padx=10,pady=15)
    global amount_entry
    amount_entry=ttk.Entry(form_frame,width=33)
    amount_entry.grid(row=2,column=1,padx=10,pady=15)
    ttk.Label(form_frame,text='Description').grid(row=3,column=0,padx=10,pady=15)
    global description_entry
    description_entry=ttk.Entry(form_frame,width=33)
    description_entry.grid(row=3,column=1,padx=10,pady=15)
    ttk.Button(window,text='TRANSFER MONEY',command=transfer_money).pack(pady=20)
    load_accounts()
    
    
    
    
    
    
            
            
    