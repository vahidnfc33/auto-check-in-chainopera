import requests
import time
import os
from datetime import datetime, timedelta, timezone

def read_token():
    try:
        with open("token.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("❌ File token.txt tidak ditemukan!")
        exit()

def get_headers(auth_token):
    return {
        "authority": "chat.chainopera.ai",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "origin": "https://chat.chainopera.ai",
        "referer": "https://chat.chainopera.ai/chat/5V6HlurJky2235ro",
        "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "cookie": f"auth_token={auth_token}"
    }

def check_in(headers):
    url = "https://chat.chainopera.ai/api/agent/ai-terminal-check-in"
    try:
        resp = requests.post(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("checkIn"):
                print("✅ Check-in berhasil!")
            else:
                print("ℹ️ Sudah check-in sebelumnya.")
            print("Response:", data)
        else:
            print("❌ Gagal check-in:", resp.status_code)
    except Exception as e:
        print("❌ Error saat check-in:", e)

def get_points(headers):
    url = "https://chat.chainopera.ai/api/agent/ai-terminal-points"
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            total_points = data.get("totalPoints", 0)
            print(f"🏆 Total poin kamu sekarang: {total_points}")
        else:
            print("❌ Gagal ambil poin:", resp.status_code)
    except Exception as e:
        print("❌ Error saat ambil poin:", e)

def countdown_to_next_run(next_run):
    while datetime.now(timezone.utc) < next_run:
        remaining = next_run - datetime.now(timezone.utc)
        hours, remainder = divmod(int(remaining.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        time_str = f"{hours:02}:{minutes:02}:{seconds:02}"
        print(f"⏳ Next execution in: {time_str}", end='\r')
        time.sleep(1)

def main():
    print("=== ChainOpera Auto Check-in Harian ===")
    auth_token = read_token()
    headers = get_headers(auth_token)

    while True:
        now = datetime.now(timezone.utc)
        print(f"\n🕒 Eksekusi pada: {now.strftime('%Y-%m-%d %H:%M:%S')} UTC")

        check_in(headers)
        get_points(headers)

        next_run = now + timedelta(days=1)
        countdown_to_next_run(next_run)

if __name__ == "__main__":
    main()
