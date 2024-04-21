from customtkinter import *
import csv

app = CTk()
app.geometry("500x500")
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

def logHandler():
    for i, row in enumerate(records):
        if entry.get() == row[1]:
            print("TESTINGG")

def hiddenHandler():
    global showstate
    showstate = rad.get()
    entry2.configure(show=showstate)

frame = CTkFrame(master=app, width=400, height=300, fg_color="#9B9B9B")
frame.pack_propagate(0)
frame.pack(expand=True)

label = CTkLabel(master=frame, text="Welcome!", text_color="black", font=('Cooper Black', 50))
label.pack(anchor="n", expand=True)

labelu = CTkLabel(master=frame, text="Enter details to log in", text_color="black")
labelu.pack(anchor="n", expand=True)

entry = CTkEntry(master=frame, placeholder_text="Username")
entry.pack(anchor="n", expand=True)

entry2 = CTkEntry(master=frame, placeholder_text="Password", show=showstate)
entry2.pack(anchor="n", expand=True)

rad = CTkCheckBox(master=frame,border_color="black", text="Show password", command=hiddenHandler, onvalue="", offvalue="*")
rad.pack(side="right",padx=50, pady=20)

btn = CTkButton(master=frame, text="Submit", command=logHandler)
btn.pack(expand=True,padx=50, pady=20, side="left")

app.mainloop()
