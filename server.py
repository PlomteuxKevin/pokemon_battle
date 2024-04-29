import pandas as pd
import numpy as np

from model.pokerate import Pokerate

from model.pitch_class import Pitch as pt

from flask import Flask, render_template, jsonify, request
from joblib import load
from sklearn.linear_model import LogisticRegression

app = Flask('')

pokerate_model = Pokerate()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/byPokemon')
def byPokemon():
    return render_template('byPokemon.html')

@app.route('/byPokemon', methods=['POST'])
def fight_by_pokemon():
    data = request.get_json()
    index_poke1, name_poke1 = data['pokemon1'].split(sep=" - ")
    index_poke2, name_poke2 = data['pokemon2'].split(sep=" - ")

    index_poke1 = int(index_poke1)
    index_poke2 = int(index_poke2)

    proba_poke1, proba_poke2, winner_name = predict(index_poke1, index_poke2)

    response_data = {
        "poke1_proba" : f"{proba_poke1:.2f}",
        "poke2_proba" : f"{proba_poke2:.2f}",
        "winner_name" : winner_name
    }

    return jsonify(response_data)

@app.route('/byTeam')
def byTeam():
    return render_template('byTeam.html')

@app.route('/pokedex')
def get_pokedex():
    df = Pokerate.pokedex

    pokemons = []
    for _, row in df.iterrows():
        number = str(row['#']).zfill(3)  # formatte le nombre sur 3 chiffres
        name = row['Name']
        pokemons.append(f"{number} - {name}")

    return jsonify(pokemons)

@app.route('/pokemonStats')
def get_pokemon_stats():
    poke_index = request.args.get('index')
    stats = pokerate_model.get_poke_stats(int(poke_index)).to_dict()

    dict = {
        'HP' : list(stats['HP'].values())[0],
        'Type 1' : list(stats['Type 1'].values())[0],
        'Type 2' : list(stats['Type 2'].values())[0],
        'Attack' : list(stats['Attack'].values())[0],
        'Defense' : list(stats['Defense'].values())[0],
        'Sp. Atk' : list(stats['Sp. Atk'].values())[0],
        'Sp. Def' : list(stats['Sp. Def'].values())[0],
        'Speed' : list(stats['Speed'].values())[0],
        'Generation' : list(stats['Generation'].values())[0],
        'Legendary' : list(stats['Legendary'].values())[0]
    }

    return jsonify(dict)

def predict(poke_1, poke_2):
    # if it's the same pokemon, do not use the IA prediction model
    if poke_1 == poke_2:
        return 0.5, 0.5, "It's a Tie!"

    # if pokemon are different, use the IA prediction model
    else:
        prediction = pokerate_model.predict_battle(poke_1, poke_2) # Use Pokemon index (from pokedex)

        if prediction[0, 0] > prediction[0, 1]:
            return prediction[0, 0], prediction[0, 1], pokerate_model.get_poke_name(poke_1)
        else:
            return prediction[0, 0], prediction[0, 1], pokerate_model.get_poke_name(poke_2)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
