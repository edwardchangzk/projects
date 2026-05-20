# Personal Expense Tracker

import json
from datetime import datetime

# User data
users = {}
current_user = None


# JSON functions
def save_users():
    try:
        with open("expenses.json", "w") as file:
            json.dump(users, file, indent=4)
    except OSError:
        print("Error: Could not save data to file.")


def load_users():
    global users

    try:
        with open("expenses.json", "r") as file:
            users = json.load(file)
    except FileNotFoundError:
        users = {}
    except json.JSONDecodeError:
        print("Error: expenses.json is corrupted or not valid JSON.")
        users = {}
    except OSError:
        print("Error: Could not read expenses.json.")
        users = {}


# Helper functions
def validate_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_monthly_total(month):
    user_expenses = users[current_user]["expenses"]
    total = 0

    for expense in user_expenses:
        if expense["dateOfPurchase"][:7] == month:
            total += expense["amount"]

    return total


# Authentication functions
def signup():
    print("==========================================")
    username = input("Create username: ").strip()
    password = input("Create password: ").strip()

    if username in users:
        print("Username already exists.")
    elif username == "" or password == "":
        print("Username or password cannot be empty.")
    else:
        users[username] = {
            "password": password,
            "expenses": [],
            "monthlyBudgets": {}
        }
        save_users()
        print("Signup successful!")

    print("==========================================")


def login():
    global current_user

    print("==========================================")
    username = input("Enter username: ").strip()
    password = input("Enter password: ").strip()

    try:
        if username in users and users[username]["password"] == password:
            current_user = username

            if "expenses" not in users[current_user]:
                users[current_user]["expenses"] = []

            if "monthlyBudgets" not in users[current_user]:
                users[current_user]["monthlyBudgets"] = {}

            save_users()

            print(f"Login successful. Welcome, {username}!")
            print("==========================================")
            expense_menu()
        else:
            print("Invalid username or password.")
            print("==========================================")

    except KeyError:
        print("Account data is incomplete or corrupted.")
        print("==========================================")


# Expense functions
def add_expense():
    while True:
        print("==========================================")
        add_expense_input = input("Please enter your expense (RM): ")
        category = input("Please enter the type of expense (Groceries, Luxury, etc.): ").strip()
        date_of_purchase = input("Please enter the date of purchase (YYYY-MM-DD): ").strip()

        try:
            amount = float(add_expense_input)

            if amount <= 0:
                print("Expense amount must be more than RM 0.")
                continue

            if category == "":
                print("Category cannot be empty.")
                continue

            if not validate_date(date_of_purchase):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            expense = {
                "amount": amount,
                "category": category,
                "dateOfPurchase": date_of_purchase
            }

            users[current_user]["expenses"].append(expense)
            save_users()

            print("Your expense has been successfully added!")
            print("==========================================")
            break

        except ValueError:
            print("Please enter a numeric value.")


def remove_expense():
    user_expenses = users[current_user]["expenses"]

    print("==========================================")

    if not user_expenses:
        print("No expenses recorded yet.")
        print("==========================================")
        return

    print("Current Expenses:")
    for i, expense in enumerate(user_expenses, start=1):
        print(
            f"{i}. RM {expense['amount']:.2f} | "
            f"Category: {expense['category']} | "
            f"Date: {expense['dateOfPurchase']}"
        )

    while True:
        choice = input("Enter the expense number to delete: ")

        try:
            choice = int(choice)

            if 1 <= choice <= len(user_expenses):
                removed = user_expenses.pop(choice - 1)
                save_users()
                print(
                    f"Removed: RM {removed['amount']:.2f} | "
                    f"Category: {removed['category']} | "
                    f"Date: {removed['dateOfPurchase']}"
                )
                print("==========================================")
                break
            else:
                print("Invalid expense number.")

        except ValueError:
            print("Please enter a whole number.")


def view_expense():
    user_expenses = users[current_user]["expenses"]

    print("==========================================")

    if not user_expenses:
        print("No expenses were added!")
    else:
        print("Here are your current expenses:")
        for i, expense in enumerate(user_expenses, start=1):
            print(
                f"{i}. RM {expense['amount']:.2f} | "
                f"Category: {expense['category']} | "
                f"Date: {expense['dateOfPurchase']}"
            )

    print("==========================================")


