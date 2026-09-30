import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from datetime import datetime


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="gym_user",
        password="Gym@123",
        database="gym_management"
    )


def open_payments():

    window = tk.Toplevel()
    window.title("Payment Management")
    window.geometry("1100x700")

    selected_payment_id = tk.StringVar()

    # ---------- VALIDATION ----------

    def validate_payment():

        member_id = member_id_entry.get().strip()
        amount = amount_entry.get().strip()
        payment_date = payment_date_entry.get().strip()

        if member_id == "":
            messagebox.showerror(
                "Error",
                "Member ID is required!",
                parent=window
            )
            return False

        if not member_id.isdigit():
            messagebox.showerror(
                "Error",
                "Member ID must be a number!",
                parent=window
            )
            return False

        if int(member_id) <= 0:
            messagebox.showerror(
                "Error",
                "Member ID must be greater than 0!",
                parent=window
            )
            return False

        if amount == "":
            messagebox.showerror(
                "Error",
                "Amount is required!",
                parent=window
            )
            return False

        try:
            amount_value = float(amount)

            if amount_value <= 0:
                messagebox.showerror(
                    "Error",
                    "Amount must be greater than 0!",
                    parent=window
                )
                return False

        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount must be a number!",
                parent=window
            )
            return False

        if payment_date == "":
            messagebox.showerror(
                "Error",
                "Payment Date is required!",
                parent=window
            )
            return False

        try:
            datetime.strptime(
                payment_date,
                "%Y-%m-%d"
            )
        except ValueError:
            messagebox.showerror(
                "Error",
                "Payment Date must be in YYYY-MM-DD format!",
                parent=window
            )
            return False

        return True

    # ---------- CLEAR ----------

    def clear_fields():

        selected_payment_id.set("")

        member_id_entry.delete(0, tk.END)
        amount_entry.delete(0, tk.END)
        payment_date_entry.delete(0, tk.END)
        payment_method_entry.delete(0, tk.END)
        search_entry.delete(0, tk.END)

    # ---------- VIEW ----------

    def view_payments():

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM payments")
            rows = cursor.fetchall()

            for row in rows:
                table.insert("", tk.END, values=row)

            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- SEARCH ----------

    def search_payment():

        search_text = search_entry.get().strip()

        if search_text == "":
            view_payments()
            return

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            SELECT * FROM payments
            WHERE member_id LIKE %s
            OR payment_method LIKE %s
            """

            value = "%" + search_text + "%"

            cursor.execute(
                query,
                (value, value)
            )

            rows = cursor.fetchall()

            for row in rows:
                table.insert("", tk.END, values=row)

            cursor.close()
            connection.close()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- ADD ----------

    def add_payment():

        if not validate_payment():
            return

        member_id = member_id_entry.get().strip()
        amount = amount_entry.get().strip()
        payment_date = payment_date_entry.get().strip()
        payment_method = payment_method_entry.get().strip()

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            INSERT INTO payments
            (member_id, amount, payment_date, payment_method)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                int(member_id),
                float(amount),
                payment_date,
                payment_method
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Payment added successfully!",
                parent=window
            )

            clear_fields()
            view_payments()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- SELECT ----------

    def select_payment(event):

        selected = table.focus()

        if selected == "":
            return

        values = table.item(selected, "values")

        if not values:
            return

        selected_payment_id.set(values[0])

        member_id_entry.delete(0, tk.END)
        member_id_entry.insert(0, values[1])

        amount_entry.delete(0, tk.END)
        amount_entry.insert(0, values[2])

        payment_date_entry.delete(0, tk.END)
        payment_date_entry.insert(0, values[3])

        payment_method_entry.delete(0, tk.END)
        payment_method_entry.insert(0, values[4])

    # ---------- UPDATE ----------

    def update_payment():

        payment_id = selected_payment_id.get()

        if payment_id == "":
            messagebox.showerror(
                "Error",
                "Select a payment from the table first!",
                parent=window
            )
            return

        if not validate_payment():
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            UPDATE payments
            SET member_id=%s,
                amount=%s,
                payment_date=%s,
                payment_method=%s
            WHERE payment_id=%s
            """

            values = (
                int(member_id_entry.get().strip()),
                float(amount_entry.get().strip()),
                payment_date_entry.get().strip(),
                payment_method_entry.get().strip(),
                payment_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Payment updated successfully!",
                parent=window
            )

            clear_fields()
            view_payments()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- DELETE ----------

    def delete_payment():

        payment_id = selected_payment_id.get()

        if payment_id == "":
            messagebox.showerror(
                "Error",
                "Select a payment from the table first!",
                parent=window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this payment?",
            parent=window
        )

        if not confirm:
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM payments WHERE payment_id=%s"

            cursor.execute(query, (payment_id,))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Payment deleted successfully!",
                parent=window
            )

            clear_fields()
            view_payments()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- TITLE ----------

    title = tk.Label(
        window,
        text="PAYMENT MANAGEMENT",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=15)

    # ---------- SEARCH ----------

    search_frame = tk.Frame(window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Search Payment:"
    ).pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(
        search_frame,
        width=30
    )
    search_entry.pack(side=tk.LEFT, padx=5)

    tk.Button(
        search_frame,
        text="Search",
        width=12,
        command=search_payment
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=view_payments
    ).pack(side=tk.LEFT, padx=5)

    # ---------- FORM ----------

    form = tk.Frame(window)
    form.pack(pady=15)

    tk.Label(
        form,
        text="Member ID"
    ).grid(row=0, column=0, padx=10, pady=8)

    member_id_entry = tk.Entry(
        form,
        width=25
    )
    member_id_entry.grid(row=0, column=1)

    tk.Label(
        form,
        text="Amount"
    ).grid(row=0, column=2, padx=10)

    amount_entry = tk.Entry(
        form,
        width=25
    )
    amount_entry.grid(row=0, column=3)

    tk.Label(
        form,
        text="Payment Date (YYYY-MM-DD)"
    ).grid(row=1, column=0, padx=10, pady=8)

    payment_date_entry = tk.Entry(
        form,
        width=25
    )
    payment_date_entry.grid(row=1, column=1)

    tk.Label(
        form,
        text="Payment Method"
    ).grid(row=1, column=2, padx=10)

    payment_method_entry = tk.Entry(
        form,
        width=25
    )
    payment_method_entry.grid(row=1, column=3)

    # ---------- BUTTONS ----------

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Payment",
        width=15,
        command=add_payment
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update Payment",
        width=15,
        command=update_payment
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete Payment",
        width=15,
        command=delete_payment
    ).grid(row=0, column=2, padx=5)

    tk.Button(
        button_frame,
        text="Clear",
        width=15,
        command=clear_fields
    ).grid(row=0, column=3, padx=5)

    tk.Button(
        button_frame,
        text="Refresh",
        width=15,
        command=view_payments
    ).grid(row=0, column=4, padx=5)

    # ---------- TABLE ----------

    columns = (
        "Payment ID",
        "Member ID",
        "Amount",
        "Payment Date",
        "Payment Method"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=180)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    table.bind(
        "<ButtonRelease-1>",
        select_payment
    )

    view_payments()