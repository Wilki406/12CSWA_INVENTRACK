from customtkinter import *
import csv

app = CTk()
app.geometry("500x500")
data = 'dataforsat.csv'
records = []

with open(data, 'r') as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        ids = row[0]
        usernames = row[1]
        pwords = row[2]

        records.append([ids, usernames, pwords])


print(records)

def click_handler():
    if entry.get() == "test":
        print("TESTINGG")

frame = CTkFrame(master=app, width=400, height=320, fg_color="#9B9B9B")
frame.pack_propagate(0)
frame.pack(expand=True)

label = CTkLabel(master=frame, text="Welcome! Sign in", text_color="black")
label.pack(anchor="n", expand=True)

labelu = CTkLabel(master=frame, text="Username", text_color="black")
labelu.pack(anchor="s", expand=True)

entry = CTkEntry(master=frame, placeholder_text="Enter Username")
entry.pack(anchor="n", expand=True)

labelp = CTkLabel(master=frame, text="Password", text_color="black")
labelp.pack(anchor="s", expand=True,)

entry2 = CTkEntry(master=frame, placeholder_text="Enter Password", show="*")
entry2.pack(anchor="n", expand=True)

rad = CTkCheckBox(master=frame,border_color="black", text="Show password")
rad.pack(anchor="center", side="right")

btn = CTkButton(master=frame, text="Submit", command=click_handler)
btn.pack(anchor='center', expand=True)

app.mainloop()
