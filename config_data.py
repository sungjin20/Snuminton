UPDATE_DATE = "2025년 10월 31일"

executives = ["김영준", "이주원", "김상원", "조재형", "김민성", "윤주영", "이지호", "강예원"]

sheet_ids = {
        '10_5th': "1RaPli5_B60ZdWi9K4cBE93fO9yhAzs0ecFZnmM8KicM",  # 10월 5주차 시트 ID
        '11_1st': "1pZvUVqGiyDm96N-Kzun5s4_8f8xDQkeI0L1mL-mOjNs",  # 11월 1주차 시트 ID
        '11_2nd': "1SOUCE8B1BPkcJEiWqHGZkuDm9lb1vT1MydOMJcmZ-sA",  # 11월 2주차 시트 ID
        '11_3rd': "1WYc86bJJs4JBzfNUegL9T0pZVzqN9dW-r2eG7P5A4II",  # 11월 3주차 시트 ID
        '11_4th': "1xpqHPz8VVYYywqajK0aKnZ5Y6C0z5CVNiITu5iN6xsU",  # 11월 4주차 시트 ID
    }

links = {
    '2025-10-28': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScu5H-PgAu-7LDWpzSj8HYh13QDGtQMPSrvu9-O78CjVqF2sw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2025-10-30': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLScCBFQpu3KPA_h4ZJkkg-SHozvnfxAZwcPhhfuPq58gBclKSg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },
    '2025-11-01': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfDlWh-UbKf2SW0KP4bLotBHdDHlfqaryQzXh88nO3K2M7EBg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[0]}/edit?usp=drivesdk'
    },

    '2025-11-04': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeNtu902gGhH-y5jZjofVj3PaOTnEF3Plij23RmheYtRYH7qA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2025-11-06': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSfdQeKug4MuG23DbXbtgz6hEjffgm6LB42ChVLANFa_M-YJeg/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },
    '2025-11-08': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSeNBNc9PxUHUMf6nsi8FqYrEjxR4NGaD1UcZausRvdmHF8PhQ/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[1]}/edit?usp=drivesdk'
    },

    '2025-11-11': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdbxagoZzNS7GOKKw65mopc_zfWDpDFWckzuUdo4djtA-oVSA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2025-11-13': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdwSHvKdUlOi-XAhN9eR16XDphfzq_runtKth010GH6F2DdBw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },
    '2025-11-15': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSd0Y-1NedJ0IiFHpEZZQsHe97X9yUowtse8AC2srVgkz2KuPw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[2]}/edit?usp=drivesdk'
    },

    '2025-11-18': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSf_a00HdZsO9yNXqJS2AZ3eQAfB9i5K0XKS66Ks_bAQ77bouQ/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2025-11-20': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdLRUeRHeCMm016IEzB3sLFvMEVXMT6X5FgRH1CNEgeX5h_JA/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },
    '2025-11-22': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSdYXfQCZsyaGi105O01t-gplbkHh0o1RsJByuh0acAvwT8xNQ/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[3]}/edit?usp=drivesdk'
    },

    '2025-11-25': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSd4FNPL45tyM5gGdHO8KHPgSMqxWM5amyosT83LAnaVbKkx1Q/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
    '2025-11-27': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSc6tQbrfWO7pOMi7kXPNkcVxQFajtRFkTIzEykLqXwhAqaeuw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
    '2025-11-29': {
        'form_link': 'https://docs.google.com/forms/d/e/1FAIpQLSf51s-FJvgVtjJTeGlo6EzHev_khtkTHkXm4r0ap8GfxUOtDw/viewform',
        'status_link': f'https://docs.google.com/spreadsheets/d/{list(sheet_ids.values())[4]}/edit?usp=drivesdk'
    },
}
