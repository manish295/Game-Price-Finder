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
    game_stores = game_json["stores"]
    prices = []
    game = Stores(game_name)
    for store in game_stores:
        if store == "Epic Games":
            prices.append(game.epic_games())
        if store == "Green Man Gaming":
            prices.append(game.green_man_gaming())
        if store == "Steam":
            prices.append(game.steam())
        if store == "Ubisoft":
            prices.append(game.ubi_store())
        if store == "Fanatical":
            prices.append(game.fanatical())  
        if store == "GamesPlanet":
            prices.append(game.gamesplanet())     
    return json.dumps(prices)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")