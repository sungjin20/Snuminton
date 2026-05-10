import html
import os
import re
import threading
import time
import webbrowser

import requests
import urllib3
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

os.environ["HTTP_PROXY"] = "http://70.10.15.10:8080"
os.environ["HTTPS_PROXY"] = "http://70.10.15.10:8080"
os.environ["PYTHONHTTPSVERIFY"] = "0"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__, template_folder="templates")
CORS(app, resources={r"/api/*": {"origins": "*"}})

TARGET_URL = "https://app2.wekkuk.com/v2/contest_badminton/apply_check_get"
CONTEST_LIST_URL = "https://app2.wekkuk.com/v2/contest_badminton/contest"
CONTEST_PATTERN = re.compile(r'goto_contest_view\((\d+),\s*"([^"]+)"\)')
CONTEST_CARD_PATTERN = re.compile(
    r'<div class="gm-top".*?onClick=\'goto_contest_view\((\d+),\s*"([^"]+)"\)\'>(.*?)</div>\s*</div>',
    re.DOTALL,
)
GM_NAME_PATTERN = re.compile(r'<p class="gm-name">\((.*?)\)</p>', re.DOTALL)
GM_STATE_PATTERN = re.compile(r'<span class="gm-color2">\[(.*?)\]</span>', re.DOTALL)
GM_TIME_PATTERN = re.compile(r'<p class="gm-time">(.*?)</p>', re.DOTALL)
PAGING_LAST_PATTERN = re.compile(r"toPage\('(\d+)',")
CONTEST_DETAIL_BLOCK_PATTERN = re.compile(
    r'<div class="gm-stem">\s*<p class="gm-item">(.*?)</p>\s*<div class="gm-text">\s*<p>(.*?)</p>',
    re.DOTALL,
)
TAG_PATTERN = re.compile(r"<[^>]+>")


def create_session():
    session = requests.Session()
    session.verify = False
    return session


def normalize_contest_name(value):
    return re.sub(r"\s+", " ", (value or "").strip()).casefold()


def clean_html_text(value):
    text = re.sub(r"<br\s*/?>", "\n", value or "", flags=re.IGNORECASE)
    text = TAG_PATTERN.sub("", text)
    text = html.unescape(text)
    return re.sub(r"[ \t\r\f\v]+", " ", text).strip()


def normalize_detail_label(value):
    cleaned = clean_html_text(value)
    return cleaned.split()[0] if cleaned else ""


def fetch_contests(query):
    session = create_session()
    response = session.get(
        CONTEST_LIST_URL,
        params={"sw": query} if query else None,
        timeout=15,
    )
    response.raise_for_status()

    contests = []
    seen_ids = set()

    for contest_id, contest_name in CONTEST_PATTERN.findall(response.text):
        if contest_id in seen_ids:
            continue
        seen_ids.add(contest_id)
        contests.append(
            {
                "id": contest_id,
                "name": html.unescape(contest_name).strip(),
            }
        )

    return contests


def extract_first(pattern, text):
    match = pattern.search(text or "")
    return clean_html_text(match.group(1)) if match else ""


def fetch_contest_page(page=1):
    session = create_session()
    response = session.get(CONTEST_LIST_URL, params={"page": page}, timeout=15)
    response.raise_for_status()

    items = []
    for contest_id, contest_name, block_html in CONTEST_CARD_PATTERN.findall(response.text):
        items.append(
            {
                "id": contest_id,
                "name": html.unescape(contest_name).strip(),
                "organizer_name": extract_first(GM_NAME_PATTERN, block_html),
                "status": extract_first(GM_STATE_PATTERN, block_html),
                "period": extract_first(GM_TIME_PATTERN, block_html),
            }
        )

    page_matches = [int(value) for value in PAGING_LAST_PATTERN.findall(response.text)]
    total_pages = max(page_matches) if page_matches else int(page or 1)

    return {
        "page": int(page),
        "total_pages": total_pages,
        "items": items,
    }


