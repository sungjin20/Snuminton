import requests

whole_make_list = [
    {
        "SPREADSHEET_NAME" : "10월 1주차 운동 신청 확인",
        "make_list" : [["9", "30", "화", "71", "2025"],
                       ["10", "2", "목", "71", "2025"],
                       ["10", "4", "토", "71-1", "2025"]]
    },
    {
        "SPREADSHEET_NAME" : "10월 2주차 운동 신청 확인",
        "make_list" : [["10", "7", "화", "71", "2025"],
                       ["10", "9", "목", "71", "2025"],
                       ["10", "11", "토", "71-1", "2025"]]
    },
    {
        "SPREADSHEET_NAME" : "10월 3주차 운동 신청 확인",
        "make_list" : [["10", "14", "화", "71", "2025"],
                       ["10", "16", "목", "71", "2025"],
                       ["10", "18", "토", "71-1", "2025"]]
    },
    {
        "SPREADSHEET_NAME" : "10월 4주차 운동 신청 확인",
        "make_list" : [["10", "21", "화", "71", "2025"],
                       ["10", "23", "목", "71", "2025"],
                       ["10", "25", "토", "71-1", "2025"]]
    },
    {
        "SPREADSHEET_NAME" : "10월 5주차 운동 신청 확인",
        "make_list" : [["10", "28", "화", "71", "2025"],
                       ["10", "30", "목", "71", "2025"],
                       ["11", "1", "토", "71-1", "2025"]]
    }
]

# createsheet
CREATESHEET_URL = "https://script.google.com/macros/s/AKfycbzRSqr1Ho9B9kRgl8hH_A8a4hQc46Ah06hnqBIb98jhRNGO0YdooUQWi4FneEgUbjsWPg/exec"
# createform
CREATEFORM_URL = "https://script.google.com/macros/s/AKfycbxuH6ZNYA-5TaHeZ_cn6XZRs0aC3nDM2-Inh0YqI86YM16FT-BfxZf5D6ksljVHuqz9_Q/exec"
# editsheet
EDITSHEET_URL = "https://script.google.com/macros/s/AKfycbzf2ZkfXydZ5fR9cTQcVyhvbcDKTf-SVclbeOJ2kOltZ93SyPoUcTjBRm25n01KDJc2/exec"

def create_spreadsheet(spreadsheet_name):
    # 요청 데이터
    data = {
        "name": spreadsheet_name
    }

    # POST 요청
    response = requests.post(CREATESHEET_URL, json=data)
    
    if response.status_code == 200:
        # 응답 데이터 처리
        result = response.json()
        print(f"Spreadsheet URL: {result['url']}")

        return result['id']
    else:
        print("Failed to create spreadsheet.")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        return None

def create_form(month, date, day, loc):
    data = {
        "month": month,
        "date": date,
        "day": day,
        "loc": loc,
        "id": sp_id
    }

    response = requests.post(CREATEFORM_URL, json=data)
    # 응답 처리
    if response.status_code == 200:
        response_data = response.json()
        if response_data.get("status") == "success":
            print(day + "요일 Form URL:", response_data["formUrl"])
        else:
            print("Error:", response_data.get("message"))
    else:
        print("HTTP Error:", response.status_code, response.text)

def rename_google_sheet(spreadsheet_id, old_sheet_name, new_sheet_name):
    # 요청에 보낼 데이터
    payload = {
        "id": spreadsheet_id,
        "oldname": old_sheet_name,
        "newname": new_sheet_name,
    }

    try:
        # POST 요청 보내기
        response = requests.post(EDITSHEET_URL, json=payload)

        # 요청 성공 여부 확인
        if response.status_code == 200:
            result = response.json()
            if result.get("success"):
                return result
            else:
                print("Error:", result.get("message"))
                return result
        else:
            print(f"HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

for element in whole_make_list:
    print(element["SPREADSHEET_NAME"])
    # 스프레드시트 생성
    sp_id = create_spreadsheet(element["SPREADSHEET_NAME"])

    make_list = element["make_list"]

    i = len(make_list) - 1
    while(i >= 0):
        create_form(make_list[i][0], make_list[i][1], make_list[i][2], make_list[i][3])
        i -= 1

    i = len(make_list) - 1
    while(i >= 0):
        rename_google_sheet(sp_id, "설문지 응답 시트" + str(len(make_list) - i), make_list[i][2] + "요일")
        i -= 1

    print("")

print("Create form and sheet successfully!")