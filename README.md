# pokemon_battle
Prédiction du vainqueur lors d'une bataille Pokemon avec SkLearn.<br />
<img width="1286" alt="Capture d’écran 2024-04-29 à 12 04 59" src="https://github.com/PlomteuxKevin/pokemon_battle/assets/168406292/5860e082-a56b-4721-acf6-f8c8bd1cdad1">


## Objectif du projet

Ce projet à été trouvé sur Kaggle : <a href="https://www.kaggle.com/datasets/terminus7/pokemon-challenge/">https://www.kaggle.com/datasets/terminus7/pokemon-challenge/</a><br />
<br />
Je ne suis pas un grand fan de Pokemon, mais il faut avoué que j'ai grandi avec. Je cherchais un projet fun où je pourrais mettre en application mes connaissances en python et en Machine Learning.<br />
C'est tout naturellement quand je suis tombé sur ce projet sur Kaggle que je me suis dit : "pourquoi pas ?".

## Déroulement du projet
### Analyse des données et création du model
Le fichier [model.ipynb](model/model.ipynb) contient toute l'analyse des données et la création du model.

### Server (Flask)
[server.py](model/server.py) est le fichier principale du projet pour l'utilisation du model. C'est un server Flash utilisant l'API [model/pokarate.py](model/pokarate.py) afin de faire tourner le model et ainsi prédire le résultat des combats.

### API
[model/pokarate.py](model/pokarate.py) contient l'API permettant d'utiliser le model.<br />
**predict_battle :** est la fonction donnant les pourcentages de victoire entre deux Pokemon.<br />
**get_poke_name :** retourne le nom du pokemon à partir de son ID.<br />
**get_poke_stats :** retour un tuple avec toutes les stats du Pokemon à partir de son ID.

## Résultat
Les premiers résultats obtenus n'étaient pas concluant. Le model mis en place prédisait parfois très bien, parfois très mal sans vraiment de logique : un pokémon de type "Foudre" pouvait avoir 100% de chance de battre un type "Roche".<br />
Après plusieurs heures passée afin d'optimiser le model je me suis rendu compte que le problème venait en réalité du dataset d'entrainement.<br />
C'est alors que j'ai compris que les données trouvées sur Kaggle représentaient les combats dans le Dessin Animé Pokémon et non le jeux vidéo ou le jeu de carte.<br />
<br />
J'en suis venu à la conclusion que le model que j'ai créé est bon ! C'est jusque que ce projet ne permettra pas à un joueur de Pokemon (jeu ou carte) de prédire le taux de victoire de ses Pokemon, mais plutôt à quelqu'un qui aurait raté des épisodes du dessin animé de connaitre le résultat d'une recontre avant d'avoir vu l'épisode.<br />
<br />
Néans moins ce projet m'a beaucoup appris, surtout l'imbrication des différents éléments d'un projet de Data Science, de l'analyse des données, en passant par la création du model et de l'API, jusqu'au produit final à destination des utilisateurs.
