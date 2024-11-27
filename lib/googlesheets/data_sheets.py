
ROK_COLUMN_HEADERS = [
    'Governor Name',
    'Governor ID',
    'Power',
    'Kill Points',
    'Deads',
    'Tier 1 Kills',
    'Tier 2 Kills',
    'Tier 3 Kills',
    'Tier 4 Kills',
    'Tier 5 Kills',
    'Rss Assistance',
    'Alliance Helps',
    'Alliance',
    'KvK Kills High',
    'KvK Deads High',
    'KvK Severely Wounds High'
]

def add_data_tab(config, new_spreadsheet_tab, data, client):
    DATA_SPREADSHEET_ID=config["DATA_SPREADSHEET_ID"]
    spreadsheet = client.open_by_key(DATA_SPREADSHEET_ID)
    worksheet = spreadsheet.add_worksheet(title=new_spreadsheet_tab, rows=500, cols=26, index=0)
    new_values=[ROK_COLUMN_HEADERS.copy()]
    worksheet.append_rows(new_values+data, value_input_option="USER_ENTERED")