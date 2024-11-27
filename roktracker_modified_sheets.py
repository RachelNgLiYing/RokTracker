import os
import sys
import time
import traceback
import requests
import webbrowser
from datetime import date, datetime, timezone
from ppadb.client import Client
import pytesseract
import tkinter as tk
from tkinter import messagebox
import xlwt
import keyboard
import random

from lib.android import get_cv2_image_from_device, resize_emulator
from lib.config import getAppConfig
from lib.googlesheets.auth import get_client
from lib.googlesheets.data_sheets import add_data_tab
from lib.googlesheets.dkp_calculation_sheets import add_looker_tab
from lib.image import read_image
from lib.rok_data import ROKSCAN_DATA

emulator_name = 'emulator-5554'
version = "RokTracker-v9.5"
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

utc_datetime = datetime.now(timezone.utc)
today_datetime = utc_datetime.strftime("%Y-%m-%d-%H%MZ")

new_gs_tab = utc_datetime.strftime("%d %B %Y %H%M UTC")

today = date.today()
Y = [285, 390, 490, 590, 605]  # Positions for governors

def tointcheck(element):
    try:
        return int(element)
    except ValueError:
        return element

def tointprint(element):
    try:
        return f'{int(element):,}'
    except ValueError:
        return str(element)

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def check_for_updates():
    response = requests.get("https://api.github.com/repos/nikolakis1919/RokTracker/releases/latest")
    if (response.json()["name"]) != version:
        bo = tk.Tk()
        bo.withdraw()
        messagebox.showinfo("Tool is outdated", "New version is available on github repository. It is highly recommended to update the tool!")
        bo.destroy()

def open_donate_link():
    webbrowser.open_new(r"https://www.buymeacoffee.com/nikolakis1919")

def open_discord_link():
    webbrowser.open_new(r"https://discord.gg/CvU96gVfjS")

def create_input_gui():
    root = tk.Tk()
    root.title('RokTracker')
    root.geometry("400x350")

    kingdom_input = tk.StringVar(root)
    curr_scan_pos_input = tk.StringVar(root)
    new_file_chkbox = tk.IntVar()
    is_repair_chkbox = tk.IntVar()
    variable2 = tk.IntVar(root)
    var1 = tk.IntVar()

    options = [50 + i * 25 for i in range(38)]
    variable2.set(options[0])

    def search():
        if kingdom_input.get():
            global kingdom, search_range, resume_scanning, new_file, current_pos, repair_mode
            kingdom = kingdom_input.get()
            search_range = variable2.get()
            resume_scanning = var1.get()
            new_file = new_file_chkbox.get()
            current_pos = curr_scan_pos_input.get()
            repair_mode = is_repair_chkbox.get()
            root.destroy()
            print("Scanning Started...")
        else:
            print("You need to fill Kingdom number!")
            kingdom_entry.focus_set()

    tk.Label(root, text='Kingdom', font=('calibre', 10, 'bold')).grid(row=0, column=0)
    kingdom_entry = tk.Entry(root, textvariable=kingdom_input, font=('calibre', 10, 'normal')).grid(row=0, column=1)
    tk.Label(root, text='Search Amount', font=('calibre', 10, 'bold')).grid(row=1, column=0)
    tk.OptionMenu(root, variable2, *options).grid(row=1, column=1)
    tk.Checkbutton(root, text="Resume Scan", variable=var1, font=('calibre', 10, 'bold')).grid(row=2, column=1, pady=4)
    tk.Button(root, text="Search", command=search).grid(row=7, column=1, pady=5)
    tk.Label(root, text=u"\u00A9 nikolakis1919", font=('calibre', 10, 'bold')).grid(row=8, column=1, pady=10)
    tk.Button(root, foreground='Green', text='Donate', command=open_donate_link, font=('calibre', 10, 'bold')).grid(row=12, column=1, pady=10)
    tk.Label(root, text='Find me on discord: nikos#4469', font=('calibre', 10, 'bold')).grid(row=9, column=1, pady=10)
    tk.Button(root, foreground='Blue', text='Join Discord', command=open_discord_link, font=('calibre', 10, 'bold')).grid(row=13, column=1, pady=10)
    
    tk.Label(root, text='Position', font=('calibre', 10, 'bold')).grid(row=3, column=0)
    tk.Entry(root, textvariable=curr_scan_pos_input, font=('calibre',10,'normal')).grid(row=3,column=1)

    tk.Checkbutton(root, text="New File", variable=new_file_chkbox, font=('calibre',10,'bold')).grid(row=4,column=1,pady=4)
    tk.Checkbutton(root, text="Is Repair", variable=is_repair_chkbox, font=('calibre',10,'bold')).grid(row=5,column=1,pady=4)



    root.mainloop()

def initialize_adb():
    return Client(host='localhost', port=5037)


def get_device(adb):
    devices = adb.devices()
    if not devices:
        print('No device attached')
        sys.exit()
    return devices[0]

