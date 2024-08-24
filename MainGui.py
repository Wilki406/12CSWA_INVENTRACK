# Programmer: Benjamin D Wilkinson

from customtkinter import *
import customtkinter
import csv
from PIL import Image
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from ttkthemes import ThemedStyle
import os
from CTkToolTip import *
import requests
import json
import re
from cryptography.fernet import Fernet
import cryptography

# Encryption.py
from Encryption import *

# Currency API
rateAPI = 'https://v6.exchangerate-api.com/v6/50c24a91bc6969ae68fe5672/latest/USD'

# Defining variables for default scale and ui colour settings
startingScale = "1"
startingUIC = "Dark"
startingCurrency = "NULL"
startingThing = []

# Defining header files for csv files and define the user data csv file

directory = "Data"
filename = "userdata.csv"
data = os.path.join(directory, filename)
edata = os.path.join(directory, "eUserData.csv")

userheaders = ["ID", "username", "password", "firstName", "lastName", "Scale", "UIC", "Currency"]
invenheaders = ["Name", "Price", "ID", "Category", "Count", "OverTime"]

def createCSV():
    if not os.path.exists(directory):
        os.makedirs(directory)

        # Create the CSV file if it doesn't exist
    if not os.path.exists(data):
        with open(data, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(userheaders)  # write the userheaders for user data

        encrypted_file = encryptCSV(data,"Data/eUserData.csv")
        if encrypted_file is None:
            print("Encryption failed.")

createCSV()

# Load data function for user log in data
def loadData(encrypted_data):
    records, usernameLists, idRank = [], [], []

    decrypted_data = decryptCSV(encrypted_data, "Data/deUserData.csv")
    if decrypted_data is None:
        print("Decryption failed. Unable to load data.")
        return records, usernameLists, idRank

    try:
        with open(decrypted_data, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row

            for row in reader:
                ids, usernames, passwords, firstNames, lastNames, scales, UICs, currencies = row
                idRank.append(int(ids))
                usernameLists.append(usernames)
                records.append([ids, usernames, passwords, firstNames, lastNames, scales, UICs, currencies])

            print(f"Loaded {len(records)} records")
            print(f"Usernames: {usernameLists}")

    except Exception as e:
        print(f"Error reading decrypted data: {e}")

    finally:
        # Remove the temporary decrypted file
        if os.path.exists(decrypted_data):
            os.remove(decrypted_data)

    return records, usernameLists, idRank # Return it all

records, usernameLists, idRank = loadData("Data/eUserData.csv") # Call upon the function to define the arrays

def test_decryption():
    decrypted_data = decryptCSV("Data/eUserData.csv", "Data/test_decrypted.csv")
    if decrypted_data:
        with open(decrypted_data, 'r') as file:
            print(file.read())
        os.remove(decrypted_data)
    else:
        print("Decryption failed")

# Call this function before attempting to sign in
test_decryption()



class MainPage(customtkinter.CTk):
    def __init__(self, sign_in_window):
        super().__init__()
        self.sign_in_window = sign_in_window

        self.CURRENCIES = {
            "USD": {"code": "USD", "symbol": "US$"},  # United States Dollar
            "EUR": {"code": "EUR", "symbol": "€"},  # Euro
            "JPY": {"code": "JPY", "symbol": "¥"},  # Japanese Yen
            "GBP": {"code": "GBP", "symbol": "£"},  # British Pound Sterling
            "AUD": {"code": "AUD", "symbol": "AU$"},  # Australian Dollar
            "CAD": {"code": "CAD", "symbol": "CA$"},  # Canadian Dollar
            "CHF": {"code": "CHF", "symbol": "₣"},  # Swiss Franc
            "CNY": {"code": "CNY", "symbol": "¥"},  # Chinese Yuan
            "HKD": {"code": "HKD", "symbol": "HK$"},  # Hong Kong Dollar
            "NZD": {"code": "NZD", "symbol": "NZ$"},  # New Zealand Dollar
            "KRW": {"code": "KRW", "symbol": "₩"},  # South Korean Won
            "SGD": {"code": "SGD", "symbol": "S$"},  # Singapore Dollar
            "NOK": {"code": "NOK", "symbol": "kr"},  # Norwegian Krone
            "INR": {"code": "INR", "symbol": "₹"},  # Indian Rupee
            "RUB": {"code": "RUB", "symbol": "₽"},  # Russian Ruble
            "CLP": {"code": "CLP", "symbol": "₱"},  # Chilean Peso

        }

        self.currency_symbols = [currency["symbol"] for currency in self.CURRENCIES.values()]

        self.title("InvenTracker") # Title the window
        self.geometry("1200x600".format(self.winfo_screenwidth(), self.winfo_screenheight())) # Window size
        self.resizable(width=True, height=True) # set the window to be resizable
        self.wm_iconbitmap('Images/invenico.ico')  # Set icon for the main window
        self.current_page = None # define the current page as no current page at the start

        self.editstate = False

        # Make these variables global to be used elsewhere
        global buttonColour
        global buttonHoverColour
        global buttonSelectedColour

        # Define the variables
        buttonColour = "#949494"
        buttonHoverColour = "#6e6e6e"
        buttonSelectedColour = "#4d4d4d"

        # make a placeholder array for the buttons on the side bar frame
        self.sidebar_buttons = []

        # main frame
        self.mainContainer = customtkinter.CTkFrame(self, corner_radius=10)
        self.mainContainer.grid(column=1, row=0, rowspan=3, padx=(10, 10), pady=(10, 10), sticky=('nsew'))
        self.mainContainer.grid_rowconfigure(2, weight=1)

        # Create frames for each page
        self.inventoryFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.reportFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.statisticsFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.settingsFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.accountFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)

        # Initialize content for each frame
        # because its 3 words im using snake case instead
        self.init_inventory_page()
        self.init_report_page()
        self.init_statistics_page()
        self.init_settings_page()
        self.init_account_page()

        # configurations
        self.grid_columnconfigure(1, weight=1) # Allow column 1 to expand horizontally
        self.grid_rowconfigure((0, 1, 2), weight=1) # Allow row 0,1,2 to expand vertically

        self.mainContainer.grid_columnconfigure(1, weight=1)  # Allow column 1 to expand horizontally

        # sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        ### Side bar widgets
        # these are all stated and made and then placed on the grid respectively as well as added onto the list of buttons
        self.titletext = customtkinter.CTkLabel(self.sidebar_frame, text="InvenTrack", text_color='#006b5f',
                                                font=('Berlin Sans FB', 28))
        self.titletext.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create sidebar buttons (keep the existing code)
        self.bt_inven = customtkinter.CTkButton(self.sidebar_frame, text="Inventory", fg_color=buttonColour,
                                                hover_color=buttonHoverColour, text_color=("black", "White"),
                                                width=175, height=60, corner_radius=0, command=self.goInventoryPage)
        self.bt_inven.grid(row=1, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_inven)

        self.bt_report = customtkinter.CTkButton(self.sidebar_frame, text="Report", fg_color=buttonColour,
                                                 hover_color=buttonHoverColour, text_color=("black", "White"),
                                                 width=175, height=60, corner_radius=0, command=self.goReportPage)
        self.bt_report.grid(row=2, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_report)

        self.bt_stats = customtkinter.CTkButton(self.sidebar_frame, text="Statistics", fg_color=buttonColour,
                                                hover_color=buttonHoverColour, text_color=("black", "White"),
                                                width=175, height=60, corner_radius=0, command=self.goStatisticsPage)
        self.bt_stats.grid(row=3, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_stats)

        self.bt_settings = customtkinter.CTkButton(self.sidebar_frame, text="Settings", fg_color=buttonColour,
                                                  hover_color=buttonHoverColour, text_color=("black", "White"),
                                                  width=175, height=60, corner_radius=0, command=self.goSettingsPage)
        self.bt_settings.grid(row=4, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_settings)

        self.bt_account = customtkinter.CTkButton(self.sidebar_frame, text="Account", fg_color=buttonColour,
                                                  hover_color=buttonHoverColour, text_color=("black", "White"),
                                                  width=175, height=60, corner_radius=0, command=self.goAccountPage)
        self.bt_account.grid(row=5, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_account)

        self.set_active_button(self.bt_inven) # Set the initial active button which is inventory

    def configureTreeview(self): # function to configure the tree view

        self.tree["columns"] = ("Name", "Price", "ID", "Category", "Count") # set the headers / columns

        self.tree['show'] = 'headings' # place headings and make them visible

        self.tree.update_idletasks() # update idle tasks

        for col in ("Price", "ID", "Count"): # iterate through 3 specific rows that use numbers
            self.tree.column(col, anchor="center") # centre anchor the column

        # Define column widths and text alignement
        self.tree.column("Name", width=150, anchor=tk.W)
        self.tree.column("Price", width=100, anchor=tk.CENTER)
        self.tree.column("ID", width=50, anchor=tk.CENTER, )
        self.tree.column("Category", width=100, anchor=tk.W)
        self.tree.column("Count", width=50, anchor=tk.CENTER)

        # Define column headings
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Price", text="Price", anchor=tk.CENTER)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Count", text="Count", anchor=tk.CENTER)

        # Create a ThemedStyle
        style = ThemedStyle(self)

        # Set the theme
        style.set_theme("equilux") # set the theme to a dark theme by default (COULD CHANGE LATER)

        # Configure the treeview colors
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', '#22559b')])

        headerFont = tkFont.Font(family="Arial", size=14, weight="bold") # define header font
        entryFont = tkFont.Font(family="Helvetica", size=8) # define text font for entries/items

        # configure the treeview
        style.configure("Treeview.Heading", font=headerFont)
        style.configure("Treeview", font=entryFont)
        style.configure('Treeview', rowheight=40)




    def init_inventory_page(self): # initialization of the inventory page

        label = CTkLabel(self.inventoryFrame, text="Inventory", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=0, row=1, padx=(30, 250), pady=(25, 25), columnspan=2, sticky="w")

        self.tree = ttk.Treeview(self.inventoryFrame, height=10)
        self.tree.grid(column=0, row=2, padx=(45, 45), pady=(0, 30), sticky='nsew')

        # Configurations to the columns and rows
        # This makes the treeview expand to the right
        self.inventoryFrame.grid_rowconfigure(2, weight=0)
        self.inventoryFrame.grid_columnconfigure(0, weight=1)
        self.inventoryFrame.grid_rowconfigure(4, weight=1)

        # Configure the Treeview
        self.configureTreeview()

        # all the inventory stuff
        self.invenWidgetFrame = customtkinter.CTkFrame(self.inventoryFrame, corner_radius=10)
        self.invenWidgetFrame.grid(column=0, row=4, rowspan=1, sticky='nsew', pady=(0, 30), padx=30)

        self.invenAddLabel = customtkinter.CTkLabel(self.inventoryFrame, text="Inventory Management:", font=('Berlin Sans FB', 20))
        self.invenAddLabel.grid(column=0, row=3, padx=40, pady=(30,10), sticky="w")

        self.addbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Add", height=30,
                                                 width=200, font=('Berlin Sans FB', 15), command=self.AddToInven,
                                                             fg_color='#00b341',
                                                             hover_color='#005720')
        self.addbutton.grid(column=0, row=1, pady=10, padx=10)

        self.removebutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Remove", height=30,
                                                    width=200, font=('Berlin Sans FB', 15),command=self.delInvenItem,
                                                    fg_color='#ab0000',hover_color='#6b0101')
        self.removebutton.grid(column=1, row=1, pady=10, padx=10)

        self.editbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Edit", height=30,
                                                  width=200, font=('Berlin Sans FB', 15), command=self.editInvenItem)
        self.editbutton.grid(column=2, row=1, pady=10, padx=10)

        self.clearbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Clear", height=30,
                                                  width=200, font=('Berlin Sans FB', 15), command=self.clrInvenEntry,
                                                   fg_color='#707070',hover_color='#3d3d3d')
        self.clearbutton.grid(column=3, row=1, pady=10, padx=10)

        self.ogc_fg = self.clearbutton.cget("fg_color")
        self.ogc_hov = self.clearbutton.cget("hover_color")


        # The entry boxes and labels

        self.inameEntryLabel = customtkinter.CTkLabel(self.invenWidgetFrame, text="Name:")
        self.inameEntryLabel.grid(column=0, row=2, pady=(10,5), padx=20,sticky="w")

        self.inameEntry = CTkEntry(self.invenWidgetFrame, corner_radius=10, height=30,width=140)
        self.inameEntry.grid(column=0, row=3, padx=10, sticky="w")



        self.priceEntryLabel = customtkinter.CTkLabel(self.invenWidgetFrame, text="Price:")
        self.priceEntryLabel.grid(column=1, row=2, pady=(10, 5), padx=20, sticky="w")

        self.priceEntry = CTkEntry(self.invenWidgetFrame, corner_radius=10, height=30, width=140)
        self.priceEntry.grid(column=1, row=3, padx=10, sticky="w")



        self.IDEntryLabel = customtkinter.CTkLabel(self.invenWidgetFrame, text="ID:")
        self.IDEntryLabel.grid(column=2, row=2, pady=(10, 5), padx=20, sticky="w")

        self.IDEntry = CTkEntry(self.invenWidgetFrame, corner_radius=10, height=30, width=140)
        self.IDEntry.grid(column=2, row=3, padx=10, sticky="w")



        self.categoryEntryLabel = customtkinter.CTkLabel(self.invenWidgetFrame, text="Category:")
        self.categoryEntryLabel.grid(column=3, row=2, pady=(10, 5), padx=20, sticky="w")

        self.categoryEntry = CTkEntry(self.invenWidgetFrame, corner_radius=10, height=30, width=140)
        self.categoryEntry.grid(column=3, row=3, padx=(10,70), sticky="w")



        self.countEntryLabel = customtkinter.CTkLabel(self.invenWidgetFrame, text="Count:")
        self.countEntryLabel.grid(column=4, row=2, pady=(10, 5), padx=20, sticky="w")

        self.countEntry = CTkEntry(self.invenWidgetFrame, corner_radius=10, height=30, width=140)
        self.countEntry.grid(column=4, row=3, padx=10, sticky="w")

        # List of entry boxes
        self.invenboxes = [
            (self.inameEntry, "nameEntry"),
            (self.priceEntry, "priceEntry"),
            (self.IDEntry, "IDEntry"),
            (self.categoryEntry, "categoryEntry"),
            (self.countEntry, "countEntry")
        ]

    def init_report_page(self): # initialise the report page
        label = CTkLabel(self.reportFrame, text="Report", text_color=("black", "White"), font=('Berlin Sans FB', 80))
        label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)

    def init_statistics_page(self): # initialise the statistics page
        label = CTkLabel(self.statisticsFrame, text="Statistics", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)

    def init_settings_page(self): # initialise the settings page
        label = CTkLabel(self.settingsFrame, text="Program Settings", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=0, row=1, padx=(30, 30), pady=(25, 25))

        label2 = CTkLabel(self.settingsFrame, text="UI Colour: ", text_color=("black", "White"),
                          font=('Berlin Sans FB', 40))
        label2.grid(column=0, row=2, padx=(30, 30), pady=(25, 25), sticky="w")

        # settings page widgets
        self.appearanceModeOptionemenu = customtkinter.CTkOptionMenu(
            self.settingsFrame,
            values=["Dark", "Light", "System"], # Colour states
            command=self.colourChange, # Function to change colour
            fg_color="#006b5f",
            dropdown_fg_color="#006b5f",
            button_color="#014f46",
            button_hover_color="#01362f")
        self.appearanceModeOptionemenu.grid(row=3, column=0, padx=(30, 20), pady=(10, 20), sticky="w")

        label3 = CTkLabel(self.settingsFrame, text="UI Scale:", text_color=("black", "White"),
                          font=('Berlin Sans FB', 40))
        label3.grid(column=0, row=4, padx=(30, 30), pady=(25, 25), sticky="w")

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.settingsFrame,
                                                               values=["80%", "90%", "100%", "110%", "120%"], # scales
                                                               command=self.change_scaling_event, # function for scale
                                                               fg_color="#006b5f",
                                                               dropdown_fg_color="#006b5f",
                                                               button_color="#014f46",
                                                               button_hover_color="#01362f")
        self.scaling_optionemenu.grid(row=5, column=0, padx=(30, 20), pady=(10, 20), sticky="w")

        label4 = CTkLabel(self.settingsFrame, text="Currency:", text_color=("black", "White"),
                          font=('Berlin Sans FB', 40))
        label4.grid(column=0, row=6, padx=(30, 30), pady=(25, 25), sticky="w")

        self.currencybox = CTkOptionMenu(self.settingsFrame,
                                         values=self.currency_symbols,
                                         command=self.currencyChange,
                                         fg_color="#006b5f",
                                         dropdown_fg_color="#006b5f",
                                         button_color="#014f46",
                                         button_hover_color="#01362f")

        self.currencybox.grid(row=7, column=0, padx=(30, 20), pady=(10, 20), sticky="w")


    def init_account_page(self): # Initialise the accounts page
        label = CTkLabel(self.accountFrame, text="Account Details", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=0, row=1, padx=(30, 30), pady=(25, 25), columnspan=1)

        self.userlabel = CTkLabel(self.accountFrame, text="Username: ", text_color=("black", "White"),
                                  font=('Berlin Sans FB', 60))
        self.userlabel.grid(column=0, row=2, sticky="w", padx=(30, 5))

        self.userlabel2 = CTkLabel(self.accountFrame, text="", text_color="#006b5f", font=('Berlin Sans FB', 60))
        self.userlabel2.grid(column=1, row=2, sticky="w")

        self.namelabel = CTkLabel(self.accountFrame, text="Fullname: ", text_color=("black", "White"),
                                  font=('Berlin Sans FB', 60))
        self.namelabel.grid(column=0, row=3, sticky="w", padx=(30, 5))

        self.namelabel2 = CTkLabel(self.accountFrame, text="", text_color="#006b5f", font=('Berlin Sans FB', 60))
        self.namelabel2.grid(column=1, row=3, sticky="w")

        self.signout = CTkButton(self.accountFrame, text="Sign Out", fg_color='#ab0000', hover_color='#6b0101', command=self.signOut)
        self.signout.grid(column=0, row=4, sticky="w", padx=(30, 5), pady=(25,0))

    def signOut(self):
        self.withdraw()  # Hide the main window

        self.goInventoryPage()

        self.clear_user_data()
        # Create a new SignIn window instead of showing the old one
        new_sign_in_window = SignIn(self)
        new_sign_in_window.mainloop()


    def clear_user_data(self):
        # Clear any user-specific data
        global userLogged, userFullname, idNum, startingScale, startingUIC, startingCurrency
        userLogged = ""
        userFullname = ""
        idNum = ""
        startingScale = "1"
        startingUIC = "Dark"
        startingCurrency = "NULL"

        self.startUserScale(1)
        customtkinter.set_appearance_mode("Dark")



    def show_frame(self, frame): # Function to show / hide frames, takes in a frame to be used
        # for loop to remove all frames
        for f in [self.inventoryFrame, self.reportFrame, self.statisticsFrame, self.settingsFrame,
                  self.accountFrame]:
            f.grid_remove() # Remove from grid (NOT DELETE)
        frame.grid(column=1, row=0, rowspan=3, padx=(10, 30), pady=(10, 10), sticky=('nsew'))
        self.current_page = frame # Sets the current frame to the frame put into function

    def startCurrency_change(self):
        with open(data,'r') as file:
            reader = csv.reader(file)
            headers = next(reader)

            for i, row in enumerate(records):
                if userLogged in row[1] and idNum in row[0]:
                    savedCurrency = records[i][7]
                    self.displayCSymbol = self.CURRENCIES[savedCurrency]["symbol"]
                    break

        self.currencybox.set(self.displayCSymbol)

    def currencyChange(self, currencyboxinput: str):
        print(currencyboxinput)
        self.displayCSymbol = currencyboxinput
        print(f"display thing {self.displayCSymbol}")

        currency = None
        for key, value in self.CURRENCIES.items():
            if value["symbol"] == currencyboxinput:
                currency = key
                break

        for i, row in enumerate(records):
            if userLogged in row[1] and idNum in row[0]:
                records[i][7] = currency

        with open(data, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(userheaders)
            writer.writerows(records)

        encryptCSV(data, edata)
        loadData(edata)

    def goInventoryPage(self):
        self.set_active_button(self.bt_inven)
        self.show_frame(self.inventoryFrame)
        self.current_page = self.inventoryFrame

        update = False

        for i, row in enumerate(records):
            if row[1] == userLogged and row[7] == "NULL": # this saves lives!!!!
                while True:
                    askCurrency = customtkinter.CTkInputDialog(text="Enter the currency you wish to use \n"
                                                                    "Out of these five settings:\n"
                                                                    "USD, AUD, YEN, GBP, EUR",
                                                               title="What currency would you like to use?")

                    selectedStartingCurrency = askCurrency.get_input()
                    if selectedStartingCurrency in self.CURRENCIES.keys():
                        records[i][7] = selectedStartingCurrency
                        print(f"selected currency {selectedStartingCurrency}")
                        self.displayCSymbol = self.CURRENCIES[selectedStartingCurrency]["symbol"]
                        update = True
                        break  # Exit the while loop

                if update:
                    with open(data, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(userheaders)
                        writer.writerows(records)

                    encryptCSV(data, edata)
                    self.currencybox.set(self.displayCSymbol)
                    loadData(edata)
                    break  # Exit the for loop

        if not update:
            self.startCurrency_change()

        # Clear previous items in the Treeview
        self.tree.delete(*self.tree.get_children())

        self.idata = (f'Data/{userLogged}_Inventory.csv')
        global invenData
        invenData = []

        global listofIDs
        listofIDs = []

        if not os.path.exists(self.idata):
            with open(self.idata, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(invenheaders)

        else:
            with open(self.idata, 'r') as file:
                reader = csv.reader(file)
                next(reader)

                for row in reader:
                    inames = row[0]
                    iprice = row[1]
                    iid = row[2]
                    icategory = row[3]
                    icount = row[4]

                    listofIDs.append(iid)

                    invenData.append([inames, iprice, iid, icategory, icount])

            # Add items from records to the Treeview
            for record in invenData:
                self.tree.insert("", "end", values=(
                record[0], (self.displayCSymbol + " " + record[1]), record[2], record[3], record[4]))

    def is_numeric(self, var): # function to check for specific variables and return true or false depending
        if isinstance(var, (int, float)): # if variable is an integer or a float return true
            return True
        if isinstance(var, str): # if the variable is a string try to print it as a float and if possible return true
            try:
                float(var)
                return True
            except ValueError: # if it's not an int or float and cant be turned into a float from a string return false
                return False
        return False # default the return to false

    def getIDs(self):
        loadData(edata)
        with open(self.idata, 'r') as file:
            reader = csv.reader(file)
            next(reader)

            for row in reader:
                iid = row[2]
                listofIDs.append(iid)
            print(listofIDs)

    def AddToInven(self):
        self.getIDs()
        if self.editstate == True:
            return
        else:
            # Loop through entries and update border colors
            for entry, name in self.invenboxes:
                if entry.get() == "": # if boxes are empty make them red / highlighted
                    entry.configure(border_color="red")
                else:
                    entry.configure(border_color="gray") # if they are not empty apply default colour

            if (self.inameEntry.get() and self.priceEntry.get() and self.IDEntry.get() and
                    self.categoryEntry.get() and self.countEntry.get()): # if all boxes have entries

                itemName = self.inameEntry.get() # define name

                if self.is_numeric(self.priceEntry.get()): # check if price is int or float
                    self.priceEntry.configure(border_color="gray") # clear past error if present
                    itemPrice = self.priceEntry.get() # define the price

                    # check if the entered ID is not found in the first elements of tuples in the list of current IDs
                    if self.IDEntry.get() not in [id[0] for id in listofIDs]:
                        self.IDEntry.configure(border_color="gray") # clear past error if present
                        itemID = self.IDEntry.get() # define variables for ID and Category
                        itemCategory = self.categoryEntry.get()

                        if self.countEntry.get().isnumeric() == True: # if count is an integer
                            self.countEntry.configure(border_color="gray") # clear error if present
                            itemCount = self.countEntry.get() # define count
                            newItem = [itemName, itemPrice, itemID, itemCategory, itemCount, startingThing] # define 2D array

                            with open(self.idata, 'w', newline='') as file: # write the header, current data, and new item
                                writer = csv.writer(file)
                                writer.writerow(invenheaders)
                                print(userheaders)
                                writer.writerows(invenData)
                                print(invenData)
                                writer.writerow(newItem)
                                print(newItem)

                            self.clrInvenEntry() # clear the boxes
                            self.goInventoryPage() # reload the page / data

                        else:
                            self.countEntry.configure(border_color="red") # error with entry
                    else:
                        self.IDEntry.configure(border_color="red") # error with entry
                else:
                    self.priceEntry.configure(border_color="red") # error with entry


    def clrInvenEntry(self): # clear entries in boxes
        if self.editstate == True:
            self.editstate = False
            for entry, name in self.invenboxes:
                    entry.delete(0, 'end')
                    entry.configure(border_color="gray")
            self.clearbutton.configure(text="Clear", fg_color=self.ogc_fg, hover_color=self.ogc_hov)
            self.confirmbutton.destroy()
            self.goInventoryPage()

        else:
            self.clearbutton.configure(text="Clear", fg_color=self.ogc_fg, hover_color=self.ogc_hov)
            for entry, name in self.invenboxes:
                    entry.delete(0, 'end')

            for entry, name in self.invenboxes: # make boxes gray to clear error sign
                entry.configure(border_color="gray")


    def delInvenItem(self): # delete inventory item function
        global invenData

        if self.editstate == True:
            return
        else:
            selected_item = self.tree.selection() # get the selection
            if selected_item:  # if something is selected
                item = self.tree.item(selected_item[0])
                row_data = item['values']

                # Save the row data as an instance variable
                self.selected_row = row_data

                print(f"Selected row: {self.selected_row}")
                #print(f"invenData before deletion {invenData}")

                # delete the item from the treeview
                self.tree.delete(selected_item[0])

                # remove the item from the invenData list
                invenData = [row for row in invenData if row[2] != str(self.selected_row[2])]
                # ^ make new list of lists of every row in invenData except if the ID matches the selected row's ID

                #print(f"invenData after deletion {invenData}")

                # update the CSV file
                with open(self.idata, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(invenheaders)
                    writer.writerows(invenData)
                    print(f"CSV updated: {self.idata}")

                print(f"Deleted item: {self.selected_row}")

    def editInvenItem(self): # edit the item

        if self.editstate == True:
            return
        else:
            self.editstate = True
            self.clearbutton.configure(text="Cancel Edit", fg_color='#ab0000',hover_color='#6b0101')

            selected_item = self.tree.selection()
            if selected_item:
                item = self.tree.item(selected_item[0])
                row_data = item['values']

                # Save the row data as an instance variable
                self.selected_row = row_data
                print(f"Selected row in editInvenItem: {self.selected_row}")
                charsToDel = len(self.displayCSymbol)
                # Clear existing entries and insert new data
                for i, (entry, name) in enumerate(self.invenboxes):
                    entry.delete(0, 'end')
                    if i == 1:  # this is the price entry
                        print(self.displayCSymbol)
                        entry.insert(0, row_data[i][charsToDel:]) # Remove the '$' sign
                    else:
                        entry.insert(0, str(row_data[i]))  # Convert all values to string

                self.confirmbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Confirm Edit",
                                                             height=30,
                                                             width=200, font=('Berlin Sans FB', 15),
                                                             command=self.confirmEdit,
                                                             fg_color='#00b341',
                                                             hover_color='#005720')

                self.confirmbutton.grid(column=4, row=1, pady=10, padx=10)
            else:
                print("No item selected for editing")

    def confirmEdit(self): # confirm the edit
        #
        # THIS JUST USES THE ABOVE FUNCTION IN A SLIGHTLY DIFFERENT WAY
        #


        if (self.inameEntry.get() and self.priceEntry.get() and self.IDEntry.get() and
                self.categoryEntry.get() and self.countEntry.get()):

            itemName = self.inameEntry.get()

            if self.is_numeric(self.priceEntry.get()):
                self.priceEntry.configure(border_color="gray")
                itemPrice = self.priceEntry.get()

                if self.IDEntry.get() not in [id[0] for id in listofIDs]:
                    self.IDEntry.configure(border_color="gray")
                    itemID = self.IDEntry.get()
                    itemCategory = self.categoryEntry.get()

                    if self.countEntry.get().isnumeric():
                        self.countEntry.configure(border_color="gray")
                        itemCount = self.countEntry.get()
                        editedItem = [itemName, itemPrice, itemID, itemCategory, itemCount] # make the new

                        print(f"Edited item: {editedItem}")
                        print(f"Selected row: {self.selected_row}")
                        print(f"Current invenData: {invenData}")

                        # Find the index of the item to be edited in invenData
                        indexToEdit = next((index for (index, d) in enumerate(invenData) if d[2] == str(self.selected_row[2])), None)

                        if indexToEdit is not None: # if there is an item with that index
                            print(f"Found item at index: {indexToEdit}")

                            # replace the old item with the edited item
                            invenData[indexToEdit] = editedItem

                            self.editstate = False

                            self.confirmbutton.destroy()

                            # update the CSV file
                            with open(self.idata, 'w', newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow(invenheaders)
                                writer.writerows(invenData)

                            print(f"Updated invenData: {invenData}")
                            self.clrInvenEntry()
                            self.goInventoryPage()
                        else:
                            print(f"Error: Item not found in inventory data. ID: {self.selected_row[2]}")
                            print(f"IDs in invenData: {[row[2] for row in invenData]}")
                    else:
                        self.countEntry.configure(border_color="red")
                else:
                    self.IDEntry.configure(border_color="red")
            else:
                self.priceEntry.configure(border_color="red")
        else:
            for entry, name in self.invenboxes:
                if entry.get() == "":
                    entry.configure(border_color="red")
            return


    def goReportPage(self): # start the report page
        self.set_active_button(self.bt_report) # set button
        self.show_frame(self.reportFrame) # show the frame
        self.current_page = self.reportFrame # set current page to this one

    def goStatisticsPage(self): # start the statistics page
        # change the frame, button and page
        self.set_active_button(self.bt_stats)
        self.show_frame(self.statisticsFrame)
        self.current_page = self.statisticsFrame

    def goSettingsPage(self): # navigate to and start the settings page
        # change the frame, button and page
        self.set_active_button(self.bt_settings)
        self.show_frame(self.settingsFrame)
        self.current_page = self.settingsFrame

        # sets the widget to the current appearance mode
        self.appearanceModeOptionemenu.set(customtkinter.get_appearance_mode())

        # i cant remember why this is here but i think i need it
        for row in records:
            if idNum == row[0] and userLogged == row[1]:
                startingScale = row[5] # get the scale
                meow = float(startingScale) # turn it into a float
                # turn it into a string with a % at the end after its been turned into a integer and multiple
                meow2 = str(int(meow * 100)) + "%"
                self.scaling_optionemenu.set(meow2)
                break # for efficiency so it doesn't go through more rows after finding needed row

    def goAccountPage(self): # go to the account page
        # change the frame, button and page
        self.set_active_button(self.bt_account)
        self.show_frame(self.accountFrame)
        self.current_page = self.accountFrame

        # Change labels to display current user data
        self.userlabel2.configure(text=userLogged)
        self.namelabel2.configure(text=userFullname)

    def set_active_button(self, active_button): # function to set the active button using a efficient for loop
        for button in self.sidebar_buttons: # iterate through the buttons to check what one is the active button
            if button == active_button:
                button.configure(fg_color="#006b5f") # change the colours
                button.configure(hover_color="#006b5f")
            else: # change them to default if not
                button.configure(fg_color=buttonColour)
                button.configure(hover_color=buttonHoverColour)

    def colourChange(self, new_appearance_mode: str):  # change UIC
        customtkinter.set_appearance_mode(new_appearance_mode.lower()) # change it
        self.update() # update window
        self.state("zoomed") # zoom back in to full screen
        if new_appearance_mode != startingUIC: # if it is a new entry
            for i, row in enumerate(records):
                if userLogged in row[1] and idNum in row[0]:
                    records[i][6] = new_appearance_mode.lower() # replace the data entry in spot to have the new UIC

            with open(data, 'w', newline='') as file: # write to the data
                writer = csv.writer(file)
                writer.writerow(userheaders) # write the userheaders
                print(userheaders)
                writer.writerows(records) # and new data
                print(records)
            encryptCSV(data, edata)

    def change_scaling_event(self, inputedScale: str): # change UI scale
        try:
            new_scaling_float = int(inputedScale.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float) # apply new scale

            for i, row in enumerate(records): # change scale in place in records / data
                if userLogged in row[1] and idNum in row[0]:
                    records[i][5] = str(new_scaling_float)

            with open(data, 'w', newline='') as file: # write the new records and userheaders
                writer = csv.writer(file)
                writer.writerow(userheaders)
                writer.writerows(records)

            encryptCSV(data, edata)

            self.show_frame(self.current_page) # re show the frame

            return

        except Exception as e:
            print(f"Error in change_scaling_event: {e}")

    def startUserScale(self, scale):  # Change UIC at program run from data
        meow = float(scale) # modify it
        customtkinter.set_widget_scaling(meow) # scale it


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, signApp=None):
        super().__init__()
        self.app = signApp
        self.title("InvenTrack") # title
        self.geometry("750x420") # window size
        self.resizable(width=False, height=False) # cant resize
        self.wm_iconbitmap('Images/invenico.ico')  # set icon for SignIn window

        self.after_id = None

        global userLogged
        userLogged = ""
        showstate = "*"

        def hidHandler(): # function for hiding the password entry box entries
            global showstate
            showstate = self.rad.get()
            self.sipasswordEntry.configure(show=showstate)

        def clearEntries(): # clear the entries in the box
            self.sipasswordEntry.delete(0, END)
            self.siuserEntry.delete(0, END)

            self.sipasswordEntry.configure(placeholder_text="Password")
            self.siuserEntry.configure(placeholder_text="Username")

            self.labelsign.configure(text="")

        def logHandler(): # big function to validate and allow for log in, into the ap
            global records, usernameLists, idRank
            records, usernameLists, idRank = loadData(edata) # load new data
            if self.siuserEntry.get() == "" and self.sipasswordEntry.get() == "":
                self.labelsign.configure(text="Enter your details", text_color="red")
            elif self.siuserEntry.get() == "":
                self.labelsign.configure(text="Enter your username", text_color="red")
            elif self.sipasswordEntry.get() == "":
                self.labelsign.configure(text="Enter your password", text_color="red")
            else:
                print(f"Loaded {len(records)} records")

                entered_username = self.siuserEntry.get()
                entered_password = self.sipasswordEntry.get()
                print(f"Attempting login with username: {entered_username}")

                for row in records:
                    if self.siuserEntry.get() == row[1] and self.sipasswordEntry.get() == row[2]:
                        fName = row[3]
                        lName = row[4]

                        global userFullname
                        userFullname = (f"{fName} {lName}")

                        global userLogged
                        userLogged = row[1]

                        global startingScale
                        startingScale = row[5]

                        global startingUIC
                        startingUIC = row[6]

                        global idNum
                        idNum = row[0]

                        # close the window
                        self.withdraw()
                        self.app.deiconify()

                        self.app.state("zoomed")  # Zoom in
                        self.app.startUserScale(startingScale)  # Factor in scale
                        self.app.colourChange(startingUIC) # Factor in UIC
                        self.app.goInventoryPage()  # Make the inventory page the landing page
                        return

                # If no match is found after checking all records
                self.labelsign.configure(text="Username and or password is incorrect", text_color="red")

        def regHandler():
            clearEntries()
            SignInWindow.withdraw()

            # open new window
            registerWindow = Registry(SignInWindow)
            registerWindow.mainloop()

        def enterDetails(event=None): #
            if self.siuserEntry.get() and self.sipasswordEntry.get():
                logHandler()
            else:
                self.labelsign.configure(text="Please enter both username and password", text_color="red")

        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        self.logo1 = customtkinter.CTkImage(dark_image=Image.open('Images/Inventrackreal.png'), size=(380, 200))
        self.logoLabel = CTkLabel(self.frame, image=self.logo1, text="", width=1, height=1)
        self.logoLabel.grid(column=1, row=1, padx=(180, 200), pady=(0, 0), columnspan=4)

        self.siuserEntry = CTkEntry(self.frame, placeholder_text="Username", height=30, width=280)
        self.siuserEntry.grid(column=1, row=3, columnspan=4, pady=(0, 10))

        self.sipasswordEntry = CTkEntry(self.frame, placeholder_text="Password", show=showstate, height=30, width=280)
        self.sipasswordEntry.grid(column=1, row=4, columnspan=4, pady=(0, 10))

        self.rad = CTkCheckBox(self.frame, border_color="black", text="Show password", command=hidHandler,
                               onvalue="", offvalue="*")
        self.rad.grid(column=1, row=5, columnspan=4, pady=(5, 20))

        self.labelsign = CTkLabel(self.frame, text="", text_color="black", font=('Berlin Sans FB', 20))
        self.labelsign.grid(column=1, row=6, padx=(0, 0), pady=(0, 10), columnspan=4, sticky='ns')

        self.btn = CTkButton(self.frame, text="Login", command=logHandler, fg_color="#30a474", hover_color="#1c5c41")
        self.btn.grid(column=1, row=7, columnspan=4, pady=(5, 20), padx=(50, 230))

        tooltip_1 = CTkToolTip(self.btn, message="Log into your Account")

        self.btn2 = CTkButton(self.frame, text="Register", command=regHandler)
        self.btn2.grid(column=2, row=7, columnspan=4, pady=(5, 20), padx=(50, 50))

        tooltip_1 = CTkToolTip(self.btn2, message="Register a New Account")

        # Binding the enter key to the function
        self.siuserEntry.bind('<Return>', enterDetails)
        self.sipasswordEntry.bind('<Return>', enterDetails)



class Registry(customtkinter.CTkToplevel): # register function
    def __init__(self, sign_in_window):
        super().__init__()
        logFeedback = ""
        self.sign_in_window = sign_in_window
        self.sign_in_window.wm_iconbitmap('Images/invenico.ico')  # Set icon for SignIn window
        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        def regBack(): # go back to sign in
            loadData(edata)
            self.withdraw()
            self.sign_in_window.deiconify()

        def checkSpace(string): # function to check how many spaces in a string
            count = 0
            for i in range(0, len(string)):
                if string[i] == " ":
                    count += 1
            return count

        def regSignup(): # this is a big function to validate
            regboxes = [
                (self.nameEntry, "nameEntry"),
                (self.usernameEntry, "usernameEntry"),
                (self.sipasswordEntry, "sipasswordEntry"),
                (self.resipasswordEntry, "resipasswordEntry")
            ]

            # Loop through entries and update border colors
            for entry, name in regboxes:
                if entry.get() == "":
                    entry.configure(border_color="red")
                else:
                    entry.configure(border_color="gray")

            if self.nameEntry.get() and self.usernameEntry.get() and self.sipasswordEntry.get() and self.resipasswordEntry.get() != "":
                fullname = self.nameEntry.get()
                username = self.usernameEntry.get()
                firstPassword = self.sipasswordEntry.get()
                secondPassword = self.resipasswordEntry.get()

                firstn = ""
                lastn = ""

                if checkSpace(self.nameEntry.get()) == 0:
                    self.labelsign.configure(text="Enter last name", text_color="red")
                    self.nameEntry.configure(border_color="red")
                    return

                elif checkSpace(self.nameEntry.get()) == 2:
                    [firstn, lastnfirst, lastntwo] = fullname.split(' ')
                    lastn = lastnfirst + " " + lastntwo
                elif checkSpace(self.nameEntry.get()) == 1:
                    [firstn, lastnfirst] = fullname.split(' ')
                    lastn = lastnfirst
                # elif checkSpace(self.nameEntry.get()) == 0:

                if firstPassword == secondPassword:
                    print("passwords match")

                    if username not in usernameLists:

                        print("username is unique")
                        try:
                            userDesRank = idRank[-1] + 1
                        except:
                            userDesRank = 1

                        newlist = [userDesRank, username, firstPassword, firstn, lastn, startingScale, startingUIC, startingCurrency]

                        with open(data, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(userheaders)
                            print(userheaders)
                            writer.writerows(records)
                            print(records)
                            writer.writerow(newlist)
                            print(newlist)

                        encryptCSV(data, edata)
                        regBack()
                        print("new user added")
                    else:
                        print("username is not unique")
                        self.labelsign.configure(text="Username taken", text_color="red")

                elif firstPassword != secondPassword:
                    print("passwords don't match")
                    self.labelsign.configure(text="Passwords do not match", text_color="red")

            else:
                self.labelsign.configure(text="Enter Details", text_color="red")

        self.title("Register") # title
        self.geometry("700x400") # window size

        self.label = CTkLabel(self.frame, text="Create an account", text_color="black", font=('Berlin Sans FB', 30))
        self.label.grid(column=1, row=1, padx=(250, 250), pady=(30, 25), columnspan=2)

        self.nameEntry = CTkEntry(self.frame, placeholder_text="Your full name", height=30, width=280,
                                  placeholder_text_color="Grey")
        self.nameEntry.grid(column=1, row=2, columnspan=2, pady=(0, 10))

        self.usernameEntry = CTkEntry(self.frame, placeholder_text="Username", height=30, width=280,
                                      placeholder_text_color="Grey")
        self.usernameEntry.grid(column=1, row=3, columnspan=2, pady=(0, 10))

        self.sipasswordEntry = CTkEntry(self.frame, placeholder_text="Password", height=30, width=280,
                                      placeholder_text_color="Grey", show="*")
        self.sipasswordEntry.grid(column=1, row=4, columnspan=4, pady=(0, 10))

        self.resipasswordEntry = CTkEntry(self.frame, placeholder_text="Re-enter password", height=30, width=280,
                                        placeholder_text_color="Grey", show="*")
        self.resipasswordEntry.grid(column=1, row=5, columnspan=4, pady=(0, 10))

        self.createBtn = CTkButton(self.frame, text="Create account", command=regSignup)
        self.createBtn.grid(column=1, row=6, columnspan=2, pady=(5, 10))

        self.labelsign = CTkLabel(self.frame, text="", text_color="black", font=('Berlin Sans FB', 20), )
        self.labelsign.grid(column=1, row=7, padx=(0, 0), pady=(0, 5), columnspan=4, sticky='ns')

        self.label = CTkLabel(self.frame, text="Already got an account?", text_color="black",
                              font=('Berlin Sans FB', 20))
        self.label.grid(column=1, row=8, padx=(250, 250), pady=(0, 10), columnspan=2)

        self.btn = CTkButton(self.frame, text="Login", command=regBack)
        self.btn.grid(column=1, row=9, padx=(250, 250), pady=(0, 50), columnspan=2)

if __name__ == "__main__":
    app = MainPage(None)  # Create MainPage instance without showing it
    SignInWindow = SignIn(app)  # Create initial SignIn instance
    app.sign_in_window = SignInWindow  # Set the sign_in_window attribute of MainPage

    SignInWindow.mainloop()  # Start with the sign-in window
