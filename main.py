from tkinter import *
import random
import string
from tkinter import messagebox
import json
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def password_maker():
    list_of_characters = string.printable
    password = random.choices(list_of_characters, k=12)
    password = ''.join(password)
    entry_password.insert(0, password)
    return password


# ---------------------------- SAVE PASSWORD ------------------------------- #


def file_save():
    data_json = {entry_website.get(): {
        "email": entry_email.get(),
        "password": entry_password.get()}}

    if len(entry_email.get()) == 0 or len(entry_password.get()) == 0 or len(entry_website.get()) == 0:
        empty_message = messagebox.showwarning(title=f"Warning!",
                                               message=f"Website: {entry_website.get()}"
                                                       f"\nEmail: {entry_email.get()}"
                                                       f"\nPassword: {entry_password.get()} \n empty places! ")

    else:
        correctness = messagebox.askyesno(title=f"{entry_password.get()}", message=f"Is it correct:\nEmail: "
                                                                                   f"{entry_email.get()}"
                                                                                   f"\nPassword: {entry_password.get()}"
                                                                                   f"\n Do you want to save?")
        if correctness == True:
            # checking emptiness file
            with open('passes.json', 'r') as file:
                reading = file.read()
            with open('passes.json', 'w') as file:
                if reading == "":
                    json.dump(data_json, file, indent=4)

                else:
                    # loading json
                    passes_data_json = json.loads(reading)
                    # update json
                    passes_data_json.update(data_json)
                    # writing json
                    json.dump(passes_data_json, file, indent=4)

            # file.write(f"\n{entry_website.get()}")
            # file.write(" | ")
            # file.write(entry_email.get())
            # file.write(" | ")
            # file.write(entry_password.get())

            entry_website.delete(0, 'end')
            entry_password.delete(0, 'end')
            entry_website.focus()
        return

# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    with open('passes.json', 'r') as file:
        data = json.load(file)
        if entry_website.get() in data:
            pyperclip.copy(data[entry_website.get()]['password'])
            available_message = messagebox.showinfo(title=f'{entry_website.get()}',
                                                    message=f"Your email: {data[entry_website.get()]['email']}\n"
                                                            f"Your password:  "
                                                            f"{data[entry_website.get()]['password']}")

        else:
            pass

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password manager")
window.config(padx=20, pady=20, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock_image = PhotoImage(file='padlock.png')
canvas.create_image(80, 100, image=lock_image)
canvas.grid(row=0, column=1)

label_website = Label(text="Website", bg="white", font=("Courier"))
label_website.grid(row=1, column=0)

entry_website = Entry(width=30)
entry_website.focus()
entry_website.grid(row=1, column=1, columnspan=2, sticky="W", padx=45)

label_email = Label(text="Email/Username", bg="white", font="Courier")
label_email.grid(row=2, column=0)

entry_email = Entry(width=35)
entry_email.insert(0, "@gmail.com")
entry_email.grid(row=2, column=1, columnspan=2)

label_password = Label(text="Password", bg="white", font="Courier")
label_password.grid(row=3, column=0)

entry_password = Entry(width=24)
entry_password.grid(row=3, column=1, sticky="E", padx=5)

generate_password_button = Button(text="Generate Password", bg="#EAEAEA", border=0, command=password_maker)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=65, bg="#EAEAEA", border=0, command=file_save)
add_button.grid(row=4, column=0, columnspan=3, pady=10)

search_button = Button(text="Search", bg="#EAEAEA", border=0, command=find_password)
search_button.grid(row=1, column=2, pady=10, ipadx=10, padx=5, sticky="E")

window.mainloop()
