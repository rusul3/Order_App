import sqlite3
from tkinter import *
from tkinter.ttk import *
from tkinter import font
from random import randint
from DatabaseFunctions import *
from AccountHandling import *
from PIL import Image, ImageTk

# Create root screen
root = Tk()
root.geometry("390x700")
root.resizable(False, False)

# store users info
_user = ""
_password = ""
_postcode = ""
_mobile = ""
_shopID = ""
_shop = ""
_total = 0
_orderNumber = 0

# 2d array for customers basket
_basketDictionary = {} 

# Colors
background =  "#AD8B7F"
itemColor = "#FFFFFF"
root.config(bg=background) # Change root background

# Font
custom_font = font.Font(family="Centaur", size=8, weight="bold")
header_font = font.Font(family="Sylfaen", size=16)

# setting the styles
mainStyle = Style()
nBarStyle = Style()
itemStyle = Style()

# Configure styles for main frame and navigation bar frame
mainStyle.configure("Main.TFrame", background=background)
nBarStyle.configure("NavBar.TFrame", background=itemColor)
itemStyle.configure("item.TFrame", background=itemColor)


def starter_screen():
    global mainFrame
    global homeButton
    global basketButton
    global profileButton

    # Title bar
    logo = Label(root, text="Beans and Brew",font=custom_font,foreground= itemColor,background=background)
    logo.place(x=180, y=30)

    logo = Label(root, text="Cafe Shop",font=custom_font,foreground= itemColor,background=background)
    logo.place(x=190, y=45)

    # Load image
    image = Image.open("logocupe2.jpg")
    image = image.resize((30, 30))
    photo = ImageTk.PhotoImage(image)
    # Create label with the image
    logo = Label(root, image=photo)
    logo.image = photo
    logo.place(x=200, y=0)

    # Where the myjority of content will fit in
    mainFrame = Frame(root, style="Main.TFrame")
    mainFrame.place(width=390, height=700, x=0, y=50)

    #welcome message
    welcome = Label(mainFrame, text="Welcome to our Coffee and Bakery Shop", font=header_font ,foreground= itemColor, background=background)
    welcome.place(x=1, y=10)

    #welcome photo
    image1 = Image.open("pexels-lisa-fotios-1855214.jpg")
    image1 = image1.resize((385, 300))
    photo = ImageTk.PhotoImage(image1)
    # Create label with the image
    w_photo = Label(mainFrame, image=photo)
    w_photo.image = photo
    w_photo.place(x=0, y=50)

    # Start the app
    openButton = Button(mainFrame, text="Sign In", command=login_screen)
    openButton.place(width=350, height=50, x=18, y=380)

    openButton = Button(mainFrame, text="Sign Up", command=register)
    openButton.place(width=350, height=50, x=18, y=450) 

    # Nav bar
    #navFrame = Frame(root, style="NavBar.TFrame")
    #navFrame.place(width=300, height=50, x=25, y=700)

    # Nav buttons
    #homeButton = Button(navFrame, text="Home", state="disabled", command=home)
    #basketButton = Button(navFrame, text="Basket", state="disabled", command=basket)
    #profileButton = Button(navFrame, text="Profile", state="disabled", command=profile)

    #homeButton.place(width=80, height=30, x=20, y=10)
    #basketButton.place(width=80, height=30, x=110, y=10)
    #profileButton.place(width=80, height=30, x=200, y=10)

    # Run the Tkinter event loop
    root.mainloop() 


# removes all the widgets from the screen/ frame
def remove_all_widgets(parent):
    for widget in parent.winfo_children():
        widget.destroy()


# put at the end of any function that is a gui if want
def add_color_to_all_widgets(parent):
    for widget in parent.winfo_children():
        if isinstance(widget, Label):
            widget.config(background=itemColor)


def reset_variables():
    global _basketDictionary, _shopID, _shop, _total, _orderNumber, basketCurrentPage, storeCurrentPage, menuCurrentPage, checkCurrentPage, orderCurrentPage
    _basketDictionary = {}
    _shopID = ""
    _shop = ""
    _total = 0
    _orderNumber = 0
    basketCurrentPage = 1
    storeCurrentPage = 1
    menuCurrentPage = 1
    checkCurrentPage = 1
    orderCurrentPage = 1


# Verify functions
def login_verify(user, pword):
    userInfo = get_user_info(user, pword)
    if userInfo:
        global _user
        global _password
        global _postcode
        global _mobile
        _user = userInfo[0]
        _password = userInfo[1]
        _postcode = userInfo[2]
        _mobile = userInfo[3]
        #homeButton.config(state="normal")
        #basketButton.config(state="normal")
        #profileButton.config(state="normal")
        store_locator()
    else:
        userIncorect.config(text="Username or Password Incorect")


def register_verify(user, pword, pcode, mobi):
    if not check_username_exists(user):
        create_new_user(user, pword, pcode, mobi)
        global _user
        global _password
        global _postcode
        global _mobile
        _user = user
        _password = pword
        _postcode = pcode
        _mobile = mobi
        #homeButton.config(state="normal")
        #basketButton.config(state="normal")
        #profileButton.config(state="normal")
        store_locator()
    else:
        accountExists.config(text="Account already exists")

