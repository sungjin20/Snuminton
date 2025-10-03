from flask import Flask, request, redirect, render_template_string, url_for, jsonify
from google.cloud import storage
import requests
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import re
from collections import defaultdict
from pytz import timezone

UPDATE_DATE = "2025년 10월 03일"

# 카카오 REST API 키와 리다이렉션 URI
REST_API_KEY = "666e0e3f02f53266bf53e64b1ef1e464"
REST_API_KEY_schedule = "b816a19be73982fa8b6e71a30406eafe"
ACCESS_TOKEN = None
TEMPLATE_ID = "115672"
TEMPLATE_ID2 = "118349"

app = Flask(__name__)

client = storage.Client()
bucket = client.get_bucket('snuminton_bucket')

# 로컬에서 테스트시 사용
#with open('config_local.json', 'r', encoding='utf-8') as f:
#    config = json.load(f)

# 서버에서는 항상 이걸 써야함
with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

env = config.get("env")
REDIRECT_URI = config.get("REDIRECT_URI")
REDIRECT_URI_schedule = config.get("REDIRECT_URI_schedule")

sheet_ids = {
        '9_4th': "1-WqVjMTRU27HQQ-yB1gGlef9tdmNPZHvle0hLbAXQAo",  # 9월 4주차 시트 ID
        '10_1st': "1CX3Iyd-37lvVmQnkshK2Xfo9vPpTZ_l5eWLglFNoezk",  # 10월 1주차 시트 ID
        '10_2nd': "1pmAxrXatwLeFi5wHB5aKw0fK8QCoLUeQMVlnALSm2fo",  # 10월 2주차 시트 ID
        '10_3rd': "1mw92mZs9h59iWfbENdaGZ2WfS8x13f1LbM6jErir988",  # 10월 3주차 시트 ID
        '10_4th': "1bo4VzMDS7CTaSwn9rrjEDT_kesWvPC8XKQJK6HQNH7Y",  # 10월 4주차 시트 ID
        '10_5th': "1RaPli5_B60ZdWi9K4cBE93fO9yhAzs0ecFZnmM8KicM",  # 10월 5주차 시트 ID
    }

links = {
    '2025-09-23': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdjc8SszJWFZYuUQ65MWsn1uE0mrFOBCQZkCzRKgNfjmbuI-g/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2025-09-25': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfatrL3ybu0t071xw2NVXAmsZQpXUdHRjtHJNZkicjBsT6p5w/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2025-09-27': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScCElro_2aN_8FRhm5D-iTx8zVoOq2Y8Nrw4nxIhYd8AKRMlw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },

    '2025-09-30': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfE6CwgUL6xyYVdiYGfohAEcd90r1fC6Cu9Zsd8TnVmFVEPPA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2025-10-02': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScFDX2dS2HlwooaBAanSfSNGiGqWKHBESH4KgKPytQ_hEZGDA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2025-10-04': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdeRMc8qA6HLeCXxMGuVHKkgNTcFXgDFb8Xp9m1mQXexe561w/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },

    '2025-10-07': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSffkcip-shbztOH1zECUeXTiEVhdNeFtqU0HYZa91zP4qOQPw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2025-10-09': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSduEPB43mBANh6b-wybZvl5FWaIf1F5YnDBYdbBKux0xmH-aw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2025-10-11': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeDS6NzIfn8O5mZdNTuH-FJJfyzJ8uIgrATHJ0JowG3319TkQ/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },

    '2025-10-14': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSczdo4fkuR2fAMWbDOGcWkOwTHZgBtFPCiuXeSKHvg4QGl3Lg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2025-10-16': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeWjLc_yZnKv-2sidCp-MWQHQP4EXqgQgi1qeyuCMNRwO99Tw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2025-10-18': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeYVSTwQkvyhdlqbiSvAoilOCCfzSndys1XcrDokgndE64I7g/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },

    '2025-10-21': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdiTcyR3jWyLkOBYvJ4x2G9oClhpFvjKW5pOKFTXmb3DNGy7g/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
    '2025-10-23': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSek9TvDc4uOSRnMx6eBOb6f1a2ss5j_oC_0h-gbKvw_GgtpZA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
    '2025-10-25': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScmk38hMPes07WZ3cuFnjgvEHqDNbv7v9p9wV33eeT3gQRdJg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },

    '2025-10-28': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScu5H-PgAu-7LDWpzSj8HYh13QDGtQMPSrvu9-O78CjVqF2sw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[5]}/edit?usp=drivesdk'
    },
    '2025-10-30': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScCBFQpu3KPA_h4ZJkkg-SHozvnfxAZwcPhhfuPq58gBclKSg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[5]}/edit?usp=drivesdk'
    },
    '2025-11-01': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfDlWh-UbKf2SW0KP4bLotBHdDHlfqaryQzXh88nO3K2M7EBg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[5]}/edit?usp=drivesdk'
    },
    # 다른 날짜들도 필요 시 추가
}

# 1. 인증 URL 생성
def get_auth_url(key, url):
    return (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={key}&redirect_uri={url}&response_type=code&scope=profile_nickname,friends,talk_message"
    )

