#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亞洲聯邦共和國（簡稱：亞聯 / RAF）
國務公務與公民數位身份管理系統 v6.5 (GitHub Official Release)
"""

import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime, timedelta

# ==================== 動態主題外觀引擎 ====================
THEMES = {
    "1": {
        "name": "⚡ 賽博霓虹 (Cyberpunk Neon)",
        "PRIMARY": "\033[95m\033[1m",  # 紫紅
        "BORDER": "\033[96m",         # 青藍
        "ACCENT": "\033[93m",         # 耀黃
        "SUCCESS": "\033[92m",        # 鮮綠
        "DANGER": "\033[91m",         # 警示紅
        "DIM": "\033[90m",            # 暗灰
        "RESET": "\033[0m"
    },
    "2": {
        "name": "🟢 駭客矩陣 (Matrix Terminal)",
        "PRIMARY": "\033[92m\033[1m", # 高亮綠
        "BORDER": "\033[32m",         # 矩陣綠
        "ACCENT": "\033[97m",         # 純白
        "SUCCESS": "\033[92m",        # 鮮綠
        "DANGER": "\033[91m",         # 警示紅
        "DIM": "\033[32m\033[2m",     # 漸隱綠
        "RESET": "\033[0m"
    },
    "3": {
        "name": "👑 帝國尊榮 (Imperial Gold)",
        "PRIMARY": "\033[93m\033[1m", # 帝國金
        "BORDER": "\033[33m",         # 亮黃
        "ACCENT": "\033[96m",         # 青玉
        "SUCCESS": "\033[92m",        # 翡翠綠
        "DANGER": "\033[91m",         # 朱紅
        "DIM": "\033[90m",            # 暗灰
        "RESET": "\033[0m"
    },
    "4": {
        "name": "🌊 深海戰術 (Ocean Tactical)",
        "PRIMARY": "\033[94m\033[1m", # 蔚藍
        "BORDER": "\033[96m",         # 冰青
        "ACCENT": "\033[93m",         # 警示黃
        "SUCCESS": "\033[92m",        # 綠
        "DANGER": "\033[91m",         # 紅
        "DIM": "\033[34m",            # 深藍
        "RESET": "\033[0m"
    },
    "5": {
        "name": "🕶️ 隱形特務 (Stealth Monochrome)",
        "PRIMARY": "\033[97m\033[1m", # 高亮白
        "BORDER": "\033[90m",         # 隱形灰
        "ACCENT": "\033[37m",         # 淺灰
        "SUCCESS": "\033[97m",        # 純白
        "DANGER": "\033[91m",         # 突顯紅
        "DIM": "\033[2m",             # 弱化
        "RESET": "\033[0m"
    }
}

FEDERAL_SECTORS = [
    "亞聯東亞核心行政區 (East Core Sector)",
    "亞聯東南亞高新特區 (ASEAN High-Tech Zone)",
    "亞聯南亞量子研發特區 (South Quantum Zone)",
    "亞聯中亞清潔能源特區 (Central Energy Hub)",
    "亞聯太平洋海空戰略區 (Pacific Aero-Marine Sector)"
]

SECURITY_LEVELS = ["Level 1 - 普通公民", "Level 2 - 公務執行員", "Level 3 - 行政資深官", "Level 4 - 國務部長", "Level 5 - 聯邦最高執政官"]
BLOOD_TYPES = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", "Q-Quantum Positive"]

# ==================== 核心系統類別 ====================
class AsianFederationGovSystem:
    def __init__(self, db_filename="raf_citizens_db.json", config_filename="raf_config.json"):
        self.db_filename = db_filename
        self.config_filename = config_filename
        self.citizens = self.load_database()
        self.current_theme_id = self.load_config().get("theme", "1")
        self.theme = THEMES.get(self.current_theme_id, THEMES["1"])

    def load_config(self):
        if os.path.exists(self.config_filename):
            try:
                with open(self.config_filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_config(self):
        with open(self.config_filename, 'w', encoding='utf-8') as f:
            json.dump({"theme": self.current_theme_id}, f, ensure_ascii=False, indent=4)

    def load_database(self):
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    def save_database(self):
        with open(self.db_filename, 'w', encoding='utf-8') as f:
            json.dump(self.citizens, f, ensure_ascii=False, indent=4)

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        T = self.theme
        banner = f"""
{T['BORDER']}{T['PRIMARY']}
=========================================================================================
 🏛️  亞 洲 聯 邦 共 和 國（ 亞 聯 ） ·  國 務 高 階 公 務 與 數 位 身 份 終 極 管 理 系 統  🏛️
      REPUBLIC OF ASIAN FEDERATION (RAF) - ULTIMATE STATE ENGINE v6.5