# Login screen
def login_screen():
    global userIncorect
    remove_all_widgets(mainFrame)

    # Labels
    logLabel = Label(mainFrame, text="Sign In", font=header_font ,foreground= itemColor, background=background)
    userLabel = Label(mainFrame, text="Enter username: ", foreground= itemColor, background=background)
    passwordLabel = Label(mainFrame, text="Enter password: ", foreground= itemColor, background=background)
    userIncorect = Label(mainFrame, text="", background=background)

    # Entry bars
    user = Entry(mainFrame)
    password = Entry(mainFrame, show="*")

    # Buttons
    loginButton = Button(mainFrame, text="Login", command = lambda: login_verify(user.get(), password.get()))
    #signupButton = Button(mainFrame, text="Sign up", command=register)

    # Layout
    logLabel.place(width=80, x=180, y=10)

    userLabel.place(width=150, x=120, y=75)
    user.place(width=200, x=120, y=100)
    passwordLabel.place(width=150, x=120, y=150)
    password.place(width=200, x=120, y=175)

    loginButton.place(width=80, x=170, y=240)
    #signupButton.place(width=80, x=160, y=240)

    userIncorect.place(width=180, x=60, y=280)


# Sign up screen
def register():
    global accountExists
    remove_all_widgets(mainFrame)

    # Labels
    regLabel = Label(mainFrame, text="Sign up", font=header_font, foreground= itemColor, background=background)
    userLabel = Label(mainFrame, text="Enter username: ",foreground= itemColor, background=background)
    passwordLabel = Label(mainFrame, text="Enter password: ", foreground= itemColor, background=background)
    postcodeLabel = Label(mainFrame, text="Enter postcode: ", foreground= itemColor, background=background)
    mobileLabel = Label(mainFrame, text="Enter mobile: ", foreground= itemColor, background=background)
    accountExists = Label(mainFrame, background=background)

    # Entry bars
    user = Entry(mainFrame)
    password = Entry(mainFrame, show="*")
    postcode = Entry(mainFrame)
    mobile = Entry(mainFrame)

    # Buttons
    signupButton = Button(mainFrame, text="Sign up", command= lambda: register_verify(user.get(), password.get(), postcode.get(), mobile.get()))
    #loginButton = Button(mainFrame, text="Login", command=login_screen)

    # Layout
    regLabel.place(width=100, x=180, y=10)

    userLabel.place(width=150, x=120, y=75)
    user.place(width=200, x=120, y=100)

    passwordLabel.place(width=150, x=120, y=140)
    password.place(width=200, x=120, y=165)

    postcodeLabel.place(width=150, x=120, y=205)
    postcode.place(width=200, x=120, y=230)

    mobileLabel.place(width=150, x=120, y=270)
    mobile.place(width=200, x=120, y=295)

    #loginButton.place(width=80, x=160, y=340)
    signupButton.place(width=80, x=180, y=340)

    accountExists.place(width=124, x=88, y=370)


storeCurrentPage = 1
def store_next_page(storeLastPage):
    global storeCurrentPage
    if storeCurrentPage != storeLastPage:
        storeCurrentPage += 1
        home()

def store_previous_page():
    global storeCurrentPage
    if storeCurrentPage != 1:
        storeCurrentPage -= 1
        home()

def store_located(id, shop):
    global _shop
    global _shopID
    _shop = shop
    _shopID = id
    home()

# Store locator screen
def store_locator():
    remove_all_widgets(mainFrame)
    #locations = get_all_store_locations() # gets a list of all the store locations
    #positiony = 0 # y position for content
    #pageCounter = 1 # used for labeling each page for the pages dictionary. Then used as a last page monitor
    #counter = 0
    #pageContent = []
    #pages = {}

    #for id, location in locations:
     #   counter += 1
      #  if counter %6 == 0:
       #     pages[pageCounter] = pageContent
        #    pageContent.clear()
         #   pageCounter += 1
        #else:
         #   pageContent.append([id, location])
    #pages[pageCounter] = pageContent
    # print(pages)
    
    # Title of the page
    regLabel = Label(mainFrame, text="Please choose from our local restaurants ",foreground= itemColor, font=header_font, background=background)
    regLabel.place(width=390, x=0, y=10)

    # location of restaurants
    Button1 = Button(mainFrame, text="Harrogate", command=service_H)
    Button1.place(width=350, height=50, x=18, y=50)

    Button2 = Button(mainFrame, text="Leeds", command=service_L)
    Button2.place(width=350, height=50, x=18, y=150)
    
    Button3 = Button(mainFrame, text="Knaresborough Castle", command=service_K)
    Button3.place(width=350, height=50, x=18, y=250) 

    # store frame
    storeFrame = Frame(mainFrame, style="Main.TFrame")
    storeFrame.place(width=390, height=650, x=0, y=300)

    positiony = 0

    counter = 0
    # Add for loop to create the content for products
    #for id, location in pages[storeCurrentPage]:
        #print(location)
        
     #   locationFrame = Frame(storeFrame)
      #  locationFrame.place(width=390, height=100, x=0, y=positiony)
       # locationFrame.config(style="Main.TFrame")
        #item = Label(locationFrame, text=location, background=background)
        #item.place(width=150, height=100, x=20, y=15)

        #counter += 1
        #positiony += 110

        #selectButton = Button(locationFrame, text="Select", command=lambda id=id, location=location: store_located(id, location))

        #selectButton = Button(locationFrame, text="Select", command=lambda: store_located(id, location))
        #selectButton.place(width=70, height=30, y=10, x=10)
   
    
