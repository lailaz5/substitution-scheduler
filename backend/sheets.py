import os
import gspread
from google.oauth2.service_account import Credentials

def get_dashboard():
    current_dir = os.path.dirname(os.path.realpath(__file__))
    credentials_path = os.path.join(current_dir, "credentials.json")

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(credentials_path, scopes=scopes)

    client = gspread.authorize(creds)

    sheet_id = "1k2cq6iODOd3XwW8KFsEnfGGqTSlxj9Ft4wEfjWyXR9g"
    sheet = client.open_by_key(sheet_id)

    worksheet = sheet.worksheet("Dashboard")
    teachers = worksheet.col_values(4)
    balances = worksheet.col_values(10)

    teacher_balance_dict = {}
    for teacher, balance in zip(teachers, balances):
        if teacher != "" and balance != "":
            teacher_balance_dict[teacher] = balance

    return teacher_balance_dict


if __name__ == "__main__":
    teacher_balances = get_dashboard()
    print(teacher_balances)