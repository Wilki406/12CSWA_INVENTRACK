from customtkinter import *
import customtkinter
import csv
from PIL import Image

data = 'dataforsat.csv'
headers = ["ID", "username", "password", "firstName", "lastName"]

# Load data function
def loadData(data):

    records = []
    idRank = []
    usernameLists = []

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

records, usernameLists, idRank = loadData(data)

class MainPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("InvenTracker")
        self.geometry("500x500".format(self.winfo_screenwidth(), self.winfo_screenheight()))
        self.resizable(width=True, height=True)
        self.wm_iconbitmap('invenico.ico')  # Set icon for MainPage


        global buttonColour
        global buttonHoverColour
        global buttonSelectedColour
        buttonColour = "#949494"
        buttonHoverColour = "#6e6e6e"
        buttonSelectedColour = "#4d4d4d"

        self.sidebar_buttons = []


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
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        ### Side bar widgets
        self.titletext = customtkinter.CTkLabel(self.sidebar_frame, text="InvenTrack", text_color='#00FFE3', font=('Berlin Sans FB', 28))
        self.titletext.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Create sidebar buttons (keep the existing code)
        self.bt_inven = customtkinter.CTkButton(self.sidebar_frame, text="Inventory", fg_color=buttonColour,
                                                hover_color=buttonHoverColour,
                                                width=175, height=60, corner_radius=0, command=self.goInventoryPage)
        self.bt_inven.grid(row=1, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_inven)

        self.bt_report = customtkinter.CTkButton(self.sidebar_frame, text="Report", fg_color=buttonColour,
                                                 hover_color=buttonHoverColour,
                                                 width=175, height=60, corner_radius=0, command=self.goReportPage)
        self.bt_report.grid(row=2, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_report)

        self.bt_stats = customtkinter.CTkButton(self.sidebar_frame, text="Statistics", fg_color=buttonColour,
                                                hover_color=buttonHoverColour,
                                                width=175, height=60, corner_radius=0, command=self.goStatisticsPage)
        self.bt_stats.grid(row=3, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_stats)

        self.bt_options = customtkinter.CTkButton(self.sidebar_frame, text="Options", fg_color=buttonColour,
                                                  hover_color=buttonHoverColour,
                                                  width=175, height=60, corner_radius=0, command=self.goOptionsPage)
        self.bt_options.grid(row=4, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_options)

        self.bt_account = customtkinter.CTkButton(self.sidebar_frame, text="Account", fg_color=buttonColour,
                                                  hover_color=buttonHoverColour,
                                                  width=175, height=60, corner_radius=0, command=self.goAccountPage)
        self.bt_account.grid(row=5, column=0, pady=30)
        self.sidebar_buttons.append(self.bt_account)


        # make the inventory page the landing page
        self.goInventoryPage()
        self.set_active_button(self.bt_inven)  # Set the initial active button

    def set_active_button(self, active_button):
        for button in self.sidebar_buttons:
            if button == active_button:
                button.configure(fg_color="#006b5f")
                button.configure(hover_color="#006b5f")
            else:
                button.configure(fg_color=buttonColour)

    def clear_frame(self):
        for widget in self.main_container.winfo_children():
            widget.destroy()


    def goInventoryPage(self):
        print("inventory")
        self.set_active_button(self.bt_inven)
        self.clear_frame()
        # Header
        self.label = CTkLabel(self.main_container, text="Inventory", text_color="white", font=('Berlin Sans FB', 50))
        self.label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)


    def goReportPage(self):
        print("report")
        self.set_active_button(self.bt_report)
        self.clear_frame()
        # Header
        self.label = CTkLabel(self.main_container, text="Report", text_color="white", font=('Berlin Sans FB', 50))
        self.label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)


    def goStatisticsPage(self):
        print("stats")
        self.set_active_button(self.bt_stats)
        self.clear_frame()
        # Header
        self.label = CTkLabel(self.main_container, text="Statistics", text_color="white", font=('Berlin Sans FB', 50))
        self.label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)


    def goOptionsPage(self):
        print("options")
        self.set_active_button(self.bt_options)
        self.clear_frame()
        # Header
        self.label = CTkLabel(self.main_container, text="Settings", text_color="white", font=('Berlin Sans FB', 50))
        self.label.grid(column=1, row=1, padx=(30, 250), pady=(25, 25), columnspan=2)

    def goAccountPage(self):
        print("account")
        self.set_active_button(self.bt_account)
        self.clear_frame()


        # Container for Page
        self.account_container = customtkinter.CTkFrame(self.main_container, corner_radius=10)
        self.account_container.grid(column=1, row=2, rowspan=3, padx=(10, 30), pady=(10, 10), sticky=('nsew'))

        # Header
        self.label = CTkLabel(self.main_container, text="Account Details", text_color="white", font=('Berlin Sans FB', 50))
        self.label.grid(column=1, row=1, padx=(30, 30), pady=(25, 25), columnspan=1)

        # Widgets
        self.userlabel = CTkLabel(self.account_container, text="Username: ", text_color="white", font=('Berlin Sans FB', 30))
        self.userlabel.grid(column=1, row=1, padx=(10, 5))

        self.userlabel2 = CTkLabel(self.account_container, text=userLogged, text_color="white", font=('Berlin Sans FB', 30))
        self.userlabel2.grid(column=2, row=1, padx=(5, 30))


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, signApp):
        super().__init__()
        self.app = signApp
        self.title("Inventrack")
        self.geometry("750x420")
        self.resizable(width=False, height=False)
        self.wm_iconbitmap('invenico.ico')  # Set icon for SignIn window

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
                        global userLogged
                        userLogged = row[1]
                        print(f"Sign in Successful, You are user {userLogged} {fName} {lName}!")

                        self.withdraw()
                        self.app.deiconify()
                        self.app.state("zoomed")

                        return

                # If no match is found after checking all records
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

        self.logo1 = customtkinter.CTkImage(dark_image=Image.open('Inventrackreal.png'), size=(380, 200))
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

        self.btn = CTkButton(self.frame, text="Register", command=regHandler)
        self.btn.grid(column=2, row=7, columnspan=4, pady=(5, 20), padx=(50, 50))

        # Binding the enter key to the function
        self.userEntry.bind('<Return>', enterDetails)
        self.passwordEntry.bind('<Return>', enterDetails)




class Registry(customtkinter.CTkToplevel):
    def __init__(self, sign_in_window):
        super().__init__()
        logFeedback = ""
        self.sign_in_window = sign_in_window
        self.sign_in_window.wm_iconbitmap('invenico.ico')  # Set icon for SignIn window
        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        def regBack():
            records, usernameLists, idRank = loadData(data)
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
                lastn = ""

                if checkSpace(self.nameEntry.get()) == 0:
                    self.labelsign.configure(text="Enter last name", text_color="red")
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
                        userDesRank = idRank[-1] + 1

                        newlist = [userDesRank, username, firstPassword, firstn, lastn]

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