# the service that restaurants offer
def service_H():
    remove_all_widgets(mainFrame)
    
    # Title of the page
    regLabel = Label(mainFrame, text="Harrogate",foreground= itemColor, font=header_font, background=background)
    regLabel.place(width=390, x=150, y=10)

    # location of restaurants
    Button1 = Button(mainFrame, text="pre-order a coffee for collection", command=home_H)
    Button1.place(width=350, height=50, x=18, y=50)

    Button2 = Button(mainFrame, text="Pre-order baked goods for collection", command=register)
    Button2.place(width=350, height=50, x=18, y=150)
    
    Button3 = Button(mainFrame, text="pre-book (online) baking lessons", command=register)
    Button3.place(width=350, height=50, x=18, y=250) 

    Button4 = Button(mainFrame, text="Book a space", command=register)
    Button4.place(width=350, height=50, x=18, y=350) 

    Button5 = Button(mainFrame, text="Customisable baked goods hampers", command=register)
    Button5.place(width=350, height=50, x=18, y=450)

    
    global storeBackButton
    #global storeNextButton
    pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    storeBackButton = Button(pageControlFrame, text="<--", command=store_previous_page)

    pageControlFrame.place(width=300, height=50, x=0, y=550)
    storeBackButton.place(width=70, height=30, y=10, x=18)
    

def store_previous_page():
    global storeCurrentPage
    store_locator() 


def service_L():
    remove_all_widgets(mainFrame)
    pageCounter = 1 # used for labeling each page for the pages dictionary. Then used as a last page monitor
    regLabel = Label(mainFrame, text="Leeds",foreground= itemColor, font=header_font, background=background)
    regLabel.place(width=390, x=150, y=10)

    # location of restaurants
    Button1 = Button(mainFrame, text="pre-order a coffee for collection", command=home_L)
    Button1.place(width=350, height=50, x=18, y=50)

    Button2 = Button(mainFrame, text="Pre-order baked goods for collection", command=register)
    Button2.place(width=350, height=50, x=18, y=150)
    
    Button3 = Button(mainFrame, text="pre-book (online) baking lessons", command=register)
    Button3.place(width=350, height=50, x=18, y=250) 

    Button4 = Button(mainFrame, text="Book a space", command=register)
    Button4.place(width=350, height=50, x=18, y=350) 

    Button5 = Button(mainFrame, text="Customisable baked goods hampers", command=register)
    Button5.place(width=350, height=50, x=18, y=450)
    
    
    global storeBackButton
    global storeNextButton
    pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    storeBackButton = Button(pageControlFrame, text="<--", command=store_previous_page)

    pageControlFrame.place(width=300, height=50, x=0, y=550)
    storeBackButton.place(width=70, height=30, y=10, x=18)
    

def store_previous_page():
    global storeCurrentPage
    store_locator() 

def service_K():
    remove_all_widgets(mainFrame)
    pageCounter = 1 # used for labeling each page for the pages dictionary. Then used as a last page monitor
    regLabel = Label(mainFrame, text="Knaresborough Castle",foreground= itemColor, font=header_font, background=background)
    regLabel.place(width=390, x=150, y=10)

    # location of restaurants
    Button1 = Button(mainFrame, text="pre-order a coffee for collection", command=home_K)
    Button1.place(width=350, height=50, x=18, y=50)

    Button2 = Button(mainFrame, text="Pre-order baked goods for collection", command=register)
    Button2.place(width=350, height=50, x=18, y=150)
    
    Button3 = Button(mainFrame, text="pre-book (online) baking lessons", command=register)
    Button3.place(width=350, height=50, x=18, y=250) 

    Button4 = Button(mainFrame, text="Book a space", command=register)
    Button4.place(width=350, height=50, x=18, y=350) 

    Button5 = Button(mainFrame, text="Customisable baked goods hampers", command=register)
    Button5.place(width=350, height=50, x=18, y=450)
    
    
    global storeBackButton
    #global storeNextButton
    pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    storeBackButton = Button(pageControlFrame, text="<--", command=store_previous_page)

    pageControlFrame.place(width=300, height=50, x=0, y=550)
    storeBackButton.place(width=70, height=30, y=10, x=18)
    

def store_previous_page():
    global storeCurrentPage
    store_locator()  



menuCurrentPage = 1
def menu_next_page(menuLastPage):
    global menuCurrentPage
    if menuCurrentPage != menuLastPage:
        menuCurrentPage += 1
        home()

def menu_previous_page():
    global menuCurrentPage
    if menuCurrentPage != 1:
        menuCurrentPage -= 1
        home()

def item_selected(item, price):
    if item in _basketDictionary:
        coffee = _basketDictionary[item]
        newQuantity = coffee[1] + 1
        newPrice = price * newQuantity
        _basketDictionary[item] = [newPrice, newQuantity]
        # print(_basketDictionary)
    else:
        _basketDictionary[item] = [price, 1]
    # print(_basketDictionary)