def total_expense():
    user_expenses = users[current_user]["expenses"]

    print("==========================================")

    if not user_expenses:
        print("No expenses to add!")
    else:
        total_expense_value = 0

        for expense in user_expenses:
            total_expense_value += expense["amount"]

        print(f"Your total expenses were RM {total_expense_value:.2f}")

    print("==========================================")


def monthly_summary():
    user_expenses = users[current_user]["expenses"]

    print("==========================================")

    if not user_expenses:
        print("No expenses recorded yet.")
        print("==========================================")
        return

    monthly_totals = {}

    for expense in user_expenses:
        month = expense["dateOfPurchase"][:7]

        if month not in monthly_totals:
            monthly_totals[month] = 0

        monthly_totals[month] += expense["amount"]

    print("Monthly Expense Summary:")

    for month, total in monthly_totals.items():
        print(f"{month}: RM {total:.2f}")

    print("==========================================")


def set_monthly_budget():
    print("==========================================")
    month = input("Enter month for budget (YYYY-MM): ").strip()
    budget_input = input("Enter allowed spending amount for this month (RM): ")

    try:
        datetime.strptime(month, "%Y-%m")

        budget = float(budget_input)

        if budget <= 0:
            print("Budget must be more than RM 0.")
            print("==========================================")
            return

        users[current_user]["monthlyBudgets"][month] = budget
        save_users()

        print(f"Budget for {month} set to RM {budget:.2f}")

    except ValueError:
        print("Invalid input. Use YYYY-MM for month and a numeric value for budget.")

    print("==========================================")


def budget_status():
    print("==========================================")
    month = input("Enter month to check (YYYY-MM): ").strip()

    try:
        datetime.strptime(month, "%Y-%m")

        monthly_budgets = users[current_user]["monthlyBudgets"]

        if month not in monthly_budgets:
            print("No budget set for this month.")
            print("==========================================")
            return

        budget = monthly_budgets[month]
        spent = get_monthly_total(month)
        remaining = budget - spent

        average_allowed_per_day = budget / 30
        remaining_per_day = remaining / 30

        print(f"Budget Status for {month}")
        print(f"Monthly Budget: RM {budget:.2f}")
        print(f"Spent So Far: RM {spent:.2f}")
        print(f"Remaining: RM {remaining:.2f}")
        print(f"Average allowed spending per day: RM {average_allowed_per_day:.2f}")

        if remaining >= 0:
            print(f"Suggested remaining daily spending: RM {remaining_per_day:.2f}")
        else:
            print(f"You are over budget by RM {abs(remaining):.2f}")

    except ValueError:
        print("Invalid month format. Please use YYYY-MM.")

    print("==========================================")


# Menus
def expense_menu():
    global current_user

    while True:
        print("==========================================")
        print(f"----- Welcome, {current_user}! -----")
        print("Please select Options:")
        print("1. Add Additional Expense")
        print("2. Delete Expense")
        print("3. View Current Expense")
        print("4. Display Total Expense")
        print("5. Monthly Summary")
        print("6. Set Monthly Budget")
        print("7. Budget Status")
        print("8. Logout")

        option = input("Enter your choice (1 - 8): ")

        if option == "1":
            add_expense()
        elif option == "2":
            remove_expense()
        elif option == "3":
            view_expense()
        elif option == "4":
            total_expense()
        elif option == "5":
            monthly_summary()
        elif option == "6":
            set_monthly_budget()
        elif option == "7":
            budget_status()
        elif option == "8":
            print("==========================================")
            print(f"Goodbye, {current_user}!")
            current_user = None
            print("==========================================")
            break
        else:
            print("Invalid option selected! Kindly choose between 1 and 8.")


def main_menu():
    while True:
        print("==========================================")
        print("----- Welcome to your Personal Expense Tracker! -----")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")

        option = input("Enter your choice (1 - 3): ")

        if option == "1":
            login()
        elif option == "2":
            signup()
        elif option == "3":
            print("==========================================")
            print("Thank you for your time!")
            print("==========================================")
            break
        else:
            print("Invalid option selected! Kindly choose between 1 and 3.")


# Run program
if __name__ == "__main__":
    load_users()
    main_menu()
