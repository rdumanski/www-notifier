import requests
from bs4 import BeautifulSoup
import time
import hashlib

# Konfiguracja
URL_TO_MONITOR = "https://przyklad.pl/promocje"
CHECK_INTERVAL = 60 # czas w sekundach (np. co minutę)

def get_page_hash():
    """Pobiera zawartość strony i tworzy jej 'odcisk palca' (hash)."""
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL_TO_MONITOR, headers=headers)
    
    # Wybieramy tekst, aby uniknąć fałszywych alarmów przez dynamiczne skrypty/reklamy
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Opcjonalnie: ogranicz się do konkretnego elementu, np. div o id="content"
    # content = soup.find("div", {"id": "content"}).text
    content = soup.get_text()
    
    return hashlib.sha256(content.encode('utf-8')).hexdigest()

def monitor():
    print("Rozpoczynam monitoring...")
    last_hash = get_page_hash()
    
    while True:
        try:
            time.sleep(CHECK_INTERVAL)
            current_hash = get_page_hash()
            
            if current_hash != last_hash:
                print(f"ALERTT! Strona uległa zmianie: {URL_TO_MONITOR}")
                last_hash = current_hash
                # Tutaj możesz dodać wysyłkę e-maila lub powiadomienie push
            else:
                print("Brak zmian...")
                
        except Exception as e:
            print(f"Wystąpił błąd: {e}")

if __name__ == "__main__":
    monitor()