# Home screen
def home_H():
    remove_all_widgets(mainFrame)
    # print(_user, _password, _postcode, _mobile, _shop)


    #photo
    image1 = Image.open("pexels-designecologist-3458448.jpg")
    image1 = image1.rotate(90, expand=True)
    image1 = image1.resize((385, 100))
    photo = ImageTk.PhotoImage(image1)
    # Create label with the image
    C_photo = Label(mainFrame, image=photo)
    C_photo.image = photo
    C_photo.place(x=0, y=10)
    # Title of the page
    #regLabel = Label(mainFrame, text="Menu", font=header_font, background=background)
    #regLabel.place(width=100, x=110, y=10)
        
    menuFrame = Frame(mainFrame, style="Main.TFrame")
    menuFrame.place(width=390, height=350, x=0, y=150)

    coffee_data = get_all_products()

    coffee_counts = {}

    counter = 0
    #pageCounter = 1
    tempPage = []
    #pages = {}
    position = 0

    for num, coffee, price in coffee_data:
        # print(coffee, price)
        coffee_counts[coffee] = 0
        tempPage.append([coffee, price])
        counter += 1
        
        #if counter % 6 == 0:
         #   pages[pageCounter] = list(tempPage)
          #  pageCounter += 1
           # tempPage.clear()
    #pages[pageCounter] = list(tempPage)
    pages = list(tempPage)

    #menuLastPage = list(pages.keys())[-1]
    # print(menuLastPage)
    # print(pages)

    #counter = 0
       # Factory function to create a callback function with correct bindings
    def make_update_count(coffee, price):
        def update_count(coffee, change, label):
            coffee_counts[coffee] += change
            label.config(text=str(coffee_counts[coffee]))
            # item_selected(coffee, price, coffee_counts[coffee])
            item_selected(coffee, price * coffee_counts[coffee])
        return update_count

    for coffee, price in pages:
        # print(coffee, price)
        coffeeFrame = Frame(menuFrame)
        coffeeFrame.place(width=390, height=50, x=0, y=position)
        coffeeFrame.config(style="Main.TFrame")
        coffeeName = Label(coffeeFrame, text=coffee, background=background)
        coffeePrice = Label(coffeeFrame, text=f"£{price}", background=background)
        #selectButton = Button(coffeeFrame, text="Select", command=lambda coffee=coffee, price=price: item_selected(coffee, price))


        # Counter for each coffee type
        #coffee_count = [0]

        # Function to update the coffee count
        #def update_count(change, label, coffee):
         #  coffee_counts[coffee] += change
          # label.config(text=str(coffee_counts[0]))
        # Call the item_selected function if needed
        # item_selected(coffee, price, coffee_count[0])

        coffee_counts[coffee] = 0

        # Generate update_count function for this coffee
        #update_count = make_update_count(coffee)
        update_count = make_update_count(coffee, price)

        # Labels and buttons for coffee count
        count_label = Label(coffeeFrame, text="0", background=background)
        increase_button = Button(coffeeFrame, text="+", command=lambda coffee=coffee, label=count_label: update_count(coffee, 1, label))
        decrease_button = Button(coffeeFrame, text="-", command=lambda coffee=coffee, label=count_label: update_count(coffee, -1, label))

        # Positioning the widgets inside the coffee frame
        #coffeeName.pack(side="right")
        #coffeePrice.pack(side="right")
        #increase_button.pack(side="right")
        #count_label.pack(side="right")
        #decrease_button.pack(side="right")
        coffeeName.place(width=150, height=30, y=10, x=10)
        coffeePrice.place(width=40, height=30, y=10, x=170)
        #selectButton.place(width=70, height=30, y=10, x=220)
        increase_button.place(y=10, x=300)
        count_label.place(y=10, x=285)
        decrease_button.place(y=10, x=200)

        
        #counter +=1
        position += 50

        #coffeeName.place(width=150, height=30, y=10, x=10)
        #coffeePrice.place(width=40, height=30, y=10, x=170)
        #selectButton.place(width=70, height=30, y=10, x=220)
        #increase_button.place(y=10, x=300)
        #count_label.place(y=10, x=285)
        #decrease_button.place(y=10, x=200)
    global storeBackButton
    #global storeNextButton
    pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    storeBackButton = Button(pageControlFrame, text="<--", command=previous_page_H)
    BasketButton = Button(mainFrame, text="Basket", command=basket)

    pageControlFrame.place(width=300, height=50, x=0, y=550)
    storeBackButton.place(width=70, height=30, y=10, x=18)
    BasketButton.place(width=350 ,heigh=50, x=18, y=500)

def previous_page_H():
   global storeCurrentPage
   service_H() 


