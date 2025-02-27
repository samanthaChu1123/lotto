from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

GAMES = {
    "大樂透": (1, 49, 6),
    "今彩 539": (1, 39, 5),
    "四星彩": (0, 9, 4),
    "三星彩": (0, 9, 3),
    "威力彩": (1, 38, 5),
}

import subprocess
import hmac
import hashlib

SECRET = "lottoserver123"  # 這要跟 GitHub 設定的 Secret 一樣

@app.route("/github-webhook", methods=["POST"])
def github_webhook():
    # 驗證 GitHub 的 Secret
    signature = request.headers.get("X-Hub-Signature-256")
    payload = request.get_data()
    expected_signature = "sha256=" + hmac.new(SECRET.encode(), payload, hashlib.sha256).hexdigest()
    
    if not hmac.compare_digest(expected_signature, signature):
        return jsonify({"message": "Invalid signature"}), 403

    # 執行 git pull
    try:
        subprocess.run(["git", "pull"], cwd="/home/ubuntu/lotto", check=True)
        subprocess.run(["sudo", "systemctl", "restart", "lotto"])  # 重新啟動 Flask 服務
        return jsonify({"message": "Updated successfully!"}), 200
    except subprocess.CalledProcessError as e:
        return jsonify({"message": "Update failed!", "error": str(e)}), 500

@app.route("/", methods=["GET", "POST"])
def index():
    numbers = []
    game = request.form.get("game")

    if request.method == "POST" and game in GAMES:
        start, end, count = GAMES[game]
        numbers = random.sample(range(start, end + 1), count)
        
        if game == "威力彩":
            second_zone = random.choice(range(1, 9))  # 第二區隨機選 1~8
            numbers.append(second_zone)

    return render_template("index.html", games=GAMES.keys(), numbers=numbers, game=game)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
