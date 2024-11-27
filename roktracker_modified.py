from ppadb.client import Client
import cv2
import sys
import os
import pytesseract
import numpy as np
import time
from matplotlib import pyplot as plt
#import xlwt 
#from xlwt import Workbook
from openpyxl import load_workbook
from openpyxl.workbook import Workbook
from openpyxl.styles import Font
from openpyxl.styles import DEFAULT_FONT
import datetime
import tkinter as tk
from tkinter import messagebox
import keyboard
from neural_network import read_ocr
import requests
import webbrowser
import traceback
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

version = "RokTracker-v8.3"
output_folder = 'output'
ss_folder = 'screenshots'

def getgovname(alliace_name):
	return alliace_name.split(" ",1);

def tointcheck(element):
	try:
		return int(element)
	except ValueError:
		return element
		
def tointprint(element):
	try:
		return str(f'{int(element):,}')
	except ValueError:
		return str(element)

#Initiliaze paths and variables
utc_datetime = datetime.datetime.now(datetime.timezone.utc)
today = utc_datetime.strftime("%Y-%m-%d-%H%MZ")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' #Change to your installation path folder.

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
os.system("")

##### Update Checker #####
response = requests.get("https://api.github.com/repos/nikolakis1919/RokTracker/releases/latest")
if (response.json()["name"]) != version:
	bo = tk.Tk()
	bo.withdraw()
	messagebox.showinfo("Tool is outdated", "New version is available on github repository. It is highly recommended to update the tool!")
	bo.destroy()


####### Tkinter Section ##########
#Create input gui
root=tk.Tk()

#Tkinter title
root.title('RokTracker')

#Tkinter window size
root.geometry("400x350")

#Tkinter function
def link():
	webbrowser.open_new(r"https://www.paypal.com/donate/?hosted_button_id=55G95MNYPVX72")

#Initialize Options for dropdown box
OPTIONS = []
for i in range(38):
	OPTIONS.append(50+i*25)
	
#Variables

kd_id_input = tk.StringVar(root)
kd_id_input.set(config.get('Default', 'KingdomId', fallback='2816'))
search_range_dropdown = tk.IntVar(root)
search_range_dropdown.set(config.getint('Default', 'SearchRange', fallback=50)) # default value
curr_scan_pos_input = tk.StringVar(root)
curr_scan_pos_input.set(config.get('Default', 'Position', fallback="1"))
resume_scan_chkbox = tk.IntVar()
resume_scan_chkbox.set(config.getboolean('Default', 'ResumeScan', fallback=False))
new_file_chkbox = tk.IntVar()
new_file_chkbox.set(config.getboolean('Default', 'NewFile', fallback=False))
is_repair_chkbox = tk.IntVar()
is_repair_chkbox.set(config.getboolean('Default', 'IsRepair', fallback=False))

#Labels
kingdom_label = tk.Label(root, text = 'Kingdom', font=('calibre',10, 'bold'))  
search_top_label = tk.Label(root, text = 'Search Amount', font=('calibre',10, 'bold'))
position_label = tk.Label(root, text = 'Position', font=('calibre',10, 'bold'))  
#Copyrights
copyright=u"\u00A9"
copyright_label=tk.Label(root, text=copyright + ' nikolakis1919 [modded by Rei]', font = ('calibre',10,'bold')) 
donation_label=tk.Button(root, foreground='Green', text='Donate to nikolakis', command=link, font = ('calibre',10,'bold'))
disc3=tk.Label(root,text='Find me on discord: nikos#4469', font = ('calibre',10,'bold'))

#Input Fields
kingdom_entry = tk.Entry(root, textvariable=kd_id_input, font=('calibre',10,'normal'))
position_entry = tk.Entry(root, textvariable=curr_scan_pos_input, font=('calibre',10,'normal'))
scan_range_selector = tk.OptionMenu(root, search_range_dropdown, *OPTIONS)
resume_scan_box =tk.Checkbutton(root, text="Resume Scan", variable=resume_scan_chkbox, font=('calibre',10,'bold'))
new_file_box = tk.Checkbutton(root, text="New File", variable=new_file_chkbox, font=('calibre',10,'bold'))
is_repair_box =tk.Checkbutton(root, text="Is Repair", variable=is_repair_chkbox, font=('calibre',10,'bold'))

