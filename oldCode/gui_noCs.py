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

# Encryption
from cryptography.fernet import Fernet
import base64

from Encryption import *

# Modifications:
# list of IDs is appended to when item is added to inventory and id.get not in list of IDs if statement fixed


startingScale = "1"
startingUIC = "Dark"

data = 'userdata.csv'
headers = ["ID", "username", "password", "firstName", "lastName", "Scale", "UIC"]
invenheaders = ["Name", "Price", "ID", "Category", "Count"]


def createCSV(data, headers):
    if not os.path.exists(data):
        key = get_encryption_key()

        # Write headers as plain text
        with open(data, 'wb') as file:
            file.write(','.join(headers).encode() + b'\n')


createCSV(data, headers)
def loadData(data):
    records = []
    idRank = []
    usernameLists = []

    key = get_encryption_key()
    with open(data, 'rb') as file:
        headers = file.readline().decode().strip()

        encryptedContent = file.read()
        decryptedContent = decrypt_data(encryptedContent, key)

        for row in decryptedContent.split('\n')[1:]: # Skip header
            if row:
                row = row.split(',')

                ids = row[0]
                usernames = row[1]
                passwords = row[2]
                firstNames = row[3]
                lastNames = row[4]
                scales = row[5]
                UICs = row[6]

                idRank.append(int(ids))
                usernameLists.append(usernames)
                records.append([ids, usernames, passwords, firstNames, lastNames, scales, UICs])

    return records, usernameLists, idRank


records, usernameLists, idRank = loadData(data)


class MainPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("InvenTracker")
        self.geometry("1200x600".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.resizable(width=True, height=True)
        self.wm_iconbitmap('Images/invenico.ico') 
        self.current_page = None

       
        global buttonColour
        global buttonHoverColour
        global buttonSelectedColour

       
        buttonColour = "#949494"
        buttonHoverColour = "#6e6e6e"
        buttonSelectedColour = "#4d4d4d"

       
        self.sidebar_buttons = []

       
        self.mainContainer = customtkinter.CTkFrame(self, corner_radius=10)
        self.mainContainer.grid(column=1, row=0, rowspan=3, padx=(10, 10), pady=(10, 10), sticky=('nsew'))
        self.mainContainer.grid_rowconfigure(2, weight=1)

       
        self.inventoryFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.reportFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.statisticsFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.optionsFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)
        self.accountFrame = customtkinter.CTkFrame(self.mainContainer, corner_radius=10)

       
       
        self.init_inventory_page()
        self.init_report_page()
        self.init_statistics_page()
        self.init_options_page()
        self.init_account_page()

       
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        self.mainContainer.grid_columnconfigure(1, weight=1) 

       
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

       
       
        self.titletext = customtkinter.CTkLabel(self.sidebar_frame, text="InvenTrack", text_color='#006b5f',
                                                font=('Berlin Sans FB', 28))
        self.titletext.grid(row=0, column=0, padx=20, pady=(20, 10))

       
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

        self.bt_options = customtkinter.CTkButton(self.sidebar_frame, text="Options", fg_color=buttonColour,
                                                  hover_color=buttonHoverColour, text_color=("black", "White"),
                                                  width=175, height=60, corner_radius=0, command=self.goOptionsPage)
        self.bt_options.grid(row=4, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_options)

        self.bt_account = customtkinter.CTkButton(self.sidebar_frame, text="Account", fg_color=buttonColour,
                                                  hover_color=buttonHoverColour, text_color=("black", "White"),
                                                  width=175, height=60, corner_radius=0, command=self.goAccountPage)
        self.bt_account.grid(row=5, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_account)

        self.set_active_button(self.bt_inven)

    def configureTreeview(self):

        self.tree["columns"] = ("Name", "Price", "ID", "Category", "Count")

        self.tree['show'] = 'headings'

        self.tree.update_idletasks()

        for col in ("Price", "ID", "Count"):
            self.tree.column(col, anchor="center")

       
        self.tree.column("Name", width=150, anchor=tk.W)
        self.tree.column("Price", width=100, anchor=tk.CENTER)
        self.tree.column("ID", width=50, anchor=tk.CENTER, )
        self.tree.column("Category", width=100, anchor=tk.W)
        self.tree.column("Count", width=50, anchor=tk.CENTER)

       
        self.tree.heading("Name", text="Name", anchor=tk.W)
        self.tree.heading("Price", text="Price", anchor=tk.CENTER)
        self.tree.heading("ID", text="ID", anchor=tk.CENTER)
        self.tree.heading("Category", text="Category", anchor=tk.W)
        self.tree.heading("Count", text="Count", anchor=tk.CENTER)

       
        style = ThemedStyle(self)

       
        style.set_theme("equilux")

       
        style.configure("Treeview",
                        background="#2a2d2e",
                        foreground="white",
                        fieldbackground="#2a2d2e")
        style.map('Treeview', background=[('selected', '#22559b')])

        headerFont = tkFont.Font(family="Arial", size=14, weight="bold")
        entryFont = tkFont.Font(family="Helvetica", size=8)

       
        style.configure("Treeview.Heading", font=headerFont)
        style.configure("Treeview", font=entryFont)
        style.configure('Treeview', rowheight=40)




    def init_inventory_page(self):
        label = CTkLabel(self.inventoryFrame, text="Inventory", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=0, row=1, padx=(30, 250), pady=(25, 25), columnspan=2, sticky="w")

        self.tree = ttk.Treeview(self.inventoryFrame, height=10)
        self.tree.grid(column=0, row=2, padx=(45, 45), pady=(0, 30), sticky='nsew')

       
       
        self.inventoryFrame.grid_rowconfigure(2, weight=0)
        self.inventoryFrame.grid_columnconfigure(0, weight=1)
        self.inventoryFrame.grid_rowconfigure(4, weight=1)

       
        self.configureTreeview()

       
        self.invenWidgetFrame = customtkinter.CTkFrame(self.inventoryFrame, corner_radius=10)
        self.invenWidgetFrame.grid(column=0, row=4, rowspan=1, sticky='nsew', pady=(0, 30), padx=30)

        self.invenAddLabel = customtkinter.CTkLabel(self.inventoryFrame, text="Inventory Management:", font=('Berlin Sans FB', 20))
        self.invenAddLabel.grid(column=0, row=3, padx=40, pady=(30,10), sticky="w")

        self.addbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Add", height=30,
                                                 width=200, font=('Berlin Sans FB', 15), command=self.AddToInven)
        self.addbutton.grid(column=0, row=1, pady=10, padx=10)

        self.removebutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Remove", height=30,
                                                    width=200, font=('Berlin Sans FB', 15),command=self.delInvenItem)
        self.removebutton.grid(column=1, row=1, pady=10, padx=10)

        self.editbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Edit", height=30,
                                                  width=200, font=('Berlin Sans FB', 15), command=self.editInvenItem)
        self.editbutton.grid(column=2, row=1, pady=10, padx=10)

        self.clearbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Clear", height=30,
                                                  width=200, font=('Berlin Sans FB', 15), command=self.clrInvenEntry)
        self.clearbutton.grid(column=3, row=1, pady=10, padx=10)

       

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

       
        self.invenboxes = [
            (self.inameEntry, "nameEntry"),
            (self.priceEntry, "priceEntry"),
            (self.IDEntry, "IDEntry"),
            (self.categoryEntry, "categoryEntry"),
            (self.countEntry, "countEntry")
        ]

    def init_report_page(self):
        label = CTkLabel(self.reportFrame, text="Report", text_color=("black", "White"), font=('Berlin Sans FB', 80))
        label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)

    def init_statistics_page(self):
        label = CTkLabel(self.statisticsFrame, text="Statistics", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)

    def init_options_page(self):
        label = CTkLabel(self.optionsFrame, text="Program Settings", text_color=("black", "White"),
                         font=('Berlin Sans FB', 80))
        label.grid(column=0, row=1, padx=(30, 30), pady=(25, 25))

        label2 = CTkLabel(self.optionsFrame, text="UI Colour: ", text_color=("black", "White"),
                          font=('Berlin Sans FB', 40))
        label2.grid(column=0, row=2, padx=(30, 30), pady=(25, 25), sticky="w")

       
        self.appearanceModeOptionemenu = customtkinter.CTkOptionMenu(
            self.optionsFrame,
            values=["Dark", "Light", "System"],
            command=self.colourChange,
            fg_color="#006b5f",
            dropdown_fg_color="#006b5f",
            button_color="#014f46",
            button_hover_color="#01362f")
        self.appearanceModeOptionemenu.grid(row=3, column=0, padx=(30, 20), pady=(10, 20), sticky="w")

        label3 = CTkLabel(self.optionsFrame, text="UI Scale:", text_color=("black", "White"),
                          font=('Berlin Sans FB', 40))
        label3.grid(column=0, row=4, padx=(30, 30), pady=(25, 25), sticky="w")

        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.optionsFrame,
                                                               values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event,
                                                               fg_color="#006b5f",
                                                               dropdown_fg_color="#006b5f",
                                                               button_color="#014f46",
                                                               button_hover_color="#01362f")
        self.scaling_optionemenu.grid(row=5, column=0, padx=(30, 20), pady=(10, 20), sticky="w")

    def init_account_page(self):
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

    def show_frame(self, frame):
       
        for f in [self.inventoryFrame, self.reportFrame, self.statisticsFrame, self.optionsFrame,
                  self.accountFrame]:
            f.grid_remove()
        frame.grid(column=1, row=0, rowspan=3, padx=(10, 30), pady=(10, 10), sticky=('nsew'))
        self.current_page = frame


    def goInventoryPage(self):
        self.set_active_button(self.bt_inven)
        self.show_frame(self.inventoryFrame)
        self.current_page = self.inventoryFrame

        self.tree.delete(*self.tree.get_children())

        global listofIDs
        listofIDs = []

        global idata
        idata = (f'{userLogged}_Inventory.csv')
        global invenData
        invenData = []

        if not os.path.exists(idata):
            with open(idata, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(invenheaders)
               
        else:
            with open(idata, 'r') as file:
                reader = csv.reader(file)
                next(reader)  # skip header

                for row in reader:
                    iid = row[2]
                    listofIDs.append(iid)
                    invenData.append([row[0], row[1], iid, row[3], row[4]])

           
            for record in invenData:
                self.tree.insert("", "end", values=(record[0], ("$" + record[1]), record[2], record[3], record[4]))

    def is_numeric(self, var):
        if isinstance(var, (int, float)):
            return True
        if isinstance(var, str):
            try:
                float(var)
                return True
            except ValueError:
                return False
        return False

    def AddToInven(self):
        global listofIDs

        for entry, name in self.invenboxes:
            if entry.get() == "":
                entry.configure(border_color="red")
            else:
                entry.configure(border_color="gray")

        print(listofIDs)
        if (self.inameEntry.get() and self.priceEntry.get() and self.IDEntry.get() and
                self.categoryEntry.get() and self.countEntry.get()):

            itemName = self.inameEntry.get()

            if self.is_numeric(self.priceEntry.get()):
                self.priceEntry.configure(border_color="gray")
                itemPrice = self.priceEntry.get()

               
                if self.IDEntry.get() not in listofIDs:
                    self.IDEntry.configure(border_color="gray")
                    itemID = self.IDEntry.get()
                    itemCategory = self.categoryEntry.get()

                    if self.countEntry.get().isnumeric() == True:
                        self.countEntry.configure(border_color="gray")
                        itemCount = self.countEntry.get()
                        newItem = [itemName, itemPrice, itemID, itemCategory, itemCount]

                        with open(idata, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(invenheaders)
                            print(headers)
                            writer.writerows(invenData)
                            print(invenData)
                            writer.writerow(newItem)
                            print(newItem)

                        listofIDs.append(itemID)
                        self.clrInvenEntry()
                        self.goInventoryPage()

                    else:
                        self.countEntry.configure(border_color="red")
                else:
                    self.IDEntry.configure(border_color="red")
            else:
                self.priceEntry.configure(border_color="red")


    def clrInvenEntry(self):
        for entry, name in self.invenboxes:
                entry.delete(0, 'end')

        for entry, name in self.invenboxes:
            entry.configure(border_color="gray")


    def delInvenItem(self):
        global invenData
        global idata
        global listofIDs

        selected_item = self.tree.selection()
        if selected_item: 
            item = self.tree.item(selected_item[0])
            row_data = item['values']

            self.selected_row = row_data

            self.tree.delete(selected_item[0])

            invenData = [row for row in invenData if row[2] != str(self.selected_row[2])]

            with open(idata, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(invenheaders)
                writer.writerows(invenData)
                print(f"CSV updated: {idata}")

    def editInvenItem(self):
        selected_item = self.tree.selection()
        if selected_item:
            item = self.tree.item(selected_item[0])
            row_data = item['values']

           
            self.selected_row = row_data
            print(f"Selected row in editInvenItem: {self.selected_row}")

           
            for i, (entry, name) in enumerate(self.invenboxes):
                entry.delete(0, 'end')
                if i == 1: 
                    entry.insert(0, row_data[i][1:]) 
                else:
                    entry.insert(0, str(row_data[i])) 

            self.confirmbutton = customtkinter.CTkButton(self.invenWidgetFrame, corner_radius=10, text="Confirm Edit",
                                                         height=30,
                                                         width=200, font=('Berlin Sans FB', 15),
                                                         command=self.confirmEdit)
            self.confirmbutton.grid(column=4, row=1, pady=10, padx=10)
        else:
            print("No item selected for editing")

    def confirmEdit(self):
       
       
       
        self.confirmbutton.destroy()
        if (self.inameEntry.get() and self.priceEntry.get() and self.IDEntry.get() and
                self.categoryEntry.get() and self.countEntry.get()):

            itemName = self.inameEntry.get()

            if self.is_numeric(self.priceEntry.get()):
                self.priceEntry.configure(border_color="gray")
                itemPrice = self.priceEntry.get()

                if self.IDEntry.get() not in listofIDs:
                    self.IDEntry.configure(border_color="gray")
                    itemID = self.IDEntry.get()
                    itemCategory = self.categoryEntry.get()

                    if self.countEntry.get().isnumeric():
                        self.countEntry.configure(border_color="gray")
                        itemCount = self.countEntry.get()
                        editedItem = [itemName, itemPrice, itemID, itemCategory, itemCount]

                        print(f"Edited item: {editedItem}")
                        print(f"Selected row: {self.selected_row}")
                        print(f"Current invenData: {invenData}")

                       
                        indexToEdit = next((index for (index, d) in enumerate(invenData) if d[2] == str(self.selected_row[2])), None)

                        if indexToEdit is not None:
                            print(f"Found item at index: {indexToEdit}")

                           
                            invenData[indexToEdit] = editedItem

                           
                            with open(idata, 'w', newline='') as file:
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
                    self.priceEntry.configure(border_color="red")
            else:
                for entry, name in self.invenboxes:
                    if entry.get() == "":
                        entry.configure(border_color="red")
            return


    def goReportPage(self):
        self.set_active_button(self.bt_report)
        self.show_frame(self.reportFrame)
        self.current_page = self.reportFrame

    def goStatisticsPage(self):
       
        self.set_active_button(self.bt_stats)
        self.show_frame(self.statisticsFrame)
        self.current_page = self.statisticsFrame

    def goOptionsPage(self):
       
        self.set_active_button(self.bt_options)
        self.show_frame(self.optionsFrame)
        self.current_page = self.optionsFrame

       
        self.appearanceModeOptionemenu.set(customtkinter.get_appearance_mode())

       
        for row in records:
            if idNum == row[0] and userLogged == row[1]:
                startingScale = row[5]
                meow = float(startingScale)
               
                meow2 = str(int(meow * 100)) + "%"
                self.scaling_optionemenu.set(meow2)
                break

    def goAccountPage(self):
       
        self.set_active_button(self.bt_account)
        self.show_frame(self.accountFrame)
        self.current_page = self.accountFrame

       
        self.userlabel2.configure(text=userLogged)
        self.namelabel2.configure(text=userFullname)

    def set_active_button(self, active_button):
        for button in self.sidebar_buttons:
            if button == active_button:
                button.configure(fg_color="#006b5f")
                button.configure(hover_color="#006b5f")
            else:
                button.configure(fg_color=buttonColour)
                button.configure(hover_color=buttonHoverColour)

    def colourChange(self, new_appearance_mode: str): 
        customtkinter.set_appearance_mode(new_appearance_mode.lower())
        self.update()
        self.state("zoomed")
        if new_appearance_mode != startingUIC:
            for i, row in enumerate(records):
                if userLogged in row[1] and idNum in row[0]:
                    records[i][6] = new_appearance_mode.lower()

            with open(data, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                print(headers)
                writer.writerows(records)
                print(records)

    def change_scaling_event(self, inputedScale: str):
        try:
            new_scaling_float = int(inputedScale.replace("%", "")) / 100
            customtkinter.set_widget_scaling(new_scaling_float)

            for i, row in enumerate(records):
                if userLogged in row[1] and idNum in row[0]:
                    records[i][5] = str(new_scaling_float)

            with open(data, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(records)

            self.show_frame(self.current_page)

            return

        except Exception as e:
            print(f"Error in change_scaling_event: {e}")

    def startUserScale(self, scale): 
        meow = float(scale)
        customtkinter.set_widget_scaling(meow)


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, signApp):
        super().__init__()
        self.app = signApp
        self.title("InvenTrack")
        self.geometry("750x420")
        self.resizable(width=False, height=False)
        self.wm_iconbitmap('Images/invenico.ico') 

        global userLogged
        userLogged = ""
        showstate = "*"


        def hidHandler():
            global showstate
            showstate = self.rad.get()
            self.passwordEntry.configure(show=showstate)

        def clearEntries():
            self.passwordEntry.delete(0, END)
            self.userEntry.delete(0, END)

            self.passwordEntry.configure(placeholder_text="Password")
            self.userEntry.configure(placeholder_text="Username")

            self.labelsign.configure(text="")

        def logHandler():
            global records, usernameLists, idRank
            records, usernameLists, idRank = loadData(data)
            if self.userEntry.get() == "" and self.passwordEntry.get() == "":
                self.labelsign.configure(text="Enter your details", text_color="red")
            elif self.userEntry.get() == "":
                self.labelsign.configure(text="Enter your username", text_color="red")
            elif self.passwordEntry.get() == "":
                self.labelsign.configure(text="Enter your password", text_color="red")
            else:
                for row in records:
                    if self.userEntry.get() == row[1] and self.passwordEntry.get() == row[2]:
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

                       
                       

                       
                        self.withdraw()
                        self.app.deiconify()

                        self.app.state("zoomed") 
                        self.app.startUserScale(startingScale) 
                        self.app.colourChange(startingUIC)
                        self.app.goInventoryPage() 
                        return

               
                self.labelsign.configure(text="Username and or password is incorrect", text_color="red")

        def regHandler():
            clearEntries()
            SignInWindow.withdraw()

           
            registerWindow = Registry(SignInWindow)
            registerWindow.mainloop()

        def enterDetails(event=None):
            if self.userEntry.get() and self.passwordEntry.get():
                logHandler()
            else:
                self.labelsign.configure(text="Please enter both username and password", text_color="red")

        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        self.logo1 = customtkinter.CTkImage(dark_image=Image.open('../Images/Inventrackreal.png'), size=(380, 200))
        self.logoLabel = CTkLabel(self.frame, image=self.logo1, text="", width=1, height=1)
        self.logoLabel.grid(column=1, row=1, padx=(180, 200), pady=(0, 0), columnspan=4)

        self.userEntry = CTkEntry(self.frame, placeholder_text="Username", height=30, width=280)
        self.userEntry.grid(column=1, row=3, columnspan=4, pady=(0, 10))

        self.passwordEntry = CTkEntry(self.frame, placeholder_text="Password", show=showstate, height=30, width=280)
        self.passwordEntry.grid(column=1, row=4, columnspan=4, pady=(0, 10))

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

       
        self.userEntry.bind('<Return>', enterDetails)
        self.passwordEntry.bind('<Return>', enterDetails)


class Registry(customtkinter.CTkToplevel):
    def __init__(self, sign_in_window):
        super().__init__()

        self.sign_in_window = sign_in_window
        self.sign_in_window.wm_iconbitmap('Images/invenico.ico') 
        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        def regBack():
            loadData(data)
            self.withdraw()
            self.sign_in_window.deiconify()

        def checkSpace(string):
            count = 0
            for i in range(0, len(string)):
                if string[i] == " ":
                    count += 1
            return count

        def regSignup():
            regboxes = [
                (self.nameEntry, "nameEntry"),
                (self.usernameEntry, "usernameEntry"),
                (self.passwordEntry, "passwordEntry"),
                (self.rePasswordEntry, "rePasswordEntry")
            ]

           
            for entry, name in regboxes:
                if entry.get() == "":
                    entry.configure(border_color="red")
                else:
                    entry.configure(border_color="gray")

            if self.nameEntry.get() and self.usernameEntry.get() and self.passwordEntry.get() and self.rePasswordEntry.get() != "":
                fullname = self.nameEntry.get()
                username = self.usernameEntry.get()
                firstPassword = self.passwordEntry.get()
                secondPassword = self.rePasswordEntry.get()

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
               

                if firstPassword == secondPassword:
                    print("passwords match")

                    if username not in usernameLists:

                        print("username is unique")
                        try:
                            userDesRank = idRank[-1] + 1
                        except:
                            userDesRank = 1

                        scaleF = 1.0
                        uiC = "dark"
                        newlist = [userDesRank, username, firstPassword, firstn, lastn, scaleF, uiC]

                        write_to_csv(newlist,data)

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

        self.title("Register")
        self.geometry("700x400")

        self.label = CTkLabel(self.frame, text="Create an account", text_color="black", font=('Berlin Sans FB', 30))
        self.label.grid(column=1, row=1, padx=(250, 250), pady=(30, 25), columnspan=2)

        self.nameEntry = CTkEntry(self.frame, placeholder_text="Your full name", height=30, width=280,
                                  placeholder_text_color="Grey")
        self.nameEntry.grid(column=1, row=2, columnspan=2, pady=(0, 10))

        self.usernameEntry = CTkEntry(self.frame, placeholder_text="Username", height=30, width=280,
                                      placeholder_text_color="Grey")
        self.usernameEntry.grid(column=1, row=3, columnspan=2, pady=(0, 10))

        self.passwordEntry = CTkEntry(self.frame, placeholder_text="Password", height=30, width=280,
                                      placeholder_text_color="Grey", show="*")
        self.passwordEntry.grid(column=1, row=4, columnspan=4, pady=(0, 10))

        self.rePasswordEntry = CTkEntry(self.frame, placeholder_text="Re-enter password", height=30, width=280,
                                        placeholder_text_color="Grey", show="*")
        self.rePasswordEntry.grid(column=1, row=5, columnspan=4, pady=(0, 10))

        self.createBtn = CTkButton(self.frame, text="Create account", command=regSignup)
        self.createBtn.grid(column=1, row=6, columnspan=2, pady=(5, 10))

        self.labelsign = CTkLabel(self.frame, text="", text_color="black", font=('Berlin Sans FB', 20), )
        self.labelsign.grid(column=1, row=7, padx=(0, 0), pady=(0, 5), columnspan=4, sticky='ns')

        self.label = CTkLabel(self.frame, text="Already got an account?", text_color="black",
                              font=('Berlin Sans FB', 20))
        self.label.grid(column=1, row=8, padx=(250, 250), pady=(0, 10), columnspan=2)

        self.btn = CTkButton(self.frame, text="Login", command=regBack)
        self.btn.grid(column=1, row=9, padx=(250, 250), pady=(0, 50), columnspan=2)

app = MainPage()

SignInWindow = SignIn(app)

SignInWindow.mainloop()
