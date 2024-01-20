from flask import Flask, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/')
def get_online_players():
    server_ip = "mc.splendidnw.com"
    server_port = 25565

    active_players = get_active_players(server_ip, server_port)
    if active_players is not None:
        return jsonify({
            "active_players": active_players,
            "is_online": active_players > 0,
            "max_players": active_players + 1
        })
    else:
        return jsonify({
            "error": "Sunucu çevrimiçi değil veya bir hata oluştu."
        })

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

if __name__ == '__main__':
    app.run()
