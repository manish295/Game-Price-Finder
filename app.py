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
        layout = {"store": store}
        if store == "Epic Games":
            layout = {**layout, **game.epic_games()} 
        if store == "Humble Store":
            layout = {**layout, **game.humble_store()} 
        if store == "Steam":
            layout = {**layout, **game.steam()} 
        if store == "Ubisoft":
            layout = {**layout, **game.ubi_store()} 
        if store == "Fanatical":
            layout = {**layout, **game.fanatical()}        
        prices.append(layout)
    game.shut_down()
    return json.dumps(prices)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")