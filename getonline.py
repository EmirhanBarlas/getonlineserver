import requests

def get_active_players(server_ip, server_port):
    try:
        response = requests.get(f"https://api.mcsrvstat.us/2/{server_ip}:{server_port}")
        data = response.json()
        if response.status_code == 200 and data["online"]:
            return data["players"]["online"]
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("Hata:", e)
        return None

server_ip = "mc.splendidnw.com"
server_port = 25565

active_players = get_active_players(server_ip, server_port)
if active_players is not None:
    print(f"Aktif oyuncu sayısı: {active_players}/{active_players + 1}")
    print(f"Sunucu çevrimiçi: {active_players > 0}")
else:
    print("Sunucu çevrimiçi değil veya bir hata oluştu.")
