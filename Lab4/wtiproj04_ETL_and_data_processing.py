import pandas as pd
import numpy as np


class PMovies:
    def __init__(self):
        self._rated_movies = pd.read_csv("../user_ratedmovies.dat.txt", sep='\t', dtype={"userID": int, "rating":np.float64})
        self._movie_genres = pd.read_csv("../movie_genres.dat.txt", sep='\t', dtype={"movieID": int})
        self._movie_genres_dummy = self._movie_genres.copy()
        self._movie_genres_dummy['dummy_column'] = 1
        self._tables = self.join()

    def join(self):
        j = self._rated_movies.join(self._movie_genres, rsuffix='genres')
        return j

    def getPivotAllTable(self):
        pivoted = self._movie_genres_dummy.pivot_table(index=['movieID'], columns='genre', values='dummy_column',
                                                 fill_value=0).add_prefix("genre-")
        joined = pd.merge(self._rated_movies, pivoted, on="movieID").drop(["date_day", "date_minute", "date_month", "date_second", "date_year", "date_hour"], axis=1).astype(int)
        return joined

    def getPivotUser(self, userID):
        joined = pd.merge(self._rated_movies[self._rated_movies.userID == userID], self._movie_genres, on="movieID")
        pivoted = joined.pivot_table(columns='genre', fill_value=0, aggfunc=np.mean, values="rating").add_prefix("genre-")
        return pivoted

    def getAvg(self):
        joined = pd.merge(self._rated_movies, self._movie_genres, on="movieID")
        pivoted = joined.pivot_table(columns='genre', fill_value=0, aggfunc=np.mean, values="rating").add_prefix("genre-")
        return pivoted

    def getDifferenceWithAvgUser(self, userID):
        return self.getAvg().subtract(self.getPivotUser(userID)).fillna(0)

    def rewriteRatingToGenreColumn(self):
         pivot = self._tables.pivot_table(index=['movieID'], columns='genre', values='rating',
                                                              fill_value=0).add_prefix("genre-")
         joined = pd.merge(self._rated_movies, pivot, on="movieID").drop(
             ["date_day", "date_minute", "date_month", "date_second", "date_year", "date_hour"], axis=1).astype(int)
         return joined


def df_to_dict(df):
    return df.to_dict(orient='records')


def dict_to_df(dict):
    df = pd.DataFrame.from_dict(dict)
    return df.sort_index(axis=1)


def loseless(df):
    xx = df.join().sort_index(axis=1)
    xx2 = dict_to_df(df_to_dict(df.join()))
    return (xx == xx2).all()


if __name__ == '__main__':
    pm = PMovies()

    # Zad 4
    print(loseless(pm))

    # Zad 5
    print("\n\n\n")
    print(df_to_dict(pm.getAvg()))
    print("\n\n\n")

    # for item in df_to_dict(pm.rewriteRatingToGenreColumn()):
    #     print(item)

    # Zad 6
    print(df_to_dict(pm.getPivotUser(78)))
    print("\n\n\n")


    # Zad 7
    print(df_to_dict(pm.getDifferenceWithAvgUser(78)))
    print("\n\n\n")

    print(pm.getPivotUser(78))
