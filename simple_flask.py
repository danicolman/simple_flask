from flask import Flask, request

import json

app = Flask(__name__)

@app.route("/")
def hello():
    return "You are here."

@app.route("/get", methods = ["GET"])
def get():
    try:
        with open("static/all_the_pokemon.json") as pokemon:
            return json.load(pokemon)
    except:
        return "Nothing to see here.  Please try again."
    
@app.route("/get-paginated", methods = ["GET"])
def get_by_page():
    limit = request.args.get("limit", default = 20, type = int)
    page = request.args.get("page", default = 0, type = int)
    try:
        with open("static/all_the_pokemon.json", "r") as pokemon:
            pokemon = json.load(pokemon)
            if limit > len(pokemon):
                return "You are asking for more than the universe can give."
            elif page > len(pokemon) // limit:
                return "You tried long division.  It wasn't very effective."
            else:
                return pokemon[page*limit:(page+1)*limit]
    except:
        return "Dunno?"

    
#Run app
if __name__ == "__main__":
    app.run(port=5000, debug = True)