import requests
import os
import sys

GITHUB_USER = "mustafaraca"
REPO_NAME = "my-updater"
BRANCH = "main"
APP_FILE_NAME = "app.py"
VERSION_FILE = "version.txt"
CURRENT_VERSION = "1.0.0"

BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USER}/{REPO_NAME}/{BRANCH}"

def url(file):
    return f"{BASE_URL}/{file}"

def get_text(link):
    return requests.get(link, timeout=5).text.strip()

def download(link):
    return requests.get(link, timeout=10).content

def restart():
    print("🔄 Yeniden başlatılıyor...")
    os.execv(sys.executable, [sys.executable, APP_FILE_NAME])

def backup():
    if os.path.exists(APP_FILE_NAME):
        os.replace(APP_FILE_NAME, APP_FILE_NAME + ".backup")

def restore():
    if os.path.exists(APP_FILE_NAME + ".backup"):
        os.replace(APP_FILE_NAME + ".backup", APP_FILE_NAME)

def update():
    try:
        print("🌐 Güncelleme kontrol ediliyor...")

        remote_version = get_text(url(VERSION_FILE))

        if remote_version == CURRENT_VERSION:
            print("✔ Güncel sürüm")
            return

        print(f"⬇ Yeni sürüm bulundu: {remote_version}")

        new_code = download(url(APP_FILE_NAME))

        backup()

        try:
            with open(APP_FILE_NAME, "wb") as f:
                f.write(new_code)
        except Exception as e:
            print("❌ Yazma hatası → geri yükleniyor")
            restore()
            return

        print("✔ Güncelleme tamamlandı")
        restart()

    except Exception as e:
        print(f"⚠ Güncelleme hatası: {e}")

if __name__ == "__main__":
    update()
    print("Program çalışıyor 🚀")