========================================================================================={T['RESET']}
{T['DIM']}當前主題: {T['name']}  |  系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  節點: 亞聯-NODE-ALPHA-9{T['RESET']}
        """
        print(banner)

    def switch_theme(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 🎨 亞聯介面視覺主題切換中心 ]{T['RESET']}\n")

        for key, t_data in THEMES.items():
            active_mark = f"{T['SUCCESS']} (使用中){T['RESET']}" if key == self.current_theme_id else ""
            print(f"  [{key}] {t_data['name']}{active_mark}")

        print("\n▶ 請選擇想要切換的外觀模式 (1-5): ", end="")
        choice = input().strip()

        if choice in THEMES:
            self.current_theme_id = choice
            self.theme = THEMES[choice]
            self.save_config()
            print(f"\n{self.theme['SUCCESS']}✅ 外觀模式已變更為：{self.theme['name']}{self.theme['RESET']}")
        else:
            print(f"\n{T['DANGER']}❌ 無效選擇，保持原有主題。{T['RESET']}")

        time.sleep(1.2)

    def generate_af_id(self, sector_code):
        year = datetime.now().year
        rand_digits = "".join([str(random.randint(0, 9)) for _ in range(6)])
        check_digit = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"RAF-{year}-{sector_code[:2].upper()}-{rand_digits}-{check_digit}"

    def generate_biometric_hash(self, name, af_id):
        raw_data = f"{name}:{af_id}:{time.time()}:{random.random()}"
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()[:24].upper()

    def generate_digital_signature(self, citizen_data):
        payload = f"{citizen_data['af_id']}|{citizen_data['name']}|{citizen_data['security_level']}"
        return hashlib.sha512(payload.encode('utf-8')).hexdigest()[:32].upper()

    def render_id_card(self, data):
        T = self.theme
        card = f"""
{T['BORDER']}+-----------------------------------------------------------------------------------------+
| {T['PRIMARY']}亞洲聯邦共和國（亞聯） 數位國家身份證 (REPUBLIC OF ASIAN FEDERATION DIGITAL ID){T['RESET']}{T['BORDER']}      |
+-----------------------------------------------------------------------------------------+
|  {T['ACCENT']}照片 / 判讀標籤{T['BORDER']}  |  【姓名】: {data['name']:<12}   【亞聯編號】: {T['SUCCESS']}{data['af_id']}{T['BORDER']}
|   [ 亞聯圖騰 ]   |  【性別/年齡】: M/F ({data['age']}歲)    【血型】: {data['blood_type']}
|   [  📸  ]     |  【所屬分區】: {data['sector']}
|   [  BIO-OK ]   |  【公務職務】: {data['occupation']}
|                 |  【安全等級】: {T['PRIMARY']}{data['security_level']}{T['BORDER']}  【社會評級】: {T['SUCCESS']}{data['civic_score']} 分{T['BORDER']}
+-----------------------------------------------------------------------------------------+
|  【DNA 雜湊特徵】: {data['biometric_hash']}
|  【核發日期】: {data['issue_date']}      【有效期限】: {data['expiry_date']}
|  【防偽數位簽章】: {data['digital_signature'][:24]}... [VERIFIED]
+-----------------------------------------------------------------------------------------+{T['RESET']}
        """
        print(card)

    def register_new_citizen(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 📝 自動化亞聯新公民身份申辦簽發 ]{T['RESET']}\n")

        name = input("▶ 請輸入公民姓名 (Name): ").strip()
        if not name:
            print(f"{T['DANGER']}❌ 姓名不可為空！操作取消。{T['RESET']}")
            time.sleep(1.5)
            return

        age_str = input("▶ 請輸入年齡 (Age): ").strip()
        age = int(age_str) if age_str.isdigit() else random.randint(18, 65)

        print("\n▶ 請選擇所屬自治行政區 (Federation Sector):")
        for idx, sector in enumerate(FEDERAL_SECTORS, 1):
            print(f"  [{idx}] {sector}")
        sector_idx = input("請選擇 (預設 1): ").strip()
        sector_idx = int(sector_idx) - 1 if sector_idx.isdigit() and 1 <= int(sector_idx) <= len(FEDERAL_SECTORS) else 0
        sector = FEDERAL_SECTORS[sector_idx]

        occupation = input("\n▶ 請輸入公務或社會職務 (Occupation): ").strip() or "亞聯自由公民"

        print(f"\n{T['BORDER']}⚡ 正在連接亞聯量子中央伺服器，分配 DNA 雜湊與社會信用評級...{T['RESET']}")
        time.sleep(1)

        af_id = self.generate_af_id(f"S{sector_idx+1}")
        bio_hash = self.generate_biometric_hash(name, af_id)
        civic_score = random.randint(650, 950)
        security_level = SECURITY_LEVELS[0] if civic_score < 800 else (SECURITY_LEVELS[1] if civic_score < 900 else SECURITY_LEVELS[2])
        blood_type = random.choice(BLOOD_TYPES)
        issue_date = datetime.now().strftime("%Y-%m-%d")
        expiry_date = (datetime.now() + timedelta(days=3650)).strftime("%Y-%m-%d")

        citizen_record = {
            "af_id": af_id, "name": name, "age": age, "sector": sector,
            "occupation": occupation, "security_level": security_level,
            "civic_score": civic_score, "blood_type": blood_type,
            "biometric_hash": bio_hash, "issue_date": issue_date,
            "expiry_date": expiry_date, "status": "ACTIVE (合法有效)"
        }

        citizen_record["digital_signature"] = self.generate_digital_signature(citizen_record)
        self.citizens[af_id] = citizen_record
        self.save_database()

        print(f"{T['SUCCESS']}✅ 身份註冊成功！已歸檔至亞聯中央資料庫。{T['RESET']}\n")
        self.render_id_card(citizen_record)
        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def search_citizen(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 🔍 亞聯國家情報與公民數據查詢系統 ]{T['RESET']}\n")

        query = input("▶ 請輸入查詢關鍵字 (姓名 或 AF-ID 編號): ").strip()
        if not query:
            return

        found = [data for af_id, data in self.citizens.items() if query.lower() in af_id.lower() or query.lower() in data['name'].lower()]

        if not found:
            print(f"\n{T['DANGER']}⚠️ 未能找到符合條件的亞聯公民紀錄。{T['RESET']}")
        else:
            print(f"\n{T['SUCCESS']}🎯 找到 {len(found)} 筆相符紀錄：{T['RESET']}\n")
            for citizen in found:
                self.render_id_card(citizen)

        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def verify_document_integrity(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 🛡 亞聯公務證件防偽與數位簽章驗證中心 ]{T['RESET']}\n")

        af_id = input("▶ 請輸入要驗證的亞聯 AF-ID: ").strip()
        if af_id not in self.citizens:
            print(f"\n{T['DANGER']}❌ 查無此 AF-ID，系統判定為未知或偽造證件！{T['RESET']}")
            time.sleep(2)
            return

        citizen = self.citizens[af_id]
        print(f"\n{T['BORDER']}⏳ 正在比對亞聯中央資料庫 SHA-512 金鑰與物理特徵...{T['RESET']}")
        time.sleep(1)

        expected_sig = self.generate_digital_signature(citizen)
        if citizen.get("digital_signature") == expected_sig:
            print(f"\n{T['SUCCESS']}✅ 驗證成功！該證件為「亞洲聯邦共和國（亞聯）國務院」官方核發，資料完好無竄改。{T['RESET']}")
            print(f"{T['DIM']}簽章雜湊: {expected_sig}{T['RESET']}")
        else:
            print(f"\n{T['DANGER']}🚨 警報！數位簽章不吻合，該證件已被非法竄改！{T['RESET']}")

        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def federal_resource_simulation(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ ⚙️ 亞聯資源調度與 AI 決策系統 ]{T['RESET']}\n")

        total_gdp = random.randint(18000, 25000)
        energy_capacity = random.randint(88, 99)

        print(f"📊 {T['PRIMARY']}亞聯整體即時總覽：{T['RESET']}")
        print(f" • 亞聯預估 GDP: {T['SUCCESS']}${total_gdp}0 億聯邦幣{T['RESET']}")
        print(f" • 清潔能源網覆蓋率: {T['BORDER']}{energy_capacity}%{T['RESET']}")
        print(f" • 登記總公民數: {T['ACCENT']}{len(self.citizens)} 人{T['RESET']}\n")

        print("-" * 65)
        print(f"{'行政分區':<32} | {'區域能源配給':<12} | {'治安狀態'}")
        print("-" * 65)
        for sector in FEDERAL_SECTORS:
            energy = f"{random.randint(90, 100)}%"
            print(f"{sector:<30} | {energy:<12} | {T['SUCCESS']}高度優化{T['RESET']}")
        print("-" * 65)

        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def issue_diplomatic_pass(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 📜 簽發亞聯最高外交豁免與公務通行證 ]{T['RESET']}\n")

        af_id = input("▶ 請輸入被授權官員/公民之 AF-ID: ").strip()
        if af_id not in self.citizens:
            print(f"{T['DANGER']}❌ 查無此公民，無法簽發外交通行證。{T['RESET']}")
            time.sleep(1.5)
            return

        citizen = self.citizens[af_id]
        pass_code = f"DIP-{random.randint(1000,9999)}-{datetime.now().strftime('%Y%m%d')}"

        document = f"""
{T['PRIMARY']}========================================================================================
 🏛️  亞 洲 聯 邦 共 和 國（ 亞 聯 ） ·  外 交 豁 免 與 高 階 通 行 許 可 證
 OFFICIAL DIPLOMATIC IMMUNITY & CLEARANCE PASS