#COFFEE ORDER FRME Leeds
def home_L():
    remove_all_widgets(mainFrame)

    #photo
    image1 = Image.open("pexels-designecologist-3458448.jpg")
    image1 = image1.rotate(90, expand=True)
    image1 = image1.resize((385, 100))
    photo = ImageTk.PhotoImage(image1)
    # Create label with the image
    C_photo = Label(mainFrame, image=photo)
    C_photo.image = photo
    C_photo.place(x=0, y=10)
        
    menuFrame = Frame(mainFrame, style="Main.TFrame")
    menuFrame.place(width=390, height=350, x=0, y=150)

    coffee_data = get_all_products()

    coffee_counts = {}

    counter = 0
    tempPage = []
    position = 0

    for num, coffee, price in coffee_data:
        coffee_counts[coffee] = 0
        tempPage.append([coffee, price])
        counter += 1

    pages = list(tempPage)
       # Factory function to create a callback function with correct bindings
    def make_update_count(coffee, price):
        def update_count(coffee, change, label):
            coffee_counts[coffee] += change
            label.config(text=str(coffee_counts[coffee]))
            item_selected(coffee, price * coffee_counts[coffee])
        return update_count

    for coffee, price in pages:
        coffeeFrame = Frame(menuFrame)
        coffeeFrame.place(width=390, height=50, x=0, y=position)
        coffeeFrame.config(style="Main.TFrame")
        coffeeName = Label(coffeeFrame, text=coffee, background=background)
        coffeePrice = Label(coffeeFrame, text=f"£{price}", background=background)

        coffee_counts[coffee] = 0

        # Generate update_count function for this coffee
        update_count = make_update_count(coffee, price)

        # Labels and buttons for coffee count
        count_label = Label(coffeeFrame, text="0", background=background)
        increase_button = Button(coffeeFrame, text="+", command=lambda coffee=coffee, label=count_label: update_count(coffee, 1, label))
        decrease_button = Button(coffeeFrame, text="-", command=lambda coffee=coffee, label=count_label: update_count(coffee, -1, label))

        coffeeName.place(width=150, height=30, y=10, x=10)
        coffeePrice.place(width=40, height=30, y=10, x=170)
        increase_button.place(y=10, x=300)
        count_label.place(y=10, x=285)
        decrease_button.place(y=10, x=200)

        position += 50

    global storeBackButton
    pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    storeBackButton = Button(pageControlFrame, text="<--", command=previous_page_L)
    BasketButton = Button(mainFrame, text="Basket", command=basket)

    pageControlFrame.place(width=300, height=50, x=0, y=550)
    storeBackButton.place(width=70, height=30, y=10, x=18)
    BasketButton.place(width=350 ,heigh=50, x=18, y=500)

def previous_page_L():
   global storeCurrentPage
   service_L() 

   
#coffee order from K
def home_K():
    remove_all_widgets(mainFrame)
    #photo
    image1 = Image.open("pexels-designecologist-3458448.jpg")
    image1 = image1.rotate(90, expand=True)
    image1 = image1.resize((385, 100))
    photo = ImageTk.PhotoImage(image1)
    # Create label with the image
    C_photo = Label(mainFrame, image=photo)
    C_photo.image = photo
    C_photo.place(x=0, y=10)
        
    menuFrame = Frame(mainFrame, style="Main.TFrame")
    menuFrame.place(width=390, height=350, x=0, y=150)

    coffee_data = get_all_products()
    coffee_counts = {}
    counter = 0
    tempPage = []
    position = 0

    for num, coffee, price in coffee_data:
        coffee_counts[coffee] = 0
        tempPage.append([coffee, price])
        counter += 1
    pages = list(tempPage)

       # Factory function to create a callback function with correct bindings
    def make_update_count(coffee, price):
        def update_count(coffee, change, label):
            coffee_counts[coffee] += change
            label.config(text=str(coffee_counts[coffee]))
            item_selected(coffee, price * coffee_counts[coffee])
        return update_count

    for coffee, price in pages:
        coffeeFrame = Frame(menuFrame)
        coffeeFrame.place(width=390, height=50, x=0, y=position)
        coffeeFrame.config(style="Main.TFrame")
        coffeeName = Label(coffeeFrame, text=coffee, background=background)
        coffeePrice = Label(coffeeFrame, text=f"£{price}", background=background)

        coffee_counts[coffee] = 0

        # Generate update_count function for this coffee
        update_count = make_update_count(coffee, price)

        # Labels and buttons for coffee count
        count_label = Label(coffeeFrame, text="0", background=background)
        increase_button = Button(coffeeFrame, text="+", command=lambda coffee=coffee, label=count_label: update_count(coffee, 1, label))
        decrease_button = Button(coffeeFrame, text="-", command=lambda coffee=coffee, label=count_label: update_count(coffee, -1, label))

        coffeeName.place(width=150, height=30, y=10, x=10)
        coffeePrice.place(width=40, height=30, y=10, x=170)

        increase_button.place(y=10, x=300)
        count_label.place(y=10, x=285)
        decrease_button.place(y=10, x=200)

        position += 50

    global storeBackButton

    pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    storeBackButton = Button(pageControlFrame, text="<--", command=previous_page_K)
    BasketButton = Button(mainFrame, text="Basket", command=basket)

    pageControlFrame.place(width=300, height=50, x=0, y=550)
    storeBackButton.place(width=70, height=30, y=10, x=18)
    BasketButton.place(width=350 ,heigh=50, x=18, y=500)

def previous_page_K():
   global storeCurrentPage
   service_K() 

