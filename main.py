import pandas as pd
import csv
from datetime import date, datetime
from data_entry import get_amount, get_category, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    CULOMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"



    @classmethod
    def initialize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.CULOMNS)
            df.to_csv(cls.CSV_FILE, index=False)

    @classmethod
    def add_entry(cls,date,amount,category,description):
        new_entry = {
            "date" : date,
            "amount": amount,
            "category" : category,
            "description" : description,
        }
        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=cls.CULOMNS)
            writer.writerow(new_entry)
            print("Entry add successfully")

    @classmethod
    def get_transection(cls,start_date,end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"],format = CSV.FORMAT)
        start_date = datetime.strptime(start_date,CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]
        if filtered_df.empty:
            print("No transection is found in given date")
        else:
            print(
                f"Transection for {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}"
                )
            print(filtered_df.to_string(index=False, formatters={"date": lambda x : x.strftime(CSV.FORMAT)}))
            
            
            total_income = filtered_df[filtered_df ["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary:")
            print(f"total Income: ${total_income:.2f}")
            print(f"total Expense: ${total_expense:.2f}")
            print(f"Net Savings: ${(total_income - total_expense):.2f}")

        return filtered_df


def add():
    CSV.initialize_csv()
    date = get_date("Enter the date of transection (DD-MM-YYYY) or enter for today date:", allow_defult=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    CSV.add_entry(date,amount,category,description)


def plot_transection(df):
    df.set_index("date",inplace=True)

    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    plt.figure(figsize=(10,5))
    plt.plot(income_df.index,income_df["amount"], label="income", color="g")
    plt.plot(expense_df.index, expense_df["amount"],label="Expense",color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title('Income and Exoense over time')
    plt.legend()
    plt.grid(True)
    plt.show()





#using chatgpt to ploting total of income,expense and net saving 
def plot_transection(df):
    df.set_index("date", inplace=True)

    # Resampling and filling missing dates with 0
    income_df = (
        df[df["category"] == "Income"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    expense_df = (
        df[df["category"] == "Expense"]
        .resample("D")
        .sum()
        .reindex(df.index, fill_value=0)
    )
    
    # Calculate total income, expense, and net savings
    total_income = income_df["amount"].sum()
    total_expense = expense_df["amount"].sum()
    net_savings = total_income - total_expense

    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label="Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense Over Time")
    plt.legend()
    plt.grid(True)

    # Adding text annotations for total income, expense, and net savings
    plt.figtext(0.15, 0.8, f"Total Income: ${total_income:.2f}", fontsize=12, color="green")
    plt.figtext(0.15, 0.75, f"Total Expense: ${total_expense:.2f}", fontsize=12, color="red")
    plt.figtext(0.15, 0.7, f"Net Savings: ${net_savings:.2f}", fontsize=12, color="blue")

    # Show plot
    plt.show()
# ending of chatgpt









def main():
    while True:
        print("\n1. Add a new transection")
        print("2. View transection and summary within a date range")
        print("3. Exit")
        choice = input("Enter the choice ('1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start date (DD-MM-YYYY): ")
            end_date = get_date("Enter the end date (DD-MM-YYYY): ")
            df = CSV.get_transection(start_date, end_date)
            if input("Do you want to see a plot? (y/n)").lower() == "y":
                plot_transection(df)

        elif choice == "3":
            print("Exiting......")
            break

        else:
            print("Invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
