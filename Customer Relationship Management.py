import mysql.connector
from tkinter import *
from tkinter import messagebox, ttk
import csv

# MySQL Database Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="piyush",
    database="crm_tool"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS crm_tool")
cursor.execute("USE crm_tool")
cursor.execute("CREATE TABLE IF NOT EXISTS Users (user_id INT AUTO_INCREMENT PRIMARY KEY,username VARCHAR(50) UNIQUE,password VARCHAR(255))")
cursor.execute("CREATE TABLE IF NOT EXISTS Customers (customer_id INT AUTO_INCREMENT PRIMARY KEY,name VARCHAR(100),email VARCHAR(100),phone VARCHAR(15),address TEXT)")
# --- Helper Functions ---

# Function to add a new user
def add_user(username, password):
    try:
        cursor.execute("INSERT INTO Users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        messagebox.showinfo("Success", f"User '{username}' created successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username already exists.")

# Function to add a new customer
def add_customer(name, email, phone, address):
    cursor.execute("INSERT INTO Customers (name, email, phone, address) VALUES (%s, %s, %s, %s)", 
                   (name, email, phone, address))
    conn.commit()
    messagebox.showinfo("Success", "Customer added successfully!")

# Function to delete a customer by ID
def delete_customer(customer_id):
    cursor.execute("DELETE FROM Customers WHERE customer_id = %s", (customer_id,))
    conn.commit()
    messagebox.showinfo("Success", "Customer deleted successfully!")

# Function to search for a customer by name
def search_customer(name):
    cursor.execute("SELECT * FROM Customers WHERE name LIKE %s", (f"%{name}%",))
    rows = cursor.fetchall()
    show_customers(rows)

# Function to show all customers in the table
def show_all_customers():
    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()
    show_customers(rows)

# Function to display customer data in the table
def show_customers(rows):
    for row in customer_table.get_children():
        customer_table.delete(row)
    for row in rows:
        customer_table.insert("", "end", values=row)

# Function to export customers to CSV
def export_customers():
    cursor.execute("SELECT * FROM Customers")
    rows = cursor.fetchall()

    with open('customer_data.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Customer ID", "Name", "Email", "Phone", "Address"])
        writer.writerows(rows)

    messagebox.showinfo("Success", "Customer data exported to 'customer_data.csv'.")

# --- GUI Components ---

# Function to open the main menu after login
def open_main_menu():
    main_menu = Tk()
    main_menu.title("CRM Tool - Main Menu")
    main_menu.geometry("990x900")

    # Add Customer Section
    Label(main_menu, text="Add Customer", font=("Arial", 14)).pack(pady=5)

    Label(main_menu, text="Name").pack()
    name_entry = Entry(main_menu)
    name_entry.pack()

    Label(main_menu, text="Email").pack()
    email_entry = Entry(main_menu)
    email_entry.pack()

    Label(main_menu, text="Phone").pack()
    phone_entry = Entry(main_menu)
    phone_entry.pack()

    Label(main_menu, text="Address").pack()
    address_entry = Entry(main_menu)
    address_entry.pack()

    Button(main_menu, text="Add Customer", command=lambda: add_customer(
        name_entry.get(), email_entry.get(), phone_entry.get(), address_entry.get())).pack(pady=10)

    # Customer List Section
    Label(main_menu, text="Customer List", font=("Arial", 14)).pack(pady=10)

    # Search Customer
    Label(main_menu, text="Search by Name").pack()
    search_entry = Entry(main_menu)
    search_entry.pack()

    Button(main_menu, text="Search", command=lambda: search_customer(search_entry.get())).pack(pady=5)
    Button(main_menu, text="Show All Customers", command=show_all_customers).pack(pady=5)

    # Export Customer Data
    Button(main_menu, text="Export to CSV", command=export_customers).pack(pady=5)
    
    # Customer Table
    global customer_table
    customer_table = ttk.Treeview(main_menu, columns=("ID", "Name", "Email", "Phone", "Address"), show="headings")
    customer_table.heading("ID", text="ID")
    customer_table.heading("Name", text="Name")
    customer_table.heading("Email", text="Email")
    customer_table.heading("Phone", text="Phone")
    customer_table.heading("Address", text="Address")
    customer_table.pack(fill=BOTH, expand=YES)

    # Delete Customer
    Label(main_menu, text="Delete Customer by ID").pack(pady=5)
    delete_entry = Entry(main_menu)
    delete_entry.pack()
    Button(main_menu, text="Delete Customer", command=lambda: delete_customer(delete_entry.get())).pack(pady=10)

# Function to handle login
def login():
    username = username_entry.get()
    password = password_entry.get()

    cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
    result = cursor.fetchone()

    if result:
        open_main_menu()
        login_window.destroy()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# Function to handle signup
def signup():
    signup_window = Toplevel()
    signup_window.title("Signup")

    Label(signup_window, text="Username").pack()
    signup_username_entry = Entry(signup_window)
    signup_username_entry.pack()

    Label(signup_window, text="Password").pack()
    signup_password_entry = Entry(signup_window, show="*")
    signup_password_entry.pack()

    Button(signup_window, text="Signup", command=lambda: add_user(
        signup_username_entry.get(), signup_password_entry.get())).pack()

# --- Login Window ---

login_window = Tk()
login_window.title("Login")
login_window.geometry("300x200")

Label(login_window, text="Username").pack()
username_entry = Entry(login_window)
username_entry.pack()

Label(login_window, text="Password").pack()
password_entry = Entry(login_window, show="*")
password_entry.pack()

Button(login_window, text="Login", command=login).pack()
Button(login_window, text="Signup", command=signup).pack()
Button(login_window, text="Exit", command=login_window.destroy).pack()

# Start the GUI event loop
login_window.mainloop()

# Close the database connection
cursor.close()
conn.close()
