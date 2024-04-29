# *************************************************************************************************************
# How to using this API
# *************************************************************************************************************
# Comments 1 : You need to have those file in model directory
# -- model/pokarate.py             (is this API file)
# -- model/pokedex.csv             (is the pokedex)
# -- model/pokemon_winner.mod      (is the IA model)
# -- model/encoder_pokemon.ec      (is the encoder the IA model need to work)
# -- model/pitch_data.py           (is a class the API need to work)
# *************************************************************************************************************
# Comments 2 : Actually the IA have difficulty to predict a 50/50% winner when the same pokemon are fighting
# The best way to
# *************************************************************************************************************
# import pokarate.py
#
# pokerate_model = Pokerate()
#
# poke_1 = 1
# poke_2 = 2
# prediction = pokerate_model.predict_battle(poke_1, poke_2) # Use Pokemon index (from pokedex)
#
# print(f"Pokemon 1 winning rate : {prediction[0, 0]:.2f}%")
# print(f"Pokemon 2 winning rate : {prediction[0, 1]:.2f}%")
#
# if prediction[0, 0] > prediction[0, 1]:
#     print(f"The winner is : {pokarate_model.get_poke_name(poke_1)}")
# else:
#     print(f"The winner is : {pokarate_model.get_poke_name(poke_2)}")
# *************************************************************************************************************

import pandas as pd
import numpy as np
import joblib
from model.pitch_class import Pitch

class Pokerate():
    pokedex = pd.read_csv('model/pokedex.csv')
    _pokedex_features = pokedex.drop(columns=['Name', 'Generation', 'Legendary'])
    _model = joblib.load('model/pokemon_winner.mod')

    def __init__(self):
        self.pitcher = Pitch()
        self.pitcher.load('model/encoder_pokemon.ec')

    def _prepare_data(self, poke_1, poke_2):
        combats = pd.DataFrame({'First_pokemon': [poke_1], 'Second_pokemon' : [poke_2]})

        train_df = combats.merge(self._pokedex_features, left_on='First_pokemon', right_on='#', suffixes=('', '_1'))
        train_df = train_df.merge(self._pokedex_features, left_on='Second_pokemon', right_on='#', suffixes=('_1', '_2'))

        train_df = train_df.drop(columns=['First_pokemon', 'Second_pokemon', '#_1', '#_2'])

        encoded_data = self.pitcher.encode(train_df)

        prepared_data = self.pitcher.pitch_data(encoded_data)

        return prepared_data

    def predict_battle(self, pokemon_index_1:int, pokemon_index_2:int) -> np.array:
        battle_data = self._prepare_data(pokemon_index_1, pokemon_index_2)
        prediction = self._model.predict_proba(battle_data)

        return prediction

    def get_poke_name(self, index_poke:int) -> pd.DataFrame:
        return self.pokedex[self.pokedex['#'] == index_poke]['Name'].item()

    def get_poke_stats(self, index_poke) -> pd.DataFrame:
        return self.pokedex[self.pokedex['#'] == index_poke]
