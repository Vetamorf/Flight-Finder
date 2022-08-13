import requests
from tkinter import *
from tkinter import messagebox

# File is responsible for talking to the Google Sheets Users and for UI

GOOGLE_SHEETS_USERS_API = "https://api.sheety.co/b9a158d10c51bfedf429994dde934a01/pythonFlightDeals2/users"
emails = []


def fetch_emails():
    response = requests.get(url=GOOGLE_SHEETS_USERS_API)
    response.raise_for_status()

    users_data = response.json()['users']
    emails_list = []
    for user in users_data:
        emails_list.append(user['email'])
    return emails_list


def join_club():
    global emails
    first_name = f_name_entry.get()
    last_name = s_name_entry.get()
    email = email_entry.get().strip()
    email_second_time = email_confirm_entry.get().strip()

    if email == email_second_time:
        if '@' in email and '.' in email:
            emails = fetch_emails()

            if email in emails:
                messagebox.showinfo(title="You're in the Club",
                                    message="You're already in the Club!"
                                            "\nWe'll email you about the best flight deals.")
                window.destroy()
            else:
                emails.append(email)

                body = {
                    'user': {
                        'firstName': first_name,
                        'lastName': last_name,
                        'email': email,
                    }
                }
                post_response = requests.post(url=GOOGLE_SHEETS_USERS_API, json=body)
                post_response.raise_for_status()

                messagebox.showinfo(title="You're in the Club",
                                    message="Registration was successful. You're in the Club now!")
                window.destroy()
        else:
            messagebox.showinfo(title='Error', message="Invalid email format")
    else:
        messagebox.showinfo(title='Error', message="Emails doesn't match. Please try again.")


def already_in_club():
    global emails
    emails = fetch_emails()

    messagebox.showinfo(title="Welcome back!",
                        message="\nWe'll email you about the best flight deals.")
    window.destroy()


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Personal Information')
window.config(padx=50, pady=50)
window.config(background='#EAF6F6')


# Labels

welcome_label = Label(text='Welcome to the Flight Club!', background='#EAF6F6',
                      font=('Arial', 12, "bold"), foreground='#56708a')
welcome_label.grid(column=0, columnspan=3, row=0)

welcome_2_label = Label(text='We find the best flight deals and email you', background='#EAF6F6',
                        font=('Arial', 12, ""), foreground='#56708a')
welcome_2_label.grid(column=0, columnspan=3, row=1, pady=20)


f_name_label = Label(text='First name:', pady=2, background='#EAF6F6')
f_name_label.grid(column=0, row=2, sticky=W)

s_name_label = Label(text='Second name:', pady=2, background='#EAF6F6')
s_name_label.grid(column=0, row=3, sticky=W)

email_label = Label(text='Email:', pady=2, background='#EAF6F6')
email_label.grid(column=0, row=4, sticky=W)

email_confirm_label = Label(text='Confirm email:', pady=2, background='#EAF6F6')
email_confirm_label.grid(column=0, row=5, sticky=W)

# Entries
f_name_entry = Entry(width=38)
f_name_entry.focus()
f_name_entry.grid(row=2, column=1, columnspan=2, sticky=W, pady=5)

s_name_entry = Entry(width=38)
s_name_entry.grid(row=3, column=1, columnspan=2, sticky=W, pady=5)

email_entry = Entry(width=38)
email_entry.grid(row=4, column=1, columnspan=2, sticky=W, pady=5)

email_confirm_entry = Entry(width=38)
email_confirm_entry.grid(row=5, column=1, columnspan=2, sticky=W, pady=5)

# Buttons

add_button = Button(text='Join the Club', width=32, command=join_club,
                    background='#97a8ba', activebackground='#56708a')
add_button.grid(row=6, column=1, columnspan=2, sticky=W, pady=10)


add_button = Button(text="I'm already in the Club", width=32, command=already_in_club,
                    background='#97a8ba', activebackground='#56708a')
add_button.grid(row=7, column=1, columnspan=2, sticky=W, pady=2)


window.mainloop()
