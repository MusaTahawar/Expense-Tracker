import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import pandas as pd

expenses_data = {}

def add_expenses():
    month = month_entry.get()
    if not month:
        messagebox.showerror("Error", "Please enter a month.")
        return

    if month in expenses_data:
        messagebox.showerror("Error", "Expenses for this month already added.")
        return

    expenses = expenses_entry.get()
    try:
        expenses = [float(expense) for expense in expenses.split(",")]
    except ValueError:
        messagebox.showerror("Error", "Invalid expense input. Use comma-separated values.")
        return

    expenses_data[month] = expenses
    update_expenses_table()

def update_expenses_table():
    expenses_listbox.delete(0, tk.END)
    for month, expenses in expenses_data.items():
        total_expenses = sum(expenses)
        expenses_listbox.insert(tk.END, f"{month}: Total Expenses = ${total_expenses:.2f}")

def calculate_expense():
    if len(expenses_data) < 2:
        messagebox.showerror("Error", "Insufficient data to calculate expenses.")
        return

    last_month_expenses = expenses_data[list(expenses_data.keys())[-2]]
    this_month_expenses = expenses_data[list(expenses_data.keys())[-1]]

    months = [list(expenses_data.keys())[-2], list(expenses_data.keys())[-1]]
    spending = [sum(last_month_expenses), sum(this_month_expenses)]

    plt.bar(months, spending)
    plt.ylabel("Spending")
    plt.xlabel('Months')
    plt.show()

def save_to_csv():
    if not expenses_data:
        messagebox.showerror("Error", "No data to save.")
        return

    df = pd.DataFrame(expenses_data)
    df.to_csv("expenses.csv", index=False)
    messagebox.showinfo("Success", "Expenses data saved to 'expenses.csv'.")

def load_from_csv():
    try:
        df = pd.read_csv("expenses.csv")
        expenses_data.clear()
        for month in df.columns:
            expenses_data[month] = df[month].tolist()
        update_expenses_table()
        messagebox.showinfo("Success", "Expenses data loaded from 'expenses.csv'.")
    except FileNotFoundError:
        messagebox.showerror("Error", "File 'expenses.csv' not found.")


root = tk.Tk()
root.title("Advanced Expense Tracker")

# Labels and entries for adding expenses
month_label = tk.Label(root, text="Month:")
month_label.grid(row=0, column=0)
month_entry = tk.Entry(root)
month_entry.grid(row=0, column=1)

expenses_label = tk.Label(root, text="Expenses (comma-separated):")
expenses_label.grid(row=1, column=0)
expenses_entry = tk.Entry(root)
expenses_entry.grid(row=1, column=1)

add_expenses_button = tk.Button(root, text="Add Expenses", command=add_expenses)
add_expenses_button.grid(row=1, column=2)


expenses_listbox = tk.Listbox(root, width=40, height=10)
expenses_listbox.grid(row=2, column=0, columnspan=3)

calculate_expenses_button = tk.Button(root, text="Calculate Expenses", command=calculate_expense)
calculate_expenses_button.grid(row=3, column=0)

# Last 2 Lines :)
save_button = tk.Button(root, text="Save to CSV", command=save_to_csv)
save_button.grid(row=3, column=1)

load_button = tk.Button(root, text="Load from CSV", command=load_from_csv)
load_button.grid(row=3, column=2)

root.mainloop()
