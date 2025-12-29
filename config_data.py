UPDATE_DATE = "2025년 12월 29일"

executives = ["김영준", "이주원", "김상원", "조재형", "김민성", "윤주영", "이지호", "강예원"]

sheet_ids = {
        '1_1st': "1G1EU3-5S_q1e-l3TiE_IiSWeRcyFXa0BhrJo5CfNCUY",  # 1월 1주차 시트 ID
        '1_2nd': "1OUDKhEGTPGijsA9XlsvT7735v-DlFW152CZTZ48jCKc",  # 1월 2주차 시트 ID
        '1_3rd': "1hOqi0v5UrmhPmum65H5bVxa9hynkVeckVtL2jD_4lh4",  # 1월 3주차 시트 ID
        '1_4th': "16-qoJHKFOcAbvl_TVtokZ6Z0fDzHLd3rfptbHcv3xnU",  # 1월 4주차 시트 ID
        '1_5th' : "1pF1jaidYbGwSnC_4HUi-ddiIBvtdVyoXZ62DjeK5siY"  # 1월 5주차 시트 ID
    }

links = {
    # 1월 1주차 (sheet_ids index 0)
    '2025-12-30': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfWOxGAoeUJl4COkLtGKi3wGITFJGPzqXKfiUAwfNcodhR0ew/viewform',  # 화
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2026-01-01': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfkgf9OgtUJLR-IePmwq1oSf6hIyBsTpKXYqCndW4WN7Sh-ig/viewform',  # 목
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2026-01-03': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSc7sR4vYogNrMXgsu9p_TbVJnxep1waYXpb8jg4PuX43p57xg/viewform',  # 토
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },

    # 1월 2주차 (sheet_ids index 1)
    '2026-01-06': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScaudF956_xtpvQK83aRXgCMysodnVqzCMgacjCbZ_hmsAZnw/viewform',  # 화
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2026-01-08': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeVVcfwHJGWYXo9_ZCMf8HOVJtOLDZ7TAOSQ13NiBzcIDifoQ/viewform',  # 목
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2026-01-10': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfVqdINcEGIyOgS6Wihue0_ALwcq1lnF9qvdeoVczKhnWeezg/viewform',  # 토
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },

    # 1월 3주차 (sheet_ids index 2)
    '2026-01-13': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeTEePWfnhHi2ZN3oCSAUVf3YjHFVyFk_-16713sQh2id7e5g/viewform',  # 화
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2026-01-15': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdtDUx92N0ysORavfwUOVVslI4Be5eS9qt8zITzo_UEf36URg/viewform',  # 목
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2026-01-17': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfuvwcMpfijjxHNekAsh4L2UsMQSA456u32cU1E9h1CttxMWA/viewform',  # 토
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },

    # 1월 4주차 (sheet_ids index 3)
    '2026-01-20': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeX30oxsmFSxaAWKE5wAmvX8zJpI7bryn7bDOVQ9au5QXPJAw/viewform',  # 화
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2026-01-22': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScH5dwVmelhCMOVBgWwcplsCPxulvrULCYLdqHLO1ccu-JDlA/viewform',  # 목
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2026-01-24': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSe5CvYTj1m44rCCa1gTo7N1O4KmTxGBBwF8DkA4M5eVxtmovA/viewform',  # 토
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },

    # 1월 5주차 (sheet_ids index 4)
    '2026-01-27': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScMXjC-LslVrkWkhZkyfZoIdmYQS6tbGluSPlfAuGw91HwP3Q/viewform',  # 화
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
    '2026-01-29': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSe2ZP0UVPPp3EwEyU45F5CKbRF0A1P3e4PMM4ZInIPx_Bu_EA/viewform',  # 목
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
    '2026-01-31': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSetgMQ3ClrK2DKpxaM9y-JRt4WTw_NIsar6rQQ0gdbrZjUIHA/viewform',  # 토
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
}