def search():
	if kd_id_input.get():
		global kingdom
		kingdom = kd_id_input.get()
		global search_range
		search_range = search_range_dropdown.get()
		global resume_scanning
		resume_scanning = resume_scan_chkbox.get()
		global new_file
		new_file = new_file_chkbox.get()
		global current_pos
		current_pos = curr_scan_pos_input.get()
		global repair_mode
		repair_mode = is_repair_chkbox.get()
		root.destroy()
		print("Scanning Started...")
	else:
		print("You need to fill Kingdom number!")
		kingdom_entry.focus_set()
		
button = tk.Button(root, text="Search", command=search)

#Positions in tkinter Grid
kingdom_label.grid(row=0,column=0)
kingdom_entry.grid(row=0,column=1)
position_label.grid(row=1,column=0)
position_entry.grid(row=1,column=1)
search_top_label.grid(row=2,column=0)
scan_range_selector.grid(row=2,column=1)
resume_scan_box.grid(row=3,column=1,pady=4)
new_file_box.grid(row=4,column=1,pady=4)
is_repair_box.grid(row=5,column=1,pady=4)
button.grid(row=6,column=1,pady=5)
copyright_label.grid(row=7,column=1,pady=10)
donation_label.grid(row=11,column=1,pady=10)
disc3.grid(row=8,column=1,pady=10)
root.mainloop()

