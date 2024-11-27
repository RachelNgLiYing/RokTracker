DATA_COLUMN_HEADERS = [
    'Username',
    'Governor ID',
    'Still in Scan',
    'Power Change from MM',
    'B KP',
    'New KP',
    'Acq KP',
    'B Acq KP',
    'B Deads',
    'New Deads',
    'Acq Deads',
    'B Acq Deads',
    'B T4 Kills',
    'New T4 Kills',
    'Acq T4 Kills',
    'B Acq T4 Kills',
    'B T5 Kills',
    'New T5 Kills',
    'Acq T5 Kills',
    'B Acq T5 Kills',
    'Dead REQ',
    'KP REQ',
    'DKP REQ',
    'Acq DKP',
    'B Acq DKP',
    'KP Reached',
    'Dead Reached',
    'Goal (%)',
    'Goal KP over DKP'
]

#Take Care of Injections
DATA_FORMULAS = {
    'Still in Scan': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),2,FALSE)), "NO", "YES")',
    'Power Change from MM': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),2,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},{GOVID_MM_COLUMN_OFFSET}, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),2,FALSE)) - VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},{GOVID_MM_COLUMN_OFFSET}, FALSE)',
    'B KP': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),3,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},3, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),3,FALSE))',
    'New KP': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),3,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},3, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),3,FALSE))',
    'Acq KP': '=$F{row_index}-IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),3,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},3, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),3,FALSE))',
    'B Acq KP':'=$F{row_index}-$E{row_index}',
    'B Deads': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),4,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},4, FALSE), (VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),4,FALSE)))',
    'New Deads': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),4,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_RANGE},4, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),4,FALSE))',
    'Acq Deads': '=$J{row_index}-(IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),4,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_RANGE},4, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),4,FALSE)))',
    'B Acq Deads': '=$J{row_index}-$I{row_index}',
    'B T4 Kills': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),8,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},8, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),8,FALSE))',
    'New T4 Kills': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),8,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},8, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),8,FALSE))',
    'Acq T4 Kills': '=$N{row_index}-(IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),8,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},8, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),8,FALSE)))',
    'B Acq T4 Kills': '=$N{row_index}-M{row_index}',
    'B T5 Kills': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),9,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},9, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),9,FALSE))',
    'New T5 Kills': '=IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),9,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},9, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{new_spreadsheet_tab}!{ENTIRE_RANGE}"),9,FALSE))',
    'Acq T5 Kills': '=$R{row_index}-(IF(ISNA(VLOOKUP(${GOVID_COLUMN}{row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),9,FALSE)), VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},9, FALSE), VLOOKUP(${GOVID_COLUMN}${row_index}, IMPORTRANGE("https://docs.google.com/spreadsheets/d/{DATA_SPREADSHEET_ID}/edit", "{BASE_SCORE_TAB_NAME}!{ENTIRE_RANGE}"),9,FALSE)))',
    'B Acq T5 Kills': '=$R{row_index}-$Q{row_index}',
    'Dead REQ': '=VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},17, FALSE)',
    'KP REQ': '=VLOOKUP(${GOVID_COLUMN}{row_index},{DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE},18, FALSE)',
    'DKP REQ': '=VLOOKUP(${GOVID_COLUMN}{row_index}, {DKP_SPREADSHEET_NAME}!{ENTIRE_MM_RANGE}, 19,FALSE)',
    'Acq DKP': '=(($O{row_index}+($S{row_index}*2)))+($K{row_index}*5)',
    'B Acq DKP': '=(($P{row_index}+($T{row_index}*2)))+($L{row_index}*5)',
    'KP Reached': '=$G{row_index}/$V{row_index}*100',
    'Dead Reached': '=$K{row_index}/$U{row_index}*100',
    'Goal (%)': '=$X{row_index}/$W{row_index}*100',
    'Goal KP over DKP': '=(($O{row_index}+($S{row_index}*2))/$W{row_index})*100'
}

def add_looker_tab(config, description, new_spreadsheet_tab, client):
  DKP_SPREADSHEET_ID=config["DKP_SPREADSHEET_ID"]
  DKP_SPREADSHEET_NAME=config["DKP_SPREADSHEET_NAME"]
   #read MM spreadsheets and

    # Call the Sheets API
  spreadsheet = client.open_by_key(DKP_SPREADSHEET_ID)
  worksheet = spreadsheet.worksheet(DKP_SPREADSHEET_NAME)
  values = worksheet.get("B2:C")

  if not values:
      print("No data found.")
      return
  
  worksheet = spreadsheet.add_worksheet(title=description, rows=500, cols=26, index=0)

  new_values = [DATA_COLUMN_HEADERS.copy()]
  for index in range(len(values)):
    currentIndex = str(index+2)
    row = values[index].copy()
    row_index_data = {
      'row_index': currentIndex,
    }
    common_dictionary = {
       **row_index_data,
      'GOVID_COLUMN': config["GOVID_COLUMN"],
      'DATA_SPREADSHEET_ID': config["DATA_SPREADSHEET_ID"],
      'BASE_SCORE_TAB_NAME': config["BASE_SCORE_TAB_NAME"],
      'ENTIRE_RANGE': config["ENTIRE_GS_DATA_RANGE"],
      'GOVID_COLUMN': config["GOVID_COLUMN"],
      'DKP_SPREADSHEET_NAME': config["DKP_SPREADSHEET_NAME"],
      'ENTIRE_MM_RANGE': config["ENTIRE_MM_RANGE"],
    }
    dictionary_with_mm_and_base = dict(
      common_dictionary,
      GOVID_MM_COLUMN_OFFSET=config["GOVID_MM_COLUMN_OFFSET"],
      new_spreadsheet_tab=new_spreadsheet_tab
    )
    new_values.append([
      row[0], #Username
      row[1], #Governor ID
      DATA_FORMULAS['Still in Scan'].format(**common_dictionary),
      DATA_FORMULAS['Power Change from MM'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['B KP'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['New KP'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['Acq KP'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['B Acq KP'].format(**row_index_data),
      DATA_FORMULAS['B Deads'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['New Deads'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['Acq Deads'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['B Acq Deads'].format(**row_index_data),
      DATA_FORMULAS['B T4 Kills'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['New T4 Kills'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['Acq T4 Kills'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['B Acq T4 Kills'].format(**row_index_data),
      DATA_FORMULAS['B T5 Kills'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['New T5 Kills'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['Acq T5 Kills'].format(**dictionary_with_mm_and_base),
      DATA_FORMULAS['B Acq T5 Kills'].format(**row_index_data),
      DATA_FORMULAS['Dead REQ'].format(**common_dictionary),
      DATA_FORMULAS['KP REQ'].format(**common_dictionary),
      DATA_FORMULAS['DKP REQ'].format(**common_dictionary),
      DATA_FORMULAS['Acq DKP'].format(**row_index_data),
      DATA_FORMULAS['B Acq DKP'].format(**row_index_data),
      DATA_FORMULAS['KP Reached'].format(**row_index_data),
      DATA_FORMULAS['Dead Reached'].format(**row_index_data),
      DATA_FORMULAS['Goal (%)'].format(**row_index_data),
      DATA_FORMULAS['Goal KP over DKP'].format(**row_index_data),
    ])

  worksheet.append_rows(new_values, value_input_option="USER_ENTERED")
