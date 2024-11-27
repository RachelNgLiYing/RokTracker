import configparser
config = configparser.ConfigParser()
config.read('config.ini')


config = {
        "ENTIRE_GS_DATA_RANGE": "$B$2:V",
        "GOVID_COLUMN": "B",
        "ENTIRE_MM_RANGE": config.get('Google SpreadSheet', 'ENTIRE_MM_RANGE', fallback='$C$2:V'),
        "GOVID_MM_COLUMN_OFFSET": 2,
        "GOOGLE_SERVICE_ACCOUNT_FILENAME": config.get('Google SpreadSheet', 'GOOGLE_SERVICE_ACCOUNT_FILENAME', fallback="google_service_account.json"),
        "DKP_SPREADSHEET_ID": config.get('Google SpreadSheet', 'DKP_SPREADSHEET_ID', fallback=''),
        "DKP_SPREADSHEET_NAME": 'DKP_Requirements',
        "MATCHMAKING_NAMES_GOVID": ['A', 'B'],
        "DATA_SPREADSHEET_ID": config.get('Google SpreadSheet', 'DATA_SPREADSHEET_ID', fallback=''),
        "BASE_SCORE_SPREADSHEET_ID": config.get('Google SpreadSheet', 'BASE_SCORE_SPREADSHEET_ID', fallback=''),
        "BASE_SCORE_TAB_NAME": config.get('Google SpreadSheet', 'BASE_SCORE_TAB_NAME', fallback=''),
        "EVENT_DESCRIPTION":config.get('Google SpreadSheet', 'EVENT_DESCRIPTION', fallback=''),
    }

def getAppConfig():
    return config