@app.route("/")
def index():
    auth_url_main = get_auth_url(REST_API_KEY, REDIRECT_URI)
    auth_url_schedule = get_auth_url(REST_API_KEY_schedule, REDIRECT_URI_schedule)
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 메뉴</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                }
                .logo-container {
                    margin-bottom: 20px;
                }
                .logo {
                    width: 80px;
                    height: 80px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .menu-container {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    width: 90%;
                    max-width: 400px;
                }
                .menu-btn {
                    width: 100%;
                    padding: 15px;
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    text-align: center;
                }
                .menu-btn:hover {
                    background-color: #fbc02d;
                }
                @media (max-width: 480px) {
                    .title {
                        font-size: 20px;
                    }
                    .menu-btn {
                        font-size: 16px;
                        padding: 12px;
                    }
                }
                footer {
                    position: absolute;
                    bottom: 10px;
                    font-size: 14px;
                    color: #888;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">스누민턴 운영부</div>
            <div class="menu-container">
                <a href="{{ url_for('attendance_selection') }}">
                    <button class="menu-btn">1. 출석 체크</button>
                </a>
                <a href="{{ url_for('etc_selection') }}">
                    <button class="menu-btn">2. 지각/불참/게스트비 체크</button>
                </a>
                <a href="{{ url_for('notice_selection') }}">
                    <button class="menu-btn">3. 운동신청공지 복사</button>
                </a>
                <a href="{{ url_for('notice_selection_guest') }}">
                    <button class="menu-btn">4. 게스트 운동신청공지 복사</button>
                </a>
                <a href="{{ auth_url_main }}">
                    <button class="menu-btn">5. 메시지 전송</button>
                </a>
                <a href="{{ auth_url_schedule }}">
                    <button class="menu-btn">6. 시간표 공지</button>
                </a>
            </div>
            <footer>© 2025 김성진. All rights reserved.<br>업데이트: """ + UPDATE_DATE + """</footer>
        </body>
        </html>
    """, auth_url_main=auth_url_main, auth_url_schedule=auth_url_schedule)

# 2. 리다이렉션 URI 엔드포인트
@app.route("/oauth")
def oauth():
    global ACCESS_TOKEN

    # 인증 코드가 없으면 오류 메시지 반환
    auth_code = request.args.get("code")
    if not auth_code:
        return "Failed to receive auth code"

    # 액세스 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "redirect_uri": REDIRECT_URI,
        "code": auth_code,
    }
    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        # 메뉴 페이지로 리다이렉트
        return redirect(url_for("menu"))
    else:
        return f"Failed to get access token: {response.json()}"

# 2. 리다이렉션 URI 엔드포인트
@app.route("/oauth_schedule")
def oauth_schedule():
    global ACCESS_TOKEN

    # 인증 코드가 없으면 오류 메시지 반환
    auth_code = request.args.get("code")
    if not auth_code:
        return "Failed to receive auth code"

    # 액세스 토큰 요청
    token_url = "https://kauth.kakao.com/oauth/token"
    token_data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY_schedule,
        "redirect_uri": REDIRECT_URI_schedule,
        "code": auth_code,
    }
    response = requests.post(token_url, data=token_data)

    if response.status_code == 200:
        ACCESS_TOKEN = response.json()["access_token"]
        # 메뉴 페이지로 리다이렉트
        return redirect(url_for("send_schedule"))
    else:
        return f"Failed to get access token: {response.json()}"

# 3. 메뉴 페이지
@app.route("/menu")
def menu():
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 메뉴</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                    font-family: Arial, sans-serif;
                    background-color: #f9f9f9;
                }
                .logo-container {
                    margin-bottom: 20px;
                }
                .logo {
                    width: 80px;
                    height: 80px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 20px;
                    text-align: center;
                }
                .menu-container {
                    display: flex;
                    flex-direction: column;
                    gap: 10px;
                    width: 90%;
                    max-width: 400px;
                }
                .menu-btn {
                    width: 100%;
                    padding: 15px;
                    font-size: 18px;
                    font-weight: bold;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    text-align: center;
                }
                .menu-btn:hover {
                    background-color: #fbc02d;
                }
                .home-btn {
                    background-color: #4caf50;
                    color: white;
                }
                .home-btn:hover {
                    background-color: #388e3c;
                }
                @media (max-width: 480px) {
                    .title {
                        font-size: 20px;
                    }
                    .menu-btn {
                        font-size: 16px;
                        padding: 12px;
                    }
                }
                footer {
                    position: absolute;
                    bottom: 10px;
                    font-size: 14px;
                    color: #888;
                    text-align: center;
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">메뉴</div>
            <div class="menu-container">
                <a href="{{ url_for('index') }}">
                    <button class="menu-btn home-btn">0. 홈으로</button>
                </a>
                <a href="{{ url_for('send_message') }}">
                    <button class="menu-btn">1. 메시지 전송</button>
                </a>
                <a href="{{ url_for('send_short_message') }}">
                    <button class="menu-btn">2. 짧은 공지 전송</button>
                </a>
            </div>
            <footer>© 2025 김성진. All rights reserved.<br>업데이트: """ + UPDATE_DATE + """</footer>
        </body>
        </html>
    """)

# 4. 메시지 전송 페이지
@app.route("/send_message", methods=["GET", "POST"])
def send_message():
    global ACCESS_TOKEN  # 전역 변수 ACCESS_TOKEN을 수정할 수 있도록 합니다.
    
    if request.method == "POST":
        message = request.form["message"]
        if ACCESS_TOKEN:
            # 메시지 전송
            url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "template_object": json.dumps({
                    "object_type": "text",
                    "text": message,
                    "link": {
                        "web_url": "http://your-web-url.com",
                        "mobile_web_url": "http://your-web-url.com",
                    },
                })
            }
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                return render_template_string(""" 
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>스누민턴 운영부 - 메시지 전송</title>
                        <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
                        <style>
                            body {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                margin: 0;
                                flex-direction: column;
                                font-family: Arial, sans-serif;
                            }
                            .success-msg {
                                font-size: 24px;
                                font-weight: bold;
                                margin-bottom: 20px;
                                color: green;
                            }
                            .button-container {
                                display: flex;
                                gap: 10px;
                            }
                            .btn {
                                padding: 10px 20px;
                                font-size: 16px;
                                background-color: #ffeb3b;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                transition: background-color 0.3s;
                            }
                            .btn:hover {
                                background-color: #fbc02d;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="success-msg">메시지가 성공적으로 전송되었습니다!</div>
                        <div class="button-container">
                            <a href="{{ url_for('send_message') }}">
                                <button class="btn">다시 보내기</button>
                            </a>
                            <a href="{{ url_for('index') }}">
                                <button class="btn">홈으로 돌아가기</button>
                            </a>
                        </div>
                    </body>
                    </html>
                """)
            else:
                return f"메시지 전송 실패: {response.json()}"
        else:
            return "로그인 상태가 아닙니다. 다시 로그인 해주세요."
        
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 메시지 전송</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                    font-family: Arial, sans-serif;
                }
                .logo-container {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .logo {
                    width: 100px;
                    height: 100px;
                    margin-bottom: 0px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                .input-container {
                    margin-bottom: 20px;
                }
                .send-btn {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    display: block;
                    margin: 0 auto;
                }
                .send-btn:hover {
                    background-color: #fbc02d;
                }
                textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 16px;
                    resize: none;
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">< 메시지 전송 ></div>
            <form method="POST">
                <div class="input-container">
                    <textarea id="message" name="message" rows="15" placeholder="내용을 입력하세요"></textarea>
                </div>
                <button type="submit" class="send-btn">나에게 보내기</button>
            </form>
        </body>
        </html>
    """)

# 5. 짧은 공지 전송 페이지
@app.route("/send_short_message", methods=["GET", "POST"])
def send_short_message():
    global ACCESS_TOKEN  # Use the global access token for authentication

    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        if ACCESS_TOKEN:
            url = "https://kapi.kakao.com/v2/api/talk/memo/send"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            data = {
                "template_id": TEMPLATE_ID,
                "template_args": json.dumps({
                    "TITLE" : title,
                    "DESC" : message
                })
            }
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                return render_template_string(""" 
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>스누민턴 운영부 - 짧은 공지 전송</title>
                        <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
                        <style>
                            body {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                margin: 0;
                                flex-direction: column;
                                font-family: Arial, sans-serif;
                            }
                            .success-msg {
                                font-size: 24px;
                                font-weight: bold;
                                margin-bottom: 20px;
                                color: green;
                            }
                            .button-container {
                                display: flex;
                                gap: 10px;
                            }
                            .btn {
                                padding: 10px 20px;
                                font-size: 16px;
                                background-color: #ffeb3b;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                transition: background-color 0.3s;
                            }
                            .btn:hover {
                                background-color: #fbc02d;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="success-msg">짧은 공지가 성공적으로 전송되었습니다!</div>
                        <div class="button-container">
                            <a href="{{ url_for('send_short_message') }}">
                                <button class="btn">다시 보내기</button>
                            </a>
                            <a href="{{ url_for('index') }}">
                                <button class="btn">홈으로 돌아가기</button>
                            </a>
                        </div>
                    </body>
                    </html>
                """)
            else:
                return f"짧은 공지 전송 실패: {response.json()}"
        else:
            return "로그인 상태가 아닙니다. 다시 로그인 해주세요."

    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 짧은 공지 전송</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                    font-family: Arial, sans-serif;
                }
                .logo-container {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .logo {
                    width: 100px;
                    height: 100px;
                    margin-bottom: 0px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                .input-container {
                    margin-bottom: 20px;
                }
                .send-btn {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    display: block;
                    margin: 0 auto;
                }
                .send-btn:hover {
                    background-color: #fbc02d;
                }
                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 16px;
                }
                textarea {
                    resize: none;
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">< 짧은 공지 전송 ></div>
            <form method="POST">
                <div class="input-container">
                    <input type="text" id="title" name="title" placeholder="제목을 입력하세요">
                </div>
                <div class="input-container">
                    <textarea id="message" name="message" rows="10" placeholder="내용을 입력하세요"></textarea>
                </div>
                <button type="submit" class="send-btn">나에게 보내기</button>
            </form>
        </body>
        </html>
    """)

# 6. 출석 체크 페이지
@app.route("/attendance_check/<week>", methods=["GET", "POST"])
def attendance_check(week):
    global ACCESS_TOKEN

    # 주차와 요일을 분리하여 추출
    week_info = week.split('_')
    week_number = f"{week_info[0]}_{week_info[1]}"  # 12_4th 또는 1_1st 등
    day_of_week = week_info[2]  # Tuesday, Thursday, Friday, Saturday 등

    sheet_id = sheet_ids.get(week_number)

    if not sheet_id:
        return jsonify({"status": "error", "message": "잘못된 주차입니다."})

    # day_of_week를 한국어로 변환하는 매핑
    day_of_week_mapping = {
        'Sunday': '일요일',
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Thursday': '목요일',
        'Saturday': '토요일'
    }

    # 예: 7_1st → "7월 1주차", Tuesday → "화"
    korean_week = f"{int(week_info[0])}월 " + {
        '1st': '1주차', '2nd': '2주차', '3rd': '3주차', '4th': '4주차', '5th': '5주차'
    }.get(week_info[1], '')

    korean_day = day_of_week_mapping.get(day_of_week, '')

    attendance_title = f"출석 체크 ({korean_week} {korean_day})"


    def get_google_sheet(sheet_id, day_of_week):
        # 영어 요일을 한국어 요일로 변환
        korean_day_of_week = day_of_week_mapping.get(day_of_week, None)
        
        if not korean_day_of_week:
            raise ValueError(f"지원되지 않는 요일: {day_of_week}")

        # 구글 스프레드시트 API 연결 설정
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('snuminton-445111-1666fdfa321c.json', scope)
        client = gspread.authorize(creds)
        
        # 한국어 요일에 해당하는 워크시트를 로드
        sheet = client.open_by_key(sheet_id).worksheet(korean_day_of_week)
        return sheet

    # 컬럼 이름에 해당하는 컬럼 번호 찾기
    def get_column_index(sheet, column_name):
        headers = sheet.row_values(1)  # 첫 번째 행을 읽어서 헤더 가져오기
        if column_name in headers:
            return headers.index(column_name) + 1  # 컬럼 번호는 1부터 시작
        else:
            return None  # 컬럼이 없으면 None 반환

    sheet_data = None
    if sheet_id:
        sheet = get_google_sheet(sheet_id, day_of_week)
        sheet_data = sheet.get_all_records()  # 스프레드시트 데이터를 읽어옵니다

        # 출석, 지각, 불참 컬럼 번호 동적으로 가져오기
        attendance_col = get_column_index(sheet, "출석")
        tardy_col = get_column_index(sheet, "지각")
        absent_col = get_column_index(sheet, "불참")

    # POST 요청 처리: 체크박스 상태 변경
    if request.method == "POST":
        data = request.json  # 이제 data는 리스트 형태
        updates = []  # 배치 업데이트에 사용할 데이터 리스트

        for entry in data:
            row_id = int(entry['row_id'])  # row_id를 숫자형으로 변환
            column = entry['column']  # '출석', '지각', '불참' 중 하나
            value = entry['value']  # 체크 상태 (True 또는 False)

            # 출석, 지각, 불참에 맞는 컬럼 번호 찾기
            column_index = None
            if column == '출석':
                column_index = attendance_col
            elif column == '지각':
                column_index = tardy_col
            elif column == '불참':
                column_index = absent_col
            elif column == '부분참 시간':
                time_col = get_column_index(sheet, "부분참 시간")
                if time_col:
                    updates.append({
                        'range': f"{chr(64 + time_col)}{row_id + 2}",
                        'values': [[value]]  # 빈 문자열도 가능
                    })
            elif column == '참가 유형':
                type_col = get_column_index(sheet, "참가 유형")
                if type_col:
                    updates.append({
                        'range': f"{chr(64 + type_col)}{row_id + 2}",
                        'values': [[value]]
                    })

            if column_index:
                # 셀 범위를 정확히 수정
                updates.append({
                    'range': f"{chr(64 + column_index)}{row_id + 2}",  # 셀 범위
                    'values': [[value]]  # 업데이트할 값
                })

                # 출석, 지각, 불참 중 다른 항목을 해제하도록 설정
                if column == '출석':
                    updates.append({
                        'range': f"{chr(64 + tardy_col)}{row_id + 2}",
                        'values': [[False]]
                    })
                    updates.append({
                        'range': f"{chr(64 + absent_col)}{row_id + 2}",
                        'values': [[False]]
                    })
                elif column == '지각':
                    updates.append({
                        'range': f"{chr(64 + attendance_col)}{row_id + 2}",
                        'values': [[False]]
                    })
                    updates.append({
                        'range': f"{chr(64 + absent_col)}{row_id + 2}",
                        'values': [[False]]
                    })
                elif column == '불참':
                    updates.append({
                        'range': f"{chr(64 + attendance_col)}{row_id + 2}",
                        'values': [[False]]
                    })
                    updates.append({
                        'range': f"{chr(64 + tardy_col)}{row_id + 2}",
                        'values': [[False]]
                    })

        if updates:
            # 배치 업데이트 수행
            sheet.batch_update(updates)

        return jsonify({"status": "success"})

    # Display spreadsheet data in a table format
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 출석 체크</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h2 {
                    margin-bottom: 20px;
                }
                .attendance-table-container {
                    width: 100%;
                    max-width: 1000px;
                    height: 500px;  /* 고정 높이 설정 */
                    overflow-y: auto;  /* 세로 스크롤 추가 */
                    margin-top: 20px;
                    display: block;
                }
                .attendance-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                }
                .attendance-table th, .attendance-table td {
                    padding: 10px;
                    text-align: center;
                    border: 1px solid #ddd;
                    word-wrap: break-word;
                }
                .attendance-table th {
                    position: sticky;
                    top: 0;
                    background-color: #f8f8f8;  /* 헤더 배경색 */
                    z-index: 1;  /* 헤더가 다른 내용 위로 표시되도록 설정 */
                }
                .update-btn {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .update-btn:hover {
                    background-color: #fbc02d;
                }
                #updateStatus {
                    margin-left: 10px;
                    font-size: 14px;
                    color: #555;
                }
                @media (max-width: 768px) {
                    .attendance-table th, .attendance-table td {
                        padding: 8px;
                    }
                }
                .filter-container {
                    display: flex;
                    flex-direction: column;
                    width: 100%;
                    max-width: 1000px;
                    margin-top: 10px;
                    gap: 10px;
                }

                .filter-row {
                    display: flex;
                    flex-wrap: wrap;
                    gap: 20px;
                    justify-content: flex-end;  /* 오른쪽 정렬 */
                }
                @media (max-width: 768px) {
                    .filter-row {
                        justify-content: flex-end;
                    }
                }
                .highlight-touch {
                    background-color: orange !important;
                }
            </style>
            <script>
                document.addEventListener("DOMContentLoaded", () => {
                    const rows = document.querySelectorAll(".attendance-table tbody tr");
                    
                    rows.forEach(row => {
                        const departmentCell = row.querySelector("td:nth-child(2)"); // "과" 열
                        if (departmentCell && departmentCell.textContent.trim() === "게스트") {
                            row.style.display = "none"; // "게스트"인 행 숨김
                        }
                        if (departmentCell && departmentCell.textContent.trim() === "오비") {
                            row.style.display = "none"; // "오비"인 행 숨김
                        }
                    });
                });

                let attendanceData = {};
                let lastUpdateTime = "";

                function handleCheckboxChange(row_id, column, checkbox) {
                    // 하나의 체크박스만 선택되도록 하려면 다른 항목을 해제해야 함
                    const columns = ['출석', '지각', '불참'];

                    // 하나만 체크되도록 다른 체크박스를 해제
                    columns.forEach(col => {
                        const checkboxes = document.getElementsByName(col + '_' + row_id);
                        checkboxes.forEach(cb => {
                            if (cb !== checkbox && cb.checked) {
                                cb.checked = false;  // 다른 체크박스를 해제
                            }
                        });
                    });

                    // 선택된 체크박스 상태 저장
                    attendanceData[row_id] = attendanceData[row_id] || {};
                    attendanceData[row_id][column] = checkbox.checked;
                }

                function updateAllAttendance() {
                    const button = document.getElementById("updateButton");
                    const statusText = document.getElementById("updateStatus");

                    // 버튼 비활성화 및 텍스트 변경
                    button.disabled = true;
                    button.textContent = "저장중...";
                    statusText.textContent = ""; // 상태 초기화

                    const data = Object.keys(attendanceData).map(row_id => {
                        return Object.keys(attendanceData[row_id]).map(column => {
                            return {
                                row_id: row_id,
                                column: column,
                                value: attendanceData[row_id][column]
                            };
                        });
                    }).flat();

                    fetch("/attendance_check/{{ week }}", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json",
                        },
                        body: JSON.stringify(data)
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status == "success") {
                            console.log("출석 정보가 모두 저장되었습니다.");

                            // attendanceData 초기화
                            attendanceData = {};

                            // 버튼 상태 및 텍스트 복원
                            button.textContent = "저장하기";
                            button.disabled = false;

                            // 최근 저장 시간 표시
                            const now = new Date();
                            lastUpdateTime = now.toLocaleTimeString();
                            statusText.textContent = `최근 저장 시각: ${lastUpdateTime}`;
                                  
                            alert("저장되었습니다.");
                        } else {
                            console.error("출석 정보 저장에 실패했습니다.");
                            button.textContent = "저장하기";
                            button.disabled = false;
                        }
                    })
                    .catch(error => {
                        console.error("출석 정보 저장 중 오류 발생:", error);
                        button.textContent = "저장하기";
                        button.disabled = false;
                    });
                }
                function handleParticipantTypeChange(row_id, selectElement) {
                    const value = selectElement.value;
                    attendanceData[row_id] = attendanceData[row_id] || {};
                    attendanceData[row_id]['참가 유형'] = value;

                    // 부분참 시간이 수정 가능한지 토글
                    const partialTimeSelect = document.getElementById("partial_time_" + row_id);
                    if (value === "부분참") {
                        partialTimeSelect.disabled = false;
                        partialTimeSelect.style.display = "inline-block";
                    } else {
                        partialTimeSelect.disabled = true;
                        partialTimeSelect.style.display = "none";
                        // 값도 초기화
                        partialTimeSelect.value = "";
                        attendanceData[row_id]['부분참 시간'] = "";
                    }

                    // ✅ 배경색 즉시 변경
                    const row = selectElement.closest("tr");
                    const role = row.getAttribute("data-role");

                    // 역할에 따른 색 우선 적용 (게스트/오비는 유지)
                    if (role === "게스트") {
                        row.style.backgroundColor = "#bcd6ac";
                    } else if (role === "오비") {
                        row.style.backgroundColor = "#cfd9f5";
                    } else {
                        row.style.backgroundColor = (value === "부분참") ? "#ffff54" : "#ffffff";
                    }
                }

                function handlePartialTimeChange(row_id, selectElement) {
                    const value = selectElement.value;
                    attendanceData[row_id] = attendanceData[row_id] || {};
                    attendanceData[row_id]['부분참 시간'] = value;
                }
                                  
                function handleNameRightClick(event, rowIndex, name) {
                    event.preventDefault();
                    if (confirm(`${name} 행을 삭제하시겠습니까?`)) {
                        disableUpdateButton(true);  // 저장 버튼 비활성화
                        fetch("/delete_row/{{ week }}", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({ row_id: rowIndex })  // ✅ row_id만 보내면 됨
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.status === "success") {
                                alert("삭제 완료되었습니다.");
                                location.reload();
                            } else {
                                alert("삭제 실패: " + data.message);
                                disableUpdateButton(false);
                            }
                        });
                    }
                }

                function disableUpdateButton(disable) {
                    const button = document.getElementById("updateButton");
                    if (button) {
                        button.disabled = disable;
                        button.textContent = disable ? "로딩 중..." : "저장하기";
                    }
                }
                function applyFilters() {
                    const hideGuestOb = document.getElementById("hideGuestObCheckbox").checked;
                    const filterUnmarked = document.getElementById("filterUnmarkedCheckbox").checked;
                    const filterQuota = document.getElementById("filterQuotaCheckbox").checked;
                    const quota = parseInt(document.getElementById("quotaInput").value);

                    const rows = Array.from(document.querySelectorAll(".attendance-table tbody tr"));
                    let quotaCounter = 0;

                    rows.forEach(row => {
                        const role = row.getAttribute("data-role");
                        const attendance = row.getAttribute("data-attendance");
                        const typeSelect = row.querySelector("select[name^='type_']");
                        const participantType = typeSelect ? typeSelect.value : "";

                        let hide = false;
                        let isQuotaTarget = false;

                        if (role === "게스트" || role === "부원" || role === "신입부원") {
                            quotaCounter++;
                            if (filterQuota && quota > 0 && quotaCounter <= quota) {
                                isQuotaTarget = true;
                            }
                        }

                        // === 배경색 복원 ===
                        if (role === "게스트") {
                            row.style.backgroundColor = "#bcd6ac";
                        } else if (role === "오비") {
                            row.style.backgroundColor = "#cfd9f5";
                        } else if (participantType === "부분참") {
                            row.style.backgroundColor = "#ffff54";
                        } else {
                            row.style.backgroundColor = "#ffffff";
                        }

                        // === 정원 초과 시 회색 처리 ===
                        if (filterQuota && quota > 0 && (role === "게스트" || role === "부원" || role === "신입부원") && !isQuotaTarget) {
                            row.style.backgroundColor = "#666666";

                            // 내부 select와 input 요소들도 회색 배경 및 텍스트 색 조정
                            row.querySelectorAll("select, input[type='checkbox']").forEach(elem => {
                                elem.style.backgroundColor = "#666666";
                                if (elem.tagName === "SELECT") {
                                    elem.style.borderColor = "#999999";
                                }
                            });
                        }
                        else {
                            row.querySelectorAll("select, input[type='checkbox']").forEach(elem => {
                                elem.style.backgroundColor = "";  // 기본값
                                elem.style.borderColor = "";
                            });
                        }

                        // === 행 숨김 처리 ===
                        if (hideGuestOb && (role === "게스트" || role === "오비")) {
                            hide = true;
                        }
                        if (filterUnmarked && attendance !== "none") {
                            hide = true;
                        }

                        row.style.display = hide ? "none" : "";
                    });
                }

                document.addEventListener("DOMContentLoaded", () => {
                    applyFilters();  // 초기 상태 반영
                });
                document.addEventListener("DOMContentLoaded", () => {
                    const rows = document.querySelectorAll(".attendance-table tbody tr");

                    rows.forEach((row, index) => {
                        const name = row.querySelector("td:nth-child(2)").textContent.trim();
                        const cells = row.querySelectorAll("td");

                        cells.forEach(cell => {
                            // 모바일: touchstart → highlight
                            cell.addEventListener("touchstart", () => {
                                row.classList.add("highlight-touch");
                            });

                            // 모바일: alert 뜨기 전에 제거
                            cell.addEventListener("contextmenu", (e) => {
                                e.preventDefault();
                                row.classList.remove("highlight-touch");  // ⭐ alert 전에 제거
                                handleNameRightClick(e, index, name);
                            });

                            // 백업: touchend or touchcancel → highlight 제거
                            cell.addEventListener("touchend", () => {
                                row.classList.remove("highlight-touch");
                            });
                            cell.addEventListener("touchcancel", () => {
                                row.classList.remove("highlight-touch");
                            });
                        });
                    });
                });
                document.addEventListener("DOMContentLoaded", () => {
                    const week = "{{ week }}";
                    const day = week.split("_")[2];  // 예: 'Tuesday'

                    const quotaInput = document.getElementById("quotaInput");
                    if (day === "Tuesday" || day === "Thursday") {
                        quotaInput.value = 24;
                    } else {
                        quotaInput.value = 36;
                    }

                    applyFilters();  // 초기 필터 적용
                });
                function toggleTimestampColumn() {
                    const show = document.getElementById("showTimestampCheckbox").checked;
                    const displayStyle = show ? "" : "none";

                    const timestampHeaders = document.querySelectorAll(".timestamp-col");
                    timestampHeaders.forEach(el => {
                        el.style.display = displayStyle;
                    });
                }
            </script>
        </head>
        <body>
            <h2>{{ attendance_title }}</h2>
            <div class="filter-container">
                <div class="filter-row">
                    <label>
                        <input type="checkbox" id="showTimestampCheckbox" onchange="toggleTimestampColumn()"> 타임스탬프 보기
                    </label>
                    <label>
                        <input type="checkbox" id="hideGuestObCheckbox" checked onchange="applyFilters()"> 게스트/오비 숨기기
                    </label>
                </div>
                <div class="filter-row">
                    <label>
                        정원:
                        <input type="number" id="quotaInput" value="0" style="width: 60px;" min="0" onchange="applyFilters()">
                    </label>
                    <label>
                        <input type="checkbox" id="filterQuotaCheckbox" onchange="applyFilters()"> 정원 필터링
                    </label>
                </div>
                <div class="filter-row">
                    <label>
                        <input type="checkbox" id="filterUnmarkedCheckbox" onchange="applyFilters()"> 출석 미체크 행 표시
                    </label>
                </div>
            </div>
            {% if sheet_data %}
            <div class="attendance-table-container">
                <table class="attendance-table">
                    <thead>
                        <tr>
                            <th class="timestamp-col" style="display:none;">타임스탬프</th>
                            <th>이름</th>
                            <th>참가 유형</th>
                            <th>부분참 시간</th>
                            <th>출석</th>
                            <th>지각</th>
                            <th>불참</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in sheet_data %}
                        <tr 
                            data-role="{{ row['참여자 구분'] }}"
                            data-attendance="{% if row['출석'] != 'TRUE' and row['지각'] != 'TRUE' and row['불참'] != 'TRUE' %}none{% else %}marked{% endif %}"
                            {% if row['참여자 구분'] == '게스트' %}
                                style="background-color: #bcd6ac;"
                            {% elif row['참여자 구분'] == '오비' %}
                                style="background-color: #cfd9f5;"
                            {% elif row['참가 유형'] == '부분참' %}
                                style="background-color: #ffff54;"
                            {% endif %}
                        >
                            <td class="timestamp-col" style="display:none;">
                                {{ row['타임스탬프'] or '' }}
                            </td>
                            <td style="cursor: context-menu;">
                                {{ row['이름'] }}
                            </td>
                            <td>
                                <select name="type_{{ loop.index0 }}" onchange="handleParticipantTypeChange({{ loop.index0 }}, this)">
                                    <option value="정참" {% if row['참가 유형'] == "정참" %}selected{% endif %}>정참</option>
                                    <option value="부분참" {% if row['참가 유형'] == "부분참" %}selected{% endif %}>부분참</option>
                                </select>
                            </td>
                            <td>
                                <select id="partial_time_{{ loop.index0 }}" name="부분참_{{ loop.index0 }}"
                                        onchange="handlePartialTimeChange({{ loop.index0 }}, this)"
                                        {% if row['참가 유형'] != "부분참" %}disabled style="display:none;"{% endif %}>
                                    <option value="19시-21시" {% if (row['부분참 시간'] or '') == "19시-21시" %}selected{% endif %}>19시-21시</option>
                                    <option value="20시-22시" {% if (row['부분참 시간'] or '') == "20시-22시" %}selected{% endif %}>20시-22시</option>
                                </select>
                            </td>
                            <td>
                                <input type="checkbox" name="출석_{{ loop.index0 }}" {% if row['출석'] == "TRUE" %}checked{% endif %} onchange="handleCheckboxChange({{ loop.index0 }}, '출석', this)">
                            </td>
                            <td>
                                <input type="checkbox" name="지각_{{ loop.index0 }}" {% if row['지각'] == "TRUE" %}checked{% endif %} onchange="handleCheckboxChange({{ loop.index0 }}, '지각', this)">
                            </td>
                            <td>
                                <input type="checkbox" name="불참_{{ loop.index0 }}" {% if row['불참'] == "TRUE" %}checked{% endif %} onchange="handleCheckboxChange({{ loop.index0 }}, '불참', this)">
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div style="margin-top: 20px;">
                <button id="updateButton" class="update-btn" onclick="updateAllAttendance()">저장하기</button>
                <span id="updateStatus"></span>
            </div>
            {% else %}
            <p>출석 데이터를 가져오는 데 실패했습니다. 다시 시도해주세요.</p>
            {% endif %}
        </body>
        </html>
    """, sheet_data=sheet_data, week=week, attendance_title=attendance_title)

# 6-1. 행 삭제 라우트
@app.route("/delete_row/<week>", methods=["POST"])
def delete_row(week):
    week_info = week.split('_')
    week_number = f"{week_info[0]}_{week_info[1]}"
    day_of_week = week_info[2]

    sheet_id = sheet_ids.get(week_number)
    if not sheet_id:
        return jsonify({"status": "error", "message": "잘못된 주차입니다."})

    day_of_week_mapping = {
        'Sunday': '일요일',
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Thursday': '목요일',
        'Saturday': '토요일'
    }

    korean_day = day_of_week_mapping.get(day_of_week)
    if not korean_day:
        return jsonify({"status": "error", "message": "잘못된 요일입니다."})

    try:
        creds = ServiceAccountCredentials.from_json_keyfile_name('snuminton-445111-1666fdfa321c.json', [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ])
        client = gspread.authorize(creds)
        sheet = client.open_by_key(sheet_id).worksheet(korean_day)

        data = request.get_json()
        row_id = int(data['row_id'])

        sheet.delete_rows(row_id + 2)  # 헤더가 1행이므로 row_id + 2
        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

def generate_html(sheet_ids: dict, links: dict, mode: str) -> str:
    day_map = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}
    day_eng = {'일': 'Sunday', '월': 'Monday', '화': 'Tuesday', '수': 'Wednesday',
               '목': 'Thursday', '금': 'Friday', '토': 'Saturday'}

    today_kst = datetime.now(timezone('Asia/Seoul'))
    today_str = today_kst.strftime('%Y-%m-%d')

    grouped = defaultdict(list)
    for date_str, info in links.items():
        for week_key, sheet_id in sheet_ids.items():
            if sheet_id in info['status_link']:
                grouped[week_key].append(date_str)
                break

    def korean_week_name(week_key):
        month, week = week_key.split('_')
        week_str = {
            '1st': '1주차',
            '2nd': '2주차',
            '3rd': '3주차',
            '4th': '4주차',
            '5th': '5주차',
        }.get(week, week)
        return f"{int(month)}월<br>{week_str}"

    html_output = '<tbody>\n'
    sorted_week_keys = sorted(grouped.keys(), key=lambda x: (int(x.split('_')[0]), x.split('_')[1]))

    for week_key in sorted_week_keys:
        html_output += f'    <tr>\n'
        html_output += f'        <td>{korean_week_name(week_key)}</td>\n'
        html_output += f'        <td>\n'
        html_output += f'            <div class="button-group">\n'

        for date_str in sorted(grouped[week_key]):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            weekday_kor = day_map[date_obj.weekday()]
            weekday_eng = day_eng[weekday_kor]
            display_date = f"{date_obj.month}/{date_obj.day}"

            week_param = f"{week_key}_{weekday_eng}"

            if mode == "attendance":
                url = url_for("attendance_check", week=week_param)
            elif mode == "etc":
                url = url_for("etc_check", week=week_param)
            else:
                raise ValueError("Invalid mode. Use 'attendance' or 'etc'.")

            # 오늘 날짜인지 확인해서 클래스 지정
            btn_class = "attendance-selection-btn"
            if date_str == today_str:
                btn_class += " today-btn"
            elif date_str < today_str:
                btn_class += " past-btn"

            html_output += f'                <div>\n'
            html_output += f'                    <a href="{url}">\n'
            html_output += f'                        <button class="{btn_class}">{weekday_kor}</button>\n'
            html_output += f'                    </a>\n'
            html_output += f'                    <div class="date-tag">{display_date}</div>\n'
            html_output += f'                </div>\n'

        html_output += f'            </div>\n'
        html_output += f'        </td>\n'
        html_output += f'    </tr>\n'

    html_output += '</tbody>'
    return html_output

# 7. 출석부 선택 페이지
@app.route("/attendance_selection")
def attendance_selection():
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 출석부 선택</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; font-family: Arial, sans-serif; }
                .attendance-selection-table { width: 100%; max-width: 400px; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
                .attendance-selection-table th, .attendance-selection-table td { padding: 10px; text-align: center; border: 1px solid #ddd; }
                .attendance-selection-btn { width: 100%; padding: 15px; font-size: 18px; background-color: #ffeb3b; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; }
                .attendance-selection-btn:hover { background-color: #fbc02d; }
                .button-group { display: flex; justify-content: space-between; gap: 10px; }
                .date-tag { font-size: 14px; color: #555; margin-top: 5px; }
                .today-btn {
                    background-color: #FB8C00 !important; /* 초록색 */
                    color: black;
                    font-weight: bold;
                }
                .attendance-selection-btn.past-btn {
                    background-color: #ccc !important;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <table class="attendance-selection-table">
                <thead>
                    <tr>
                        <th>주차</th>
                        <th>운동 신청 현황</th>
                    </tr>
                </thead>
                {{ generate_html(sheet_ids, links, mode)|safe }}
            </table>
        </body>
        </html>
    """, generate_html=generate_html, sheet_ids=sheet_ids, links=links, mode="attendance")

