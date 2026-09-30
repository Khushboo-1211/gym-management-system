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


def open_attendance():

    window = tk.Toplevel()
    window.title("Attendance Management")
    window.geometry("1100x700")

    selected_attendance_id = tk.StringVar()

    # ---------- FUNCTIONS ----------

    def clear_fields():
        selected_attendance_id.set("")

        member_id_entry.delete(0, tk.END)
        attendance_date_entry.delete(0, tk.END)
        status_entry.delete(0, tk.END)
        search_entry.delete(0, tk.END)

    def view_attendance():

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            cursor.execute("SELECT * FROM attendance")
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

    def search_attendance():

        search_text = search_entry.get()

        if search_text == "":
            view_attendance()
            return

        for row in table.get_children():
            table.delete(row)

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            SELECT * FROM attendance
            WHERE member_id LIKE %s
            OR status LIKE %s
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

    def add_attendance():

        member_id = member_id_entry.get()
        attendance_date = attendance_date_entry.get()
        status = status_entry.get()

        if member_id == "" or attendance_date == "":
            messagebox.showerror(
                "Error",
                "Member ID and Attendance Date are required!",
                parent=window
            )
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            INSERT INTO attendance
            (member_id, attendance_date, status)
            VALUES (%s, %s, %s)
            """

            values = (
                member_id,
                attendance_date,
                status
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Attendance added successfully!",
                parent=window
            )

            clear_fields()
            view_attendance()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    def select_attendance(event):

        selected = table.focus()

        if selected == "":
            return

        values = table.item(selected, "values")

        if not values:
            return

        selected_attendance_id.set(values[0])

        member_id_entry.delete(0, tk.END)
        member_id_entry.insert(0, values[1])

        attendance_date_entry.delete(0, tk.END)
        attendance_date_entry.insert(0, values[2])

        status_entry.delete(0, tk.END)
        status_entry.insert(0, values[3])

    def update_attendance():

        attendance_id = selected_attendance_id.get()

        if attendance_id == "":
            messagebox.showerror(
                "Error",
                "Select an attendance record from the table first!",
                parent=window
            )
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = """
            UPDATE attendance
            SET member_id=%s,
                attendance_date=%s,
                status=%s
            WHERE attendance_id=%s
            """

            values = (
                member_id_entry.get(),
                attendance_date_entry.get(),
                status_entry.get(),
                attendance_id
            )

            cursor.execute(query, values)
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Attendance updated successfully!",
                parent=window
            )

            clear_fields()
            view_attendance()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    def delete_attendance():

        attendance_id = selected_attendance_id.get()

        if attendance_id == "":
            messagebox.showerror(
                "Error",
                "Select an attendance record from the table first!",
                parent=window
            )
            return

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this attendance record?",
            parent=window
        )

        if not confirm:
            return

        try:
            connection = get_connection()
            cursor = connection.cursor()

            query = "DELETE FROM attendance WHERE attendance_id=%s"

            cursor.execute(query, (attendance_id,))
            connection.commit()

            cursor.close()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Attendance deleted successfully!",
                parent=window
            )

            clear_fields()
            view_attendance()

        except Exception as e:
            messagebox.showerror(
                "Database Error",
                str(e),
                parent=window
            )

    # ---------- TITLE ----------

    title = tk.Label(
        window,
        text="ATTENDANCE MANAGEMENT",
        font=("Arial", 24, "bold")
    )
    title.pack(pady=15)

    # ---------- SEARCH ----------

    search_frame = tk.Frame(window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Search Attendance:"
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
        command=search_attendance
    ).pack(side=tk.LEFT, padx=5)

    tk.Button(
        search_frame,
        text="Show All",
        width=12,
        command=view_attendance
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
        text="Attendance Date (YYYY-MM-DD)"
    ).grid(row=0, column=2, padx=10)

    attendance_date_entry = tk.Entry(
        form,
        width=25
    )
    attendance_date_entry.grid(row=0, column=3)

    tk.Label(
        form,
        text="Status"
    ).grid(row=1, column=0, padx=10, pady=8)

    status_entry = tk.Entry(
        form,
        width=25
    )
    status_entry.grid(row=1, column=1)

    # ---------- BUTTONS ----------

    button_frame = tk.Frame(window)
    button_frame.pack(pady=10)

    tk.Button(
        button_frame,
        text="Add Attendance",
        width=15,
        command=add_attendance
    ).grid(row=0, column=0, padx=5)

    tk.Button(
        button_frame,
        text="Update Attendance",
        width=15,
        command=update_attendance
    ).grid(row=0, column=1, padx=5)

    tk.Button(
        button_frame,
        text="Delete Attendance",
        width=15,
        command=delete_attendance
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
        command=view_attendance
    ).grid(row=0, column=4, padx=5)

    # ---------- TABLE ----------

    columns = (
        "Attendance ID",
        "Member ID",
        "Attendance Date",
        "Status"
    )

    table = ttk.Treeview(
        window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        table.heading(column, text=column)
        table.column(column, width=220)

    table.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=15
    )

    table.bind(
        "<ButtonRelease-1>",
        select_attendance
    )

    view_attendance()