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

@app.route("/crud", methods = ["POST"])
def add_pokemon():
    if not request.args.get("action"):
        return "Whaddya want me to do here?"
    
    if not request.get_json():
        return "Please use a valid Pokemon array."
    else:
        pokemon = request.get_json()
        try:
            action = request.args.get("action")
            if action == "add":
                with open("static/all_the_pokemon.json", "r") as pokedex:
                    pokedex_json = json.load(pokedex)
                with open("static/all_the_pokemon.json", "w") as pokedex:
                    pokedex_json.append(pokemon)
                    json.dump(pokedex_json, pokedex)
                return "Pokemon added to Pokedex."
                
            elif action == "delete":
                with open("static/all_the_pokemon.json", "r") as pokedex:
                    pokedex_json = json.load(pokedex)
                with open("static/all_the_pokemon.json", "w") as pokedex:
                    pokedex_json = [mon for mon in pokedex_json if mon["name"] != pokemon["name"]]
                    json.dump(pokedex_json, pokedex)
                return f"{pokemon['name']} deleted."
                        
            elif action == "edit":
                with open("static/all_the_pokemon.json", "r") as pokedex:
                    pokedex_json = json.load(pokedex)
                with open("static/all_the_pokemon.json", "w") as pokedex:
                    for mon in pokedex_json:
                        if pokemon["name"] == mon["name"]:
                            mon.update(pokemon)
                    json.dump(pokedex_json, pokedex)
                return f"{pokemon['name']} updated."
            else:
                return "Please choose a valid action: add, edit, or delete."

        except:
            return "Not much of a Pokemon trainer, are you?"

#Run app
if __name__ == "__main__":
    app.run(port=5000, debug = True)