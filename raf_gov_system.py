#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
亞洲聯邦共和國（簡稱：亞聯 / RAF）
國務公務與公民數位身份管理系統 v8.0 (Pure Standard Library Version)
"""

import hashlib
import json
import os
import random
import sys
import time
from datetime import datetime, timedelta

THEMES = {
    "1": {"name": "⚡ 賽博霓虹", "PRIMARY": "\033[95m\033[1m", "BORDER": "\033[96m", "ACCENT": "\033[93m", "SUCCESS": "\033[92m", "DANGER": "\033[91m", "DIM": "\033[90m", "RESET": "\033[0m"},
    "2": {"name": "🟢 駭客矩陣", "PRIMARY": "\033[92m\033[1m", "BORDER": "\033[32m", "ACCENT": "\033[97m", "SUCCESS": "\033[92m", "DANGER": "\033[91m", "DIM": "\033[32m\033[2m", "RESET": "\033[0m"},
    "3": {"name": "👑 帝國尊榮", "PRIMARY": "\033[93m\033[1m", "BORDER": "\033[33m", "ACCENT": "\033[96m", "SUCCESS": "\033[92m", "DANGER": "\033[91m", "DIM": "\033[90m", "RESET": "\033[0m"},
    "4": {"name": "🌊 深海戰術", "PRIMARY": "\033[94m\033[1m", "BORDER": "\033[96m", "ACCENT": "\033[93m", "SUCCESS": "\033[92m", "DANGER": "\033[91m", "DIM": "\033[34m", "RESET": "\033[0m"},
    "5": {"name": "🕶️ 隱形特務", "PRIMARY": "\033[97m\033[1m", "BORDER": "\033[90m", "ACCENT": "\033[37m", "SUCCESS": "\033[97m", "DANGER": "\033[91m", "DIM": "\033[2m", "RESET": "\033[0m"}
}

FEDERAL_SECTORS = [
    "亞聯東亞核心行政區 (East Core Sector)",
    "亞聯東南亞高新特區 (ASEAN High-Tech Zone)",
    "亞聯南亞量子研發特區 (South Quantum Zone)",
    "亞聯中亞清潔能源特區 (Central Energy Hub)",
    "亞聯太平洋海空戰略區 (Pacific Aero-Marine Sector)"
]

SECURITY_LEVELS = ["Level 1 - 普通公民", "Level 2 - 公務執行員", "Level 3 - 行政資深官", "Level 4 - 國務部長", "Level 5 - 聯邦最高執政官"]

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
            except Exception: return {}
        return {}

    def save_config(self):
        with open(self.config_filename, 'w', encoding='utf-8') as f:
            json.dump({"theme": self.current_theme_id}, f, ensure_ascii=False, indent=4)

    def load_database(self):
        if os.path.exists(self.db_filename):
            try:
                with open(self.db_filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception: return {}
        return {}

    def save_database(self):
        with open(self.db_filename, 'w', encoding='utf-8') as f:
            json.dump(self.citizens, f, ensure_ascii=False, indent=4)

    def print_banner(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        T = self.theme
        print(f"""{T['BORDER']}{T['PRIMARY']}
=========================================================================================
 🏛️  亞 洲 聯 邦 共 和 國（ 亞 聯 ） ·  國 務 高 階 公 務 與 數 位 身 份 終 極 管 理 系 統  🏛️
      REPUBLIC OF ASIAN FEDERATION (RAF) - ULTIMATE STATE ENGINE v8.0
