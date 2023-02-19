import gspread
from WorkingWithDB import DB

sa = gspread.service_account(filename='account.json')
sh = sa.open('orbitrazh-data')

wks = sh.worksheet('list1')


def update():
    wks.update('A1:J', DB.get_all_data())