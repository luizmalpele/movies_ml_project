import pandas as pd

movie_poster_db = pd.read_csv("../data/Movie_posterURL.csv")
missing_posters = movie_poster_db[movie_poster_db["posterURL"].notnull()].drop(["year", "posterURL"], axis=1)
print(missing_posters)
missing_posters.to_csv("../available_poster_imgs.csv")