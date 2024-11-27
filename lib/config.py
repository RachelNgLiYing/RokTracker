import configparser
config = configparser.ConfigParser()
config.read('config.ini')


file_config = {
    "Default": {
        "KINGDOM_ID": config.get('Default', 'KINGDOM_ID', fallback='1234'),
        "SEARCH_RANGE": config.getint('Default', 'SEARCH_RANGE', fallback=350),
        "RESUME_SCAN": config.getboolean('Default', 'RESUME_SCAN', fallback=False),
    },
    "Google SpreadSheet": {
        "ENTIRE_MM_RANGE": config.get('Google SpreadSheet', 'ENTIRE_MM_RANGE', fallback='$C$2:V'),
        "GOOGLE_SERVICE_ACCOUNT_FILENAME": config.get('Google SpreadSheet', 'GOOGLE_SERVICE_ACCOUNT_FILENAME', fallback="google_service_account.json"),
        "DKP_SPREADSHEET_ID": config.get('Google SpreadSheet', 'DKP_SPREADSHEET_ID', fallback=''),
        "DATA_SPREADSHEET_ID": config.get('Google SpreadSheet', 'DATA_SPREADSHEET_ID', fallback=''),
        "BASE_SCORE_SPREADSHEET_ID": config.get('Google SpreadSheet', 'BASE_SCORE_SPREADSHEET_ID', fallback=''),
        "BASE_SCORE_TAB_NAME": config.get('Google SpreadSheet', 'BASE_SCORE_TAB_NAME', fallback=''),
        "BASE_SCORE_SPREADSHEET_ID": config.get('Google SpreadSheet', 'EVENT_DESCRIPTION', fallback=''),
        "EVENT_DESCRIPTION": config.get('Google SpreadSheet', 'EVENT_DESCRIPTION', fallback=''),
    }
}

config = {
        "ENTIRE_GS_DATA_RANGE": "$B$2:V",
        "GOVID_COLUMN": "B",
        "GOVID_MM_COLUMN_OFFSET": 2,
        "DKP_SPREADSHEET_NAME": 'DKP_Requirements',
        "MATCHMAKING_NAMES_GOVID": ['A', 'B'],
        **file_config["Google SpreadSheet"],
        **file_config["Default"]
    }

def getAppConfig():
    return config

def getFileConfig():
    return file_config