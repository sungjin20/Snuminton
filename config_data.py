UPDATE_DATE = "2025년 10월 31일"

executives = ["김영준", "이주원", "김상원", "조재형", "김민성", "윤주영", "이지호", "강예원"]

sheet_ids = {
        '10_5th': "1RaPli5_B60ZdWi9K4cBE93fO9yhAzs0ecFZnmM8KicM",  # 10월 5주차 시트 ID
        '11_1st': "1pZvUVqGiyDm96N-Kzun5s4_8f8xDQkeI0L1mL-mOjNs",  # 11월 1주차 시트 ID
        '11_2nd': "1SOUCE8B1BPkcJEiWqHGZkuDm9lb1vT1MydOMJcmZ-sA",  # 11월 2주차 시트 ID
        '11_3rd': "1WYc86bJJs4JBzfNUegL9T0pZVzqN9dW-r2eG7P5A4II",  # 11월 3주차 시트 ID
        '11_4th': "1xpqHPz8VVYYywqajK0aKnZ5Y6C0z5CVNiITu5iN6xsU",  # 11월 4주차 시트 ID
    }
# test
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>스누민턴 운영부</title>
    <link rel="icon" href="static/스누민턴%20로고.png" type="image/png">

    <!-- Google Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&family=Roboto:wght@400;500;700&display=swap" rel="stylesheet">

    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <style>
        :root {
            --primary-blue: #0066cc;
            --primary-yellow: #ffeb3b;
            --secondary-blue: #e6f0ff;
            --dark-gray: #333333;
            --light-gray: #f5f5f5;
            --white: #ffffff;
            --shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans KR', 'Roboto', sans-serif;
            background-color: var(--light-gray);
            color: var(--dark-gray);
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Header Styles */
        header {
            background-color: var(--white);
            box-shadow: var(--shadow);
            padding: 1rem 2rem;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        .header-container {
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .logo-title {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .logo {
            width: 50px;
            height: 50px;
        }

        .title {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-blue);
        }

        /* Main Content Styles */
        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
            width: 100%;
        }

        .hero {
            text-align: center;
            margin-bottom: 3rem;
            max-width: 800px;
        }

        .hero h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            color: var(--primary-blue);
        }

        .hero p {
            font-size: 1.1rem;
            color: #555;
        }

        /* Menu Grid */
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1.5rem;
            width: 100%;
            max-width: 1000px;
        }

        .menu-card {
            background-color: var(--white);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow);
            transition: var(--transition);
            display: flex;
            flex-direction: column;
            height: 100%;
        }

        .menu-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        }

        .card-icon {
            background-color: var(--secondary-blue);
            padding: 1.5rem;
            text-align: center;
            font-size: 2.5rem;
            color: var(--primary-blue);
        }

        .card-content {
            padding: 1.5rem;
            flex-grow: 1;
            display: flex;
            flex-direction: column;
        }

        .card-content h3 {
            font-size: 1.3rem;
            margin-bottom: 0.5rem;
            color: var(--primary-blue);
        }

        .card-content p {
            color: #666;
            margin-bottom: 1rem;
            flex-grow: 1;
        }

        .btn {
            display: inline-block;
            background-color: var(--primary-blue);
            color: var(--white);
            padding: 0.8rem 1.5rem;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 500;
            transition: var(--transition);
            text-align: center;
        }

        .btn:hover {
            background-color: #0052a3;
            transform: translateY(-2px);
        }

        /* Footer Styles */
        footer {
            background-color: var(--dark-gray);
            color: var(--white);
            padding: 2rem;
            text-align: center;
        }

        .footer-content {
            max-width: 1200px;
            margin: 0 auto;
        }

        .social-links {
            display: flex;
            justify-content: center;
            gap: 1.5rem;
            margin: 1rem 0;
        }

        .social-links a {
            color: var(--white);
            font-size: 1.5rem;
            transition: var(--transition);
        }

        .social-links a:hover {
            color: var(--primary-yellow);
        }

        .copyright {
            margin-top: 1rem;
            font-size: 0.9rem;
            color: #bbb;
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            .header-container {
                flex-direction: column;
                gap: 1rem;
            }

            .hero h1 {
                font-size: 2rem;
            }

            .menu-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <!-- Header -->
    <header>
        <div class="header-container">
            <div class="logo-title">
                <img class="logo" src="../static/스누민턴%20로고.png" alt="스누민턴 로고">
                <div class="title">스누민턴 운영부</div>
            </div>
        </div>
    </header>

    <!-- Main Content -->
    <main>
        <section class="hero">
            <h1>스누민턴 운영 관리 시스템</h1>
            <p>동아리 운영에 필요한 모든 기능을 한 곳에서 간편하게 관리하세요</p>
        </section>

        <section class="menu-grid">
            <!-- 출석 체크 -->
            <div class="menu-card">
                <div class="card-icon">
                    <i class="fas fa-clipboard-check"></i>
                </div>
                <div class="card-content">
                    <h3>출석 체크</h3>
                    <p>동아리 활동 출석을 간편하게 관리하고 기록하세요</p>
                    <a href="{{ url_for('attendance_selection') }}" class="btn">사용하기</a>
                </div>
            </div>

            <!-- 지각/불참/게스트비 체크 -->
            <div class="menu-card">
                <div class="card-icon">
                    <i class="fas fa-clock"></i>
                </div>
                <div class="card-content">
                    <h3>지각/불참/게스트비 체크</h3>
                    <p>지각, 불참, 게스트비 관리를 효율적으로 처리하세요</p>
                    <a href="{{ url_for('etc_selection') }}" class="btn">사용하기</a>
                </div>
            </div>

            <!-- 운동신청공지 복사 -->
            <div class="menu-card">
                <div class="card-icon">
                    <i class="fas fa-copy"></i>
                </div>
                <div class="card-content">
                    <h3>운동신청공지 복사</h3>
                    <p>운동 신청 공지를 쉽게 생성하고 공유하세요</p>
                    <a href="{{ url_for('notice_selection') }}" class="btn">사용하기</a>
                </div>
            </div>

            <!-- 게스트 운동신청공지 복사 -->
            <div class="menu-card">
                <div class="card-icon">
                    <i class="fas fa-user-friends"></i>
                </div>
                <div class="card-content">
                    <h3>게스트 운동신청공지 복사</h3>
                    <p>게스트를 위한 운동 신청 공지를 생성하세요</p>
                    <a href="{{ url_for('notice_selection_guest') }}" class="btn">사용하기</a>
                </div>
            </div>

            <!-- 메시지 전송 -->
            <div class="menu-card">
                <div class="card-icon">
                    <i class="fas fa-paper-plane"></i>
                </div>
                <div class="card-content">
                    <h3>메시지 전송</h3>
                    <p>동아리 멤버들에게 공지를 빠르게 전송하세요</p>
                    <a href="{{ auth_url_main }}" class="btn">사용하기</a>
                </div>
            </div>

            <!-- 시간표 공지 -->
            <div class="menu-card">
                <div class="card-icon">
                    <i class="fas fa-calendar-alt"></i>
                </div>
                <div class="card-content">
                    <h3>시간표 공지</h3>
                    <p>동아리 시간표를 공유하고 관리하세요</p>
                    <a href="{{ auth_url_schedule }}" class="btn">사용하기</a>
                </div>
            </div>
        </section>
    </main>

    <!-- Footer -->
    <footer>
        <div class="footer-content">
            <div class="social-links">
                <a href="https://www.instagram.com/snuminton/"><i class="fab fa-instagram"></i></a>
            </div>
            <div class="copyright">
                &copy; 2025 김성진. All rights reserved.<br>
                업데이트: """ + UPDATE_DATE + """
            </div>
        </div>
    </footer>
</body>
</html>
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
