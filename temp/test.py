from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime
import re
from decimal import Decimal, ROUND_HALF_UP
import xlwings as xw
from digital import *

app = xw.App(visible=False)
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)  # 실행 완료 후 브라우저 꺼짐 방지
chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 자동화 도구 인식 방지
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
wait = WebDriverWait(driver, 10)
url = "https://member.jinhak.com/MemberV3/MemberJoin/MemberLogIn.aspx"
driver.get(url)

my_id_list = ["widepis"]
my_pw_list = ["ida_consult"]
student_name_list = ["김라온"]

for account_num in range(len(my_id_list)):
    print(f"####### {len(my_pw_list)}개의 계정 중 {account_num + 1}번째 계정 입력 시작 #######")
    my_id = my_id_list[account_num]
    my_pw = my_pw_list[account_num]
    student_name = student_name_list[account_num]

    wb = xw.Book(f"result/{student_name} 학생 IDA 정시지원 분석 리포트.xlsx")
    ws1 = wb.sheets['기본입력시트']
    row1 = 8
    while ws1.range('D' + str(row1)).value is not None: row1 += 1
    ws2 = wb.sheets['추세별입력시트']
    row2 = 6
    while ws2.range('C' + str(row2)).value is not None: row2 += 1

    id_input = wait.until(EC.presence_of_element_located((By.ID, "txtMemID"))) 
    pw_input = driver.find_element(By.ID, "txtMemPass")
    id_input.send_keys(my_id)
    time.sleep(1)
    pw_input.send_keys(my_pw)
    time.sleep(1)
    login_button = driver.find_element(By.XPATH, '//*[@id="panel_1"]/div/div[1]/div[3]/button')
    login_button.click()
    time.sleep(1)

    api_url = "https://www.jinhak.com/jh/api/regular/library/application-major-list?periodCode=J1"
    script = f"""
        const response = await fetch('{api_url}');
        const data = await response.json();
        return data;
    """
    majorList = driver.execute_script(script)
    for idx in range(len(majorList)):
        major = majorList[idx]
        majorId = major['majorId']

        url = "https://www.jinhak.com/jh/high3/regular/four-year-university/report/pass-predict?periodCode=J1&majorId=" + majorId
        driver.get(url)
        time.sleep(2)
        '''
        try:
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.w-1\/2.md\:w-auto.grow.md\:grow-0.inline-flex.items-center.justify-center.border.border-transparent.sm\:rounded-lg.md\:rounded-lg.md\:min-w-\[10\.625rem\].h-\[3rem\].md\:px-4.text-base.leading-none.lg\:text-lg.text-white.bg-blue-800.rounded')))
            element.click()
        except TimeoutException:
            pass
        '''

        gun = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span[1]/span[1]'))).text + "군"

        university = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span[1]/span[2]').text

        department = driver.find_element(By.XPATH, '/html/body/div[3]/div/div[1]/div[2]/div[1]/div/div/div[1]/span/span/span[2]').text

        date = "'" + datetime.now().strftime('%m/%d')

        temp = driver.find_elements(By.XPATH, "//b[contains(text(), '등 / ')]")[-1].text
        numbers = re.findall(r'\d+', temp)
        my_rank = int(numbers[0])

        target_number = int(numbers[1])

        initial = None
        try:
            temp = driver.find_element(By.XPATH, "//p[contains(text(), '(최초합 ')]").text
            numbers = re.findall(r'\d+', temp)
            initial = int(numbers[0])
        except NoSuchElementException as e:
            print("최초합 크롤링 실패 : " + str(e))
            initial = 0

        initial_plus_addition = int(driver.find_elements(By.CSS_SELECTOR, ".mt-3.lg\\:mt-4.first\\:mt-0.flex.w-full.items-start.justify-between.text-xs.sm\\:text-sm.text-left.md\\:text-center.md\\:text-base.flex-wrap")[-1].find_element(By.CSS_SELECTOR, "div.text-right p b").text.replace("명", ""))

        temp = driver.find_elements(By.CSS_SELECTOR, ".px-2.md\\:px-\\[0\\.625rem\\].text-2xs.sm\\:text-sm.xl\\:text-base")
        competetion_rate_2025 = temp[0].find_element(By.CSS_SELECTOR, "li:nth-of-type(3) span:nth-of-type(2) b").text
        competetion_rate_2024 = temp[1].find_element(By.CSS_SELECTOR, "li:nth-of-type(3) span:nth-of-type(2) b").text
        competetion_rate_2023 = temp[2].find_element(By.CSS_SELECTOR, "li:nth-of-type(3) span:nth-of-type(2) b").text
        if competetion_rate_2025 == '-': competetion_rate_2025 = 0
        else: competetion_rate_2025 = float(competetion_rate_2025)
        if competetion_rate_2024 == '-': competetion_rate_2024 = 0
        else: competetion_rate_2024 = float(competetion_rate_2024)
        if competetion_rate_2023 == '-': competetion_rate_2023 = 0
        else: competetion_rate_2023 = float(competetion_rate_2023)

        can_number = int(driver.find_element(By.CSS_SELECTOR, 'div[style="text-shadow: rgb(255, 255, 255) 1px 1px 0px, rgb(255, 255, 255) -1px -1px 0px, rgb(255, 255, 255) 1px -1px 0px, rgb(255, 255, 255) -1px 1px 0px;"]').text.replace("칸", ""))

        can_my_rank = int(driver.find_element(By.XPATH, "//div[contains(text(), '등(나)')]").text.replace("등(나)", ""))

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
            competetion_rate_by_can.append(float(competetion_rate[i].text.replace("%", "")) / 100.0)
        competetion_rate_down = None
        competetion_rate_up = None
        if can_number >= 2 and can_number <= 7:
            competetion_rate_down = competetion_rate_by_can[7-can_number]
        elif can_number == 1:
            competetion_rate_down = 0
        elif can_number == 8:
            competetion_rate_down = competetion_rate_by_can[0]
        if can_number >= 3 and can_number <= 8:
            competetion_rate_up = competetion_rate_by_can[8-can_number]
        elif can_number <= 2:
            competetion_rate_up = 0

        url = f"https://www.jinhak.com/jh/high3/regular/four-year-university/report/prediction-change?periodCode=J1&majorId={majorId}"
        driver.get(url)

        api_url = f"https://www.jinhak.com/jh/api/regular/report/prediction-change/self-phantom?periodCode=J1&majorId={majorId}"
        script = f"""
            const response = await fetch('{api_url}');
            const data = await response.json();
            return data;
        """
        api_data = driver.execute_script(script)
        student_score = float(Decimal(api_data['convertedScore']).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))

        initial_cut = ""
        final_cut = ""
        today = datetime.now().strftime('%m/%d')
        for i in api_data['timelines']:
            if today in i['analysisDate']:
                gubun = i['firstCutConvertedScore']['gubun']
                values = i['firstCutConvertedScore']['values']
                if gubun == "digitalM":
                    num_len = len(values) // 3
                    for j in range(num_len):
                        up = values[j].split(" ")[0]
                        mid = values[j + num_len].split(" ")[0]
                        down = values[j + num_len*2].split(" ")[0]
                        initial_cut += decode_cut(gubun, up, down, mid)
                else:
                    num_len = len(values) // 2
                    for j in range(num_len):
                        up = values[j].split(" ")[0]
                        down = values[j + num_len].split(" ")[0]
                        initial_cut += decode_cut(gubun, up, down)
                
                gubun = i['finalCutConvertedScore']['gubun']
                values = i['finalCutConvertedScore']['values']
                if gubun == "digitalM":
                    num_len = len(values) // 3
                    for j in range(num_len):
                        up = values[j].split(" ")[0]
                        mid = values[j + num_len].split(" ")[0]
                        down = values[j + num_len*2].split(" ")[0]
                        final_cut += decode_cut(gubun, up, down, mid)
                else:
                    num_len = len(values) // 2
                    for j in range(num_len):
                        up = values[j].split(" ")[0]
                        down = values[j + num_len].split(" ")[0]
                        final_cut += decode_cut(gubun, up, down)
                break
        initial_cut = float(Decimal(initial_cut).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        final_cut = float(Decimal(final_cut).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
                
        print(f"####### ({idx + 1}/{len(majorList)}) 크롤링 완료 #######")
        '''
        print("#######################################")
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
        '''
        ws1.range('D' + str(row1)).value = gun
        ws1.range('E' + str(row1)).value = university
        ws1.range('F' + str(row1)).value = department
        ws1.range('G' + str(row1)).value = date
        ws1.range('H' + str(row1)).value = my_rank
        ws1.range('I' + str(row1)).value = target_number
        ws1.range('J' + str(row1)).value = initial
        ws1.range('K' + str(row1)).value = initial_plus_addition
        ws1.range('M' + str(row1)).value = competetion_rate_2025
        ws1.range('N' + str(row1)).value = competetion_rate_2024
        ws1.range('O' + str(row1)).value = competetion_rate_2023
        ws1.range('P' + str(row1)).value = can_number
        ws1.range('Q' + str(row1)).value = can_my_rank
        ws1.range('R' + str(row1)).value = can_initial_rank
        ws1.range('S' + str(row1)).value = can_final_rank
        ws1.range('AB' + str(row1)).value = competetion_rate_down
        ws1.range('AE' + str(row1)).value = competetion_rate_up

        '''
        print(initial_cut)
        print(final_cut)
        print(student_score)
        '''
        ws2.range('C' + str(row2)).value = gun
        ws2.range('D' + str(row2)).value = university
        ws2.range('E' + str(row2)).value = department
        ws2.range('F' + str(row2)).value = date
        ws2.range('I' + str(row2)).value = initial_cut
        ws2.range('J' + str(row2)).value = final_cut
        ws2.range('K' + str(row2)).value = student_score
        #print("#######################################")

        row1 += 1
        row2 += 1

    wb.save(f"result/{student_name} 학생 IDA 정시지원 분석 리포트.xlsx")
    wb.close()
    url = "https://member.jinhak.com/MemberV3/MemberJoin/MemberLogOut.aspx?ReturnSite=JM&ReturnURL=https://member.jinhak.com/MemberV3/MemberJoin/MemberLogIn.aspx"
    driver.get(url)

app.quit()