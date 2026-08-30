from flask import Flask, render_template_string, jsonify, request
import requests

app = Flask(__name__)
API_URL = "https://api.guerrillamail.com/ajax.php"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="id">
<head>
    <title>HestiaMail - Secure Disposable Email</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
            margin: 0; 
            padding: 20px; 
            background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 50%, #ffffff 100%); 
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .container { 
            width: 100%; 
            max-width: 750px; 
            background: white; 
            padding: 30px; 
            border-radius: 20px; 
            box-shadow: 0 12px 35px rgba(0,0,0,0.15); 
            box-sizing: border-box;
            position: relative;
            overflow: visible; 
        }

        /* Dekorasi Bunga Sakura di Setiap Sudut */
        .sakura {
            position: absolute;
            width: 45px;
            height: 45px;
            z-index: 10;
        }
        .sakura-tl { top: -20px; left: -20px; transform: rotate(-15deg); }
        .sakura-tr { top: -20px; right: -20px; transform: rotate(15deg); }
        .sakura-bl { bottom: -20px; left: -20px; transform: rotate(45deg); }
        .sakura-br { bottom: -20px; right: -20px; transform: rotate(-45deg); }

        /* Tombol Menu Kiri (Hamburger) */
        .menu-btn {
            position: absolute;
            top: 20px;
            left: 25px;
            background: #fff0f3;
            border: 1px solid #ffccd5;
            color: #d63384;
            padding: 7px 12px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            z-index: 12;
            transition: all 0.3s;
        }
        .menu-btn:hover { background: #ff4d6d; color: white; }

        /* Widget Pemutar Musik Melayang di Pojok Kanan Bawah */
        .music-widget {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: white;
            border: 2px solid #ffccd5;
            border-radius: 30px;
            padding: 8px 15px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 5px 20px rgba(255, 77, 109, 0.2);
            z-index: 1500;
        }
        .music-btn {
            background: #ff4d6d;
            color: white;
            border: none;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            cursor: pointer;
            font-size: 14px;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: background 0.3s;
        }
        .music-btn:hover { background: #c9184a; }
        .music-title {
            font-size: 12px;
            font-weight: bold;
            color: #d63384;
        }

        /* Sidebar Tunggal */
        .sidebar {
            position: fixed;
            top: 0;
            left: -320px;
            width: 300px;
            height: 100%;
            background: white;
            box-shadow: 5px 0 25px rgba(0,0,0,0.2);
            z-index: 100;
            transition: left 0.35s ease;
            padding: 25px;
            box-sizing: border-box;
            overflow-y: auto;
        }
        .sidebar.open { left: 0; }

        .sidebar-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 2px solid #ffe5ec;
            padding-bottom: 10px;
        }
        .sidebar-header h2 { margin: 0; font-size: 18px; color: #d63384; }
        .close-sidebar { background: none; border: none; font-size: 22px; cursor: pointer; color: #666; }
        .close-sidebar:hover { color: #ff4d6d; }

        .overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.4);
            z-index: 99;
            display: none;
            backdrop-filter: blur(2px);
        }
        .overlay.active { display: block; }

        /* Welcome Modal Pop-up di Tengah Layar */
        .welcome-modal-overlay {
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0, 0, 0, 0.6);
            backdrop-filter: blur(4px);
            z-index: 2000;
            display: flex;
            justify-content: center;
            align-items: center;
            opacity: 0;
            visibility: hidden;
            transition: all 0.3s ease;
        }
        .welcome-modal-overlay.active {
            opacity: 1;
            visibility: visible;
        }
        .welcome-modal-box {
            background: white;
            width: 90%;
            max-width: 400px;
            padding: 30px;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 15px 35px rgba(255, 77, 109, 0.3);
            border: 2px solid #ffccd5;
            transform: scale(0.8);
            transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        }
        .welcome-modal-overlay.active .welcome-modal-box {
            transform: scale(1);
        }
        .welcome-modal-box h2 {
            color: #d63384;
            margin-top: 0;
            font-size: 24px;
        }
        .welcome-modal-box p {
            color: #666;
            font-size: 14px;
            line-height: 1.5;
            margin-bottom: 25px;
        }
        .welcome-btn {
            background: #ff4d6d;
            color: white;
            border: none;
            padding: 12px 25px;
            font-size: 15px;
            font-weight: bold;
            border-radius: 12px;
            cursor: pointer;
            transition: background 0.3s, transform 0.2s;
            width: 100%;
        }
        .welcome-btn:hover {
            background: #c9184a;
            transform: translateY(-2px);
        }

        /* Desain Sistem Laci (Accordion Menu) */
        .drawer-item {
            margin-bottom: 12px;
            border: 1px solid #ffccd5;
            border-radius: 10px;
            overflow: hidden;
            background: #fff5f7;
        }
        .drawer-toggle {
            width: 100%;
            background: #fff0f3;
            border: none;
            padding: 12px 15px;
            text-align: left;
            font-size: 13px;
            font-weight: bold;
            color: #c9184a;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
            transition: background 0.3s;
        }
        .drawer-toggle:hover { background: #ffe3e9; }
        .drawer-content {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease-out, padding 0.3s ease-out;
            padding: 0 15px;
            background: white;
        }
        .drawer-content.open {
            max-height: 320px;
            padding: 12px 15px;
        }

        .lang-switch-box {
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
            justify-content: center;
        }
        .lang-btn {
            background: #f1f3f5;
            border: 1px solid #ced4da;
            padding: 6px 10px;
            font-size: 12px;
            font-weight: bold;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.3s;
            flex: 1 1 40%;
            text-align: center;
        }
        .lang-btn.active {
            background: #ff4d6d;
            color: white;
            border-color: #ff4d6d;
        }

        .fb-container { 
            background: #fff0f3; 
            border: 1px dashed #ff4d6d; 
            border-radius: 8px; 
            padding: 8px 10px; 
            font-size: 13px; 
            color: #444; 
            text-align: center;
            margin-bottom: 8px; 
        }
        .fb-link {
            color: #1877f2;
            font-weight: bold;
            text-decoration: none;
            margin-left: 4px;
        }
        .fb-link:hover { text-decoration: underline; }

        .creator-tag { 
            color: #ff4d6d; 
            font-size: 12px; 
            font-weight: bold; 
            font-style: italic; 
            text-align: center;
            line-height: 1.4; 
        }

        .widget-value { font-size: 13px; color: #333; font-weight: bold; text-align: center; }
        .world-clock-item { font-size: 12px; color: #444; margin-bottom: 6px; display: flex; justify-content: space-between; }
        
        h1 { color: #d63384; text-align: center; margin-top: 15px; margin-bottom: 5px; font-size: 30px; font-weight: 800; }
        .subtitle { text-align: center; color: #666; font-size: 14px; margin-bottom: 20px; }
        
        .email-container { display: flex; flex-direction: column; align-items: center; gap: 12px; text-align: center; }
        .email-box { background: #fff0f3; border: 1px solid #ffccd5; padding: 14px; font-size: 18px; font-weight: bold; border-radius: 10px; color: #c9184a; word-break: break-all; width: 90%; }
        
        .controls-row {
            display: flex;
            gap: 10px;
            width: 90%;
            justify-content: center;
        }
        .domain-select {
            background: #fff;
            border: 2px solid #ffccd5;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
            border-radius: 10px;
            color: #d63384;
            cursor: pointer;
            outline: none;
            transition: border-color 0.3s;
        }
        .domain-select:hover { border-color: #ff4d6d; }
        
        .copy-btn { background: #ff4d6d; color: white; border: none; padding: 12px 20px; font-size: 15px; font-weight: bold; border-radius: 10px; cursor: pointer; transition: background 0.3s; flex-grow: 1; }
        .copy-btn:hover { background: #c9184a; }
        .copy-btn.copied { background: #28a745; }
        
        .inbox-header { display: flex; justify-content: space-between; align-items: center; margin-top: 35px; border-bottom: 2px solid #ffe5ec; padding-bottom: 10px; margin-bottom: 20px; }
        .inbox-header h2 { margin: 0; font-size: 20px; color: #333; }
        
        .refresh-btn { background: #ff4d6d; color: white; border: none; padding: 8px 16px; font-size: 14px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: background 0.3s; display: flex; align-items: center; gap: 5px; }
        .refresh-btn:hover { background: #c9184a; }
        .refresh-btn:disabled { background: #6c757d; cursor: not-allowed; }
        
        .message { 
            background: #ffffff;
            border: 1px solid #ffccd5;
            border-radius: 12px;
            padding: 18px;
            margin-bottom: 15px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            transition: transform 0.2s;
        }
        .message:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(255, 77, 109, 0.1);
        }
        .message h3 { margin: 0 0 8px 0; font-size: 17px; color: #d63384; word-break: break-word; }
        .message p { margin: 0 0 12px 0; color: #666; font-size: 13px; line-height: 1.4; }
        .content { 
            margin-top: 10px; background: #fff5f7; padding: 15px; border-radius: 8px; font-size: 13px; color: #333; border-left: 4px solid #ff4d6d; 
            word-break: break-word; overflow-wrap: break-word; max-width: 100%; line-height: 1.5;
        }
        
        .footer { text-align: center; margin-top: 35px; padding-top: 15px; border-top: 1px dashed #ffccd5; color: #888; font-size: 13px; }
        .footer strong { color: #ff4d6d; }

        @media (max-width: 480px) {
            body { padding: 10px; }
            .container { padding: 15px; }
            .menu-btn { top: 12px; left: 12px; padding: 5px 10px; font-size: 13px; }
            h1 { font-size: 24px; margin-top: 25px; }
            .controls-row { flex-direction: column; }
            .music-widget { bottom: 10px; right: 10px; padding: 6px 12px; }
        }
    </style>
</head>
<body>
    <div id="youtube-player-container" style="display:none;">
        <iframe id="youtubeIframe" width="0" height="0" src="" title="YouTube audio player" frameborder="0" allow="autoplay"></iframe>
    </div>

    <div class="music-widget">
        <button class="music-btn" id="playPauseBtn" onclick="toggleMusicWidget()">▶</button>
        <span class="music-title">🎵 Surrender</span>
    </div>

    <div class="welcome-modal-overlay active" id="welcomeModal">
        <div class="welcome-modal-box">
            <h2 data-i18n="welcomeTitle">✨ Selamat Datang!</h2>
            <p data-i18n="welcomeDesc">HestiaMail siap mengamankan privasi Anda dengan email sementara yang cepat dan praktis.</p>
            <button class="welcome-btn" onclick="closeWelcomeModal()" data-i18n="welcomeBtn">Mulai Sekarang</button>
        </div>
    </div>

    <div class="overlay" id="overlay" onclick="toggleSidebar()"></div>

    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <h2 data-i18n="menuTitle">Menu Utama</h2>
            <button class="close-sidebar" onclick="toggleSidebar()">&times;</button>
        </div>
        
        <div class="drawer-item">
            <button class="drawer-toggle" onclick="toggleDrawer('drawerLang')">
                <span data-i18n="langMenu">🌐 Pengaturan Bahasa</span> <span>▼</span>
            </button>
            <div class="drawer-content" id="drawerLang">
                <div class="lang-switch-box">
                    <button class="lang-btn active" id="btn-id" onclick="switchLanguage('id')">🇮🇩 ID</button>
                    <button class="lang-btn" id="btn-en" onclick="switchLanguage('en')">🇬🇧 EN</button>
                    <button class="lang-btn" id="btn-zh" onclick="switchLanguage('zh')">🇨🇳 中文</button>
                    <button class="lang-btn" id="btn-ja" onclick="switchLanguage('ja')">🇯🇵 日本語</button>
                    <button class="lang-btn" id="btn-ko" onclick="switchLanguage('ko')">🇰🇷 한국어</button>
                </div>
            </div>
        </div>

        <div class="drawer-item">
            <button class="drawer-toggle" onclick="toggleDrawer('drawerTime')">
                <span data-i18n="timeMenu">⏰ Waktu & Kalender</span> <span>▼</span>
            </button>
            <div class="drawer-content" id="drawerTime">
                <div style="margin-bottom: 10px;">
                    <div style="font-size: 11px; color: #c9184a; font-weight: bold; margin-bottom: 3px;" data-i18n="calTitle">📅 Kalender</div>
                    <div class="widget-value" id="current-date">Memuat...</div>
                </div>
                <div>
                    <div style="font-size: 11px; color: #c9184a; font-weight: bold; margin-bottom: 3px;" data-i18n="clockTitle">🌍 Jam Dunia</div>
                    <div id="world-clocks">
                        <div class="world-clock-item"><span>Jakarta (WIB):</span> <span id="clock-jkt">--:--:--</span></div>
                        <div class="world-clock-item"><span>London (GMT):</span> <span id="clock-lon">--:--:--</span></div>
                        <div class="world-clock-item"><span>New York (EST):</span> <span id="clock-nyt">--:--:--</span></div>
                    </div>
                </div>
            </div>
        </div>

        <div class="drawer-item">
            <button class="drawer-toggle" onclick="toggleDrawer('drawerInfo')">
                <span data-i18n="infoMenu">✨ Tentang Web & Info</span> <span>▼</span>
            </button>
            <div class="drawer-content" id="drawerInfo">
                <div class="fb-container">
                    <span data-i18n="fbLabel">Akun Facebook:</span><br>
                    <a href="https://facebook.com/Hestiaa.sr" target="_blank" class="fb-link">Hestiaa.sr</a>
                </div>
                <div class="creator-tag" data-i18n="creatorText">✨ Web ini diciptakan oleh Hestia asal Indonesia 🇮🇩</div>
            </div>
        </div>
    </div>

    <div class="container">
        <svg class="sakura sakura-tl" viewBox="0 0 100 100"><ellipse cx="50" cy="22" rx="12" ry="20" fill="#ff758c"/><ellipse cx="50" cy="78" rx="12" ry="20" fill="#ff758c"/><ellipse cx="22" cy="50" rx="20" ry="12" fill="#ff758c"/><ellipse cx="78" cy="50" rx="20" ry="12" fill="#ff758c"/><circle cx="50" cy="50" r="8" fill="#ffccd5"/></svg>
        <svg class="sakura sakura-tr" viewBox="0 0 100 100"><ellipse cx="50" cy="22" rx="12" ry="20" fill="#ff758c"/><ellipse cx="50" cy="78" rx="12" ry="20" fill="#ff758c"/><ellipse cx="22" cy="50" rx="20" ry="12" fill="#ff758c"/><ellipse cx="78" cy="50" rx="20" ry="12" fill="#ff758c"/><circle cx="50" cy="50" r="8" fill="#ffccd5"/></svg>
        <svg class="sakura sakura-bl" viewBox="0 0 100 100"><ellipse cx="50" cy="22" rx="12" ry="20" fill="#ff758c"/><ellipse cx="50" cy="78" rx="12" ry="20" fill="#ff758c"/><ellipse cx="22" cy="50" rx="20" ry="12" fill="#ff758c"/><ellipse cx="78" cy="50" rx="20" ry="12" fill="#ff758c"/><circle cx="50" cy="50" r="8" fill="#ffccd5"/></svg>
        <svg class="sakura sakura-br" viewBox="0 0 100 100"><ellipse cx="50" cy="22" rx="12" ry="20" fill="#ff758c"/><ellipse cx="50" cy="78" rx="12" ry="20" fill="#ff758c"/><ellipse cx="22" cy="50" rx="20" ry="12" fill="#ff758c"/><ellipse cx="78" cy="50" rx="20" ry="12" fill="#ff758c"/><circle cx="50" cy="50" r="8" fill="#ffccd5"/></svg>

        <button class="menu-btn" onclick="toggleSidebar()">☰ Menu</button>

        <h1>HestiaMail</h1>
        <div class="subtitle" data-i18n="subtitle">Email aman sekali pakai</div>
        
        <div class="email-container">
            <div class="email-box" id="email-text">Memuat...</div>
            
            <div class="controls-row">
                <select class="domain-select" id="domainSelect" onchange="changeDomain()">
                    <option value="spam4.me">@spam4.me</option>
                    <option value="pokemail.net">@pokemail.net</option>
                    <option value="grr.la">@grr.la</option>
                </select>
                <button class="copy-btn" id="copyBtn" onclick="copyToClipboard()" data-i18n="copyBtn">Salin Email</button>
            </div>
        </div>
        
        <div class="inbox-header">
            <h2 data-i18n="inboxTitle">Kotak Masuk</h2>
            <button class="refresh-btn" id="refreshBtn" onclick="fetchMessages()" data-i18n="refreshBtn">Refresh 🔄</button>
        </div>
        
        <div id="inbox"></div>
        
        <div class="footer" data-i18n="footer">
            &copy; 2026 <strong>HestiaMail</strong>. Hak Cipta Dilindungi.
        </div>
    </div>

    <script>
        let currentEmailUser = "";
        let currentLang = 'id';
        let token = "";
        let isPlaying = false;

        const translations = {
            id: {
                menuTitle: "Menu Utama",
                langMenu: "🌐 Pengaturan Bahasa",
                timeMenu: "⏰ Waktu & Kalender",
                infoMenu: "✨ Tentang Web & Info",
                subtitle: "Email aman sekali pakai",
                welcomeTitle: "✨ Selamat Datang!",
                welcomeDesc: "HestiaMail siap mengamankan privasi Anda dengan email sementara yang cepat dan praktis.",
                welcomeBtn: "Mulai Sekarang",
                creatorText: "✨ Web ini diciptakan oleh Hestia asal Indonesia 🇮🇩",
                fbLabel: "Akun Facebook:",
                calTitle: "📅 Kalender Hari Ini",
                clockTitle: "🌍 Jam Dunia",
                copyBtn: "Salin Email",
                copiedBtn: "Tersalin!",
                inboxTitle: "Kotak Masuk",
                refreshBtn: "Refresh 🔄",
                loadingBtn: "Memuat...",
                emptyInbox: "Belum ada pesan baru masuk.",
                footer: "&copy; 2026 <strong>HestiaMail</strong>. Hak Cipta Dilindungi.",
                fromText: "Dari:",
                dateText: "Tanggal:"
            },
            en: {
                menuTitle: "Main Menu",
                langMenu: "🌐 Language Settings",
                timeMenu: "⏰ Time & Calendar",
                infoMenu: "✨ About Web & Info",
                subtitle: "Secure disposable email",
                welcomeTitle: "✨ Welcome!",
                welcomeDesc: "HestiaMail is ready to secure your privacy with fast and practical temporary emails.",
                welcomeBtn: "Get Started",
                creatorText: "✨ This website was created by Hestia from Indonesia 🇮🇩",
                fbLabel: "Facebook Account:",
                calTitle: "📅 Today's Calendar",
                clockTitle: "🌍 World Clock",
                copyBtn: "Copy Email",
                copiedBtn: "Copied!",
                inboxTitle: "Inbox",
                refreshBtn: "Refresh 🔄",
                loadingBtn: "Loading...",
                emptyInbox: "No new messages yet.",
                footer: "&copy; 2026 <strong>HestiaMail</strong>. All Rights Reserved.",
                fromText: "From:",
                dateText: "Date:"
            },
            zh: {
                menuTitle: "主菜单",
                langMenu: "🌐 语言设置",
                timeMenu: "⏰ 时间与日历",
                infoMenu: "✨ 关于网页与信息",
                subtitle: "安全的一次性邮箱",
                welcomeTitle: "✨ 欢迎光临！",
                welcomeDesc: "HestiaMail 随时准备通过快速实用的一次性邮箱来保护您的隐私。",
                welcomeBtn: "立即开始",
                creatorText: "✨ 本网站由来自印尼的 Hestia 创建 🇮🇩",
                fbLabel: "Facebook 账号：",
                calTitle: "📅 今日日历",
                clockTitle: "🌍 世界时钟",
                copyBtn: "复制邮箱",
                copiedBtn: "已复制！",
                inboxTitle: "收件箱",
                refreshBtn: "刷新 🔄",
                loadingBtn: "加载中...",
                emptyInbox: "暂无新消息。",
                footer: "&copy; 2026 <strong>HestiaMail</strong>. 版权所有。",
                fromText: "发件人：",
                dateText: "日期："
            },
            ja: {
                menuTitle: "メインメニュー",
                langMenu: "🌐 言語設定",
                timeMenu: "⏰ 時間とカレンダー",
                infoMenu: "✨ ウェブ情報",
                subtitle: "安全な使い捨てメール",
                welcomeTitle: "✨ ようこそ！",
                welcomeDesc: "HestiaMailは、高速で実用的な一時メールであなたのプライバシーを守ります。",
                welcomeBtn: "今すぐ始める",
                creatorText: "✨ このウェブサイトはインドネシアのHestiaによって作成されました 🇮🇩",
                fbLabel: "Facebookアカウント：",
                calTitle: "📅 本日のカレンダー",
                clockTitle: "🌍 世界時計",
                copyBtn: "メールをコピー",
                copiedBtn: "コピーしました！",
                inboxTitle: "受信トレイ",
                refreshBtn: "更新 🔄",
                loadingBtn: "読み込み中...",
                emptyInbox: "新着メッセージはありません。",
                footer: "&copy; 2026 <strong>HestiaMail</strong>. 無断複写・転載を禁じます。",
                fromText: "差出人：",
                dateText: "日付："
            },
            ko: {
                menuTitle: "메인 메뉴",
                langMenu: "🌐 언어 설정",
                timeMenu: "⏰ 시간 및 달력",
                infoMenu: "✨ 웹 정보",
                subtitle: "안전한 임시 이메일",
                welcomeTitle: "✨ 환영합니다!",
                welcomeDesc: "HestiaMail은 빠르고 실용적인 임시 이메일로 사용자의 개인정보를 보호합니다.",
                welcomeBtn: "시작하기",
                creatorText: "✨ 이 웹사이트는 인도네시아의 Hestia가 만들었습니다 🇮🇩",
                fbLabel: "페이스북 계정:",
                calTitle: "📅 오늘의 달력",
                clockTitle: "🌍 세계 시계",
                copyBtn: "이메일 복사",
                copiedBtn: "복사됨!",
                inboxTitle: "받은편지함",
                refreshBtn: "새로고침 🔄",
                loadingBtn: "불러오는 중...",
                emptyInbox: "새로운 메시지가 없습니다.",
                footer: "&copy; 2026 <strong>HestiaMail</strong>. 판권 소유.",
                fromText: "보낸 사람:",
                dateText: "날짜:"
            }
        };

        // Fungsi Tombol Widget Musik (Play / Pause YouTube)
        function toggleMusicWidget() {
            const ytIframe = document.getElementById('youtubeIframe');
            const btn = document.getElementById('playPauseBtn');
            
            if (!isPlaying) {
                ytIframe.src = "https://www.youtube.com/embed/nagMxzLZfLk?autoplay=1&loop=1&playlist=nagMxzLZfLk";
                btn.innerText = "⏸";
                isPlaying = true;
            } else {
                ytIframe.src = "";
                btn.innerText = "▶";
                isPlaying = false;
            }
        }

        // Tutup Pop-up Welcome Modal & Putar Lagu YouTube Otomatis
        function closeWelcomeModal() {
            document.getElementById('welcomeModal').classList.remove('active');
            const ytIframe = document.getElementById('youtubeIframe');
            const btn = document.getElementById('playPauseBtn');
            
            ytIframe.src = "https://www.youtube.com/embed/nagMxzLZfLk?autoplay=1&loop=1&playlist=nagMxzLZfLk";
            btn.innerText = "⏸";
            isPlaying = true;
        }

        window.onload = function() {
            initEmailData();
        };

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('open');
            document.getElementById('overlay').classList.toggle('active');
        }

        function toggleDrawer(drawerId) {
            const drawer = document.getElementById(drawerId);
            drawer.classList.toggle('open');
        }

        function switchLanguage(lang) {
            currentLang = lang;
            const langs = ['id', 'en', 'zh', 'ja', 'ko'];
            langs.forEach(l => {
                const btn = document.getElementById('btn-' + l);
                if (btn) btn.classList.toggle('active', l === lang);
            });

            document.querySelectorAll('[data-i18n]').forEach(el => {
                const key = el.getAttribute('data-i18n');
                if (translations[lang] && translations[lang][key]) {
                    el.innerHTML = translations[lang][key];
                }
            });
            updateDateTime();
            renderInbox();
        }

        function initEmailData() {
            fetch('/api/init')
                .then(res => res.json())
                .then(data => {
                    currentEmailUser = data.username;
                    token = data.token;
                    updateEmailDisplay();
                    fetchMessages();
                });
        }

        function updateEmailDisplay() {
            const select = document.getElementById('domainSelect');
            const selectedDomain = select.value;
            const fullEmail = currentEmailUser + '@' + selectedDomain;
            document.getElementById('email-text').innerText = fullEmail;
        }

        function changeDomain() {
            updateEmailDisplay();
        }

        let cachedMessages = [];

        function updateDateTime() {
            const now = new Date();
            let locale = 'id-ID';
            if (currentLang === 'en') locale = 'en-US';
            else if (currentLang === 'zh') locale = 'zh-CN';
            else if (currentLang === 'ja') locale = 'ja-JP';
            else if (currentLang === 'ko') locale = 'ko-KR';

            const optionsDate = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
            document.getElementById('current-date').innerText = now.toLocaleDateString(locale, optionsDate);
            const optionsTime = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
            try {
                document.getElementById('clock-jkt').innerText = new Intl.DateTimeFormat(locale, { ...optionsTime, timeZone: 'Asia/Jakarta' }).format(now);
                document.getElementById('clock-lon').innerText = new Intl.DateTimeFormat(locale, { ...optionsTime, timeZone: 'Europe/London' }).format(now);
                document.getElementById('clock-nyt').innerText = new Intl.DateTimeFormat(locale, { ...optionsTime, timeZone: 'America/New_York' }).format(now);
            } catch (e) {
                document.getElementById('clock-jkt').innerText = now.toLocaleTimeString();
            }
        }

        setInterval(updateDateTime, 1000);
        updateDateTime();

        function copyToClipboard() {
            const emailText = document.getElementById("email-text").innerText;
            navigator.clipboard.writeText(emailText).then(() => {
                const btn = document.getElementById("copyBtn");
                btn.innerText = translations[currentLang].copiedBtn;
                btn.classList.add("copied");
                setTimeout(() => {
                    btn.innerText = translations[currentLang].copyBtn;
                    btn.classList.remove("copied");
                }, 2000);
            });
        }

        function renderInbox() {
            const inboxDiv = document.getElementById('inbox');
            inboxDiv.innerHTML = ''; 
            
            const filteredData = cachedMessages.filter(msg => msg.from !== "no-reply@guerrillamail.com");
            
            if(filteredData.length === 0) {
                inboxDiv.innerHTML = '<p style="text-align: center; color: #999; margin-top: 20px;">' + translations[currentLang].emptyInbox + '</p>';
            } else {
                filteredData.forEach(msg => {
                    const fromLabel = translations[currentLang].fromText;
                    const dateLabel = translations[currentLang].dateText;
                    inboxDiv.innerHTML += `
                        <div class="message">
                            <h3>${msg.subject}</h3>
                            <p><strong>${fromLabel}</strong> ${msg.from}<br><strong>${dateLabel}</strong> ${msg.date}</p>
                            <div class="content">${msg.textBody}</div>
                        </div>
                    `;
                });
            }
        }

        function fetchMessages() {
            const btn = document.getElementById("refreshBtn");
            btn.innerText = translations[currentLang].loadingBtn;
            btn.disabled = true;

            fetch(`/api/messages?token=${token}`)
                .then(response => response.json())
                .then(data => {
                    cachedMessages = data;
                    renderInbox();
                })
                .catch(err => console.log("Koneksi gagal"))
                .finally(() => {
                    btn.innerText = translations[currentLang].refreshBtn;
                    btn.disabled = false;
                });
        }
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/init')
def api_init():
    try:
        res = requests.get(f"{API_URL}?f=get_email_address&lang=en", headers=HEADERS, timeout=10)
        if res.status_code == 200:
            data = res.json()
            full_email = data['email_addr']
            username = full_email.split('@')[0]
            token = data['sid_token']
            return jsonify({'username': username, 'token': token})
    except:
        pass
    return jsonify({'username': 'user123', 'token': ''})

@app.route('/api/messages')
def get_messages():
    try:
        token = request.args.get('token')
        if not token:
            return jsonify([])
        list_res = requests.get(f"{API_URL}?f=get_email_list&offset=0&sid_token={token}", headers=HEADERS, timeout=10)
        
        if list_res.status_code != 200:
            return jsonify([])
            
        inbox = list_res.json().get('list', [])
        inbox = inbox[:5] 
        
        messages = []
        for msg in inbox:
            mail_id = msg['mail_id']
            detail_res = requests.get(f"{API_URL}?f=fetch_email&email_id={mail_id}&sid_token={token}", headers=HEADERS, timeout=10)
            
            if detail_res.status_code == 200:
                detail = detail_res.json()
                messages.append({
                    'subject': detail.get('mail_subject', '(Tanpa Subjek)'),
                    'from': detail.get('mail_from', 'Tidak diketahui'),
                    'date': detail.get('mail_date', ''),
                    'textBody': detail.get('mail_body', 'Isi pesan kosong.')
                })
        return jsonify(messages)
    except:
        return jsonify([]) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
