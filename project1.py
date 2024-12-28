import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

import dashboard  # Import the dashboard module
from database import db_connection


# Authenticate user
def authentication():
    username = username_entry.get()
    password = password_entry.get()

    query = "SELECT username, password FROM users WHERE username = %s"
    conn = db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, (username,))
        res = cursor.fetchone()

        if res:
            db_username, db_password = res
            if db_username == username and str(db_password) == password:
                print(f"Welcome {username}")
                root.destroy()  # Close the login window
                dashboard.open_dashboard(username)  # Open the dashboard
            else:
                messagebox.showerror(title='Invalid',message='Invalid username or password!')
        else:
            messagebox.showerror(title='Not found',message='User not found')
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

# Create the main window
root = tk.Tk()
root.title("WELCOME SIMULATION BANK")
root.geometry("800x450+383+106")
root.resizable(0, 0)
root.configure(background="#023047")

# Add the title
title = tk.Label(root, text="SIMULATION BANK",
                 font=("Helvetica", 28, "bold"), fg="blue", bg="#023047")
title.place(x=50, y=20)

# Add username label and entry
username_label = tk.Label(root, text="Enter Your Username", font=("Helvetica", 12), bg="#023047")
username_label.place(x=50, y=100)
username_entry = tk.Entry(root, width=30, font=("Helvetica", 12), bd=2, fg='yellow')
username_entry.place(x=50, y=130)

# Add password label and entry
password_label = tk.Label(root, text="Enter Your Password", font=("Helvetica", 12), bg="#023047")
password_label.place(x=50, y=180)
password_entry = tk.Entry(root, width=30, font=("Helvetica", 12), bd=2, show="*", fg='yellow')
password_entry.place(x=50, y=210)

# Add login button
login_button = tk.Button(root, text="Login", font=("Helvetica", 12, "bold"),
                         bg="white", fg="black", width=20, command=authentication)
login_button.place(x=70, y=260)

# Add an image on the right
try:
    image_path = "images/logo.png"  # Update this path to your image file
    image = Image.open(image_path).resize((420, 447))
    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(root, image=image_tk, bg="#023047")
    image_label.place(x=380, y=0)
except Exception as e:
    print(f"Error loading image: {e}")

# Run the application
root.mainloop()
