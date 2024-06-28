from customtkinter import *
import customtkinter
import csv
import tkinter
from PIL import Image
import json

data = 'dataforsat.csv'
records = []
idRank = []
usernameLists = []
headers = ["ID","username","password","firstName","lastName"]

# Load data function
def loadData():
    with open(data, 'r') as file:
        reader = csv.reader(file)
        next(reader)

        for row in reader:
            ids = row[0]
            usernames = row[1]
            passwords = row[2]
            firstNames = row[3]
            lastNames = row[4]

            idRank.append(int(ids))
            usernameLists.append(usernames)
            records.append([ids, usernames, passwords, firstNames, lastNames])

    return records, usernameLists, idRank

records, usernameLists, idRank = loadData()


class MainPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Tracker")
        self.geometry("100x100".format(self.winfo_screenwidth(), self.winfo_screenheight()))

        self.resizable(width=True, height=True)
        self.wm_iconbitmap('invenico.ico')  # Set icon for MainPage

        # main frame
        self.main_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_container.grid(column=1, row=0, rowspan=3, padx=(10, 10), pady=(10, 10), sticky=('nsew'))
        self.main_container.grid_rowconfigure(4, weight=1)

        # configurations
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=300, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=3, sticky='nsew')
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.titletext = customtkinter.CTkLabel(self.sidebar_frame, text="InvenTrack", text_color="#33F2FF",
                                                font=('Berlin Sans FB', 28))
        self.titletext.grid(row=0, column=0, padx=20, pady=(20, 10))

        # sidebar tab buttons
        self.bt_inven = customtkinter.CTkButton(self.sidebar_frame, text="Inventory", fg_color='#EA0000',
                                               hover_color='#B20000', width=175, height=60, corner_radius=0)
        self.bt_inven.grid(row=1, column=0, pady=30)

class SignIn(customtkinter.CTkToplevel):
    def __init__(self, signApp):
        super().__init__()
        self.app = signApp
        self.title("Inventrack")
        self.geometry("750x420")
        self.resizable(width=False, height=False)
        self.wm_iconbitmap('invenico.ico')  # Set icon for SignIn window

        global userLogged
        userLogged = 0
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
                        userLogged = row[0]
                        print(f"Sign in Successful, You are user {userLogged} {fName} {lName}!")

                        self.withdraw()
                        self.app.deiconify()
                        self.app.state("zoomed")

                        return

                    else:
                        self.labelsign.configure(text="Username and or password is incorrect", text_color="red")

        def regHandler():
            clearEntries()
            SignInWindow.withdraw()
            registerWindow = Registry(SignInWindow)
            registerWindow.mainloop()

        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        self.logo1 = customtkinter.CTkImage(dark_image=Image.open('Inventrackreal.png'), size=(380, 200))
        self.logoLabel = CTkLabel(self.frame, image=self.logo1, text="", width=1, height=1)
        self.logoLabel.grid(column=1, row=1, padx=(200, 210), pady=(0, 0), columnspan=4)

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

        self.btn = CTkButton(self.frame, text="Register", command=regHandler)
        self.btn.grid(column=2, row=7, columnspan=4, pady=(5, 20), padx=(50, 50))


class Registry(customtkinter.CTkToplevel):
    def __init__(self, sign_in_window):
        super().__init__()
        logFeedback = ""
        self.sign_in_window = sign_in_window
        self.sign_in_window.wm_iconbitmap('invenico.ico')  # Set icon for SignIn window
        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        def regBack():
            records, usernameLists, idRank = loadData()
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

            # Loop through entries and update border colors
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
                lastnfirst = ""
                lastntwo = ""

                if checkSpace(self.nameEntry.get()) == 0:
                    self.labelsign.configure(text="Enter last name", text_color="red")
                    return

                elif checkSpace(self.nameEntry.get()) == 2:
                    [firstn, lastnfirst, lastntwo] = fullname.split(' ')
                    lastname = lastnfirst + " " + lastntwo
                elif checkSpace(self.nameEntry.get()) == 1:
                    [firstn, lastnfirst] = fullname.split(' ')
                    lastname = lastnfirst
                # elif checkSpace(self.nameEntry.get()) == 0:

                if firstPassword == secondPassword:
                    print("passwords match")

                    if username not in usernameLists:

                        print("username is unique")
                        userDesRank = idRank[-1] + 1

                        newlist = [userDesRank, username, firstPassword, firstn, lastname]

                        with open(data, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(headers)
                            print(headers)
                            writer.writerows(records)
                            print(records)
                            writer.writerow(newlist)
                            print(newlist)

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
