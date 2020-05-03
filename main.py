import gspread
import json
import os
import datetime
import calendar

from oauth2client.service_account import ServiceAccountCredentials

today = datetime.datetime.now()

def worksheet():
    sheetname = today.strftime('%Y%m')
    try:
        return workfile.worksheet(sheetname)
    except gspread.exceptions.WorksheetNotFound:
        return initialize_sheet(sheetname)
    except:
        pass

def initialize_sheet(sheetname):
    wc = workfile.add_worksheet(title=sheetname, rows=0, cols=0)
    wc.update('A1:C1', [['日付', '出勤', '退勤']])
    startday = today.replace(day=1)
    monthrange = calendar.monthrange(today.year, today.month)[1]
    wc.update(
        f'A2:A{monthrange + 1}',
        [[(startday + datetime.timedelta(days=i)).strftime('%m/%d')] for i in range(monthrange)])
    return wc

def dakoku(worksheet):
    today_row_num = worksheet.find(today.strftime('%m/%d')).row
    row = worksheet.row_values(today_row_num)
    # 未出勤
    if len(row) == 1:
        worksheet.update(f'B{today_row_num}', today.strftime('%H:%M'))
    # 継続的な打刻、これが途絶えたタイミングが退勤になる
    else:
        worksheet.update(f'C{today_row_num}', today.strftime('%H:%M'))

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gcloud.json', scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = os.getenv('SPREADSHEET_KEY')

workfile = gc.open_by_key(SPREADSHEET_KEY)

worksheet = worksheet()

try:
    dakoku(worksheet)
except Exception as e:
    print(e)