========================================================================================{T['RESET']}
【通行證字號】: {T['ACCENT']}{pass_code}{T['RESET']}
【持證人】: {citizen['name']}  ({citizen['af_id']})
【官方職務】: {citizen['occupation']}
【安全簽發層級】: {citizen['security_level']}
【權利聲明】: 茲證明持證人代表亞洲聯邦共和國（亞聯）執行最高國務公務，
             於亞聯全境及盟國特區內享有全額通行、外交豁免與最高等級通關特權。

【核發機關】: 亞洲聯邦共和國（亞聯）國務院外務總署 (RAF Department of State)
========================================================================================
        """
        print(document)

        file_name = f"Pass_{citizen['name']}_{pass_code}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(document)
        print(f"{T['SUCCESS']}✅ 外交通行證已寫入並匯出為本地文件: {file_name}{T['RESET']}")

        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def run(self):
        while True:
            self.print_banner()
            T = self.theme
            print(f"{T['PRIMARY']}【 系統核心功能選單 】{T['RESET']}\n")
            print(f"  {T['SUCCESS']}[1]{T['RESET']} 📝 申辦/自動生成 亞聯數位公民身份證")
            print(f"  {T['SUCCESS']}[2]{T['RESET']} 🔍 檢索亞聯公民資料庫與數位證件")
            print(f"  {T['SUCCESS']}[3]{T['RESET']} 🛡️ 驗證證件數位簽章與防偽金鑰")
            print(f"  {T['SUCCESS']}[4]{T['RESET']} ⚙️ 檢視亞聯國家資源調度與 AI 決策狀態")
            print(f"  {T['SUCCESS']}[5]{T['RESET']} 📜 自動簽發亞聯外交豁免通行許可")
            print(f"  {T['ACCENT']}[6]{T['RESET']} 🎨 視覺外觀主題模式切換 (Switch UI Theme)")
            print(f"  {T['DANGER']}[0]{T['RESET']} 🚪 退出亞聯國務公務系統\n")

            choice = input(f"{T['PRIMARY']}請選擇國務操作項目 (0-6): {T['RESET']}").strip()

            if choice == '1':
                self.register_new_citizen()
            elif choice == '2':
                self.search_citizen()
            elif choice == '3':
                self.verify_document_integrity()
            elif choice == '4':
                self.federal_resource_simulation()
            elif choice == '5':
                self.issue_diplomatic_pass()
            elif choice == '6':
                self.switch_theme()
            elif choice == '0':
                print(f"\n{T['BORDER']}感謝使用亞洲聯邦共和國（亞聯）國務公務系統。關閉安全通道...{T['RESET']}")
                sys.exit()

if __name__ == "__main__":
    app = AsianFederationGovSystem()
    app.run()
