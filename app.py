from flask import Flask, render_template, request
import random

app = Flask(__name__)

GAMES = {
    "大樂透": (1, 49, 6),
    "今彩 539": (1, 39, 5),
    "四星彩": (0, 9, 4),
    "三星彩": (0, 9, 3),
    "威力彩": (1, 38, 5),
    "bingo 五星": (1, 80, 5)  # 這裡可以加入更多遊戲
}

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
    app.run(host='0.0.0.0', port=5000, debug=True)
