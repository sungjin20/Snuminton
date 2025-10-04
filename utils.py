from flask import url_for
from google.cloud import secretmanager
from datetime import datetime, timedelta
from collections import defaultdict
from pytz import timezone
import json

def get_secret(secret_id, credentials=None, version_id="latest"):
    client = secretmanager.SecretManagerServiceClient(credentials=credentials)
    name = f"projects/sodium-diode-445205-v1/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    payload = response.payload.data.decode("UTF-8")
    return json.loads(payload)

def get_auth_url(key, url):
    return (
        f"https://kauth.kakao.com/oauth/authorize"
        f"?client_id={key}&redirect_uri={url}&response_type=code&scope=profile_nickname,friends,talk_message"
    )

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

def upload_to_gcs(file, bucket):
    if file and file.filename:
        filename = file.filename
        blob = bucket.blob(f'uploads/{filename}')
        blob.upload_from_file(file, content_type=file.content_type)
        return f'{bucket.name}/uploads/{filename}'
    return None

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