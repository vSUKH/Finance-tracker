from datetime import datetime

date_format = "%d-%m-%Y"
CATEGORY = {"I" : "Income", "E": "Expense"}
def get_date(prompt, allow_defult=False):
    date_str = input(prompt)
    if allow_defult and not date_str:
        return datetime.today().strftime(date_format)
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid format ! Please enter the date in DD-MM-YYYY format")
        return get_date(prompt, allow_defult)
    


def get_amount():
        try:
            amount = float(input("Enter the amount: "))
            if amount <= 0:
                  raise ValueError("Amount must be non-nagetive and non-zero value.")
            return amount
        except ValueError as e:
             print(e)
             return get_amount()
        

def get_category():
     category = input("Enter the category ('I' for Income or 'E' for Expense): ").upper()
     if category in CATEGORY:
          return CATEGORY[category]
     print("Invalid category. Please enter 'I' for income or 'E' for expanse.")
     return get_category()
    

def get_description():
    return input ("Enter a description (optional) : ")