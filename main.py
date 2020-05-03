import gspread
import json
import os
import datetime

from oauth2client.service_account import ServiceAccountCredentials

today = datetime.datetime.now()

def worksheet():
    sheetname = today.strftime('%Y%m')
    try:
        return workfile.worksheet(sheetname)
    except gspread.exceptions.WorksheetNotFound:
        return workfile.add_worksheet(title=sheetname, rows="100", cols="20")
    except:
        pass



scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('gcloud.json', scope)
gc = gspread.authorize(credentials)

SPREADSHEET_KEY = os.getenv('SPREADSHEET_KEY')

workfile = gc.open_by_key(SPREADSHEET_KEY)

worksheet = worksheet()

worksheet.update_cell(1,1, today.strftime('%H:%M'))

