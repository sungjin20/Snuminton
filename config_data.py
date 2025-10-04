UPDATE_DATE = "2025년 10월 04일"

executives = ["김영준", "이주원", "김상원", "조재형", "김민성", "윤주영", "이지호", "강예원"]

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