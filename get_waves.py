from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import credentials  

import time
import requests
import csv
# import pandas as pd
# from io import StringIO
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading


# Plot Map ?? : https://pypi.org/project/Cartopy/

minLongitude = 66 # x1
maxLongitude = 100 # x2

minLatitude = 24 # y1
maxLatitude = 4 # y2


# 1) Get Session ID

# 2) Send Requests : Long ; Lat Info
# 3) Send Requests : CSV File
# 4) Gave in .csv
# 5) Repeat 2


#  Creates a JxJ Node Matrix
total_xy_axis_values = 5

x_offset = (100 - 66) / total_xy_axis_values  # Each X_Node
y_offset = (24 - 4) / total_xy_axis_values    # Each Y_Node

fp_all_waves_data = "./wavesData/all_waves_data.csv"
fp_day1_waves_data = "./wavesData/day1_waves_data.csv"
fp_day2_waves_data = "./wavesData/day2_waves_data.csv"
fp_day3_waves_data = "./wavesData/day3_waves_data.csv"

def get_sessionid(email:str, password:str) -> str:
    """Login into the website: https://sarat.incois.gov.in/shipforecast/Login.jsp
    
    Retrieve JSESSIONID ; JSESSIONID [both are unique]
    Keyword arguments:
    argument -- None

    Return: JSESSIONID's [ ]str
    """
    # Configure Browser
    options = Options()
    service = Service("chromedriver.exe")
    browser = webdriver.Chrome(service = service, options = options)
    actions = ActionChains(browser)

    # Open URL
    browser.get("https://sarat.incois.gov.in/shipforecast/Login.jsp")
    time.sleep(3)

    # Enter Email and Password and read JSESSIONID from cookies
    email_pass_captcha = browser.find_elements(by= By.TAG_NAME, value= "input")
    email_pass_captcha[0].send_keys(email)
    email_pass_captcha[1].send_keys(password)
    captcha = input("Please Input Captcha Here: ")
    email_pass_captcha[2].send_keys(captcha)
    email_pass_captcha[3].click()
    time.sleep(3)
    cookies_list = browser.get_cookies()
    return cookies_list[0]["value"]
    

