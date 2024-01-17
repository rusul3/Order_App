import sqlite3

def new_location(location):
    conn = sqlite3.connect("BeansAndBrewDatabase.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO storeLocations (location) VALUES (?)", (location,))
    conn.commit()
    conn.close()

def new_product(productName, price):
    conn = sqlite3.connect("BeansAndBrewDatabase.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO products (productName, price) VALUES (?, ?)", (productName, price))
    conn.commit()
    conn.close()

locationArray = [
    "Brothers Osborne", 
    "Micheal Ashton", 
    "Chris Stapelton"
]

coffee_types = [
    "Espresso",
    "Americano",
    "Latte",
    "Cappuccino",
    "Macchiato",
    "Turkish Coffee"
]

coffee_prices = [
    2.50,
    2.00,
    3.50,
    3.00,
    3.50,
    4.75
]

for loc in locationArray:
    new_location(loc)
    print("Location added:", loc)

for coffee, price in zip(coffee_types, coffee_prices):
    new_product(coffee, price)
    print("Product added:", coffee, "Price:", price)
