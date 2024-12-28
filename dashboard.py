import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from database import create_user, get_user, record_transaction, get_transaction_history, get_balance, update_balance


# Database Operations


def open_dashboard(username):
    user = get_user(username)
    user_id = user[0]  # Assuming the first column is the user ID

    def show_balance():
        # Clear previous widgets
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Fetch updated user data
        updated_user = get_user(username)

        # Main balance frame
        balance_frame = tk.Frame(right_frame, bg="#F4F9FF", bd=2, relief="flat")
        balance_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Header Section
        header_frame = tk.Frame(balance_frame, bg="#0D47A1", height=70)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Account Balance",
            font=("Poppins", 24, "bold"),
            fg="white",
            bg="#0D47A1",
            anchor="w",
            padx=20,
        )
        header_label.pack(side="left", pady=15)

        # Content Section
        content_frame = tk.Frame(balance_frame, bg="white", bd=2, relief="solid")
        content_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.65)

        # Display current balance
        balance_label = tk.Label(
            content_frame,
            text=f"{updated_user[6]:,.2f}",
            font=("Poppins", 36, "bold"),
            fg="#4CAF50",
            bg="white",
        )
        balance_label.pack(pady=20)

        # Subtext for balance
        balance_subtext = tk.Label(
            content_frame,
            text="Your current available balance",
            font=("Poppins", 14),
            fg="#888888",
            bg="white",
        )
        balance_subtext.pack(pady=5)

        # Separator for styling
        separator = tk.Frame(content_frame, bg="#DDDDDD", height=2, bd=0, relief="flat")
        separator.pack(fill="x", pady=20)

        # Fetch and display recent transactions
        transactions = get_transaction_history(updated_user[0])  # Fetch transactions using user ID
        recent_transactions = transactions[-1:]  # Get the last 3 transactions
        print(recent_transactions)

        # Recent transactions header
        history_title_label = tk.Label(
            content_frame,
            text="Recent Transactions",
            font=("Poppins", 16, "bold"),
            fg="#1E88E5",
            bg="white",
        )
        history_title_label.pack(pady=0)

        # Container for transaction history
        transactions_frame = tk.Frame(content_frame, bg="white")
        transactions_frame.pack(fill="both", expand=True, padx=10)

        if recent_transactions:
            for transaction in recent_transactions:
                date = transaction[5]  # Transaction date
                description = transaction[4]  # Description
                amount = transaction[3]  # Amount
                if amount >= 0:
                    amount_color = "#4CAF50"
                else:
                    amount_color = "#E53935"  # Positive or negative color

                # Transaction item
                transaction_item = tk.Frame(transactions_frame, bg="#F9F9F9", pady=5, padx=10, relief="flat")
                transaction_item.pack(fill="x", pady=5)

                # Transaction details
                tk.Label(
                    transaction_item,
                    text=date,
                    font=("Poppins", 10),
                    fg="#888888",
                    bg="#F9F9F9",
                    anchor="w",
                ).grid(row=0, column=0, sticky="w")
                tk.Label(
                    transaction_item,
                    text=description,
                    font=("Poppins", 12),
                    fg="#333333",
                    bg="#F9F9F9",
                    anchor="w",
                ).grid(row=1, column=0, sticky="w")
                tk.Label(
                    transaction_item,
                    text=f"${amount:,.2f}",
                    font=("Poppins", 12, "bold"),
                    fg=amount_color,
                    bg="#F9F9F9",
                    anchor="e",
                ).grid(row=1, column=1, sticky="e")
        else:
            # No transactions message
            no_transactions_label = tk.Label(
                transactions_frame,
                text="No recent transactions",
                font=("Poppins", 12),
                fg="#888888",
                bg="white",
            )
            no_transactions_label.pack(pady=20)

        # Back button


    def show_transaction_history():
        # Clear previous widgets
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Create main frame for transaction history
        history_frame = tk.Frame(right_frame, bg="#EAF6FF", bd=2, relief="flat")
        history_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Header Section
        header_frame = tk.Frame(history_frame, bg="#0D47A1", height=70)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Transaction History",
            font=("Poppins", 24, "bold"),
            fg="white",
            bg="#0D47A1",
            anchor="w",
            padx=20,
        )
        header_label.pack(side="left", pady=15)

        # Transactions Frame
        transactions_frame = tk.Frame(history_frame, bg="#FFFFFF", bd=2, relief="solid")
        transactions_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.65)

        # Create a Treeview widget
        style = ttk.Style()
        style.configure(
            "Treeview",
            font=("Poppins", 12),
            rowheight=30,
            background="#FAFAFA",
            fieldbackground="#FAFAFA",
            foreground="#333333",
        )
        style.configure(
            "Treeview.Heading",
            font=("Poppins", 14, "bold"),
            background="#0D47A1",
            foreground="black",
        )

        tree = ttk.Treeview(
            transactions_frame,
            columns=("Date", "Description", "Amount"),
            show="headings",
            height=10,
        )
        tree.heading("Date", text="Date")
        tree.heading("Description", text="Description")
        tree.heading("Amount", text="Amount")

        # Set column properties
        tree.column("Date", anchor="center", width=150)
        tree.column("Description", anchor="w", width=300)
        tree.column("Amount", anchor="center", width=150)

        # Fetch transaction history
        transactions = get_transaction_history(user_id)

        # Insert transaction data into the Treeview
        for transaction in transactions:
            # Ensure indices match your database schema
            date = transaction[4]  # Adjust index if necessary
            description = transaction[4]
            amount = transaction[3]
            tree.insert("", "end", values=(date, description, f"${amount:,.2f}"))

        # Add a vertical scrollbar
        scrollbar = ttk.Scrollbar(
            transactions_frame, orient="vertical", command=tree.yview
        )
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(pady=10, padx=10, fill="both", expand=True)

        # Back Button

    def transfer_funds():
        # Clear previous widgets
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Main Transfer Frame
        transfer_frame = tk.Frame(right_frame, bg="#EAF6FF", bd=2, relief="flat")
        transfer_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Header Section
        header_frame = tk.Frame(transfer_frame, bg="#0D47A1", height=70)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Transfer Funds",
            font=("Poppins", 24, "bold"),
            fg="white",
            bg="#0D47A1",
            anchor="w",
            padx=20,
        )
        header_label.pack(side="left", pady=15)

        # Transfer Form
        form_frame = tk.Frame(transfer_frame, bg="#FFFFFF", bd=2, relief="solid")
        form_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.65)

        # Recipient Account Entry
        tk.Label(
            form_frame,
            text="Recipient Account Number:",
            font=("Poppins", 16),
            bg="#FFFFFF",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=15)
        recipient_entry = tk.Entry(
            form_frame, font=("Poppins", 14), width=40, bd=2, relief="solid"
        )
        recipient_entry.pack(pady=5, padx=20)

        # Amount to Transfer Entry
        tk.Label(
            form_frame,
            text="Amount to Transfer:",
            font=("Poppins", 16),
            bg="#FFFFFF",
            fg="#333333",
        ).pack(anchor="w", padx=20, pady=15)
        amount_entry = tk.Entry(
            form_frame, font=("Poppins", 14), width=40, bd=2, relief="solid"
        )
        amount_entry.pack(pady=5, padx=20)

        # Function to Perform Transfer
        def perform_transfer():
            recept = recipient_entry.get()
            amount = amount_entry.get()
            if not amount.strip().isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
                return

            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
                return

            # Perform payment logic
            update_balance(user_id, -amount)  # Deduct amount from user's account
            record_transaction(
                user_id,
                amount,
                "transfer",
                f"Paid {recept}",
            )  # Record the transaction
            messagebox.showinfo(
                title="Payment Successful",
                message=f"Successfully paid ${amount:,.2f} for {recept}.",
            )
        # Transfer Button
        transfer_button = tk.Button(
            transfer_frame,
            text="Transfer",
            font=("Poppins", 15, "bold"),
            bg="#1B5E20",
            fg="black",
            width=15,
            relief="flat",
            cursor="hand2",
            command=perform_transfer,
        )
        transfer_button.place(relx=0.3, rely=0.9)



    def pay_bills():
        # Clear the right_frame
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Main Frame for Bill Payment
        bill_frame = tk.Frame(right_frame, bg="#EAF6FF", bd=2, relief="flat")
        bill_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Header Section
        header_frame = tk.Frame(bill_frame, bg="#0D47A1", height=70)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Pay Bills",
            font=("Poppins", 24, "bold"),
            fg="white",
            bg="#0D47A1",
            anchor="w",
            padx=20,
        )
        header_label.pack(side="left", pady=15)

        # Content Section
        content_frame = tk.Frame(bill_frame, bg="white", bd=2, relief="solid")
        content_frame.place(relx=0.05, rely=0.2, relwidth=0.9, relheight=0.65)

        # Utility Selection
        tk.Label(
            content_frame,
            text="Select Utility:",
            font=("Poppins", 14),
            bg="white",
            fg="black",
        ).place(relx=0.05, rely=0.1)

        utilities = ["Electricity", "Water", "Internet", "Gas"]
        utility_var = tk.StringVar(content_frame)
        utility_var.set(utilities[0])
        utility_dropdown = tk.OptionMenu(content_frame, utility_var, *utilities)
        utility_dropdown.config(
            font=("Poppins", 12),
            width=20,
            relief="flat",
            bg="black",
            fg="white",
        )
        utility_dropdown.place(relx=0.35, rely=0.10, width=250)

        # Bill Amount Entry
        tk.Label(
            content_frame,
            text="Amount to Pay:",
            font=("Poppins", 14),
            bg="white",
            fg="black",
        ).place(relx=0.05, rely=0.3)

        bill_amount_entry = tk.Entry(
            content_frame,
            font=("Poppins", 12),
            width=30,
            bd=2,
            relief="solid",
            bg="black",
            fg="white",
        )
        bill_amount_entry.place(relx=0.35, rely=0.28)

        # Perform Payment Function
        def perform_payment():
            utility = utility_var.get()
            amount = bill_amount_entry.get()
            if not amount.strip().isdigit():
                messagebox.showerror("Invalid Input", "Please enter a valid amount.")
                return

            amount = float(amount)
            if amount <= 0:
                messagebox.showerror("Invalid Amount", "Amount must be greater than zero.")
                return

            # Perform payment logic
            update_balance(username, -amount)  # Deduct amount from user's account
            record_transaction(
                user_id,
                amount,
                "bill_payment",
                f"Paid {utility}",
            )  # Record the transaction
            messagebox.showinfo(
                title="Payment Successful",
                message=f"Successfully paid ${amount:,.2f} for {utility}.",
            )


        # Pay Button


        # Back Button
        back_button = tk.Button(
            bill_frame,
            text="Pay",
            font=("Poppins", 15, "bold"),
            bg="#1B5E20",
            fg="black",
            width=15,
            relief="flat",
            cursor="hand2",
            command=perform_payment,
        )
        back_button.place(relx=0.3, rely=0.9)

    def manage_profile():
        # Clear previous widgets
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Fetch updated user data
        updated_user = get_user(username)

        # Main Profile Frame
        profile_frame = tk.Frame(right_frame, bg="#EAF6FF", bd=2, relief="flat")
        profile_frame.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Header Section
        header_frame = tk.Frame(profile_frame, bg="#0D47A1", height=70)
        header_frame.pack(fill="x")

        header_label = tk.Label(
            header_frame,
            text="Account Profile",
            font=("Poppins", 24, "bold"),
            fg="white",
            bg="#0D47A1",
            anchor="w",
            padx=20,
        )
        header_label.pack(side="left", pady=15)

        # Profile Card
        profile_card = tk.Frame(profile_frame, bg="#FFFFFF", bd=2, relief="solid")
        profile_card.place(relx=0.05, rely=0.19, relwidth=0.9, relheight=0.7)

        # Account Details Section
        details_frame = tk.Frame(profile_card, bg="#F9FAFB")
        details_frame.place(relx=0.05, rely=0, relwidth=0.9, relheight=1)

        profile_details = {
            "Account Holder": updated_user[3],
            "Email": updated_user[4],
            "Phone Number": updated_user[5],
            "Account Balance": f"{updated_user[6]:,.2f}",
        }

        for label, value in profile_details.items():
            tk.Label(
                details_frame,
                text=f"{label}:",
                font=("Poppins", 16, "bold"),
                bg="#F9FAFB",
                fg="#555555",
            ).pack(anchor="w", padx=15, pady=8)
            tk.Label(
                details_frame,
                text=value,
                font=("Poppins", 14),
                bg="#F9FAFB",
                fg="#333333",
            ).pack(anchor="w", padx=30)

        # Back Button

    dashboard = tk.Tk()
    dashboard.title("User  Dashboard")
    dashboard.geometry("800x450+383+106")
    dashboard.resizable(0, 0)
    dashboard.configure(background="#023047")

    left_frame = tk.Frame(dashboard, bg="#023047", width=300, height=450)
    left_frame.pack(side="left", fill="y")

    right_frame = tk.Frame(dashboard, bg="#023047", width=500, height=450)
    right_frame.pack(side="right", fill="both", expand=True)

    dashboard_image = Image.open("images/dashboard.webp")
    dashboard_image = dashboard_image.resize((900, 450))
    dashboard_photo = ImageTk.PhotoImage(dashboard_image)

    bg_label = tk.Label(right_frame, image=dashboard_photo)
    bg_label.image = dashboard_photo
    bg_label.place(relwidth=1, relheight=1)

    welcome_label = tk.Label(left_frame, text=f"Welcome, {user[3 ]}!",
                              font=("Helvetica", 16, "bold"), fg="blue", bg="#023047")
    welcome_label.pack(anchor="nw", padx=10, pady=10)

    tk.Button(left_frame, text="View Balance", font=("Helvetica", 12, "bold"),
              bg="white", fg="black", width=20, command=show_balance).pack(pady=10)

    tk.Button(left_frame, text="Transaction History", font=("Helvetica", 12, "bold"),
              bg="white", fg="black", width=20, command=show_transaction_history).pack(pady=10)

    tk.Button(left_frame, text="Transfer Funds", font=("Helvetica", 12, "bold"),
              bg="white", fg="black", width=20, command=transfer_funds).pack(pady=10)

    tk.Button(left_frame, text="Pay Bills", font=("Helvetica", 12, "bold"),
              bg="white", fg="black", width=20, command=pay_bills).pack(pady=10)

    tk.Button(left_frame, text="Profile", font=("Helvetica", 12, "bold"),
              bg="white", fg="black", width=20, command=manage_profile).pack(pady=10)

    tk.Button(left_frame, text="Logout", font=("Helvetica", 12, "bold"),
              bg="red", fg="black", width=20, command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()

# #Run independently for testing
# if __name__ == "__main__":
#     open_dashboard("Sheezzi")