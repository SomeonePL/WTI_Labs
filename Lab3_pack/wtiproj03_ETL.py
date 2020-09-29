import pandas as pd
import numpy as np


class PMovies:
    def __init__(self):
        self._rated_movies = pd.read_csv("../user_ratedmovies.dat.txt", sep='\t', dtype={"userID": int, "rating":np.float64})
        self._movie_genres = pd.read_csv("../movie_genres.dat.txt", sep='\t', dtype={"movieID": int})
        self._movie_genres_dummy = self._movie_genres.copy()
        self._movie_genres_dummy['dummy_column'] = 1

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


if __name__ == '__main__':
    pm = PMovies()
    print(pm._tables)
    print(pm.getPivotUser(78))