def upload_to_gcs(file):
    if file and file.filename:
        filename = file.filename
        blob = bucket.blob(f'uploads/{filename}')
        blob.upload_from_file(file, content_type=file.content_type)
        return f'{bucket.name}/uploads/{filename}'
    return None

# 8. 시간표 공지 전송 페이지
@app.route("/send_schedule", methods=["GET", "POST"])
def send_schedule():
    global ACCESS_TOKEN  # Use the global access token for authentication

    if request.method == "POST":
        title = request.form["title"]
        message = request.form["message"]
        uploaded_file_1 = request.files.get("image")
        uploaded_file_2 = request.files.get("image2")

        image_url_1 = None
        image_url_2 = None
        if uploaded_file_1:
            image_url_1 = upload_to_gcs(uploaded_file_1)
        if uploaded_file_2:
            image_url_2 = upload_to_gcs(uploaded_file_2)

        if ACCESS_TOKEN:
            url = "https://kapi.kakao.com/v2/api/talk/memo/send"
            headers = {
                "Authorization": f"Bearer {ACCESS_TOKEN}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
            match = re.search(r"open\.kakao\.com/([a-zA-Z0-9/_-]+)", message)
            data = {
                "template_id": TEMPLATE_ID2,
                "template_args": json.dumps({
                    "TITLE": title,
                    "DESC": match.group(1),
                    "SCHEDULE_1": image_url_1,
                    "SCHEDULE_2": image_url_2,
                })
            }
            response = requests.post(url, headers=headers, data=data)
            if response.status_code == 200:
                return render_template_string(""" 
                    <html>
                    <head>
                        <meta charset="UTF-8">
                        <meta name="viewport" content="width=device-width, initial-scale=1.0">
                        <title>스누민턴 운영부 - 시간표 공지 전송</title>
                        <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
                        <style>
                            body {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                margin: 0;
                                flex-direction: column;
                                font-family: Arial, sans-serif;
                            }
                            .success-msg {
                                font-size: 24px;
                                font-weight: bold;
                                margin-bottom: 20px;
                                color: green;
                            }
                            .button-container {
                                display: flex;
                                gap: 10px;
                            }
                            .btn {
                                padding: 10px 20px;
                                font-size: 16px;
                                background-color: #ffeb3b;
                                border: none;
                                border-radius: 5px;
                                cursor: pointer;
                                transition: background-color 0.3s;
                            }
                            .btn:hover {
                                background-color: #fbc02d;
                            }
                        </style>
                    </head>
                    <body>
                        <div class="success-msg">시간표 공지가 성공적으로 전송되었습니다!</div>
                        <div class="button-container">
                            <a href="{{ url_for('send_schedule') }}">
                                <button class="btn">다시 보내기</button>
                            </a>
                            <a href="{{ url_for('index') }}">
                                <button class="btn">홈으로 돌아가기</button>
                            </a>
                        </div>
                    </body>
                    </html>
                """)
            else:
                return f"시간표 공지 전송 실패: {response.json()}"
        else:
            return "로그인 상태가 아닙니다. 다시 로그인 해주세요."

    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 시간표 공지 전송</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                    font-family: Arial, sans-serif;
                }
                .logo-container {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .logo {
                    width: 100px;
                    height: 100px;
                    margin-bottom: 0px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
                .input-container {
                    margin-bottom: 20px;
                }
                .send-btn {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                    display: block;
                    margin: 0 auto;
                }
                .send-btn:hover {
                    background-color: #fbc02d;
                }
                input, textarea {
                    width: 100%;
                    padding: 10px;
                    margin: 5px 0;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    font-size: 16px;
                }
                textarea {
                    resize: none;
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">< 시간표 공지 전송 ></div>
            <form method="POST" enctype="multipart/form-data">
                <div class="input-container">
                    <input type="text" id="title" name="title" value="1월 1주차 운동신청톡방입니다." placeholder="제목을 입력하세요">
                </div>
                <div class="input-container">
                    <textarea id="message" name="message" rows="5" placeholder="오픈채팅방 주소를 입력하세요"></textarea>
                </div>
                <div class="input-container">
                    <input type="file" id="image" name="image" accept="image/*" style="display: none;">
                    <button type="button" onclick="document.getElementById('image').click()">이번주 시간표 선택</button>
                    <span id="file-name">이번주 시간표를 선택하세요</span>
                </div>
                <div class="input-container">
                    <input type="file" id="image2" name="image2" accept="image/*" style="display: none;">
                    <button type="button" onclick="document.getElementById('image2').click()">다음주 시간표 선택</button>
                    <span id="file-name2">다음주 시간표를 선택하세요</span>
                </div>
                <script>
                    document.getElementById('image').addEventListener('change', function() {
                        var fileName = this.files.length > 0 ? this.files[0].name : "";
                        document.getElementById('file-name').textContent = fileName;
                    });
                    document.getElementById('image2').addEventListener('change', function() {
                        var fileName = this.files.length > 0 ? this.files[0].name : "";
                        document.getElementById('file-name2').textContent = fileName;
                    });
                </script>
                <button type="submit" class="send-btn">나에게 보내기</button>
            </form>
        </body>
        </html>
    """)

# 9. 지각/불참/게스트비 수정화면 선택 페이지
@app.route("/etc_selection")
def etc_selection():
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 출석부 선택</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; font-family: Arial, sans-serif; }
                .attendance-selection-table { width: 100%; max-width: 400px; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
                .attendance-selection-table th, .attendance-selection-table td { padding: 10px; text-align: center; border: 1px solid #ddd; }
                .attendance-selection-btn { width: 100%; padding: 15px; font-size: 18px; background-color: #ffeb3b; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; }
                .attendance-selection-btn:hover { background-color: #fbc02d; }
                .button-group { display: flex; justify-content: space-between; gap: 10px; }
                .date-tag { font-size: 14px; color: #555; margin-top: 5px; }
                .today-btn {
                    background-color: #FB8C00 !important; /* 초록색 */
                    color: black;
                    font-weight: bold;
                }
                .attendance-selection-btn.past-btn {
                    background-color: #ccc !important;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <table class="attendance-selection-table">
                <thead>
                    <tr>
                        <th>주차</th>
                        <th>운동 신청 현황</th>
                    </tr>
                </thead>
                {{ generate_html(sheet_ids, links, mode)|safe }}
            </table>
        </body>
        </html>
    """, generate_html=generate_html, sheet_ids=sheet_ids, links=links, mode="etc")

@app.route("/get_existing_lateness_data", methods=["GET"])
def get_existing_lateness_data():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('snuminton-445111-1666fdfa321c.json', scope)
        client = gspread.authorize(creds)
        lateness_sheet = client.open_by_key("16VrMl9DrhpSnPoY03Lr0pVBCq6uqKLxvq0RsyAyDBZM").worksheet("지각콕")

        # 2행을 헤더로 설정하여 가져오기
        existing_data = lateness_sheet.get_all_records(expected_headers=["번호", "날짜", "이름"], head=2)

        return jsonify(existing_data)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# 10. 지각/불참/게스트비 체크 페이지
@app.route("/etc_check/<week>", methods=["GET", "POST"])
def etc_check(week):
    global ACCESS_TOKEN

    # 주차와 요일을 분리하여 추출
    week_info = week.split('_')
    week_number = f"{week_info[0]}_{week_info[1]}"  # 12_4th 또는 1_1st 등
    day_of_week = week_info[2]  # Tuesday, Thursday, Friday, Saturday 등

    sheet_id = sheet_ids.get(week_number)

    if not sheet_id:
        return jsonify({"status": "error", "message": "잘못된 주차입니다."})

    # day_of_week를 한국어로 변환하는 매핑
    day_of_week_mapping = {
        'Sunday': '일요일',
        'Monday': '월요일',
        'Tuesday': '화요일',
        'Thursday': '목요일',
        'Saturday': '토요일'
    }

    # 예: 7_1st → "7월 1주차", Tuesday → "화"
    korean_week = f"{int(week_info[0])}월 " + {
        '1st': '1주차', '2nd': '2주차', '3rd': '3주차', '4th': '4주차', '5th': '5주차'
    }.get(week_info[1], '')

    korean_day = day_of_week_mapping.get(day_of_week, '')

    attendance_title = f"비고 수정 ({korean_week} {korean_day})"

    def get_google_sheet(sheet_id, day_of_week):
        korean_day_of_week = day_of_week_mapping.get(day_of_week, None)
        if not korean_day_of_week:
            raise ValueError(f"지원되지 않는 요일: {day_of_week}")

        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('snuminton-445111-1666fdfa321c.json', scope)
        client = gspread.authorize(creds)

        sheet = client.open_by_key(sheet_id).worksheet(korean_day_of_week)
        return sheet
    
    # 컬럼 이름에 해당하는 컬럼 번호 찾기
    def get_column_index(sheet, column_name):
        headers = sheet.row_values(1)  # 첫 번째 행을 읽어서 헤더 가져오기
        if column_name in headers:
            return headers.index(column_name) + 1  # 컬럼 번호는 1부터 시작
        else:
            return None  # 컬럼이 없으면 None 반환
        
    sheet_data = None
    sheet = get_google_sheet(sheet_id, day_of_week)
    sheet_data = sheet.get_all_records()

    column_index = get_column_index(sheet, "비고")

    # POST 요청 처리: 비고 내용 업데이트
    if request.method == "POST":
        data = request.json
        updates = data.get("updates", [])
        lateness_data = data.get("lateness", [])

        # Google Sheets 인증 및 지각콕 명단 가져오기
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('snuminton-445111-1666fdfa321c.json', scope)
        client = gspread.authorize(creds)
        lateness_sheet = client.open_by_key("16VrMl9DrhpSnPoY03Lr0pVBCq6uqKLxvq0RsyAyDBZM").worksheet("지각콕")

        # 기존 지각콕 명단 데이터 가져오기
        existing_data = lateness_sheet.get_all_records(expected_headers=["번호", "날짜", "이름"], head=2)
        existing_set = {(row["날짜"], row["이름"]) for row in existing_data}

        # 새로운 데이터 중 기존에 없는 데이터만 필터링
        new_lateness_data = [(week, entry["name"]) for entry in lateness_data if (week, entry["name"]) not in existing_set]

        # 비고 업데이트 (출석 시트)
        if updates:
            sheet = get_google_sheet(sheet_id, day_of_week)
            column_index = get_column_index(sheet, "비고")
            batch_updates = [
                {'range': f"{chr(64 + column_index)}{entry['row_id'] + 2}", 'values': [[entry['remarks']]]}
                for entry in updates
            ]
            sheet.batch_update(batch_updates)

        # 중복되지 않는 새로운 데이터 추가
        if new_lateness_data:
            existing_data = lateness_sheet.get_all_values()
            last_row_number = len(existing_data) - 2  # 1부터 시작하는 번호 반영
            new_rows = [[last_row_number + i + 1, new_lateness_data[i][0], new_lateness_data[i][1]] for i, entry in enumerate(new_lateness_data)]
            lateness_sheet.append_rows(new_rows, value_input_option="USER_ENTERED")

        return jsonify({"status": "success"})

    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 비고 수정</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    flex-direction: column;
                    font-family: Arial, sans-serif;
                    padding: 20px;
                }
                h2 {
                    margin-bottom: 20px;
                }
                .attendance-table-container {
                    width: 100%;
                    max-width: 1000px;
                    height: 500px;  /* 고정 높이 설정 */
                    overflow-y: auto;  /* 세로 스크롤 추가 */
                    margin-top: 20px;
                    display: block;
                }
                .attendance-table {
                    width: 100%;
                    border-collapse: collapse;
                    font-size: 14px;
                }
                .attendance-table th, .attendance-table td {
                    padding: 10px;
                    text-align: center;
                    border: 1px solid #ddd;
                    word-wrap: break-word;
                }
                .attendance-table th {
                    position: sticky;
                    top: 0;
                    background-color: #f8f8f8;  /* 헤더 배경색 */
                    z-index: 1;  /* 헤더가 다른 내용 위로 표시되도록 설정 */
                }
                .update-btn {
                    padding: 10px 20px;
                    font-size: 16px;
                    background-color: #ffeb3b;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .update-btn:hover {
                    background-color: #fbc02d;
                }
                #updateStatus {
                    margin-left: 10px;
                    font-size: 14px;
                    color: #555;
                }
                @media (max-width: 768px) {
                    .attendance-table th, .attendance-table td {
                        padding: 8px;
                    }
                }
            </style>
            <script>
                let remarksData = {};

                function handleRemarksChange(row_id, input) {
                    remarksData[row_id] = input.value;
                }

                function updateRemarks() {
                    const button = document.getElementById("updateButton");
                    button.disabled = true;
                    button.innerText = "업데이트 중...";

                    const weekDate = "{{ week }}";  // 직접 사용

                    fetch("/get_existing_lateness_data")
                        .then(response => response.json())
                        .then(existingData => {
                            const existingSet = new Set(existingData.map(entry => `${entry.date}_${entry.name}`));

                            const updates = [];
                            const latenessData = [];

                            document.querySelectorAll(".attendance-table tbody tr").forEach((row, index) => {
                                const name = row.cells[0].innerText.trim();
                                const remarks = row.cells[4].querySelector("select").value.trim();

                                updates.push({ row_id: index, remarks: remarks });

                                if (remarks === "지각콕 확인") {
                                    const entryKey = `${weekDate}_${name}`;
                                    if (!existingSet.has(entryKey)) {
                                        latenessData.push({ date: weekDate, name: name });
                                    }
                                }
                            });

                            return fetch("/etc_check/" + weekDate, {
                                method: "POST",
                                headers: { "Content-Type": "application/json" },
                                body: JSON.stringify({ updates: updates, lateness: latenessData })
                            });
                        })
                        .then(response => response.json())
                        .then(data => {
                            button.disabled = false;
                            button.innerText = "비고 업데이트";

                            if (data.status === "success") {
                                alert("비고가 성공적으로 업데이트되었습니다.");
                            } else {
                                alert("비고 업데이트에 실패했습니다.");
                            }
                        })
                        .catch(error => {
                            console.error("비고 업데이트 중 오류:", error);
                            alert("오류가 발생했습니다.");
                            button.disabled = false;
                            button.innerText = "비고 업데이트";
                        });
                }

                function filterRows() {
                    const rows = document.querySelectorAll('.attendance-table tbody tr');
                    rows.forEach(row => {
                        const course = row.querySelector('.course').innerText;
                        const late = row.querySelector('.late').innerText;
                        const absence = row.querySelector('.absence').innerText;
                        if (course !== '게스트' && late !== 'O' && absence !== 'O') {
                            row.style.display = 'none';
                        } else {
                            row.style.display = '';
                        }
                    });
                }

                window.onload = filterRows;  // 페이지가 로드될 때 필터링 실행
            </script>
        </head>
        <body>
            <h2>{{ attendance_title }}</h2>
            {% if sheet_data %}
            <div class="attendance-table-container">
                <table class="attendance-table">
                    <thead>
                        <tr>
                            <th>이름</th>
                            <th>참여자 구분</th>
                            <th>지각</th>
                            <th>불참</th>
                            <th>비고</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% for row in sheet_data %}
                        <tr>
                            <td>{{ row['이름'] }}</td>
                            <td class="course">{{ row['참여자 구분'] }}</td>
                            <td class="late">
                                {% if row['지각'] == "TRUE" %}
                                    O
                                {% else %}
                                    &nbsp;
                                {% endif %}
                            </td>
                            <td class="absence">
                                {% if row['불참'] == "TRUE" %}
                                    O
                                {% else %}
                                    &nbsp;
                                {% endif %}
                            </td>
                            <td>
                                <select onchange="handleRemarksChange({{ loop.index0 }}, this)">
                                    <option value="" {% if row['비고'] == "" %} selected {% endif %}></option>
                                    <option value="게스트비 확인" {% if row['비고'] == "게스트비 확인" %} selected {% endif %}>게스트비 확인</option>
                                    <option value="불참비 확인" {% if row['비고'] == "불참비 확인" %} selected {% endif %}>불참비 확인</option>
                                    <option value="지각콕 확인" {% if row['비고'] == "지각콕 확인" %} selected {% endif %}>지각콕 확인</option>
                                </select>
                            </td>
                        </tr>
                        {% endfor %}
                    </tbody>
                </table>
            </div>
            <div>
                <button id="updateButton" class="update-btn" onclick="updateRemarks()">비고 업데이트</button>
                <span id="updateStatus"></span>
            </div>
            {% else %}
            <p>조건에 맞는 데이터가 없습니다.</p>
            {% endif %}
        </body>
        </html>
    """, sheet_data=sheet_data, week=week, attendance_title=attendance_title)

def generate_notice_html(sheet_ids: dict, links: dict, mode: str) -> str:
    day_map = {0: '월', 1: '화', 2: '수', 3: '목', 4: '금', 5: '토', 6: '일'}

    grouped = defaultdict(list)
    for date_str, info in links.items():
        for week_key, sheet_id in sheet_ids.items():
            if sheet_id in info['status_link']:
                grouped[week_key].append(date_str)
                break

    def korean_week_name(week_key):
        month, week = week_key.split('_')
        week_str_map = {
            '1st': '1주차',
            '2nd': '2주차',
            '3rd': '3주차',
            '4th': '4주차',
            '5th': '5주차',
        }
        week_str = week_str_map.get(week, week)
        return f"{int(month)}월<br>{week_str}"

    base_path = "/notice" if mode == "user" else "/notice_guest"

    today = datetime.now(timezone('Asia/Seoul')).date()
    target_delta = 2 if mode == "user" else 1
    target_date = today + timedelta(days=target_delta)  # ✅ 기준 날짜 계산

    html_output = '<tbody>\n'
    sorted_week_keys = sorted(grouped.keys(), key=lambda x: (int(x.split('_')[0]), x.split('_')[1]))

    for week_key in sorted_week_keys:
        html_output += f'    <tr>\n'
        html_output += f'        <td>{korean_week_name(week_key)}</td>\n'
        html_output += f'        <td>\n'
        html_output += f'            <div class="button-group">\n'

        for date_str in sorted(grouped[week_key]):
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            weekday_kor = day_map[date_obj.weekday()]
            weekday_full = {0:'월요일',1:'화요일',2:'수요일',3:'목요일',4:'금요일',5:'토요일',6:'일요일'}[date_obj.weekday()]
            display_date = f"{date_obj.month}/{date_obj.day}"

            url = f"{base_path}?date={date_str}&day={weekday_full}"

            # ✅ 버튼 색상 클래스 지정
            btn_class = "attendance-selection-btn"
            if date_obj == target_date:
                btn_class += " highlight-orange-btn"
            elif date_obj < today:
                btn_class += " past-btn"

            html_output += f'                <div>\n'
            html_output += f'                    <a href="{url}">\n'
            html_output += f'                        <button class="{btn_class}">{weekday_kor}</button>\n'
            html_output += f'                    </a>\n'
            html_output += f'                    <div class="date-tag">{display_date}</div>\n'
            html_output += f'                </div>\n'

        html_output += f'            </div>\n'
        html_output += f'        </td>\n'
        html_output += f'    </tr>\n'

    html_output += '</tbody>'

    return html_output

# 11. 운동 신청 공지 선택 페이지
@app.route("/notice_selection")
def notice_selection():
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 운동 신청 공지 선택</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; font-family: Arial, sans-serif; }
                .attendance-selection-table { width: 100%; max-width: 400px; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
                .attendance-selection-table th, .attendance-selection-table td { padding: 10px; text-align: center; border: 1px solid #ddd; }
                .attendance-selection-btn { width: 100%; padding: 15px; font-size: 18px; background-color: #ffeb3b; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; }
                .attendance-selection-btn:hover { background-color: #fbc02d; }
                .button-group { display: flex; justify-content: space-between; gap: 10px; }
                .date-tag { font-size: 14px; color: #555; margin-top: 5px; }
                .highlight-orange-btn {
                    background-color: #FB8C00 !important; /* 진한 주황 */
                    color: black;
                    font-weight: bold;
                }
                .attendance-selection-btn.past-btn {
                    background-color: #ccc !important;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <table class="attendance-selection-table">
                <thead>
                    <tr>
                        <th>주차</th>
                        <th>운동 신청 공지</th>
                    </tr>
                </thead>
                {{ generate_notice_html(sheet_ids, links, mode)|safe }}
            </table>
        </body>
        </html>
    """, generate_notice_html=generate_notice_html, sheet_ids=sheet_ids, links=links, mode="user")