def download_waves_node(JSESSIONID:str, x:str, y:str) -> list[str]:
    # print(f"Jsession Id : {JSESSIONID}")
    url = "https://sarat.incois.gov.in/shipforecast/ship_route.jsp"
    csv_url = "https://sarat.incois.gov.in/shipforecast/final_forecastcsv.csv" 
    header = {
        "Host": "sarat.incois.gov.in",
        "Cookie": f"JSESSIONID={JSESSIONID}",
        "Cache-Control": "max-age=0",
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "en-US",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "https://sarat.incois.gov.in",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://sarat.incois.gov.in/shipforecast/shipforecast.jsp",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }
    csv_header = {
        "Host": "sarat.incois.gov.in",
        "Cookie": f"JSESSIONID={JSESSIONID}",
        "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "en-US",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Referer": "https://sarat.incois.gov.in/shipforecast/ship_route.jsp",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive"
    }
    data = {
                "fix": "Fixed",
                "lat": f"{y}",
                "lon": f"{x}",
                "speed": "1",
                "bar": "1",
                "it": "2024-09-13",
                "time": "00",
                "email": "",
                "submit": "submit"
    }
    try:
        # Request for forecast of the above coordinates
        response = requests.post(url= url, headers= header, data= data)
        # Get the response in csv
        response = requests.get(url = csv_url, headers= csv_header)
    except Exception as e:
        print(f"Error: {e}")
    global global_current_node_count
    print(f"NodeNum : {global_current_node_count}  |  Node : <{x}, {y}> Completed")
    return [JSESSIONID, response.text]


global global_csv_content
global global_csv_lock
global global_current_node_count
global global_if_header_saved

def increament_and_store_global_node_count(content):
    global global_csv_lock
    global global_current_node_count
    global global_csv_content
    global global_if_header_saved
    # Store the header for the first time
    with global_csv_lock:
        if global_if_header_saved == False:
            global_csv_content += content
            global_if_header_saved = True

        else:
            global_csv_content += content[142:]

        global_current_node_count += 1

def create_new_request_to_account(executor, jsessionid, node_list):
    new_future = executor.submit(download_waves_node, jsessionid, node_list[global_current_node_count][0], node_list[global_current_node_count][1])
    jsessionid, csv_content = new_future.result()
    increament_and_store_global_node_count(content= csv_content)
    if global_current_node_count < len(node_list):
        create_new_request_to_account(executor= executor, jsessionid= jsessionid, node_list= node_list)


def manage_accounts(futures, node_list, executor):
    global global_current_node_count
    global global_csv_content
    global global_csv_lock

    global_csv_content = ""
    global_csv_lock = threading.Lock()
    
    for future in as_completed(futures):
        jsessionid, csv_content = future.result()
        increament_and_store_global_node_count(content= csv_content)
        
        if global_current_node_count < len(node_list):
            create_new_request_to_account(executor= executor, jsessionid= jsessionid, node_list= node_list)
            
        

global _start_time
def tic():
    global _start_time
    _start_time = time.perf_counter()

def toc():
    """Stop the timer and return the elapsed time."""
    if _start_time is None:
        raise RuntimeError("toc() called before tic()")
    elapsed_time = time.perf_counter() - _start_time
    print(f"Elapsed time: {elapsed_time:0.4f} seconds")
    return elapsed_time

def multi_process_fetch(JSESSIONLIST: list[str], node_list: list[str]) -> str:
    global global_current_node_count
    global global_csv_content
    global global_if_header_saved
    global _start_time
    _start_time = None
    global_if_header_saved = False
    global_current_node_count = 0
    tic()
    with ThreadPoolExecutor(max_workers=len(JSESSIONLIST)) as executor:
        futures = set()
        for session in JSESSIONLIST:
            if global_current_node_count < len(node_list):
                futures.add(executor.submit(download_waves_node, session, node_list[global_current_node_count][0], node_list[global_current_node_count][1]))
                global_current_node_count += 1
        
        manage_accounts(futures, node_list, executor)
    
    executor.shutdown(wait= True)
    toc()
    return global_csv_content
        


def download_waves_data(JSESSIONIDLIST: list[str]):
    """Downloads Waves Data By Entering Range of Node [Longitudes, Latitudes]

    The Function Uses the Session ID and Requests the Data Server, and stores in one csv file
    
    Keyword arguments:
    argument -- JSESSIONID : str

    Return: return_description
    """
    
    print(f"x_offset : {x_offset}  |  y_offset : {y_offset}")
    y = minLatitude
    
    total_accounts = len(JSESSIONIDLIST)
    print(f"Total Accounts : {total_accounts}")
    node_list = []
    
    node_count = 0
    while(y > maxLatitude):
        x = minLongitude
        while(x <= maxLongitude):
            node_count += 1
            newx = "{:.3f}".format(x)
            newy = "{:.3f}".format(y)
            node_list.append([newx, newy])
            x+= x_offset
        y -= y_offset
    print(f"Length Nodes : {len(node_list)}")
       
    # Start Request for all Accounts -> 10
    csv_content = multi_process_fetch(JSESSIONLIST= JSESSIONIDLIST, node_list = node_list)
    
    try:
        # print(f"DATA: \n{csv_content}")
        with open("./wavesData/all_waves_data.csv", 'w', encoding='utf') as file:
            file.write(csv_content)
        print("Stored All Waves Data at: './wavesData/all_waves_data.csv' ✔️")
    except:
        print("Error is Saving, Printing Content : \n", csv_content)


def clean_waves_data():
    """Formatting and Removing uneccassary spaces and newlines from the Scrapped File
    
    Keyword arguments:
    argument -- None
    Return: None
    """
    
    print("\nCleaning Downloaded Data ...")
    
    all_waves_data_file = open(fp_all_waves_data, 'r', encoding='utf-8')
    all_waves_content = all_waves_data_file.read()
    all_waves_data_file.close()
    all_waves_content = all_waves_content.replace(",....", ",-99")
    all_waves_list = all_waves_content.split("\n")
    trim_waves_list = []
    
    for index in all_waves_list:    
        data_points = index.split(",")
        data_points = [i.strip() for i in data_points]
        trim_waves_list.append(data_points)
    
    with open(fp_all_waves_data, "w", newline='') as file:
        write = csv.writer(file)
        write.writerows(trim_waves_list[:-1])
    print("Stored All Cleaned Waves Data at: './wavesData/all_waves_data.csv' ✔️")


def segregate_data():
    """Organizes Forecast Data Into Different Dates
    
    Keyword arguments:
    argument -- None
    Return: None
    """
    
    print("Organinzing Data into Multiple Days ...")
    day1_wave_list = []
    day2_wave_list = []
    day3_wave_list = []

    current_day = -1 # Day 1, Day 2, Day 3 ; day = -1 [for personal reasons]
    current_now = 0
    with open(fp_all_waves_data, "r", newline='') as file:
        read = csv.reader(file)
        ifheader = True

        for row in read:
            if ifheader :
                day1_wave_list.append(row)
                day2_wave_list.append(row)
                day3_wave_list.append(row)
                ifheader = False
                continue
            try:
                current_now = row[1]
            except:
                continue
            if current_now == "00":
                current_day = (current_day + 1) % 3
            match current_day:
                case 0:
                    day1_wave_list.append(row)
                case 1:
                    day2_wave_list.append(row)
                case 2:
                    day3_wave_list.append(row)
    
    with open(fp_day1_waves_data, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(day1_wave_list)
        print(f"Stored Day1 at: {fp_day1_waves_data} ✔️")

    with open(fp_day2_waves_data, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(day2_wave_list)
        print(f"Stored Day1 at: {fp_day2_waves_data} ✔️")

    with open(fp_day3_waves_data, "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerows(day3_wave_list)
        print(f"Stored Day1 at: {fp_day3_waves_data} ✔️")
    
def save_session_ids (JSESSIONLIST: list[str]):
    with open("SESSION_IDS", "r") as file:
        if len(file.read()) > 0:
            print("SESSION IDs Already Stored")
            print("Please Delete to New Sessions")
            return
    with open("SESSION_IDS", "w") as file:
        for session in JSESSIONLIST:
            file.write(session + "\n")

    print("Stored Current Session ID at: `SESSION_IDS`")

def get_sessionids_from_file() ->  list[str]:
    try:
        with open("SESSION_IDS", "r") as file:
            session_list = []
            content = file.read().strip()
            if len(content) == 0 :
                print("SESSION_IDS empty")
                return session_list
            return content.split("\n")
    except Exception as e:
        print(f"Error in get_session_ids : {e}")

if __name__ == "__main__":
    try:
        JSESSIONLIST = get_sessionids_from_file()
        print("Number of Session IDs : ",len(JSESSIONLIST))
        if len(JSESSIONLIST) == 0:
            for email in credentials.INCOIS_EMAIL_LIST:
                JSESSIONLIST.append(get_sessionid(email= email, password= credentials.INCOIS_PASSWORD))
            save_session_ids(JSESSIONLIST= JSESSIONLIST)
        print(f"Recieved JSESSIONIDs : {JSESSIONLIST}")
        
        download_waves_data(JSESSIONIDLIST= JSESSIONLIST)
        clean_waves_data()
        segregate_data()
    except Exception as e:
        print("Some Error Occured : \n", e)
    