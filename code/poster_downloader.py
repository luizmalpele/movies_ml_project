import pandas as pd

movie_poster_db = pd.read_csv("../data/Movie_posterURL.csv")
missing_posters = movie_poster_db[movie_poster_db["posterURL"].isnull()]

print(movie_poster_db.to_numpy()[5][0])