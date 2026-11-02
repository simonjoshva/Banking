import tkinter as tk
from tkinter import ttk,messagebox
from database import create_connection
from datetime import datetime
def save_customer():
    name=name_entry.get()
    if not name.replace("","").isalpha():
        messagebox.showwarning("Warning","Name must contains only letters")
        return
    phone=phone_entry.get()
    if not phone.isdigit():
        messagebox.showwarning("Warning","Phone number must contain only numbers")
        return
    if len(phone)!=10:
        messagebox.showwarning("Warning","Phone number must contain 10 digits")
        return
    email=email_entry.get()
    address=address_entry.get()
    gender=gender_combo.get()
    dob=dob_entry.get()
    try:
        datetime.strptime(dob,"%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Warning","Date must be in YYYY-MM-DD format")
        return
    
    if name=="" or phone=="" or gender=="" or dob=="":
        messagebox.showwarning("Warning","Please fill all required fields")
        return
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""INSERT INTO customers (name,phone,email,address,gender,date_of_birth)VALUES(%s,%s,%s,%s,%s,%s)"""
        values=(name,phone,email,address,gender,dob)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        messagebox.showinfo("Success","Customer added Successfully")
        clear_fields()
        load_customers()

def clear_fields():
    name_entry.delete(0,tk.END)
    phone_entry.delete(0,tk.END)
    email_entry.delete(0,tk.END)
    address_entry.delete(0,tk.END)
    dob_entry.delete(0,tk.END)
    gender_combo.set("")
    search_entry.delete(0,tk.END)
    
def load_customers():
    for item in customer_table.get_children():
        customer_table.delete(item)
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""SELECT id,name,phone,email,address,gender,date_of_birth FROM customers ORDER BY id DESC"""
        cursor.execute(query)
        customers=cursor.fetchall()
        for customer in customers:
            customer_table.insert("",tk.END,values=customer)
        cursor.close()
        connection.close()
        
def search_customer():
    search=search_entry.get()
    for item in customer_table.get_children():
        customer_table.delete(item)
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""SELECT id,name,phone,email,address,gender,date_of_birth FROM customers WHERE name LIKE %s OR phone LIKE %s OR id LIKE %s ORDER BY id DESC"""
        search_value="%"+search+"%"
        cursor.execute(query,(search_value,search_value,search_value))
        customers=cursor.fetchall()
        for customer in customers:
            customer_table.insert("",tk.END,values=customer)
        cursor.close()
        connection.close()
def select_customer(event):
    selected=customer_table.selection()
    if not selected:
        return
    item=customer_table.item(selected[0])
    value=item["values"]
    name_entry.delete(0,tk.END)
    name_entry.insert(0,value[1])
    phone_entry.delete(0,tk.END)
    phone_entry.insert(0,value[2])
    email_entry.delete(0,tk.END)
    email_entry.insert(0,value[3])
    address_entry.delete(0,tk.END)
    address_entry.insert(0,value[4])
    gender_combo.set(value[5])
    dob_entry.delete(0,tk.END)
    dob_entry.insert(0,value[6])
    
def update_customer():
    selected=customer_table.selection()
    if not selected:
        messagebox.showwarning("Warning","Please select a customer")
        return
    item=customer_table.item(selected[0])
    customer_id=item["values"][0]
    name=name_entry.get()
    
    phone=phone_entry.get()
        
    email=email_entry.get()
    address=address_entry.get()
    gender=gender_combo.get()
    dob=dob_entry.get()
    
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""UPDATE customers SET name=%s,phone=%s,email=%s,address=%s,gender=%s,date_of_birth=%s WHERE id=%s"""
        values=(name,phone,email,address,gender,dob,customer_id)
        cursor.execute(query,values)
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo("Success","Customer updated successfully")
        load_customers()
        clear_fields()
    
