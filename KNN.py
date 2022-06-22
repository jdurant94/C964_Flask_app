import pandas as pd
import numpy as np
import matplotlib as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
import re
from scipy.sparse import csr_matrix

# import data
game_data_clean = pd.read_csv("game_data_clean.csv")
game_data_clean.rename(columns={'Unnamed: 0': 'gameid'}, inplace=True)

# simplify variable
game_data = game_data_clean

# concat and create metadata dataframe
game_metadata = pd.concat([pd.get_dummies(game_data_clean["developers"]),
                           pd.get_dummies(game_data_clean["publishers"]),
                           game_data_clean["genres"].str.get_dummies(', ')], axis=1)

game_data["titles"] = game_data["titles"].map(lambda titles: re.sub('[^A-Za-z0-9]+', " ", titles))

#   fit data to scaler

scaler = MinMaxScaler()
game_metadata = scaler.fit_transform(game_metadata)
np.round(game_metadata, 2)

# set up KNN

knn = NearestNeighbors(n_neighbors=20, algorithm='ball_tree').fit(game_metadata)
distances, indices = knn.kneighbors(game_metadata)


# Functions

def get_index_from_titles(title):
    return game_data[game_data["titles"] == title].index.tolist()[0]


all_game_titles = list(game_data.titles.values)

# spit out recs

def get_recs(query=None, id=None):
    if id:
        for id in indices[id][1:]:
            print(game_data["titles"][id])
    if query:
        found_id = get_index_from_titles(query)
        games_list = []
        for id in indices[found_id][1:]:
            # games_list. = game_data["titles"][id]
            games_list.append(game_data["titles"][id])
        return games_list


print("KNN is running")

