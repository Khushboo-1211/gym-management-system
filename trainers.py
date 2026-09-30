import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="gym_user",
        password="Gym@123",
        database="gym_management"
    )


def open_trainers():

    window = tk.Toplevel()
    window.title("Trainer Management")
    window.geometry("1100x700")

    selected_trainer_id = tk.StringVar()

    # ---------- VALIDATION ----------

    def validate_trainer():

        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        salary = salary_entry.get().strip()

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

        if not phone.isdigit() or not (10 <= len(phone) <= 15):
            messagebox.showerror(
                "Error",
                "Phone must contain 10 to 15 digits!",
                parent=window
            )
            return False

        if salary == "":
            messagebox.showerror(
                "Error",
                "Salary is required!",
                parent=window
            )
            return False

        try:
            salary_value = float(salary)

            if salary_value < 0:
                messagebox.showerror(
                    "Error",
                    "Salary cannot be negative!",
                    parent=window
                )
                return False

        except ValueError:
            messagebox.showerror(
                "Error",
                "Salary must be a number!",
                parent=window
            )
            return False

        return True

    # ---------- CLEAR ----------

    def clear_fields():

        selected_trainer_id.set("")

        name_entry.delete(0, tk.END)
        phone_entry.delete(0, tk.END)
        specialization_entry.delete(0, tk.END)
        salary_entry.delete(0, tk.END)
        search_entry.delete(0, tk.END)

    # ---------- VIEW ----------

    def view_trainers():

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM trainers")
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

    def search_trainer():

        search_text = search_entry.get().strip()

        if search_text == "":
            view_trainers()
            return

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            SELECT * FROM trainers
            WHERE name LIKE %s
            OR phone LIKE %s
            OR specialization LIKE %s
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

    # ---------- ADD ----------

    def add_trainer():

        if not validate_trainer():
            return

        name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        specialization = specialization_entry.get().strip()
        salary = salary_entry.get().strip()

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            INSERT INTO trainers
            (name, phone, specialization, salary)
            VALUES (%s, %s, %s, %s)
            """

            values = (
                name,
                phone,
                specialization,
                float(salary)
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Trainer added successfully!",
                parent=window
            )

            clear_fields()
            view_trainers()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- SELECT ----------

    def select_trainer(event):

        selected = table.focus()

        if selected == "":
            return

        values = table.item(selected, "values")

        if not values:
            return

        selected_trainer_id.set(values[0])

        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, values[2])

        specialization_entry.delete(0, tk.END)
        specialization_entry.insert(0, values[3])

        salary_entry.delete(0, tk.END)
        salary_entry.insert(0, values[4])

    # ---------- UPDATE ----------

    def update_trainer():

        trainer_id = selected_trainer_id.get()

        if trainer_id == "":
            messagebox.showerror(
                "Error",
                "Select a trainer from the table first!",
                parent=window
            )
            return

        if not validate_trainer():
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            UPDATE trainers
            SET name=%s,
                phone=%s,
                specialization=%s,
                salary=%s
            WHERE trainer_id=%s
            """

            values = (
                name_entry.get().strip(),
                phone_entry.get().strip(),
                specialization_entry.get().strip(),
                float(salary_entry.get().strip()),
                trainer_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Trainer updated successfully!",
                parent=window
            )

            clear_fields()
            view_trainers()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- DELETE ----------

    def delete_trainer():

        trainer_id = selected_trainer_id.get()

        if trainer_id == "":
            messagebox.showerror(
                "Error",
                "Select a trainer from the table first!",
                parent=window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this trainer?",
            parent=window
        )

        if not confirm:
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM trainers WHERE trainer_id=%s"

            cursor.execute(query, (trainer_id,))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Trainer deleted successfully!",
                parent=window
            )

            clear_fields()
            view_trainers()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- TITLE ----------

    title = tk.Label(
        window,
        text="TRAINER MANAGEMENT",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=15)

    # ---------- SEARCH ----------

    search_frame = tk.Frame(window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Search Trainer:"
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
        command=search_trainer
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=view_trainers
    ).pack(side=tk.LEFT, padx=5)

    # ---------- FORM ----------

    form = tk.Frame(window)
    form.pack(pady=15)

    tk.Label(
        form,
        text="Name"
    ).grid(row=0, column=0, padx=10, pady=8)

    name_entry = tk.Entry(
        form,
        width=25
    )
    name_entry.grid(row=0, column=1)

    tk.Label(
        form,
        text="Phone"
    ).grid(row=0, column=2, padx=10)

    phone_entry = tk.Entry(
        form,
        width=25
    )
    phone_entry.grid(row=0, column=3)

    tk.Label(
        form,
        text="Specialization"
    ).grid(row=1, column=0, padx=10, pady=8)

    specialization_entry = tk.Entry(
        form,
        width=25
    )
    specialization_entry.grid(row=1, column=1)

    tk.Label(
        form,
        text="Salary"
    ).grid(row=1, column=2, padx=10)

    salary_entry = tk.Entry(
        form,
        width=25
    )
    salary_entry.grid(row=1, column=3)

    # ---------- BUTTONS ----------

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Trainer",
        width=15,
        command=add_trainer
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update Trainer",
        width=15,
        command=update_trainer
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete Trainer",
        width=15,
        command=delete_trainer
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
        command=view_trainers
    ).grid(row=0, column=4, padx=5)

    # ---------- TABLE ----------

    columns = (
        "ID",
        "Name",
        "Phone",
        "Specialization",
        "Salary"
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
        select_trainer
    )

    view_trainers()