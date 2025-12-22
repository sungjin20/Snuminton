from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import re
from digital import *

my_id = "widepis"
my_pw = "ida_consult"
student_name = "김라온"
teacher_name = "이우종"
majorId = "TWpZeE1URXpOVEUub1hWcmFTbnRpN3pvdW8wNA"

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 실행 완료 후 브라우저 꺼짐 방지
chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 도구 인식 방지

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

url = "https://member.jinhak.com/MemberV3/MemberJoin/MemberLogIn.aspx"
driver.get(url)

# 페이지 로딩 대기 (최대 10초)
wait = WebDriverWait(driver, 10)

id_input = wait.until(EC.presence_of_element_located((By.ID, "txtMemID"))) 
pw_input = driver.find_element(By.ID, "txtMemPass")

id_input.send_keys(my_id)
time.sleep(1) # 사람처럼 보이기 위한 짧은 지연
pw_input.send_keys(my_pw)
time.sleep(1)
login_button = driver.find_element(By.XPATH, '//*[@id="panel_1"]/div/div[1]/div[3]/button')
login_button.click()
time.sleep(1)
url = "https://www.jinhak.com/jh/high3/regular/four-year-university/report/pass-predict?periodCode=J1&majorId=" + majorId
driver.get(url)
element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.w-1\/2.md\:w-auto.grow.md\:grow-0.inline-flex.items-center.justify-center.border.border-transparent.sm\:rounded-lg.md\:rounded-lg.md\:min-w-\[10\.625rem\].h-\[3rem\].md\:px-4.text-base.leading-none.lg\:text-lg.text-white.bg-blue-800.rounded')))
element.click()

gun = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span[1]/span[1]'))).text + "군"

university = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span[1]/span[2]').text

department = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span[2]').text

date = "'" + datetime.now().strftime('%m/%d')

temp = driver.find_elements(By.XPATH, "//b[contains(text(), '등 / ')]")[-1].text
numbers = re.findall(r'\d+', temp)
my_rank = numbers[0]

target_number = numbers[1]

temp = driver.find_element(By.XPATH, "//p[contains(text(), '(최초합 ')]").text
numbers = re.findall(r'\d+', temp)
initial = numbers[0]

initial_plus_addition = driver.find_elements(By.CSS_SELECTOR, ".mt-3.lg\\:mt-4.first\\:mt-0.flex.w-full.items-start.justify-between.text-xs.sm\\:text-sm.text-left.md\\:text-center.md\\:text-base.flex-wrap")[-1].find_element(By.CSS_SELECTOR, "div.text-right p b").text.replace("명", "")

temp = driver.find_elements(By.CSS_SELECTOR, ".px-2.md\\:px-\\[0\\.625rem\\].text-2xs.sm\\:text-sm.xl\\:text-base")
competetion_rate_2025 = temp[0].find_element(By.CSS_SELECTOR, "li:nth-of-type(3) span:nth-of-type(2) b").text
competetion_rate_2024 = temp[1].find_element(By.CSS_SELECTOR, "li:nth-of-type(3) span:nth-of-type(2) b").text
competetion_rate_2023 = temp[2].find_element(By.CSS_SELECTOR, "li:nth-of-type(3) span:nth-of-type(2) b").text

can_number = int(driver.find_element(By.CSS_SELECTOR, 'div[style="text-shadow: rgb(255, 255, 255) 1px 1px 0px, rgb(255, 255, 255) -1px -1px 0px, rgb(255, 255, 255) 1px -1px 0px, rgb(255, 255, 255) -1px 1px 0px;"]').text.replace("칸", ""))

can_my_rank = driver.find_element(By.XPATH, "//div[contains(text(), '등(나)')]").text.replace("등(나)", "")

can_initial_rank = None
can_final_rank = None
api_url = f"https://www.jinhak.com/jh/api/regular/report/pass-prediction/competitor-distribution?periodCode=J1&majorId={majorId}&evaluationStepCode=0"
script = f"""
    const response = await fetch('{api_url}');
    const data = await response.json();
    return data;
"""
api_data = driver.execute_script(script)
checked_initial_rank = False
for i in api_data['competitors']:
    if int(i['stabilityLevel']) != can_number: continue
    if not checked_initial_rank:
        can_initial_rank = i['totalRank']
        checked_initial_rank = True
    can_final_rank = i['totalRank']

competetion_rate = driver.find_elements(By.CSS_SELECTOR, ".flex.h-full.items-center.justify-center.w-full.gap-x\-\[0\.125rem\].md\:gap-x-1")
competetion_rate_by_can = []
for i in range(6):
    competetion_rate_by_can.append(competetion_rate[i].text)
competetion_rate_down = None
competetion_rate_up = None
if can_number >= 2 and can_number <= 7:
    competetion_rate_down = competetion_rate_by_can[7-can_number]
elif can_number == 1:
    competetion_rate_down = "0%"
if can_number >= 3 and can_number <= 8:
    competetion_rate_up = competetion_rate_by_can[8-can_number]
elif can_number <= 2:
    competetion_rate_up = "0%"

url = f"https://www.jinhak.com/jh/high3/regular/four-year-university/report/prediction-change?periodCode=J1&majorId={majorId}"
driver.get(url)

api_url = f"https://www.jinhak.com/jh/api/regular/report/prediction-change/self-phantom?periodCode=J1&majorId={majorId}"
script = f"""
    const response = await fetch('{api_url}');
    const data = await response.json();
    return data;
"""
api_data = driver.execute_script(script)
student_score = api_data['convertedScore']

today = datetime.now().strftime('%m/%d')
initial_cut = ""
final_cut = ""
for i in api_data['timelines']:
    if today in i['analysisDate']:
        gubun = i['firstCutConvertedScore']['gubun']
        values = i['firstCutConvertedScore']['values']
        if gubun == "digitalM":
            num_len = len(values) // 3
            for j in range(num_len):
                up = values[j]
                mid = values[j + num_len]
                down = values[j + num_len*2]
                initial_cut += decode_cut(gubun, up, down, mid)
        else:
            num_len = len(values) // 2
            for j in range(num_len):
                up = values[j]
                down = values[j + num_len]
                initial_cut += decode_cut(gubun, up, down)
        
        gubun = i['finalCutConvertedScore']['gubun']
        values = i['finalCutConvertedScore']['values']
        if gubun == "digitalM":
            num_len = len(values) // 3
            for j in range(num_len):
                up = values[j]
                mid = values[j + num_len]
                down = values[j + num_len*2]
                final_cut += decode_cut(gubun, up, down, mid)
        else:
            num_len = len(values) // 2
            for j in range(num_len):
                up = values[j]
                down = values[j + num_len]
                final_cut += decode_cut(gubun, up, down)
    break
        
print(gun)
print(university)
print(department)
print(date)
print(my_rank)
print(target_number)
print(initial)
print(initial_plus_addition)
print(competetion_rate_2025)
print(competetion_rate_2024)
print(competetion_rate_2023)
print(can_number)
print(can_my_rank)
print(can_initial_rank)
print(can_final_rank)
print(competetion_rate_down)
print(competetion_rate_up)
print("############")
print(student_score)
print(initial_cut)
print(final_cut)