def setup_excel():
    wb = xlwt.Workbook()
    sheet1 = wb.add_sheet(str(today))
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.bold = True
    style.font = font

    headers = ['Governor Name', 'Governor ID', 'Power', 'Kill Points', 'Deads', 'Tier 1 Kills', 'Tier 2 Kills', 'Tier 3 Kills', 'Tier 4 Kills', 'Tier 5 Kills', 'Rss Assistance', 'Alliance Helps', 'Alliance','KvK Kills High', 'KvK Deads High', 'KvK Severely Wounds High']
    for col, header in enumerate(headers):
        sheet1.write(0, col, header, style)
    return wb, sheet1

def randomize_time(max_time: float):
    """
    Pauses the program execution for a random duration between max_time and 2/3 of max_time.
    
    Parameters:
    max_time (float): The maximum time in seconds.
    """
    lower_limit = max_time * 2 / 3
    sleep_time = random.uniform(lower_limit, max_time)
    time.sleep(sleep_time)


def read_ocr_from_image(image, config=""):
    return pytesseract.image_to_string(image, config=config)

def capture_image(device, filename):
    image = device.screencap()
    with open(filename, 'wb') as f:
        f.write(image)
    return

def print_progress_bar(iteration, total, bar_length=40):
    """Prints a progress bar to the console.
    
    Parameters:
        iteration (int): The current iteration number.
        total (int): The total number of iterations.
        bar_length (int): The length of the progress bar.
    """
    progress = (iteration / total)
    arrow = '=' * int(round(progress * bar_length) - 1)
    spaces = ' ' * (bar_length - len(arrow))
    sys.stdout.write(f'\r[{arrow}{spaces}] {iteration} out of {total} Scanned\n\n')
    sys.stdout.flush()

