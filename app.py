from flask import Flask, render_template, request
from stores import Stores

app = Flask(__name__)
app.secret_key = "shhhhh"

@app.route("/")
def index():
    return render_template("index.html")

def game_scraping():
    pass



if __name__ == "__main__":
    app.run(debug=True)