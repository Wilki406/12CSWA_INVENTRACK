from customtkinter import *
import customtkinter
import csv

data = 'dataforsat.csv'
records = []
idRank = []
headers = ["ID","username","password","firstName","lastName"]
usernameLists = []

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


records,usernameLists,idRank = loadData()



class MainPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Tracker")
        self.geometry("1000x500")


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, signApp):
        super().__init__()
        self.app = signApp
        self.title("Sign In")
        self.geometry("700x393")
        self.resizable(width=False, height=False)

        showstate = "*"
        logFeedback = ""

        def hidHandler():
            global showstate
            showstate = self.rad.get()
            self.passwordEntry.configure(show=showstate)

        def logHandler():

            if self.userEntry.get() == "" and self.passwordEntry.get() == "":
                self.labelsign.configure(text="! Enter your details", text_color="red")
            elif self.userEntry.get() == "":
                self.labelsign.configure(text="! Enter your username", text_color="red")
            elif self.passwordEntry.get() == "":
                self.labelsign.configure(text="! Enter your password", text_color="red")
            else:
                for row in records:
                    if self.userEntry.get() == row[1] and self.passwordEntry.get() == row[2]:
                        fName = row[3]
                        lName = row[4]

                        print(f"Sign in Successful, {fName} {lName}!")

                        self.withdraw()
                        self.app.deiconify()
                        return

                    else:
                        self.labelsign.configure(text="! Password is incorrect", text_color="red")



        def regHandler():
            SignInWindow.withdraw()
            registerWindow = Registry(SignInWindow)
            registerWindow.mainloop()

        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        self.label = CTkLabel(self.frame, text="Welcome!", text_color="black", font=('Berlin Sans FB', 50))
        self.label.grid(column=1, row=1, padx=(250, 250), pady=(40, 0), columnspan=4)

        self.labelu = CTkLabel(self.frame, text="Enter details to log in", text_color="black",
                               font=('Berlin Sans FB', 20))
        self.labelu.grid(column=1, row=2, columnspan=4, pady=(0, 50))

        self.userEntry = CTkEntry(self.frame, placeholder_text="Username", height=30, width=280)
        self.userEntry.grid(column=1, row=3, columnspan=4, pady=(0, 10))

        self.passwordEntry = CTkEntry(self.frame, placeholder_text="Password", show=showstate, height=30, width=280)
        self.passwordEntry.grid(column=1, row=4, columnspan=4, pady=(0, 10))

        self.rad = CTkCheckBox(self.frame, border_color="black", text="Show password", command=hidHandler, onvalue="", offvalue="*")
        self.rad.grid(column=1, row=5, columnspan=4, pady=(5, 20))

        self.labelsign = CTkLabel(self.frame, text=logFeedback, text_color="black", font=('Berlin Sans FB', 20))
        self.labelsign.grid(column=1, row=6, padx=(250, 250), pady=(0, 10), columnspan=4)

        self.btn = CTkButton(self.frame, text="Login", command=logHandler, fg_color="#30a474", hover_color="#1c5c41")
        self.btn.grid(column=1, row=7, columnspan=4, pady=(5, 20), padx=(50, 230))

        self.btn = CTkButton(self.frame, text="Register", command=regHandler)
        self.btn.grid(column=2, row=7, columnspan=4, pady=(5, 20), padx=(50, 50))