#######RokTracker
#Initialize the connection to adb
adb = Client(host='localhost', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

#Prolly a good idea to have only 1 device while running this
device = devices[0]


######Excel Formatting
if resume_scanning and new_file and not repair_mode:
	file_name_prefix = 'NEXT'
else:
	file_name_prefix = 'TOP'
	
if config.get('Default', 'PreviousFile') and resume_scanning and not new_file:
	file_name = config.get('Default', 'PreviousFile')
else:
	file_name = output_folder+ '/' + file_name_prefix + str(search_range) + '-' +str(today)+ '-' + kingdom +'.xlsx'

print(file_name)

if resume_scanning and repair_mode and not new_file:
	wb = load_workbook(file_name)
	page = wb.active
	print('continue')
else:
	wb = Workbook()
	page = wb.active
	page.title = str(today)
	#Initialize Excel Sheet Header
	row = page.row_dimensions[1]
	row.font = Font(name='Arial', size=10, bold=True)
	headers = [
		'Position',
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
		'Alliance',
		'Expected Pos'
	]
	page.column_dimensions['A'].width = 8
	page.column_dimensions['B'].width = 15
	page.column_dimensions['C'].width = 15
	page.column_dimensions['D'].width = 18
	page.column_dimensions['E'].width = 18
	page.column_dimensions['F'].width = 18
	page.column_dimensions['G'].width = 18
	page.column_dimensions['H'].width = 18
	page.column_dimensions['I'].width = 18
	page.column_dimensions['J'].width = 18
	page.column_dimensions['K'].width = 18
	page.column_dimensions['L'].width = 20
	page.column_dimensions['M'].width = 25
	page.column_dimensions['N'].hidden = True
	page.append(headers)

#Resume Scan options. Refine the loop
j = 0
if resume_scanning:
	j = int(current_pos) - 1
	if not repair_mode:
		search_range = search_range + j - 1

#Position for next governor to check
Y = [285, 389, 487, 592, 615]

#The loop in TOP XXX Governors in kingdom - It works both for power and killpoints Rankings
#MUST have the tab opened to the 1st governor(Power or Killpoints)


##### Save button listener#####
stop = False
def onkeypress(event):
	global stop
	if event.name == '\\':
		print("Your scan will be terminated when current governor scan is over!")
		stop = True

keyboard.on_press(onkeypress)

#first 3 has laurels around numbers
positioning_width_tuple = [(212, 24, 28, 50), (185, 24, 61, 50)]
threshold_tuple = [(cv2.IMREAD_COLOR, 220), (cv2.IMREAD_GRAYSCALE, 150)]
roi_name_width_tuple = [(333, 27, 358, 58), (333, 30, 358, 58)]
roi_power_width_tuple = [(1186, 25, 170, 50), (1186, 25, 170, 50)]


gov_position = int(current_pos)
sheetoffset = 0
ran_before = False
has_error = False

try:
	for i in range(j, search_range):
		if stop:
			print("Scan Terminated! Saving the current progress...")
			break
		if i>4:
			k = 4
		else:
			k = i
			
		gov_dead = 0
		gov_kills_tier1 = 0
		gov_kills_tier2 = 0
		gov_kills_tier3 = 0
		gov_kills_tier4 = 0
		gov_kills_tier5 = 0
		gov_rss_assistance = 0

		if k > 3:
			current_threshold = threshold_tuple[1]
			roi_width = positioning_width_tuple[1]
			name_roi_width = roi_name_width_tuple[1]
			power_roi_width = roi_power_width_tuple[1]
		else:
			current_threshold = threshold_tuple[0]
			roi_width = positioning_width_tuple[0]
			name_roi_width = roi_name_width_tuple[0]
			power_roi_width = roi_power_width_tuple[0]


		image_check = device.screencap()
		numpy_array =  np.frombuffer(image_check, np.byte)
		image_check = cv2.imdecode(numpy_array, current_threshold[0])
		_, thresh1 = cv2.threshold(image_check, current_threshold[1], 255, cv2.THRESH_BINARY) 

		roi = (roi_width[0], Y[k]-roi_width[1], roi_width[2], roi_width[3])
		im_position_listing = thresh1[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		position = pytesseract.image_to_string(im_position_listing, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		current_pos = position.strip()
		
		ran_before = True
		#Open governor
		device.shell(f'input tap 690 ' + str(Y[k]))
		time.sleep(1.8)
		
		##### Ensure that governor tab is open #####
		gov_info = False
		count = 0
		while not (gov_info):
			image_check = device.screencap()
			numpy_array =  np.frombuffer(image_check, np.byte)
			image_check = cv2.imdecode(numpy_array, cv2.IMREAD_GRAYSCALE)
			roi = (294, 786, 116, 29)
			im_check_more_info = image_check[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
			check_more_info = pytesseract.image_to_string(im_check_more_info,config="-c tessedit_char_whitelist=MoreInfo")

			###
			if 'MoreInfo' not in check_more_info:
				_, thresh1 = cv2.threshold(image_check, current_threshold[1], 255, cv2.THRESH_BINARY) 
				roi = (roi_width[0], Y[k]-roi_width[1], roi_width[2], roi_width[3])
				name_roi = (name_roi_width[0], Y[k]-name_roi_width[1], name_roi_width[2], name_roi_width[3])
				power_roi = (power_roi_width[0], Y[k]-power_roi_width[1], power_roi_width[2], power_roi_width[3])
				im_position_listing = thresh1[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

				d_name_alliance = thresh1[int(name_roi[1]):int(name_roi[1]+name_roi[3]), int(name_roi[0]):int(name_roi[0]+name_roi[2])]
				d_power = thresh1[int(power_roi[1]):int(power_roi[1]+power_roi[3]), int(power_roi[0]):int(power_roi[0]+power_roi[2])]

				d_alliance = d_name_alliance[31:83,0:358]
				d_name = d_name_alliance[0:32,0:358]
				position = pytesseract.image_to_string(im_position_listing, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
				current_pos = position.strip()
				alliance_tag = (pytesseract.image_to_string(d_alliance, config="--psm 10 --oem 3")).strip()
				gov_name = (pytesseract.image_to_string(d_name, config="--psm 10 --oem 3")).strip()
				print(alliance_tag)
				print(gov_name)

				if (alliance_tag != '-' and alliance_tag != ''):
					[tag, gov_name] = getgovname(gov_name)
					alliance_tag = ''.join([tag, alliance_tag])
				else: 
					alliance_tag = '-'
				gov_power = pytesseract.image_to_string(d_power, config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
				
				device.shell(f'input swipe 690 605 690 499')
				#device.shell(f'input swipe 690 605 690 540')
				device.shell(f'input tap 690 ' + str(Y[k]))
				
				print('Position: ' + current_pos + '\nGovernor ID: -\nGovernor Name: ' + gov_name + '\nGovernor Power: ' + tointprint(gov_power) + '\nGovernor Killpoints: -\nTier 1 kills: -\nTier 2 kills: -\nTier 3 kills: -\nTier 4 kills: -\nTier 5 kills: -\nGovernor Dead Troops: -\nGovernor RSS Assistance: -\nAlliance: ' + str(alliance_tag) + '\n')
				page.append([
					current_pos,
					gov_name,
					'-',
					tointcheck(gov_power),
					'-',
					'-',
					'-',
					'-',
					'-',
					'-',
					'-',
					'-',
					str(alliance_tag),
					gov_position,
				])
				gov_position = gov_position + 1
				count += 1
				time.sleep(2)
				if count == 10:
					break
			else:
				gov_info = True
				break
		
		#nickname copy
		device.shell(f'input tap 654 245')
		time.sleep(1.3)
		
		##### Governor main page capture #####
		image = device.screencap()
		numpy_array =  np.frombuffer(image, np.byte)
		gov_info_img = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)

		#with open(('gov_info.png'), 'wb') as f:
		#			f.write(image)
		#image = cv2.imread('gov_info.png')
		image = gov_info_img.copy()
		#Power and Killpoints
		roi = (733, 192, 200, 35)
		im_gov_id = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		#image = cv2.imread('gov_info.png')
		
		image = gov_info_img.copy()
		roi = (874, 327, 224, 40)
		im_gov_power = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		roi = (1106, 327, 224, 40)
		im_gov_killpoints = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		gov_name = tk.Tk().clipboard_get()


		#New image for alliance tag
		#image = cv2.imread('gov_info.png')
		image = gov_info_img.copy()
		kernel = np.ones((2, 2), np.uint8)
	 
		image = cv2.erode(image, kernel) 
		roi = (598, 331, 250, 40) #alliance tag
		im_alliance_tag = image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		
		#kills tier
		device.shell(f'input tap 1118 314')
        
		#1st image OCR
		gov_id = read_ocr(im_gov_id)
		gov_killpoints2 = pytesseract.image_to_string(im_gov_killpoints,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		gov_power2 = pytesseract.image_to_string(im_gov_power,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		gov_power = read_ocr(im_gov_power)
		gov_killpoints = read_ocr(im_gov_killpoints)
		gov_killpoints = gov_killpoints2 if (len(''.join(str(gov_killpoints).split()))-1 > len(str(gov_killpoints))) else gov_killpoints
		gov_power = gov_power2 if (len(''.join(str(gov_power2).split()))-1 > len(str(gov_power))) else gov_power

		time.sleep(1)
		##### Kill tier Capture #####
		image = device.screencap()
		numpy_array =  np.frombuffer(image, np.byte)
		image2 = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
		#with open(('kills_tier.png'), 'wb') as f:
		#			f.write(image)
		#image2 = cv2.imread('kills_tier.png')
		image2 = cv2.fastNlMeansDenoisingColored(image2,None,20,20,7,3)
		_,image2 = cv2.threshold(image2,180,255,cv2.THRESH_BINARY)
		roi = (862, 430, 215, 26) #tier 1
		im_kills_tier1 = image2[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

		roi = (862, 475, 215, 26) #tier 2
		im_kills_tier2 = image2[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

		roi = (862, 516, 215, 26) #tier 3
		im_kills_tier3 = image2[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

		roi = (862, 561, 215, 26) #tier 4
		im_kills_tier4 = image2[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

		roi = (862, 606, 215, 26) #tier 5
		im_kills_tier5 = image2[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]

		#More info tab
		device.shell(f'input tap 350 740') 
		
		##### Kill tier OCR #####
		gov_kills_tier1 = pytesseract.image_to_string(im_kills_tier1,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		gov_kills_tier2 = pytesseract.image_to_string(im_kills_tier2,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		gov_kills_tier3 = pytesseract.image_to_string(im_kills_tier3,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		gov_kills_tier4 = pytesseract.image_to_string(im_kills_tier4,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		gov_kills_tier5 = pytesseract.image_to_string(im_kills_tier5,config="--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789")
		time.sleep(1)
		
		
		##### More Info Page Capture #####
		image = device.screencap()
		
		numpy_array =  np.frombuffer(image, np.byte)
		image3 = cv2.imdecode(numpy_array, cv2.IMREAD_COLOR)
		#with open(('more_info.png'), 'wb') as f:
		#			f.write(image)
		#image3 = cv2.imread('more_info.png')
		kernel = np.ones((2, 2), np.uint8)
		image3 = cv2.dilate(image3, kernel)
		roi = (1130, 443, 183, 40) #dead
		im_dead = image3[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		roi = (1130, 668, 183, 40) #rss assistance
		im_rss_assistance = image3[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		
		#2nd check for deads with more filters to avoid some errors
		roi = (1130, 443, 183, 40) #dead
		thresh = 127
		thresh_image = cv2.threshold(image3, thresh, 255, cv2.THRESH_BINARY)[1]
		im_dead2 = thresh_image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		roi = (1130, 668, 183, 40) #rss assistance
		im_rss_assistance2 = thresh_image[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		
		#3rd check for deads with more filters to avoid some errors
		roi = (1130, 443, 183, 40) #dead
		blur_img = cv2.GaussianBlur(image3, (3, 3), 0)
		im_dead3 = blur_img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		roi = (1130, 668, 183, 40) #rss assistance
		im_rss_assistance3 = blur_img[int(roi[1]):int(roi[1]+roi[3]), int(roi[0]):int(roi[0]+roi[2])]
		
		##### More info page OCR #####
		gov_dead = read_ocr(im_dead)
		gov_dead2 = read_ocr(im_dead2)
		gov_dead3 = read_ocr(im_dead3)
		gov_rss_assistance = read_ocr(im_rss_assistance)
		gov_rss_assistance2 = read_ocr(im_rss_assistance2)
		gov_rss_assistance3 = read_ocr(im_rss_assistance3)
		
		
		##### Alliance tag #####
		gray = cv2.cvtColor(im_alliance_tag,cv2.COLOR_BGR2GRAY)
		threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
		alliance_tag = (pytesseract.image_to_string(threshold_img, config="--oem 3 --psm 10")).strip()
		
		
		#Just to check the progress, printing in cmd the result for each governor
		if gov_power == '':
			gov_power = 'Unknown'
		if gov_killpoints =='':
			gov_killpoints = 'Unknown'
		if gov_dead == '' :
			if gov_dead2 == '':
				if gov_dead3 =='':
					gov_dead = 'Unknown'
				else:			
					gov_dead = gov_dead3
			else:
				gov_dead = gov_dead2
		if gov_kills_tier1 == '' :
			gov_kills_tier1 = '0'
		if gov_kills_tier2 == '' :
			gov_kills_tier2 = '0'
		if gov_kills_tier3 == '' :
			gov_kills_tier3 = '0'
		if gov_kills_tier4 == '' :
			gov_kills_tier4 = '0'
		if gov_kills_tier5 == '' :
			gov_kills_tier5 = '0'
		if gov_rss_assistance == '' :
			if gov_rss_assistance2 =='':
				if gov_rss_assistance3 =='':
					gov_rss_assistance = 'Unknown'
				else: 
					gov_rss_assistance = gov_rss_assistance3
			else:
				gov_rss_assistance= gov_rss_assistance2
		print('Position: ' + current_pos + '\nGovernor ID: ' + str(gov_id) + '\nGovernor Name: ' + gov_name + '\nGovernor Power: ' + tointprint(gov_power) + '\nGovernor Killpoints: ' + tointprint(gov_killpoints) + '\nTier 1 kills: ' + tointprint(gov_kills_tier1) + '\nTier 2 kills: ' + tointprint(gov_kills_tier2) + '\nTier 3 kills: ' + tointprint(gov_kills_tier3) + '\nTier 4 kills: ' + tointprint(gov_kills_tier4) + '\nTier 5 kills: ' + tointprint(gov_kills_tier5) + '\nGovernor Dead Troops: ' + tointprint(gov_dead) + '\nGovernor RSS Assistance: ' + tointprint(gov_rss_assistance) +'\nAlliance: ' + str(alliance_tag) + '\n')
		device.shell(f'input tap 1396 58') #close more info
		time.sleep(0.5)
		device.shell(f'input tap 1365 104') #close governor info
		time.sleep(1)

		#Write results in excel file
		page.append([
			current_pos,
			gov_name,
			tointcheck(gov_id),
			tointcheck(gov_power),
			tointcheck(gov_killpoints),
			tointcheck(gov_dead),
			tointcheck(gov_kills_tier1),
			tointcheck(gov_kills_tier2),
			tointcheck(gov_kills_tier3),
			tointcheck(gov_kills_tier4),
			tointcheck(gov_kills_tier5),
			tointcheck(gov_rss_assistance),
			str(alliance_tag),
			gov_position,
		])
		gov_position = gov_position + 1
except:
	print('An issue has occured at position: ' + str(gov_position) +'. Please rerun the tool and use "resume scan option" from where tool stopped. If issue seems to remain, please contact me on discord!')
	#Save the excel file in the following format e.g. TOP300-2021-12-25-1253.xls or NEXT300-2021-12-25-1253.xls
	traceback.print_exc()
	pass


DEFAULT_FONT.name = 'Arial'
DEFAULT_FONT.size = 10

wb.save(file_name)

if has_error:
	config['Default']['Position'] = str(current_pos)
	config['Default']['ResumeScan'] = str(True)
	config['Default']['IsRepair'] = str(True)
else: 
	config['Default']['Position'] = str(1)
	config['Default']['ResumeScan'] = str(False)
	config['Default']['IsRepair'] = str(False)
	
config['Default']['KingdomId'] = kingdom
config['Default']['PreviousFile'] = file_name

#Fix last gov permission
with open('config.ini', 'w') as configfile:
  config.write(configfile)