UPDATE_DATE = "2025년 12월 1일"

executives = ["김영준", "이주원", "김상원", "조재형", "김민성", "윤주영", "이지호", "강예원"]

sheet_ids = {
        '12_1st': "1qGHi4uKjjjRH94WKpcwDz8i-v8jUJokWjQpfb_03wCQ",  # 12월 1주차 시트 ID
        '12_2nd': "1pTd8QsXFzkiiGiU9eua9lg7RGZamKLFLSkmbq9g106Q",  # 12월 2주차 시트 ID
        '12_3rd': "1oQLofLCleTsOwi_EPjJZeRhDslP7xU5dvoTh8-GmQSo",  # 12월 3주차 시트 ID
        '12_4th': "1qqIy6iIO2KVkCj7b7MXZAvu_P94cTHWo3m65j_1TKrM",  # 12월 4주차 시트 ID
    }

links = {
    '2025-12-02': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSd1L2TgVbXM_fAwE8oDwkit_3kn5b5edsgouGFXbMrqNHZWBw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2025-12-04': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScC0YRSnIRUfdHJwrR6xdaFoJqbSwOlWDGKzds6agykMyX-1w/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2025-12-06': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdNO5lIjztwo2Ejgu2jHUeYVR19nNLMGNAVVZlU5Ov8DL8bsg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },

    '2025-12-09': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdCUZCHf0jdSqLXQf0-oDn2N-CsH0dNGd9ewMAWPK_7HT-LIg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2025-12-11': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdPjYgp7ujtUY3Q50cFPsIXxFtbJBavEsinKQcn05bU0K5Diw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2025-12-13': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeRhLyRBsWbfOY7tkX9cZk82FxQmn231WV927U-ciKri4aIFg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },

    '2025-12-16': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSezvXqjAXoFDq1PQusUdbGYMR2KCqIqOoLbt59sWMcJyKptkA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2025-12-18': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeaKZYEE6aeggvw4KcqTtXmZ3k8J7VC8AgFg3WzkjPav426Bg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2025-12-20': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSe2FO3V4X9rbddzu3Iyb27lqxjxiX-8aT_GvHhl1wVaI3ckTQ/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },

    '2025-12-23': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdhxZ_Uft_gmgpk0C1aNioWTGZ-u2Dx1Vpr4uUe_KS87_0uoA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2025-12-25': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSccEn8IK__jqXo4rnp0QB-FLAvaWWsDjnTXB-tzCvrKyya7LA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2025-12-27': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSejaedVDkLM9VcOw0n53R5EXuN1YJs51BDlC6nCwqy3UIwtEw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },

    # '2025-11-25': {
    #     'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSd4FNPL45tyM5gGdHO8KHPgSMqxWM5amyosT83LAnaVbKkx1Q/viewform',
    #     'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    # },
    # '2025-11-27': {
    #     'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSc6tQbrfWO7pOMi7kXPNkcVxQFajtRFkTIzEykLqXwhAqaeuw/viewform',
    #     'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    # },
    # '2025-11-29': {
    #     'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSf51s-FJvgVtjJTeGlo6EzHev_khtkTHkXm4r0ap8GfxUOtDw/viewform',
    #     'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    # },
}
