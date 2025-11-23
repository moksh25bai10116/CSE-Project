import datetime
import json
import os

DATA_FILE = "money_data.json"


def load_money_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {"balance": 0, "history": []}
    else:
        return {"balance": 0, "history": []}


def save_money_data(stuff):
    with open(DATA_FILE, "w") as w:
        json.dump(stuff, w, indent=4)


def add_income(db):
    raw_amt = input("Enter income amount: ")
    try:
        amt = float(raw_amt)
    except ValueError:
        print("That wasn’t a number, try again.")
        return

    note = input("Enter note (e.g., pocket money, salary): ")

    old_balance = db.get("balance", 0)
    db["balance"] = old_balance + amt

    db["history"].append({
        "type": "Income",
        "amount": amt,
        "note": note,
        "date": str(datetime.datetime.now())
    })

    save_money_data(db)
    print("Income added!")


def add_expense(info):
    raw = input("Enter expense amount: ")
    try:
        spent = float(raw)
    except ValueError:
        print("Not a valid number.")
        return

    reason = input("Enter note (e.g., food, travel): ")

    if spent > info.get("balance", 0):
        print("Not enough balance!")
        return

    info["balance"] = info["balance"] - spent

    info["history"].append({
        "type": "Expense",
        "amount": spent,
        "note": reason,
        "date": str(datetime.datetime.now())
    })

    save_money_data(info)
    print("Expense added.")


def show_balance(wallet):
    print("\nCurrent Balance: ₹" + str(wallet["balance"]) + "\n")


def show_history(data):
    print("\n=--= Transaction History =--=")
    hist = data.get("history", [])

    if not hist:
        print("No transactions yet.\n")
        return

    for h in hist:
        print(f"{h['date']} | {h['type']} | ₹{h['amount']} | {h['note']}")
    print("")


def main():
    data = load_money_data()

    while True:
        print("\n=/\/= Student Money Manager =\/\=")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. View Transaction History")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_income(data)
        elif choice == "2":
            add_expense(data)
        elif choice == "3":
            show_balance(data)
        elif choice == "4":
            show_history(data)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
