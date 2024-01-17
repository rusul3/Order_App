import sqlite3


'''
this class is to be used with the profile tab in later updates
'''
class Account:
    def __init__(self, username, password, postcode, mobile):
        self.user = username
        self.password = password
        self.postcode = postcode
        self.mobile = mobile
    
    def create_user(self):
        conn = sqlite3.connect("BeansAndBrewDatabase.db")
        cur = conn.cursor()
        cur.execute("INSERT INTO account (username, password, postcode, mobile) VALUES (?, ?, ?, ?)",
                    (self.username, self.password, self.postcode, self.mobile))
        conn.commit()
        conn.close()
    
    def edit_information(self, new_password, new_postcode, new_mobile):
        conn = sqlite3.connect("BeansAndBrewDatabase.db")
        cur = conn.cursor()
        cur.execute("UPDATE account SET password=?, postcode=?, mobile=? WHERE username=?", (new_password, new_postcode, new_mobile, self.username))
        conn.commit()
        conn.close()
    
    def delete_account(self):
        conn = sqlite3.connect("BeansAndBrewDatabase.db")
        cur = conn.cursor()
        cur.execute("DELETE FROM account WHERE username=?", (self.username,))
        conn.commit()
        conn.close()
    
    def veiw_orders(self):
        conn = sqlite3.connect("BeansAndBrewDatabase.db")
        cur = conn.cursor()
        cur.execute("SELECT * FROM orders WHERE username=?", (self.username,))
        orders = cur.fetchall()
        conn.close()
        return orders

    