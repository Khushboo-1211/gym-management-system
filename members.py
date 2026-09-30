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


def open_members():

    window = tk.Toplevel()
    window.title("Member Management")
    window.geometry("1250x750")

    selected_member_id = tk.StringVar()

    # ---------- VALIDATION FUNCTIONS ----------

    def valid_date(date_text):
        if date_text == "":
            return True

        try:
            datetime.strptime(date_text, "%Y-%m-%d")
            return True
        except ValueError:
            return False

    def valid_phone(phone):
        return phone.isdigit() and 10 <= len(phone) <= 15

    def valid_email(email):
        if email == "":
            return True

        return "@" in email and "." in email

    # ---------- CLEAR FIELDS ----------

    def clear_fields():

        selected_member_id.set("")

        name_entry.delete(0, tk.END)
        age_entry.delete(0, tk.END)
        gender_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        plan_entry.delete(0, tk.END)
        join_date_entry.delete(0, tk.END)
        expiry_date_entry.delete(0, tk.END)

        search_entry.delete(0, tk.END)

    # ---------- VIEW MEMBERS ----------

    def view_members():

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM members")
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

    # ---------- SEARCH MEMBER ----------

    def search_member():

        search_text = search_entry.get()

        if search_text == "":
            view_members()
            return

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            SELECT * FROM members
            WHERE name LIKE %s
            OR phone LIKE %s
            OR email LIKE %s
            """

            value = "%" + search_text + "%"

            cursor.execute(
                query,
                (value, value, value)
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

    # ---------- VALIDATE MEMBER DATA ----------

    def validate_member_data():

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        join_date = join_date_entry.get().strip()
        expiry_date = expiry_date_entry.get().strip()

        if name == "":
            messagebox.showerror(
                "Error",
                "Name is required!",
                parent=window
            )
            return False

        if phone == "":
            messagebox.showerror(
                "Error",
                "Phone number is required!",
                parent=window
            )
            return False

        if age != "" and not age.isdigit():
            messagebox.showerror(
                "Error",
                "Age must be a number!",
                parent=window
            )
            return False

        if age != "" and (int(age) < 1 or int(age) > 100):
            messagebox.showerror(
                "Error",
                "Please enter a valid age between 1 and 100!",
                parent=window
            )
            return False

        if not valid_phone(phone):
            messagebox.showerror(
                "Error",
                "Phone must contain 10 to 15 digits!",
                parent=window
            )
            return False

        if not valid_email(email):
            messagebox.showerror(
                "Error",
                "Please enter a valid email address!",
                parent=window
            )
            return False

        if not valid_date(join_date):
            messagebox.showerror(
                "Error",
                "Join Date must be in YYYY-MM-DD format!",
                parent=window
            )
            return False

        if not valid_date(expiry_date):
            messagebox.showerror(
                "Error",
                "Expiry Date must be in YYYY-MM-DD format!",
                parent=window
            )
            return False

        if join_date != "" and expiry_date != "":
            join = datetime.strptime(
                join_date,
                "%Y-%m-%d"
            )

            expiry = datetime.strptime(
                expiry_date,
                "%Y-%m-%d"
            )

            if expiry < join:
                messagebox.showerror(
                    "Error",
                    "Expiry Date cannot be before Join Date!",
                    parent=window
                )
                return False

        return True

    # ---------- ADD MEMBER ----------

    def add_member():

        if not validate_member_data():
            return

        name = name_entry.get().strip()
        age = age_entry.get().strip()
        gender = gender_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()
        plan = plan_entry.get().strip()
        join_date = join_date_entry.get().strip()
        expiry_date = expiry_date_entry.get().strip()

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            INSERT INTO members
            (name, age, gender, phone, email,
             membership_plan, join_date, expiry_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                name,
                age if age != "" else None,
                gender,
                phone,
                email,
                plan,
                join_date if join_date != "" else None,
                expiry_date if expiry_date != "" else None
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Member added successfully!",
                parent=window
            )

            clear_fields()
            view_members()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- SELECT MEMBER ----------

    def select_member(event):

        selected = table.focus()

        if selected == "":
            return

        values = table.item(selected, "values")

        if not values:
            return

        selected_member_id.set(values[0])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        age_entry.delete(0, tk.END)
        age_entry.insert(0, values[2])

        gender_entry.delete(0, tk.END)
        gender_entry.insert(0, values[3])

        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, values[4])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[5])

        plan_entry.delete(0, tk.END)
        plan_entry.insert(0, values[6])

        join_date_entry.delete(0, tk.END)
        join_date_entry.insert(0, values[7])

        expiry_date_entry.delete(0, tk.END)
        expiry_date_entry.insert(0, values[8])

    # ---------- UPDATE MEMBER ----------

    def update_member():

        member_id = selected_member_id.get()

        if member_id == "":
            messagebox.showerror(
                "Error",
                "Select a member from the table first!",
                parent=window
            )
            return

        if not validate_member_data():
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            UPDATE members
            SET name=%s,
                age=%s,
                gender=%s,
                phone=%s,
                email=%s,
                membership_plan=%s,
                join_date=%s,
                expiry_date=%s
            WHERE member_id=%s
            """

            age = age_entry.get().strip()
            join_date = join_date_entry.get().strip()
            expiry_date = expiry_date_entry.get().strip()

            values = (
                name_entry.get().strip(),
                age if age != "" else None,
                gender_entry.get().strip(),
                phone_entry.get().strip(),
                email_entry.get().strip(),
                plan_entry.get().strip(),
                join_date if join_date != "" else None,
                expiry_date if expiry_date != "" else None,
                member_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Member updated successfully!",
                parent=window
            )

            clear_fields()
            view_members()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- DELETE MEMBER ----------

    def delete_member():

        member_id = selected_member_id.get()

        if member_id == "":
            messagebox.showerror(
                "Error",
                "Select a member from the table first!",
                parent=window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this member?",
            parent=window
        )

        if not confirm:
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM members WHERE member_id=%s"

            cursor.execute(query, (member_id,))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Member deleted successfully!",
                parent=window
            )

            clear_fields()
            view_members()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- TITLE ----------

    title = tk.Label(
        window,
        text="MEMBER MANAGEMENT",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=15)

    # ---------- SEARCH ----------

    search_frame = tk.Frame(window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Search Member:"
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
        command=search_member
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=view_members
    ).pack(side=tk.LEFT, padx=5)

    # ---------- FORM ----------

    form = tk.Frame(window)
    form.pack(pady=10)

    tk.Label(
        form,
        text="Name"
    ).grid(row=0, column=0, padx=10, pady=6)

    name_entry = tk.Entry(
        form,
        width=25
    )
    name_entry.grid(row=0, column=1)

    tk.Label(
        form,
        text="Age"
    ).grid(row=0, column=2, padx=10)

    age_entry = tk.Entry(
        form,
        width=25
    )
    age_entry.grid(row=0, column=3)

    tk.Label(
        form,
        text="Gender"
    ).grid(row=1, column=0, padx=10, pady=6)

    gender_entry = tk.Entry(
        form,
        width=25
    )
    gender_entry.grid(row=1, column=1)

    tk.Label(
        form,
        text="Phone"
    ).grid(row=1, column=2, padx=10)

    phone_entry = tk.Entry(
        form,
        width=25
    )
    phone_entry.grid(row=1, column=3)

    tk.Label(
        form,
        text="Email"
    ).grid(row=2, column=0, padx=10, pady=6)

    email_entry = tk.Entry(
        form,
        width=25
    )
    email_entry.grid(row=2, column=1)

    tk.Label(
        form,
        text="Membership Plan"
    ).grid(row=2, column=2, padx=10)

    plan_entry = tk.Entry(
        form,
        width=25
    )
    plan_entry.grid(row=2, column=3)

    tk.Label(
        form,
        text="Join Date (YYYY-MM-DD)"
    ).grid(row=3, column=0, padx=10, pady=6)

    join_date_entry = tk.Entry(
        form,
        width=25
    )
    join_date_entry.grid(row=3, column=1)

    tk.Label(
        form,
        text="Expiry Date (YYYY-MM-DD)"
    ).grid(row=3, column=2, padx=10)

    expiry_date_entry = tk.Entry(
        form,
        width=25
    )
    expiry_date_entry.grid(row=3, column=3)

    # ---------- BUTTONS ----------

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Member",
        width=15,
        command=add_member
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update Member",
        width=15,
        command=update_member
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete Member",
        width=15,
        command=delete_member
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
        command=view_members
    ).grid(row=0, column=4, padx=5)

    # ---------- TABLE ----------

    columns = (
        "ID",
        "Name",
        "Age",
        "Gender",
        "Phone",
        "Email",
        "Plan",
        "Join Date",
        "Expiry Date"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=125)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    table.bind(
        "<ButtonRelease-1>",
        select_member
    )

    view_members()