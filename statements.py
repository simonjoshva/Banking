import tkinter as tk
from tkinter import ttk,messagebox
from database import create_connection
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import(
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
    )
from tkinter import filedialog


def load_accounts():
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select id,account_number from accounts where status='Active' order by account_number"""
        cursor.execute(query)
        accounts=cursor.fetchall()
        account_combo["values"]=[f"{account[0]}-{account[1]}" for account in accounts]
        cursor.close()
        connection.close()
        
def load_statement():
    for item in statement_table.get_children():
        statement_table.delete(item)
    account=account_combo.get()
    if account =="":
        return
    account_id=account.split("-")[0]
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query="""select id,transaction_type,amount,balance_after,description,transaction_date from transactions where account_id=%s order by id desc"""
        cursor.execute(query,(account_id,))
        transactions=cursor.fetchall()
        for transaction in transactions:
            statement_table.insert("",tk.END,values=transaction)
        cursor.close()
        connection.close()
        
def generate_pdf():
    account=account_combo.get()
    if account=="":
        messagebox.showwarning("Warning","Please select an account")
        return
    account_id=account.split("-")[0]
    account_number=account.split("-")[1]
    connection=create_connection()
    if not connection:
        messagebox.showerror("Error","Database connection failed")
        return
    cursor=connection.cursor()
    query="""select transaction_type,amount,balance_after,description,transaction_date from transactions where account_id=%s order by transaction_date ASC"""
    cursor.execute(query,(account_id,))
    transactions=cursor.fetchall()
    cursor.close()
    connection.close()
    connection=create_connection()
    cursor=connection.cursor()
    query="""select name from customers"""
    cursor.execute(query)
    customer_name=cursor.fetchone()
    print(customer_name[0])
    connection.close()
    
    if not transactions:
        messagebox.showwarning("Warning","No transaction found for this account")
        return
    file_path=filedialog.asksaveasfilename(defaultextension=".pdf",filetypes=[("PDF Files","*pdf")],
    initialfile=f"Statement_{account_number}.pdf")
    if not file_path:
        return
    document=SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=30,
        leftMargin=30,
        topMargin=30,
        bottonMargin=30)
    styles=getSampleStyleSheet()
    elements=[]
    title=Paragraph("BANK ACCOUNT STATEMENT",styles['Title'])
    elements.append(title)
    elements.append(Spacer(1,15))
    customer_info=Paragraph(f"<b>Customer Name</b>{customer_name[0]}",styles["Normal"])
    account_info=Paragraph(f"<b>Account Number</b>{account_number}",styles["Normal"])
    elements.append(customer_info)
    elements.append(account_info)
    elements.append(Spacer(1,15))
    data=[["Type","Amount","Balance","Description","Date"]]
    for transaction in transactions:
        transaction_type=transaction[0]
        amount=transaction[1]
        balance=transaction[2]
        description=transaction[3]
        transaction_date=transaction[4]
        data.append([transaction_type,f"Rs{float(amount):,.2f}",f"Rs{float(balance):,.2f}",description or"",str(transaction_date)])
    table=Table(data,colWidths=[70,80,80,120,110])
    table.setStyle(
        TableStyle([
            ("BACKROUND",(0,0),(-1,0),colors.lightgrey),
            ("TEXTCOLOR",(0,0),(-1,0),colors.black),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"),
            ("GRID",(0,0),(-1,-1),0.5,colors.black),
            ("ALIGN",(1,1),(2,-1),"RIGHT"),
            ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("FONTSIZE",(0,0),(-1,-1),8,),
            ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("TOPPADDING",(0,0),(-1,-1),6),
            ]))
    elements.append(table)
    document.build(elements)
    messagebox.showinfo("Success","Account Statement PDF Generated successfullY")
    
        
        
    
    
    
        
def open_statement():
    window=tk.Toplevel()
    window.title('Account Statements')
    window.geometry('1000x600')
    title=ttk.Label(window,text='ACCOUNT STATEMENT',font=('Arial',20,'bold'))
    title.pack(pady=20)
    select_frame=ttk.Frame(window)
    select_frame.pack(pady=10)
    ttk.Label(select_frame,text='Select Account').pack(side="left",padx=10)
    global account_combo
    account_combo=ttk.Combobox(select_frame,width=30,state="readonly")
    account_combo.pack(side="left",padx=10)
    ttk.Button(select_frame,text='VIEW STATEMENT',command=load_statement).pack(side="left",padx=10)
    ttk.Button(select_frame,text='Generate PDF',command=generate_pdf).pack(side="left",padx=10)
    table_frame=ttk.Frame(window)
    table_frame.pack(fill="both",expand=True,padx=20,pady=20)
    columns=("ID","Type","Amount","Balance After","Description","Date")
    global statement_table
    statement_table=ttk.Treeview(table_frame,columns=columns,show="headings",height=18)
    for column in columns:
        statement_table.heading(column,text=column)
        statement_table.column(column,width=150)
    statement_table.pack(side="left",fill="both",expand=True)
    scrollbar=ttk.Scrollbar(table_frame,orient="vertical",command=statement_table.yview)
    scrollbar.pack(side="right",fill="y")
    statement_table.configure(yscrollcommand=scrollbar.set)
    load_accounts()
    
    
    