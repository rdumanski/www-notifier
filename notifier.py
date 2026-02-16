import requests
import time
import hashlib
from bs4 import BeautifulSoup

# --- CONFIGURATION ---
URL_TO_MONITOR = "https://www.prezydent.pl/prawo/ustawy-podpisane/ustawy-podpisane-w-lutym-2026-r,114968"
# Pick a very random name so others don't "guess" your notifications
TOPIC_NAME = "monitor_zmian_xyz_9988" 
NTFY_URL = f"https://ntfy.sh/podpis"
CHECK_INTERVAL = 300  # 10 minutes

def send_notification(message):
    """Sends a push notification without any passwords."""
    try:
        requests.post(NTFY_URL, 
                      data=message.encode('utf-8'),
                      headers={
                          "Title": "Zmiana na stronie!",
                          "Priority": "high",
                          "Tags": "bell,warning"
                      })
    except Exception as e:
        print(f"Błąd powiadomienia: {e}")

def get_page_hash():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL_TO_MONITOR, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    # Monitor only the text to avoid hidden code changes
    content = soup.get_text()
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def monitor():
    print(f"Monitoring... Subskrybuj temat 'podpis' w aplikacji ntfy.")
    send_notification("Monitor uruchomiony pomyślnie!")
    
    try:
        last_hash = get_page_hash()
    except:
        return

    while True:
        time.sleep(CHECK_INTERVAL)
        try:
            current_hash = get_page_hash()
            if current_hash != last_hash:
                send_notification(f"Wykryto zmianę na: {URL_TO_MONITOR}")
                last_hash = current_hash
        except Exception as e:
            print(f"Błąd: {e}")

if __name__ == "__main__":
    monitor()
