from flask import Flask, json, render_template, request
from stores import Stores

app = Flask(__name__)
app.secret_key = "shhhhh"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/scrape", methods=["POST"])
def game_scrape():
    print("Incoming...")
    print(request.get_json())
    game_json = request.get_json()
    game_name = game_json["game_name"]
    prices = []
    game = Stores(game_name)
    prices.append(game.steam())
    prices.append(game.epic_games())
    prices.append(game.ubi_store())
    prices.append(game.fanatical())
    prices.append(game.green_man_gaming())
    prices.append(game.gamesplanet())     
    return json.dumps(prices)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")