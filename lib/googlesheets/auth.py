
import os.path
import gspread
from google.oauth2.service_account import Credentials

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

def get_client(config):
  creds = None
  if os.path.exists(config["GOOGLE_SERVICE_ACCOUNT_FILENAME"]):
    creds =  Credentials.from_service_account_file(config["GOOGLE_SERVICE_ACCOUNT_FILENAME"], scopes=SCOPES)
  return gspread.authorize(creds)