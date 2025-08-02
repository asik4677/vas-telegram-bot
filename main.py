import time
import requests
from bs4 import BeautifulSoup
from telegram import Bot

BOT_TOKEN = '7807393497:AAH3e95KJwthMTM8VvAyYp_MYJLDxzCl_pc'
GROUP_ID = -1002143117403

bot = Bot(token=BOT_TOKEN)

def detect_service(message):
    if "Facebook" in message or "FB-" in message:
        return "FACEBOOK"
    elif "WhatsApp" in message or "wa.me" in message:
        return "WHATSAPP"
    elif "Telegram" in message:
        return "TELEGRAM"
    return "UNKNOWN"

def detect_country(number):
    if number.startswith("225"): return "Côte d'Ivoire"
    elif number.startswith("51"): return "Peru"
    elif number.startswith("63"): return "Philippines"
    elif number.startswith("93"): return "Afghanistan"
    elif number.startswith("229"): return "Benin"
    elif number.startswith("84"): return "Vietnam"
    elif number.startswith("673"): return "Brunei"
    elif number.startswith("234"): return "Nigeria"
    elif number.startswith("44"): return "United Kingdom"
    elif number.startswith("1"): return "USA/Canada"
    elif number.startswith("880"): return "Bangladesh"
    elif number.startswith("91"): return "India"
    elif number.startswith("7"): return "Russia"
    elif number.startswith("62"): return "Indonesia"
    elif number.startswith("33"): return "France"
    elif number.startswith("20"): return "Egypt"
    elif number.startswith("974"): return "Qatar"
    elif number.startswith("90"): return "Turkey"
    elif number.startswith("30"): return "Greece"
    else: return "Unknown Country"

def scrape_otp():
    url = "https://www.ivasms.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.select("table tbody tr")
    
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 3: continue
        number = cols[0].text.strip()
        message = cols[2].text.strip()

        if not message or len(message) < 4: continue
        otp = ''.join([x for x in message if x.isdigit()][:6])
        service = detect_service(message)
        country = detect_country(number)

        text = f"""🔔 {country} {service} OTP Received...

⚙️ Service: {service}
🌐 Country: {country}
☎️ Number: {number}
🔑 Your OTP: {otp}

✉️ Full-Message:
{message}

👨‍💻 Developer: @asik_2_0_bd
"""
        bot.send_message(chat_id=GROUP_ID, text=text)
        time.sleep(1)

while True:
    try:
        scrape_otp()
    except Exception as e:
        print("Error:", e)
    time.sleep(10)
