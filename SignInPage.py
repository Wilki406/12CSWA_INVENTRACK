from customtkinter import *
import customtkinter
import csv

data = 'dataforsat.csv'
records = []
showstate = "*"

with open(data, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        ids = row[0]
        usernames = row[1]
        pwords = row[2]

        records.append([ids, usernames, pwords])

print(records)

class MainPage(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Inventory Tracker")
        self.geometry("1920x1080")


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.title("Sign In")
        self.geometry("800x600")

        def hiddenHandler():
            global showstate
            showstate = self.rad.get()
            self.entry2.configure(show=showstate)

        def logHandler():
            for row in records:
                if self.entry.get() == row[1]:
                    print("TESTINGG")
                    if self.entry2.get() == row[2]:
                        print("Sign in Successful")
                        self.withdraw()  # hide the SignIn window
                        self.app.deiconify()  # show the MainPage window
                        return

        def regHandler():
            SignInWindow.withdraw()
            registerWindow = Registry(SignInWindow)
            registerWindow.mainloop()

        self.frame = CTkFrame(self, width=500, height=400, fg_color="#9B9B9B")
        self.frame.grid()

        self.label = CTkLabel(self.frame, text="Welcome!", text_color="black", font=('Cooper Black', 50))
        self.label.grid(column=1, row=1, padx=(250,250), columnspan=4)

        self.labelu = CTkLabel(self.frame, text="Enter details to log in", text_color="black")
        self.labelu.grid(column=1,row=2, columnspan=4, pady=(0,50))

        self.entry = CTkEntry(self.frame, placeholder_text="Username",height=30, width=280)
        self.entry.grid(column=1,row=3, columnspan=4,pady=(0,10))

        self.entry2 = CTkEntry(self.frame, placeholder_text="Password", show=showstate, height=30, width=280)
        self.entry2.grid(column=1, row=4, columnspan=4,pady=(0,100))

        self.btn = CTkButton(self.frame, text="Submit", command=logHandler)
        self.btn.grid(column=1,row=6, columnspan=2, pady=5)

        self.btn = CTkButton(self.frame, text="Register", command=regHandler)
        self.btn.grid(column=2, row=6, columnspan=2, pady=5)

        self.rad = CTkCheckBox(self.frame, border_color="black", text="Show password", command=hiddenHandler, onvalue="", offvalue="*")
        self.rad.grid(column=3, row=6, columnspan=3, pady=5)

class Registry(customtkinter.CTkToplevel):
    def __init__(self, sign_in_window):
        super().__init__()
        self.sign_in_window = sign_in_window

        self.frame2 = CTkFrame(self, width=500, height=300, fg_color="#9B9B9B")
        self.frame2.pack(expand=True)

        def regBack():
            self.withdraw()
            self.sign_in_window.deiconify()

        self.title("Register")
        self.geometry("800x200")

        self.btn = CTkButton(self.frame2, text="Back", command=regBack)
        self.btn.grid(pady=5)



app = MainPage()
SignInWindow = SignIn(app)
SignInWindow.mainloop()

