from flask import Flask, render_template, request
import random

app = Flask(__name__)

GAMES = {
    "大樂透": (1, 49, 6),
    "今彩539": (1, 39, 5),
    "powerball": (1, 69, 5)  # 這裡可以加入更多遊戲
}

@app.route("/", methods=["GET", "POST"])
def index():
    numbers = []
    game = request.form.get("game")
    if request.method == "POST" and game in GAMES:
        start, end, count = GAMES[game]
        numbers = random.sample(range(start, end + 1), count)
    return render_template("index.html", games=GAMES.keys(), numbers=numbers)

if __name__ == "__main__":
    app.run(debug=True)
