import tkinter as tk
from tkinter import messagebox
import random
import pyperclip
import json
# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)
    password_list = []
    for char in range(nr_letters):
        password_list.append(random.choice(letters))
    for char in range(nr_symbols):
        password_list.append(random.choice(symbols))
    for char in range(nr_numbers):
        password_list.append(random.choice(numbers))
    random.shuffle(password_list)
    password = "".join(password_list)
    password_input.delete(0, tk.END)
    password_input.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    url = url_input.get().title()
    email = email_input.get()
    password = password_input.get()

    if url == "" or email == "" or password=="":
        messagebox.showerror(title="Error", message="Credentials can't be empty!")
    elif "@" and ".com" not in email:
        messagebox.showerror(title="Error", message="Enter a valid email!")
    else:
        new_data = {
            url: {
                "Email": email,
                "Password": password
            }
        }
        try:
            with open("passwords.json", "r+") as file:
                data = json.load(file)
                data.update(new_data)
                file.seek(0)
                file.truncate()
                json.dump(data, file, indent=4)
        except (json.decoder.JSONDecodeError, FileNotFoundError):
            with open("passwords.json", "w") as file:
                json.dump(new_data, file, indent=4)
        url_input.delete(0, tk.END)
        password_input.delete(0, tk.END)
        toggle_text("Password Saved Successfully✅", "green")
# ---------------------------- LOAD PASSWORD ------------------------------- #
def load_credentials():
    url = url_input.get().title()
    try:
        with open("passwords.json", "r") as data_file:
            data = json.load(data_file)
            email = data[url]["Email"]
            password = data[url]["Password"]
            email_input.delete(0, tk.END)
            email_input.insert(0, email)
            password_input.delete(0, tk.END)
            password_input.insert(0, password)
    except FileNotFoundError:
        messagebox.showerror(title="File Not Found", message="It seems the password save file has been moved or deleted.")
    except KeyError:
        toggle_text("Error! No such entry exists❎", "red")
    
# ---------------------------- TOGGLE CONFIRMATION TEXT ------------------------------- #
def toggle_text(display_text, color):
    confirmation["text"] = display_text
    confirmation["fg"] = color
    window.after(3000, lambda: confirmation.config(text=""))
# ---------------------------- UI SETUP ------------------------------- #

window = tk.Tk()
window.title("Password Manager")
window.config(padx=40, pady=40)

canvas = tk.Canvas(width=200, height=200)
lock_image = tk.PhotoImage(file="logo.png")
canvas.create_image(122, 100, image=lock_image)
canvas.grid(row=0, column=1)

web_text = tk.Label(text="Website:", font=("Times New Roman", 12))
web_text.grid(row=1, column=0)

url_input = tk.Entry(width=33)
url_input.grid(row=1, column=1)
url_input.focus()

search = tk.Button(text="Search", font=("Times New Roman", 12), width=14, command=load_credentials)
search.grid(row=1, column=2)
email_text = tk.Label(text="Email/Username:", font=("Times New Roman", 12))
email_text.grid(row=2, column=0)

email_input = tk.Entry(width=56)
email_input.grid(row=2, column=1, columnspan=2)
email_input.insert(0, "sumitkumar993182@gmail.com")
password_text = tk.Label(text="Password:", font=("Times New Roman", 12))
password_text.grid(row=3, column=0)

password_input = tk.Entry(width=33)
password_input.grid(row=3, column=1)

gen_password_button = tk.Button(text="Generate Password", width=14, font=("Times New Roman", 12), command=generate_password)
gen_password_button.grid(row=3, column=2)

add_button = tk.Button(text="Add", width=37, font=("Times New Roman", 12), command=save_password)
add_button.grid(row=4, column=1, columnspan=2)


confirmation = tk.Label(text="")
confirmation.grid(row=5, column=1, columnspan=3)
window.mainloop()