========================================================================================={T['RESET']}
{T['DIM']}當前主題: {T['name']}  |  系統時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  |  節點: 亞聯-NODE-ALPHA-9{T['RESET']}""")

    def switch_theme(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 🎨 亞聯介面視覺主題切換中心 ]{T['RESET']}\n")
        for key, t_data in THEMES.items():
            mark = f"{T['SUCCESS']} (使用中){T['RESET']}" if key == self.current_theme_id else ""
            print(f"  [{key}] {t_data['name']}{mark}")
        choice = input("\n▶ 請選擇主題 (1-5): ").strip()
        if choice in THEMES:
            self.current_theme_id = choice
            self.theme = THEMES[choice]
            self.save_config()
            print(f"\n{self.theme['SUCCESS']}✅ 外觀模式已變更！{self.theme['RESET']}")
        time.sleep(1)

    def generate_af_id(self, sector_code):
        year = datetime.now().year
        rand_digits = "".join([str(random.randint(0, 9)) for _ in range(6)])
        check_digit = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        return f"RAF-{year}-{sector_code[:2].upper()}-{rand_digits}-{check_digit}"

    def generate_digital_signature(self, citizen_data):
        payload = f"{citizen_data['af_id']}|{citizen_data['name']}|{citizen_data['security_level']}"
        return hashlib.sha512(payload.encode('utf-8')).hexdigest()[:32].upper()

    def render_id_card(self, data):
        T = self.theme
        print(f"""
{T['BORDER']}+-----------------------------------------------------------------------------------------+
| {T['PRIMARY']}亞洲聯邦共和國（亞聯） 數位國家身份證 (REPUBLIC OF ASIAN FEDERATION DIGITAL ID){T['RESET']}{T['BORDER']}      |
+-----------------------------------------------------------------------------------------+
|  {T['ACCENT']}照片判讀標籤{T['BORDER']}   |  【姓名】: {data['name']:<12}   【亞聯編號】: {T['SUCCESS']}{data['af_id']}{T['BORDER']}
|   [ 亞聯圖騰 ]   |  【性別/年齡】: M/F ({data['age']}歲)    【血型】: {data['blood_type']}
|   [  📸  ]     |  【所屬分區】: {data['sector']}
|   [  BIO-OK ]   |  【公務職務】: {data['occupation']}
|                 |  【安全等級】: {T['PRIMARY']}{data['security_level']}{T['BORDER']}  【社會評級】: {T['SUCCESS']}{data['civic_score']} 分{T['BORDER']}
+-----------------------------------------------------------------------------------------+
|  【DNA 雜湊特徵】: {data['biometric_hash']}
|  【防偽數位簽章】: {data['digital_signature'][:24]}... [VERIFIED]
+-----------------------------------------------------------------------------------------+{T['RESET']}""")

    def register_new_citizen(self):
        self.print_banner()
        T = self.theme
        print(f"{T['ACCENT']}[ 📝 自動化亞聯新公民身份申辦簽發 ]{T['RESET']}\n")
        name = input("▶ 請輸入公民姓名 (Name): ").strip()
        if not name: return
        age = int(input("▶ 請輸入年齡: ").strip() or "25")
        for idx, sector in enumerate(FEDERAL_SECTORS, 1):
            print(f"  [{idx}] {sector}")
        sector_idx = int(input("請選擇分區 (1-5): ").strip() or "1") - 1
        occupation = input("▶ 請輸入職務: ").strip() or "亞聯自由公民"

        af_id = self.generate_af_id(f"S{sector_idx+1}")
        civic_score = random.randint(680, 950)
        sec_level = SECURITY_LEVELS[0] if civic_score < 800 else (SECURITY_LEVELS[1] if civic_score < 900 else SECURITY_LEVELS[2])
        bio_hash = hashlib.sha256(f"{name}:{af_id}:{time.time()}".encode()).hexdigest()[:24].upper()

        record = {
            "af_id": af_id, "name": name, "age": age, "sector": FEDERAL_SECTORS[sector_idx],
            "occupation": occupation, "security_level": sec_level, "civic_score": civic_score,
            "blood_type": "Q-Quantum Positive", "biometric_hash": bio_hash,
            "issue_date": datetime.now().strftime("%Y-%m-%d"), "expiry_date": "2036-10-02"
        }
        record["digital_signature"] = self.generate_digital_signature(record)
        self.citizens[af_id] = record
        self.save_database()

        print(f"\n{T['SUCCESS']}✅ 成功歸檔至亞聯中央資料庫 (raf_citizens_db.json)。{T['RESET']}")
        self.render_id_card(record)
        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def search_citizen(self):
        self.print_banner()
        T = self.theme
        q = input("▶ 請輸入關鍵字 (姓名/AF-ID): ").strip().lower()
        found = [data for af_id, data in self.citizens.items() if q in af_id.lower() or q in data['name'].lower()]
        for c in found: self.render_id_card(c)
        input(f"\n{T['DIM']}按下 Enter 鍵返回主選單...{T['RESET']}")

    def run(self):
        while True:
            self.print_banner()
            T = self.theme
            print(f"  {T['SUCCESS']}[1]{T['RESET']} 📝 申辦亞聯數位公民身份證")
            print(f"  {T['SUCCESS']}[2]{T['RESET']} 🔍 檢索國家公民情報資料庫")
            print(f"  {T['ACCENT']}[3]{T['RESET']} 🎨 視覺主題模式切換")
            print(f"  {T['DANGER']}[0]{T['RESET']} 🚪 退出系統\n")
            choice = input(f"{T['PRIMARY']}請選擇項目 (0-3): {T['RESET']}").strip()
            if choice == '1': self.register_new_citizen()
            elif choice == '2': self.search_citizen()
            elif choice == '3': self.switch_theme()
            elif choice == '0': sys.exit()

if __name__ == "__main__":
    AsianFederationGovSystem().run()
