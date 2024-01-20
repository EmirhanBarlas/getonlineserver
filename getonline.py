from flask import Flask, jsonify # Flask kütüphanesini kullanarak bir API oluşturmak için 
from flask_cors import CORS # Cross-Origin Resource Sharing (CORS) hatasını önlemek için
import requests # Sunucu API'sine istek göndermek için

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_online_players():
    server_ip = "mc.splendidnw.com" # Sunucu IP adresi
    server_port = 25565 # Sunucu portu

    active_players = get_active_players(server_ip, server_port) # Sunucudaki çevrimiçi oyuncu sayısını al
    if active_players is not None:
        return jsonify({
            "active_players": active_players, # Çevrimiçi oyuncu sayısı
            "is_online": active_players > 0, # Sunucu çevrimiçi mi?
            "max_players": active_players + 1 # Sunucuya girebilecek en fazla oyuncu sayısı
        })
    else:
        return jsonify({
            "error": "Sunucu çevrimiçi değil veya bir hata oluştu."
        })

def get_active_players(server_ip, server_port): # Sunucudaki çevrimiçi oyuncu sayısını al
    try:
        response = requests.get(f"https://api.mcsrvstat.us/2/{server_ip}:{server_port}") # Sunucu API'sine istek gönder 
        data = response.json() # Sunucu API'sinden gelen veriyi JSON olarak al
        if response.status_code == 200 and data["online"]: # Sunucu çevrimiçi mi?
            return data["players"]["online"] # Sunucudaki çevrimiçi oyuncu sayısını al
        else: 
            return None # Sunucu çevrimiçi değil veya bir hata oluştu
    except requests.exceptions.RequestException as e: # İstek gönderilirken bir hata oluştu
        print("Hata:", e) # Hata mesajını yazdır
        return None # Sunucu çevrimiçi değil veya bir hata oluştu

if __name__ == '__main__': 
    app.run() 