def format_time(seconds):
    """Helper function to format time in MM:SS format."""
    minutes = int(seconds // 60)
    seconds = int(seconds % 60)
    return f"{minutes:02d}:{seconds:02d}"


def go_to_rank_page_from_main(device):
    #Open rank screen 
    device.shell(f'input tap 52 52')
    randomize_time(1.3)
    device.shell(f'input tap 516.7 740')
    randomize_time(1.3)
    device.shell(f'input tap 331.5 522.5')
    randomize_time(1.3)


def main_loop(device, sheet1):
    if not resume_scanning:
        go_to_rank_page_from_main(device)
    stop = False

    def onkeypress(event):
        nonlocal stop
        if event.name == '\\':
            print("Your scan will be terminated when current governor scan is over!")
            stop = True

    keyboard.on_press(onkeypress)

    all_data = []
    #while this saves data on buffer
    j = 4 if resume_scanning else 0
    try:
        start_time = time.time()
        for i in range(j, search_range + j):
            if stop:
                print("Scan Terminated! Saving the current progress...")
                break

            k = min(i, 4)
            device.shell(f'input tap 690 {Y[k]}')
            randomize_time(1.3)

            # Open governor and ensure the tab is open
            for _ in range(5):
                check_more_info_png = get_cv2_image_from_device(device)
                info_check = read_image(check_more_info_png, ROKSCAN_DATA['more_info_check'])
                if 'MoreInfo' in info_check:
                     break
                device.shell(f'input swipe 690 605 690 540')
                device.shell(f'input tap 690 {Y[k]}')
                randomize_time(1.2)
            #copy nickname
            device.shell(f'input tap 654 245')
            gov_id = read_image(check_more_info_png, ROKSCAN_DATA['gov_id_image'])

            gov_name = tk.Tk().clipboard_get()
            #read kvk stats
            device.shell(f'input tap 1226 486')
            gov_killpoints = read_image(check_more_info_png, ROKSCAN_DATA['gov_killpoints_image'])
            randomize_time(0.5)
            kvk_stats_png = get_cv2_image_from_device(device)
            gov_kills_high = read_image(kvk_stats_png, ROKSCAN_DATA['gov_kills_high_image'])
            gov_power = read_image(check_more_info_png, ROKSCAN_DATA['gov_power_image'])
            
            randomize_time(0.5)
            for _ in range(2):
                device.shell(f'input tap 1118 314')
                randomize_time(0.7)


            alliance_tag = read_image(check_more_info_png, ROKSCAN_DATA['alliance_tag_image'])
            
            gov_deads_high = read_image(kvk_stats_png, ROKSCAN_DATA['gov_deads_high_image'])
            gov_sevs_high = read_image(kvk_stats_png, ROKSCAN_DATA['gov_sevs_high_image'])

            kills_tier_png = get_cv2_image_from_device(device)
            device.shell(f'input tap 350 740')
            
            kills_tiers = []
            for y in range(430, 630, 45):
                kills_tiers.append(read_image(kills_tier_png, ROKSCAN_DATA['kills_tiers_image'], [y]))

            randomize_time(0.5)
            more_info_png = get_cv2_image_from_device(device)
            gov_dead = read_image(more_info_png, ROKSCAN_DATA['gov_dead_image'])
            gov_rss_assistance = read_image(more_info_png, ROKSCAN_DATA['gov_rss_assistance_image'])
            
            device.shell(f'input tap 1396 58') #close more info
            
            gov_alliance_helps = read_image(more_info_png, ROKSCAN_DATA['gov_helps_image'])
            


            print(f'Governor ID: {gov_id}Governor Name: {gov_name}\nGovernor Power: {tointprint(gov_power)}\nGovernor Killpoints: {tointprint(gov_killpoints)}\nTier 1 kills: {tointprint(kills_tiers[0])}\nTier 2 kills: {tointprint(kills_tiers[1])}\nTier 3 kills: {tointprint(kills_tiers[2])}\nTier 4 kills: {tointprint(kills_tiers[3])}\nTier 5 kills: {tointprint(kills_tiers[4])}\nGovernor Deads: {tointprint(gov_dead)}\nGovernor RSS Assistance: {tointprint(gov_rss_assistance)}\nGovernor Alliance Helps: {tointprint(gov_alliance_helps)}\nGovernor Alliance: {alliance_tag}Governor KvK High Kill: {tointprint(gov_kills_high)}\nGovernor KvK High Deads:{tointprint(gov_deads_high)}\nGovernor KvK High Severely Wounded:{tointprint(gov_sevs_high)}')
            
            # Update progress bar
            print_progress_bar(i + 1 - j, search_range)
            randomize_time(0.5)
            
            device.shell(f'input tap 1365 104') #close governor info
            # Write data to Excel
            sheet1.write(i - j + 1, 0, gov_name)
            sheet1.write(i - j + 1, 1, tointcheck(gov_id))
            sheet1.write(i - j + 1, 2, tointcheck(gov_power))
            sheet1.write(i - j + 1, 3, tointcheck(gov_killpoints))
            sheet1.write(i - j + 1, 4, tointcheck(gov_dead))
            sheet1.write(i - j + 1, 5, tointcheck(kills_tiers[0]))
            sheet1.write(i - j + 1, 6, tointcheck(kills_tiers[1]))
            sheet1.write(i - j + 1, 7, tointcheck(kills_tiers[2]))
            sheet1.write(i - j + 1, 8, tointcheck(kills_tiers[3]))
            sheet1.write(i - j + 1, 9, tointcheck(kills_tiers[4]))
            sheet1.write(i - j + 1, 10, tointcheck(gov_rss_assistance))
            sheet1.write(i - j + 1, 11, tointcheck(gov_alliance_helps))
            sheet1.write(i - j + 1, 12, alliance_tag)
            sheet1.write(i - j + 1, 13, tointcheck(gov_kills_high))
            sheet1.write(i - j + 1, 14, tointcheck(gov_deads_high))
            sheet1.write(i - j + 1, 15, tointcheck(gov_sevs_high))
            all_data.append([
                gov_name,
                tointcheck(gov_id),
                tointcheck(gov_power),
                tointcheck(gov_killpoints),
                tointcheck(gov_dead),
                tointcheck(kills_tiers[0]),
                tointcheck(kills_tiers[2]),
                tointcheck(kills_tiers[3]),
                tointcheck(kills_tiers[4]),
                tointcheck(gov_rss_assistance),
                tointcheck(gov_alliance_helps),
                alliance_tag,
                tointcheck(gov_kills_high),
                tointcheck(gov_deads_high),
                tointcheck(gov_sevs_high),
            ])

            #ETA
            elapsed_time = time.time() - start_time
            loops_completed = i + 1 - j
            remaining_loops = search_range - loops_completed
            average_time_per_loop = elapsed_time / loops_completed
            estimated_remaining_time = remaining_loops * average_time_per_loop
            estimated_remaining_minutes = estimated_remaining_time / 60
            print(f"Time running: {elapsed_time:.2f}s | Estimated remaining time: {estimated_remaining_minutes:.2f} mins\n")
            print('----------------------------------------------------------------\n')
            randomize_time(1)

            
    except:
        print('An issue has occured. Please rerun the tool and use "resume scan option" from where tool stopped. If issue seems to remain, please contact me on discord!')
        #Save the excel file in the following format e.g. TOP300-2021-12-25-1253.xls or NEXT300-2021-12-25-1253.xls
        traceback.print_exc()
        pass
    if resume_scanning :
        file_name_prefix = 'NEXT'
    else:
        file_name_prefix = 'TOP'
    wb.save(f'output/Governor_Scan_{file_name_prefix}-{search_range-j}_{kingdom}_{today_datetime}.xls')
    #googlesheets
    
    config = getAppConfig()
    client = get_client(config)

    data_description = config["EVENT_DESCRIPTION"] +' - ' + (utc_datetime.strftime("%d %b"))
    add_data_tab(config, new_gs_tab, all_data, client)
    add_looker_tab(config, data_description, new_gs_tab, client)
    print("Governor Scan Completed.")

if __name__ == "__main__":
    check_for_updates()
    create_input_gui()
    adb = initialize_adb() 
    device = get_device(adb)
    resize_emulator(device)
    wb, sheet1 = setup_excel()
    main_loop(device, sheet1)