# Profile screen
def profile():
    remove_all_widgets(mainFrame)

    # Labels
    regLabel = Label(mainFrame, text="Sign up", font=header_font, background=background)
    userLabel = Label(mainFrame, text="Enter username: ", background=background)
    passwordLabel = Label(mainFrame, text="Enter password: ", background=background)
    postcodeLabel = Label(mainFrame, text="Enter postcode: ", background=background)
    mobileLabel = Label(mainFrame, text="Enter mobile: ", background=background)

    user = Label(mainFrame, text=_user, background=background)
    password = Label(mainFrame, text="*"*len(_password), background=background)
    postcode = Label(mainFrame, text=_postcode, background=background)
    mobile = Label(mainFrame, text=_mobile, background=background)

    # Buttons
    signOutButton = Button(mainFrame, text="SignOut", command=starter_screen)

    # Layout
    regLabel.place(width=100, x=110, y=10)

    userLabel.place(width=150, x=50, y=75)
    user.place(width=200, x=50, y=100)

    passwordLabel.place(width=150, x=50, y=140)
    password.place(width=200, x=50, y=165)

    postcodeLabel.place(width=150, x=50, y=205)
    postcode.place(width=200, x=50, y=230)

    mobileLabel.place(width=150, x=50, y=270)
    mobile.place(width=200, x=50, y=295)

    signOutButton.place(width=60, x=120, y=340)
    

# Basket screen
basketCurrentPage = 1
def basket_next_page(basketLastPage):
    global basketCurrentPage
    if basketCurrentPage != basketLastPage:
        basketCurrentPage += 1
        basket()

def basket_previous_page():
    global basketCurrentPage
    if basketCurrentPage != 1:
        basketCurrentPage -= 1
        basket()

def update_basket(coffee, price, quantity):
    coffeeDict = get_all_products_dictioanary()
    # print(quantity)
    coffeeInfo = coffeeDict[coffee]
    # print(coffeeInfo[1])
    newPrice = float(coffeeInfo[1]) * float(quantity)
    _basketDictionary[coffee] = [newPrice, quantity]
    basket()

def delete_item_from_basket(item):
    _basketDictionary.pop(item)
    basket()

def basket():
    remove_all_widgets(mainFrame)
    global _total
    _total = 0

    # Title of the page
    regLabel = Label(mainFrame, text="Basket", font=header_font, foreground= itemColor,background=background)
    regLabel.place(width=100, x=180, y=10)

    # Basket frame
    basketFrame= Frame(mainFrame, style="Main.TFrame")
    basketFrame.place(width=300, height=300, x=0, y=50)

    # Add forloop to create the content for products
    counter = 0
    pageCounter = 1
    tempPage = []
    pages = {}
    position = 0

    for coffee in _basketDictionary:
        #print(coffee)
        
        tempPage.append([coffee])
        counter += 1
        
        if counter % 5 == 0:
            pages[pageCounter] = list(tempPage)
            pageCounter += 1
            tempPage.clear()
    pages[pageCounter] = list(tempPage)

    basketLastPage = list(pages.keys())[-1]
    #print(basketLastPage)
    #print(pages)

    counter = 0
    for product in pages[basketCurrentPage]:
        coffee = _basketDictionary[product[0]]
        price = coffee[0]
        quantity = coffee[1]
        # print(price, quantity)

        coffeeFrame = Frame(basketFrame)
        coffeeFrame.place(width=300, height=50, x=10, y=position)
        coffeeFrame.config(style="Main.TFrame")
        quantityEntry = Entry(coffeeFrame)
        coffeeName = Label(coffeeFrame, text=product, background=background)
        coffeePrice = Label(coffeeFrame, text=f"£{price}", background=background)
        updateButton = Button(coffeeFrame, text="update", command=lambda entry=quantityEntry, coffee=product[0], price=price: update_basket(coffee, price, entry.get()))
        binButton = Button(coffeeFrame, text="bin", command=lambda coffee=product[0]: delete_item_from_basket(coffee))
        quantityEntry.insert(END, quantity)

        counter +=1
        position += 50
        
        quantityEntry.place(width=20, height=30, y=10, x=5)
        coffeeName.place(width=130, height=30, y=10, x=30)
        coffeePrice.place(width=40, height=30, y=10, x=170)
        updateButton.place(width=70, height=20, y=3, x=220)
        binButton.place(width=70, height=20, y=28, x=220)
        

    #global basketBackButton
    #global basketNextButton
    #pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    #basketBackButton = Button(pageControlFrame, text="<--", command=basket_previous_page)
    #pageLabel = Label(pageControlFrame, text=f"Page {basketCurrentPage}", background=background)
    #basketNextButton = Button(pageControlFrame, text="-->", command=lambda: basket_next_page(basketLastPage))

    #pageControlFrame.place(width=300, height=50, x=0, y=300)
    #basketBackButton.place(width=70, height=30, y=10, x=18)
    #pageLabel.place(width=40, height=30, y=10, x=130)
    #basketNextButton.place(width=70, height=30, y=10, x=212)

    #if basketCurrentPage == 1:
     #   basketBackButton.configure(state="disabled")
    #else:
     #   basketBackButton.configure(state="normal")

    #if basketCurrentPage == basketLastPage:
     #   basketNextButton.configure(state="disabled")
    #else:
     #   basketNextButton.configure(state="normal")

    
    # Checkout button
    checkoutButton = Button(mainFrame, text="checkout", command=checkout_screen)
    checkoutButton.place(width=350, height=50, x=18, y=360)

    if len(_basketDictionary) == 0:
        checkoutButton.config(state="disabled") 
    
    for product in _basketDictionary:
        _total += _basketDictionary[product][0]

    #totalLabel = Label(mainFrame, text=f"Total: £{_total}", font=header_font, background=background, foreground= itemColor)
    #totalLabel.place(width=80, height=30, x=180, y=260)