def delete_customer():
    selected=customer_table.selection()
    if not selected:
        messagebox.showwarning("Warning","Please select a customer")
        return
    item=customer_table.item(selected[0])
    customer_id=item["values"][0]
    confirm=messagebox.askyesno("Confirm Delete","Are you sure want to delete this customer?")
    if not confirm:
        return
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""DELETE FROM customers WHERE id=%s"""
        cursor.execute(query,(customer_id,))
        connection.commit()
        cursor.close()
        connection.close()
        messagebox.showinfo(
            "success",
            "customer deleted successfully"
            )
        load_customers()
        clear_fields()
        
    

def open_customers():
    window=tk.Toplevel()
    window.title("Customer Management")
    window.geometry("600x550")
    #window.resizable(False,False)
    title=ttk.Label(window,text="CUSTOMER MANAGEMENT",font=("Arial",20,'bold'))
    title.pack(pady=20)
    form_frame=ttk.Frame(window)
    form_frame.pack(padx=40)
    ttk.Label(form_frame,text="Name").grid(row=0,column=0,sticky="w",padx=8)
    global name_entry
    name_entry=ttk.Entry(form_frame,width=35)
    name_entry.grid(row=0,column=1,pady=8)
    ttk.Label(form_frame,text="Phone").grid(row=1,column=0,sticky="w",pady=8)
    global phone_entry
    phone_entry=ttk.Entry(form_frame,width=35)
    phone_entry.grid(row=1,column=1,pady=8)
    ttk.Label(form_frame,text="Email").grid(row=2,column=0,sticky="w",pady=8)
    global email_entry
    email_entry=ttk.Entry(form_frame,width=35)
    email_entry.grid(row=2,column=1,pady=8)
    ttk.Label(form_frame,text="Address").grid(row=3,column=0,sticky="w",pady=8)
    global address_entry
    address_entry=ttk.Entry(form_frame,width=35)
    address_entry.grid(row=3,column=1,pady=8)
    ttk.Label(form_frame,text="Gender").grid(row=4,column=0,sticky="w",pady=8)
    global gender_combo
    gender_combo=ttk.Combobox(form_frame,values=["Male","Female","Others"],width=32,state='readonly')
    gender_combo.grid(row=4,column=1,pady=8)
    ttk.Label(form_frame,text="Date of Birth").grid(row=5,column=0,sticky="w",pady=8)
    global dob_entry
    dob_entry=ttk.Entry(form_frame,width=35)
    dob_entry.grid(row=5,column=1,pady=8)
    button_frame=ttk.Frame(window)
    button_frame.pack(pady=25)
    ttk.Button(button_frame,text="SAVE CUSTOMER",command=save_customer).grid(row=0,column=0,padx=10)
    ttk.Button(button_frame,text="CLEAR",command=clear_fields).grid(row=0,column=1,padx=10)
    ttk.Button(button_frame,text="UPDATE CUSTOMER",command=update_customer).grid(row=0,column=2,padx=10)
    ttk.Button(button_frame,text="DELETE CUSTOMER",command=delete_customer).grid(row=0,column=3,padx=10)
    
    name_entry.focus()
    search_frame=ttk.Frame(window)
    search_frame.pack(pady=10)
    ttk.Label(search_frame,text='search').pack(side='left',pady=5)
    global search_entry
    search_entry=ttk.Entry(search_frame,width=35)
    search_entry.pack(side="left",pady=5)
    ttk.Button(search_frame,text='SEARCH',command=search_customer).pack(side="left",padx=5)
    ttk.Button(search_frame,text='SHOW ALL',command=load_customers).pack(side="left",padx=5)
    table_frame=ttk.Frame(window)
    table_frame.pack(fill='both',expand=True,padx=20,pady=10)
    columns=("ID","Name","Phone","Email","Address","Gender","DOB")
    global customer_table
    customer_table=ttk.Treeview(table_frame,columns=columns,show="headings",height=12)
    for column in columns:
        customer_table.heading(column,text=column)
        customer_table.column(column,width=130)
    customer_table.bind("<ButtonRelease-1>",select_customer)
    customer_table.pack(side="left",fill="both",expand=True)
    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=customer_table.yview)
    scrollbar.pack(side="right",fill="y")
    customer_table.configure(yscrollcommand=scrollbar.set)
    load_customers()
    name_entry.focus()
    
    
    