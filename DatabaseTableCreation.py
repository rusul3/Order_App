import sqlite3

'''
Create the database
'''
def create_database():
    conn = sqlite3.connect("BeansAndBrewDatabase.db")
    conn.close()

'''
All the table creation
'''
def create_account_table():
    conn = sqlite3.connect("BeansAndBrewDatabase.db") #Connecting to the table/ creating the database file if it doesnt exist
    cur = conn.cursor() # Creating the cursor to preform  sql code
    cur.execute("CREATE TABLE IF NOT EXISTS account (username VARCHAR(12) PRIMARY KEY, password VARCHAR(30), postcode VARCHAR(8), mobile INTEGER)") # executing the sql code (creating the table and columns)
    conn.commit() # Making the action stay
    conn.close() # closing the table

def create_store_location_table():
    conn = sqlite3.connect("BeansAndBrewDatabase.db") #Connecting to the table/ creating the database file if it doesnt exist
    cur = conn.cursor() # Creating the cursor to preform  sql code
    cur.execute("CREATE TABLE IF NOT EXISTS storeLocations (storeID INTEGER PRIMARY KEY AUTOINCREMENT, location TEXT)") # executing the sql code (creating the table and columns)
    conn.commit() # Making the action stay
    conn.close() # closing the table

def create_product_table():
    conn = sqlite3.connect("BeansAndBrewDatabase.db") #Connecting to the table/ creating the database file if it doesnt exist
    cur = conn.cursor() # Creating the cursor to preform  sql code
    cur.execute("CREATE TABLE IF NOT EXISTS products (productID INTEGER PRIMARY KEY AUTOINCREMENT, productName TEXT, price FLOAT)") # executing the sql code (creating the table and columns)
    conn.commit() # Making the action stay
    conn.close() # closing the table

def create_orders_table():
    conn = sqlite3.connect("BeansAndBrewDatabase.db") #Connecting to the table/ creating the database file if it doesnt exist
    cur = conn.cursor() # Creating the cursor to preform  sql code
    cur.execute("CREATE TABLE IF NOT EXISTS orders (orderID INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(12), storeID INTEGER, quantities VARCHAR(255), items VARCHAR(255), prices VARCHAR(255), total FLOAT, FOREIGN KEY (username) REFERENCES account (username), FOREIGN KEY (storeID) REFERENCES storeLocations (storeID))") # executing the sql code (creating the table and columns)
    conn.commit() # Making the action stay
    conn.close() # closing the table


create_database()
create_account_table()
create_store_location_table()
create_product_table()
create_orders_table()