checkCurrentPage = 1
def check_next_page(checkLastPage):
    global checkCurrentPage
    if checkCurrentPage != checkLastPage:
        checkCurrentPage += 1
        checkout_screen()

def check_previous_page():
    global checkCurrentPage
    if checkCurrentPage != 1:
        checkCurrentPage -= 1
        checkout_screen()

def checkout_screen():
    remove_all_widgets(mainFrame)
    
    # Title of the page
    regLabel = Label(mainFrame, text="Checkout", font=header_font, background=background, foreground= itemColor)
    regLabel.place(width=120, x=180, y=10)

    # Store label
    storeLabel = Label(mainFrame, text=f"Store: {_shop}", background=background, foreground= itemColor)
    storeLabel.place(width=150, x=10, y=50)

    # Item total
    storeLabel = Label(mainFrame, text=f"Total: £{_total}", background=background, foreground= itemColor)
    storeLabel.place(width=120, x=180, y=50)

    # Item veiwer
    itemFrame= Frame(mainFrame, style="Main.TFrame")
    itemFrame.place(width=300, height=120, x=10, y=70)

    counter = 0
    pageCounter = 1
    tempPage = []
    pages = {}
    position = 0

    for coffee in _basketDictionary:
        #print(coffee)
        
        tempPage.append([coffee])
        counter += 1
        
        if counter % 3 == 0:
            pages[pageCounter] = list(tempPage)
            pageCounter += 1
            tempPage.clear()
    pages[pageCounter] = list(tempPage)

    checkLastPage = list(pages.keys())[-1]
    #print(basketLastPage)
    #print(pages)
    
    # Add forloop to create the content for products
    counter = 0
    for product in pages[checkCurrentPage]:
        coffee = _basketDictionary[product[0]]
        price = coffee[0]
        quantity = coffee[1]
        # print(price, quantity)

        coffeeFrame = Frame(itemFrame, style="Main.TFrame")
        coffeeFrame.place(width=300, height=50, x=10, y=position)

        quantityLabel = Label(coffeeFrame, text=quantity, background=background, foreground= itemColor)
        coffeeLabel = Label(coffeeFrame, text=product, background=background, foreground= itemColor)
        priceLabel = Label(coffeeFrame, text=f"£{price}", background=background, foreground= itemColor)

        quantityLabel.place(width=20, height=20, y=5, x=10)
        coffeeLabel.place(width=120, height=20,y=5, x=100)
        priceLabel.place(width=50, height=20, y=5, x=250)

        position +=50

    #global checkBackButton
    #global checkNextButton
    #pageControlFrame = Frame(itemFrame, style="Main.TFrame")
    #checkBackButton = Button(pageControlFrame, text="<--", command=check_previous_page)
    #pageLabel = Label(pageControlFrame, text=f"Page {basketCurrentPage}", background=background)
    #checkNextButton = Button(pageControlFrame, text="-->", command=lambda: check_next_page(checkLastPage))

    #pageControlFrame.place(width=300, height=30, x=0, y=90)
    #checkBackButton.place(width=70, height=20, y=5, x=18)
    #pageLabel.place(width=40, height=20, y=5, x=130)
    #checkNextButton.place(width=70, height=20, y=5, x=212)

    #if checkCurrentPage == 1:
     #   checkBackButton.configure(state="disabled")
    #else:
     #   checkBackButton.configure(state="normal")

    #if checkCurrentPage == checkLastPage:
     #   checkNextButton.configure(state="disabled")
    #else:
     #   checkNextButton.configure(state="normal")

    # Card information
    # Labels 
    nameOnCardLabel = Label(mainFrame, text="Name on card", background=background, foreground= itemColor)
    cardNumberLabel = Label(mainFrame, text="Card number", background=background, foreground= itemColor)
    cvv2Label = Label(mainFrame, text="CVV2", background=background, foreground= itemColor)

    # Entry
    nameOnCard = Entry(mainFrame)
    cardNumber = Entry(mainFrame)
    cvv2 = Entry(mainFrame)
    
    # Layout
    nameOnCardLabel.place(width=150, x=50, y=300)
    nameOnCard.place(width=200, x=50, y=320)
    cardNumberLabel.place(width=150, x=50, y=350)
    cardNumber.place(width=200, x=50, y=400)
    cvv2Label.place(width=150, x=50, y=430)
    cvv2.place(width=200, x=50, y=460)

    # Pay button
    payButton = Button(mainFrame, text="Pay", command=paying_process)
    payButton.place(width=350, height=50, x=18, y=500)


