from tkinter import *
from tkinter import messagebox,ttk
from database import create_connection
from dashboard import open_dashboard
def login():
    username=eusername.get()
    password=epass.get()
    if username=="" or password=="":
        messagebox.showwarning('warning','please enter username and password')
        return
    connection=create_connection()
    if connection:
        cursor=connection.cursor()
        query=""" SELECT id,user_name,role From users WHERE user_name=%s AND password=%s"""
        cursor.execute(query,(username,password))
        user=cursor.fetchone()
        cursor.close()
        connection.close()
        if user:
            messagebox.showinfo('success','Login Successfull')
            root.withdraw()
            open_dashboard(
                user[1],
                user[2])
            print(user[1],user[2])
        else:
            messagebox.showerror('LOgin Failed','Invalid username or Password')
root=Tk()
style=ttk.Style()
style.theme_use("clam")
style.configure("Title.TLabel")
root.title('Bank Management System-Login')
root.geometry('400x300')
#root.resizable(False,False)
title_label=ttk.Label(root,text='BANK MANAGEMENT SYSTEM',font=('Arial',18,'bold'),style="Title.TLabel")
title_label.pack()
lusername=Label(root,text='Username',font=('Arial',11))
lusername.pack()
eusername=Entry(root,width=30)
eusername.pack(pady=5)
lpassword=Label(root,text='Password',font=('Arial',11))
lpassword.pack(pady=5)
epass=Entry(root,width=30,show="*")
epass.pack(pady=50)
loginbutton=Button(root,text='LOGIN',width=15,command=login)
loginbutton.pack(pady=20)
root.mainloop()