def fetch_contest_detail(contest_id):
    session = create_session()
    response = session.get(f"{CONTEST_LIST_URL}/{contest_id}", timeout=15)
    response.raise_for_status()

    detail_map = {}
    for raw_label, raw_value in CONTEST_DETAIL_BLOCK_PATTERN.findall(response.text):
        label = normalize_detail_label(raw_label)
        value = clean_html_text(raw_value)
        if label and value:
            detail_map[label] = value

    if not detail_map:
        raise ValueError("Contest detail not found")

    title = detail_map.get("대회명", "")
    period_raw = detail_map.get("대회기간", "")
    status_match = re.search(r"\[(.*?)\]", period_raw)

    return {
        "id": str(contest_id),
        "name": title,
        "status": status_match.group(1).strip() if status_match else "",
        "period": re.sub(r"^\[[^\]]+\]\s*", "", period_raw).strip(),
        "location": detail_map.get("대회장소", ""),
        "host": detail_map.get("주최", ""),
        "organizer": detail_map.get("주관", ""),
        "support": detail_map.get("후원", ""),
        "sponsor": detail_map.get("협찬", ""),
        "notice": detail_map.get("안내", ""),
        "fields": detail_map,
    }


@app.route("/api/contests", methods=["GET"])
def contest_lookup():
    query = request.args.get("query", "").strip()
    if len(query) < 2:
        return jsonify(
            {
                "err": "Y",
                "err_msg": "대회명은 2자 이상 입력해 주세요.",
                "items": [],
            }
        ), 400

    try:
        contests = fetch_contests(query)
    except requests.exceptions.Timeout:
        return jsonify({"err": "Y", "err_msg": "대회 목록 조회 시간 초과", "items": []}), 504
    except requests.RequestException:
        return jsonify({"err": "Y", "err_msg": "대회 목록 조회 실패", "items": []}), 502

    normalized_query = normalize_contest_name(query)
    exact_matches = [
        item for item in contests if normalize_contest_name(item["name"]) == normalized_query
    ]
    partial_matches = [
        item for item in contests if normalize_contest_name(item["name"]) != normalized_query
    ]

    return jsonify(
        {
            "err": "N",
            "err_msg": "",
            "items": exact_matches + partial_matches,
        }
    )


@app.route("/api/contest-list", methods=["GET"])
def contest_list():
    page = request.args.get("page", "1").strip() or "1"
    try:
        page_number = max(int(page), 1)
    except ValueError:
        return jsonify({"err": "Y", "err_msg": "올바른 페이지 번호가 아닙니다.", "items": []}), 400

    try:
        data = fetch_contest_page(page_number)
    except requests.exceptions.Timeout:
        return jsonify({"err": "Y", "err_msg": "대회 목록 조회 시간 초과", "items": []}), 504
    except requests.RequestException:
        return jsonify({"err": "Y", "err_msg": "대회 목록 조회 실패", "items": []}), 502

    return jsonify({"err": "N", "err_msg": "", **data})


@app.route("/api/contest/<contest_id>", methods=["GET"])
def contest_detail(contest_id):
    try:
        detail = fetch_contest_detail(contest_id)
    except requests.exceptions.Timeout:
        return jsonify({"err": "Y", "err_msg": "대회 상세 조회 시간 초과"}), 504
    except requests.RequestException:
        return jsonify({"err": "Y", "err_msg": "대회 상세 조회 실패"}), 502
    except ValueError:
        return jsonify({"err": "Y", "err_msg": "대회 정보를 찾지 못했습니다."}), 404

    return jsonify({"err": "N", "err_msg": "", "item": detail})


@app.route("/api/badminton", methods=["POST"])
def proxy():
    payload = request.form.to_dict()
    try:
        session = create_session()
        response = session.post(
            TARGET_URL,
            data=payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        response.raise_for_status()
        return jsonify(response.json())
    except ValueError:
        return jsonify({"err": "Y", "err_msg": "Invalid JSON response"}), 502
    except requests.exceptions.Timeout:
        return jsonify({"err": "Y", "err_msg": "Timeout"}), 504
    except requests.RequestException:
        return jsonify({"err": "Y", "err_msg": "Server Error"}), 500


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


def open_browser():
    time.sleep(0.8)
    webbrowser.open_new("http://127.0.0.1:5001/")


if __name__ == "__main__":
    if os.getenv("WERKZEUG_RUN_MAIN") == "true":
        threading.Thread(target=open_browser, daemon=True).start()
    app.run(host="127.0.0.1", port=5001, debug=False)