# Checkout screen
def paying_process():
    coffeeList = ""
    priceList = ""
    quantityList = ""

    lastCoffee = list(_basketDictionary.keys())[-1]
    # print(lastCoffee)

    for coffee in _basketDictionary:
        if coffee == lastCoffee:
            coffeeList += coffee
            priceList += str(_basketDictionary[coffee][0])
            quantityList += str(_basketDictionary[coffee][1])
        else:
            coffeeList += f"{coffee}, "
            priceList += f"{_basketDictionary[coffee][0]}, "
            quantityList += f"{_basketDictionary[coffee][1]}, "

    # print(coffeeList)
    # print(priceList)
    # print(quantityList)

    global _orderNumber
    _orderNumber = randint(100000, 999999)

    while check_order_id(_orderNumber):
        _orderNumber = randint(100000, 999999)

    add_order(_orderNumber, _user, _shopID, quantityList, coffeeList, priceList, _total)
    ordered_screen()
    homeButton = Button (mainFrame, text="Order", command=close_w)
    homeButton.place(width=350, height=50, y=500, x=18)


# Order screen
def leave_ordered_screen():
    #homeButton.config(state="normal")
    #basketButton.config(state="normal")
    #profileButton.config(state="normal")
    reset_variables()
    #close_w()

orderCurrentPage = 1
def order_next_page(orderLastPage):
    global orderCurrentPage
    if orderCurrentPage != orderLastPage:
        orderCurrentPage += 1
        ordered_screen()

def order_previous_page():
    global orderCurrentPage
    if orderCurrentPage != 1:
        orderCurrentPage -= 1
        ordered_screen()

def ordered_screen():
    remove_all_widgets(mainFrame)
    #homeButton.config(state="disabled")
    #basketButton.config(state="disabled")
    #profileButton.config(state="disabled")



    # Title of the page
    regLabel = Label(mainFrame, text=f"Order # {_orderNumber}", font=header_font, background=background, foreground= itemColor)
    regLabel.place(width=300, x=150, y=10)

    pages = {}
    orderPageCounter = 1
    itemCounter = 0
    pageContent = []
    yposition = 50
    #print(_basketDictionary)

    for product in _basketDictionary:

        pageContent.append([product])
        itemCounter += 1

        #print(product)
        if itemCounter %5 == 0:
            pages[orderPageCounter] = list(pageContent)
            pageContent = []
            orderPageCounter +=1
        
        pages[orderPageCounter] = list(pageContent)
    
    itemCounter = 0
    for item in pages[orderCurrentPage]:
        coffee = _basketDictionary[product]
        price = coffee[0]
        quantity = coffee[1]
        #print(price, quantity)
        
        coffeeFrame = Frame(mainFrame, style="Main.TFrame")
        coffeeFrame.place(width=300, height=50, x=20, y=yposition)
        yposition += 50

        coffeeLabel = Label(coffeeFrame, text=item, background=background, foreground= itemColor)
        priceLabel = Label(coffeeFrame, text=f"£{price}", background=background, foreground= itemColor)
        quantityLabel = Label(coffeeFrame, text=quantity, background=background, foreground= itemColor)

        quantityLabel.place(width=40, height=30, y=10, x=20)
        coffeeLabel.place(width=120, height=30, y=10, x=100)
        priceLabel.place(width=60, height=30, y=10, x=240)

    #global orderBackButton
    #global orderNextButton
    #pageControlFrame = Frame(mainFrame, style="Main.TFrame")
    #orderBackButton = Button(pageControlFrame, text="<--", command=order_previous_page)
    #pageLabel = Label(pageControlFrame, text=f"Page {orderCurrentPage}", background=background)
    #orderNextButton = Button(pageControlFrame, text="-->", command=lambda: order_next_page(orderPageCounter))

    #pageControlFrame.place(width=350, height=50, x=0, y=350)
    #orderBackButton.place(width=70, height=30, y=10, x=18)
    #pageLabel.place(width=40, height=30, y=10, x=130)
    #orderNextButton.place(width=70, height=30, y=10, x=212)

    #if orderCurrentPage == 1:
     #   orderBackButton.configure(state="disabled")
    #else:
     #   orderBackButton.configure(state="normal")

    #if orderCurrentPage == orderPageCounter:
     #   orderNextButton.configure(state="disabled")
    #else:
     #   orderNextButton.configure(state="normal")

    totalLabel = Label(mainFrame, text="Total:", font=header_font, background=background, foreground= itemColor)
    totalLabel.place(width=100, x=20, y=320)

    #newHomeButton = Button(mainFrame, text="Return Home", command=leave_ordered_screen)
    #newHomeButton.place(width=80, height=30, x=110, y=320)
   
    costLabel = Label(mainFrame, text=f"£{_total}", font=header_font, background=background ,foreground= itemColor)
    costLabel.place(width=100, x=80, y=320)

 


def close_window():
    root.destroy()

def close_w():
  remove_all_widgets(mainFrame)
# Create a label with a message
  message_label = Label(mainFrame, text="THANKS", font=header_font, foreground= itemColor, background=background)
  message_label.place(width=350, height=50, x=30, y=50)

  message_label2 = Label(mainFrame, text="We will send you a message", font=header_font, foreground= itemColor, background=background)
  message_label2.place(width=350, height=50, x=30, y=100)

  message_label1 = Label(mainFrame, text="to collect your order", font=header_font, foreground= itemColor, background=background)
  message_label1.place(width=350, height=50, x=30, y=150)
 

# Create a Close button
  close_button = Button(mainFrame, text="Close", command=close_window)
  close_button.place(width=350, height=50, x=18, y=480)

if __name__ == "__main__":
    starter_screen()