class Registry(customtkinter.CTkToplevel):
    def __init__(self, sign_in_window):
        super().__init__()


        self.sign_in_window = sign_in_window
        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        def regBack():
            self.withdraw()
            self.sign_in_window.deiconify()

        def checkSpace(string):
            count = 0
            for i in range(0, len(string)):
                if string[i] == " ":
                    count += 1
            return count

        def regSignup():
            records, usernameLists, idRank = loadData()
            if self.nameEntry.get() == "":
                self.nameEntry.configure(border_color="red")

            if self.nameEntry.get() != "":
                self.nameEntry.configure(border_color="gray")

            if self.usernameEntry.get() == "":
                self.usernameEntry.configure(border_color="red")

            if self.usernameEntry.get() != "":
                self.usernameEntry.configure(border_color="gray")

            if self.passwordEntry.get() == "":
                self.passwordEntry.configure(border_color="red")

            if self.passwordEntry.get() != "":
                self.passwordEntry.configure(border_color="gray")

            if self.rePasswordEntry.get() == "":
                self.rePasswordEntry.configure(border_color="red")

            if self.rePasswordEntry.get() != "":
                self.rePasswordEntry.configure(border_color="gray")

            if self.nameEntry.get() and self.usernameEntry.get() and self.passwordEntry.get() and self.rePasswordEntry.get() != "":
                fullname = self.nameEntry.get()
                username = self.usernameEntry.get()
                firstPassword = self.passwordEntry.get()
                secondPassword = self.rePasswordEntry.get()

                firstn = ""
                lastnfirst = ""
                lastntwo = ""

                if checkSpace(self.nameEntry.get()) == 2:
                    [firstn, lastnfirst, lastntwo] = fullname.split(' ')
                    lastname = lastnfirst + " " + lastntwo
                elif checkSpace(self.nameEntry.get()) == 1:
                    [firstn, lastnfirst] = fullname.split(' ')
                    lastname = lastnfirst

                if firstPassword == secondPassword:
                    print("passwords match")
                    print(username, usernameLists)

                    if username not in usernameLists:

                        print("username is unique")
                        userDesRank = idRank[-1] + 1

                        newlist = [userDesRank, username, firstPassword, firstn, lastname]

                        with open(data, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(headers)
                            writer.writerows(records)
                            writer.writerow(newlist)

                        print(newlist)

                        regBack()
                    else:
                        print("username is not unique")

                elif firstPassword != secondPassword:
                    print("passwords don't match")


        self.title("Register")
        self.geometry("700x400")

        self.label = CTkLabel(self.frame, text="Create an account", text_color="black", font=('Berlin Sans FB', 30))
        self.label.grid(column=1, row=1, padx=(250, 250), pady=(30, 25), columnspan=2)

        self.nameEntry = CTkEntry(self.frame, placeholder_text="Your full name", height=30, width=280,
                                  placeholder_text_color="Grey")
        self.nameEntry.grid(column=1, row=2, columnspan=2, pady=(0, 10))

        self.usernameEntry = CTkEntry(self.frame, placeholder_text="Username", height=30, width=280, placeholder_text_color="Grey")
        self.usernameEntry.grid(column=1, row=3, columnspan=2, pady=(0, 10))

        self.passwordEntry = CTkEntry(self.frame, placeholder_text="Password", height=30, width=280,
                                      placeholder_text_color="Grey",show="*")
        self.passwordEntry.grid(column=1, row=4, columnspan=4, pady=(0, 10))

        self.rePasswordEntry = CTkEntry(self.frame, placeholder_text="Re-enter password", height=30, width=280,
                                        placeholder_text_color="Grey",show="*")
        self.rePasswordEntry.grid(column=1, row=5, columnspan=4, pady=(0, 10))

        self.createBtn = CTkButton(self.frame, text="Create account", command=regSignup)
        self.createBtn.grid(column=1, row=6, columnspan=2, pady=(5, 15))

        self.label = CTkLabel(self.frame, text="Already got an account?", text_color="black",
                              font=('Berlin Sans FB', 20))
        self.label.grid(column=1, row=7, padx=(250, 250), pady=(0, 15), columnspan=2)

        self.btn = CTkButton(self.frame, text="Login", command=regBack)
        self.btn.grid(column=1, row=8, padx=(250, 250), pady=(0, 50), columnspan=2)


app = MainPage()
SignInWindow = SignIn(app)
SignInWindow.mainloop()