# 12. 운동 신청 공지 복사 페이지
@app.route("/notice", methods=["GET", "POST"])
def notice():
    # 임원진 리스트
    executives = ["김영준", "이주원", "김상원", "조재형", "김민성", "윤주영", "이지호", "강예원"]

    date = request.args.get("date", datetime.today().strftime('%Y-%m-%d'))
    day = request.args.get("day", datetime.strptime(date, '%Y-%m-%d').strftime('%A'))
    
    if day in ["화요일", "목요일"]:
        member_count = "24"
    else:
        member_count = "40"

    day_kor = day[0]

    link_data = links.get(date, {'form_link': '#', 'status_link': '#'})
    form_link = link_data['form_link']
    status_link = link_data['status_link']

    date_obj = datetime.strptime(date, '%Y-%m-%d')
    month = date_obj.month
    day2 = date_obj.day

    title_text = f"<{month}/{day2}({day_kor}) 운동 신청 공지>"

    selected_executives = request.form.getlist("executives") if request.method == "POST" else []
    executive_text = " ".join(selected_executives) if selected_executives else ""

    # 공지 내용
    notice_text = f"""
{form_link}
⬆{month}월 {day2}일 {day} 운동 신청링크

# 23시 이전에 제출한 응답은 자동삭제.
# 00시 이후 신청 내용 변경 불가.
# 운동 정원 : {member_count}명
# 출석 체크 시간 : 19시 10분 (지각콕 : 1개)
# 불참비 : 4000원 (3333292003038 카카오뱅크 윤주영)

2일 전 23시부터 선착순 신청 받습니다~! 

[참여 임원진]
{executive_text}

🫠 현황 확인 링크
{status_link}"""

    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 운동 신청 공지</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body { display: flex; justify-content: center; align-items: center; flex-direction: column; height: 100vh; margin: 0; font-family: Arial, sans-serif; padding: 20px; }
                .container {
                    width: 100%;
                    max-width: 600px;
                    margin: auto;
                }
                fieldset {
                    border: 2px solid #ccc;
                    padding: 20px;
                    border-radius: 10px;
                    width: 100%;
                    box-sizing: border-box;
                }
                textarea {
                    width: 100%;
                    height: 300px;
                    padding: 15px;
                    font-size: 16px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                    box-sizing: border-box;
                }
                button { margin-top: 20px; padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background-color: #45a049; }
                .logo-container { display: flex; flex-direction: column; align-items: center; }
                .logo { width: 100px; height: 100px; margin-bottom: 10px; }
                .title { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 10px; }
                .checkbox-group {
                    display: grid;
                    grid-template-columns: repeat(4, 1fr);
                    gap: 10px;
                }

                .checkbox-group label {
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                    white-space: nowrap;
                    font-size: 16px;
                }

                .checkbox-group input[type="checkbox"] {
                    transform: scale(1.2);
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">{{ title_text }}</div>

            <div class="container">
                <form method="post" onsubmit="showAlert()">
                    <fieldset>
                        <legend style="font-weight: bold; font-size: 16px;">참여 임원진 선택:</legend>
                        <div class="checkbox-group" style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
                            {% for exec in executives %}
                                <label>
                                    <input type="checkbox" name="executives" value="{{ exec }}" {% if exec in selected_executives %}checked{% endif %}>
                                    {{ exec }}
                                </label>
                            {% endfor %}
                        </div>
                    </fieldset>
                    <div style="text-align: center; margin-top: 15px;">
                        <button type="submit">임원진 추가</button>
                    </div>
                </form>

                <textarea id="noticeText">{{ notice_text }}</textarea>
            </div>
                                  
            <button onclick="copyToClipboard()">공지 복사하기</button>

            <script>
                function showAlert() {
                    alert("참여 임원진이 반영되었습니다!");
                }

                function copyToClipboard() {
                    var copyText = document.getElementById("noticeText");
                    copyText.select();
                    document.execCommand("copy");
                    alert("공지 내용이 복사되었습니다!");
                }
            </script>
        </body>
        </html>
    """, notice_text=notice_text, executives=executives, selected_executives=selected_executives, title_text=title_text)

# 13. 게스트 운동 신청 공지 선택 페이지
@app.route("/notice_selection_guest")
def notice_selection_guest():
    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 게스트 운동 신청 공지 선택</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; flex-direction: column; font-family: Arial, sans-serif; }
                .attendance-selection-table { width: 100%; max-width: 400px; border-collapse: collapse; margin-top: 20px; font-size: 14px; }
                .attendance-selection-table th, .attendance-selection-table td { padding: 10px; text-align: center; border: 1px solid #ddd; }
                .attendance-selection-btn { width: 100%; padding: 15px; font-size: 18px; background-color: #ffeb3b; border: none; border-radius: 5px; cursor: pointer; transition: background-color 0.3s; }
                .attendance-selection-btn:hover { background-color: #fbc02d; }
                .button-group { display: flex; justify-content: space-between; gap: 10px; }
                .date-tag { font-size: 14px; color: #555; margin-top: 5px; }
                                  .highlight-orange-btn {
                    background-color: #FB8C00 !important; /* 진한 주황 */
                    color: black;
                    font-weight: bold;
                }
                .attendance-selection-btn.past-btn {
                    background-color: #ccc !important;
                    color: #666;
                }
            </style>
        </head>
        <body>
            <table class="attendance-selection-table">
                <thead>
                    <tr>
                        <th>주차</th>
                        <th>게스트 운동 신청 공지</th>
                    </tr>
                </thead>
                {{ generate_notice_html(sheet_ids, links, mode)|safe }}
            </table>
        </body>
        </html>
    """, generate_notice_html=generate_notice_html, sheet_ids=sheet_ids, links=links, mode="guest")

# 14. 게스트 운동 신청 공지 복사 페이지
@app.route("/notice_guest")
def notice_guest():
    date = request.args.get('date')
    day = request.args.get('day')
    if (day == "화요일") or (day == "목요일"):
        member_count = "24"
        place = "71동 종합체육관"
    else:
        member_count = "40"
        place = "71-1동 301호"

    link_data = links.get(date, {'form_link': '#', 'status_link': '#'})

    form_link = link_data['form_link']
    status_link = link_data['status_link']

    date_obj = datetime.strptime(date, '%Y-%m-%d')
    month = date_obj.month
    day2 = date_obj.day

    day_kor = day[0]
    title_text = f"<{month}/{day2}({day_kor}) 게스트 운동 신청 공지>"

    # 공지 내용
    notice_text = f"""
{form_link}
⏫ {month}월 {day2}일 {day} 운동 신청링크

운동장소
19시-22시 : {place}

* 주요 내용 *
1. 정원({member_count}명) 꽉 차기 전까지 신청 가능
2. 운동 1일전 15시 이후의 신청만 인정
ex) 목요일 운동신청이면 수요일 3시부터 신청 인정
3. 게스트비 : 4000원
3333292003038 카카오뱅크 윤주영 

반드시 아래 입금자명을 지켜주세요. 
입금자명 : “이름+날짜”
예시) “홍길동1/3”

셔틀콕 구입비 (게스트) : 24000원
4. 게스트비 입금 시 환불 불가

# 스누민턴 부원이 우선 신청하기 때문에, 정원이 부원으로 모두 채워지면 게스트 신청이 불가합니다!
# 정원 미달 시, 운동 1일전 15시 이후에 신청해주시고 게스트비 입금하시면 됩니다~

🫠 운동 신청 현황 확인 링크
{status_link}"""

    return render_template_string("""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>스누민턴 운영부 - 게스트 운동 신청 공지</title>
            <link rel="icon" href="{{ url_for('static', filename='스누민턴 로고.png') }}" type="image/png">
            <style>
                body { display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: Arial, sans-serif; flex-direction: column; padding: 20px; }
                textarea { width: 100%; max-width: 600px; height: 300px; padding: 15px; font-size: 16px; border: 1px solid #ccc; border-radius: 5px; }
                button { margin-top: 20px; padding: 10px 20px; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
                button:hover { background-color: #45a049; }
                .logo-container {
                    position: relative;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }
                .logo {
                    width: 100px;
                    height: 100px;
                    margin-bottom: 0px;
                }
                .title {
                    font-size: 24px;
                    font-weight: bold;
                    color: #333;
                    margin-bottom: 10px;
                }
            </style>
        </head>
        <body>
            <div class="logo-container">
                <img class="logo" src="{{ url_for('static', filename='스누민턴 로고.png') }}" alt="스누민턴 로고">
            </div>
            <div class="title">{{ title_text }}</div>
            <textarea id="noticeText">{{ notice_text }}</textarea>
            <button onclick="copyToClipboard()">공지 복사하기</button>

            <script>
                function copyToClipboard() {
                    var copyText = document.getElementById("noticeText");
                    copyText.select();
                    document.execCommand("copy");
                    alert("공지 내용이 복사되었습니다!");
                }
            </script>
        </body>
        </html>
    """, notice_text=notice_text, title_text=title_text)

if __name__ == "__main__":
    if env == "local":
        app.run(port=5000)

    elif env == "server":
        import os

        # Cloud Run은 기본적으로 PORT 환경 변수를 사용
        port = int(os.environ.get("PORT", 8080))
        app.run(host="0.0.0.0", port=port)