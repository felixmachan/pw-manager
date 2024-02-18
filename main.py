# coding= utf-8
import tkinter
import tkinter.ttk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from PIL import Image, ImageTk
from random import choice, randint, shuffle
from pyperclip import copy
import json
FONT = ("Arial", 12, "normal")
PINK = "#FFC0D9"
BUTTER = "#F9F9E0"
BLUE = "#8ACDD7"
usernames = []


with open("usernames.txt") as us:
    usnames = us.readlines()
    for names in usnames:
        usernames.append(names[0:-1])


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
#Password Generator Project
def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_numbers + password_letters
    shuffle(password_list)

    passwordd = "".join(password_list)
    pwentry.insert(0, passwordd)
    copy(passwordd)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = webentry.get()
    user_name = usernameentry.get()
    pw = pwentry.get()
    new_data = {
        website: {
            "email": user_name,
            "password": pw,
        }
    }

    if pw != "" and user_name != "" and website != "":
        is_ok = messagebox.askokcancel(title=f"{website}",
                                       message=f"Details entered:\nPassword: {pw}\nUsername: {user_name}")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)

            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)

            else:
                data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

            webentry.delete(0, END)
            usernameentry.delete(0, END)
            pwentry.delete(0, END)
            usernameentry.insert(0, user_name)

            if user_name not in usernames:
                with open("usernames.txt", "a") as usn:
                    usn.write(user_name)
                    usn.write("\n")
    else:
        messagebox.showwarning(title="Blank spaces", message="Please don't leave any blank spaces!")
# ---------- FIND PASSWORD -----------#
def find_password():
    website = webentry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No data file found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title=website, message=f"You have no saved account for {website}")



# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Babó Jelszó Kezelője")
window.config(padx=20, pady=20, bg=PINK)
window.minsize(400, 300)

image = Image.open("Cute-Penguin-icon.png")
resize = image.resize((180, 180))
img = ImageTk.PhotoImage(resize)

canvas = Canvas(width=200, height=200, bg=PINK, highlightthickness=0)
# pw_img = PhotoImage(file="logo.png")
canvas.create_image(80, 100, image=img)
canvas.grid(column=1, row=0, columnspan=2)

# ----------Website------------------ #

# Label
weblabel = Label(text="Website:", bg=PINK, highlightthickness=0)
weblabel.grid(column=0, row=1)

# entry
webentry = Entry(width=17, bg=BUTTER)
webentry.grid(column=1, row=1, columnspan=1)
webentry.focus()


# ----------Email/username------------------ #

# Label
username = Label(text="Email/Username:", bg=PINK, highlightthickness=0)
username.grid(column=0, row=2)

# entry
# usernameentry = Entry(width=35)
# usernameentry.grid(column=1, row=2, columnspan=2)
# usernameentry.insert(0, "panna.bartos914@gmail.com")

current_username = tkinter.StringVar()
usernameentry = tkinter.ttk.Combobox(width=35)
usernameentry.config(background=BUTTER)
usernameentry["values"] = usernames
usernameentry.grid(column=1, row=2, columnspan=2)
style = ttk.Style()
style.theme_use('clam')
style.configure("TCombobox", fieldbackground=BUTTER, background="white")


# usernameentry.insert(0, "panna.bartos914@gmail.com")


# ----------Password------------------ #

# Label
password = Label(text="Password:", bg=PINK, highlightthickness=0)
password.grid(column=0, row=3)

# entry
pwentry = Entry(width=17, bg=BUTTER)
pwentry.grid(column=1, row=3)


# generate
gen_pw = Button(text="Generate Password", width=15, bg=BUTTER, command=generate_password)
gen_pw.grid(column=2, row=3)

# search
search = Button(text="Search", width=15, bg=BUTTER, command=find_password, height=1)
search.grid(column=2, row=1)

# add
add = Button(text="Add", width=30, command=save, bg=BLUE)
add.grid(row=4, column=1, columnspan=2)


window.mainloop()
