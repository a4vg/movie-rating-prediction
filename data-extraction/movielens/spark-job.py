from pyspark.sql import HiveContext, Row, SparkSession

import time
from datetime import datetime

spark = SparkSession.builder \
        .appName("scheduled-tmdb") \
        .master("local") \
        .enableHiveSupport() \
        .getOrCreate()

sc = spark.sparkContext
hc = HiveContext(sc)
MovieRating = Row("updatedtime", "movielensid", "tmdbid", "rating")
spark.sql("CREATE TABLE IF NOT EXISTS MovieLensRTRatings (updatedtime STRING, movielensid BIGINT, tmdbid BIGINT, rating DOUBLE) USING hive")

def get_movies_id():
  hc.table("default.final").registerTempTable("final_temp")
  hc.table("default.links").registerTempTable("links_temp")
  r = hc.sql("SELECT f.id id, l.tmdbid tmdbid FROM final_temp f JOIN links_temp l ON f.id=l.movieId")
  return r.rdd.map(lambda row: (row.id, row.tmdbid)).collect()

def get_movie(movielens_id, tmdb_id):
    api_key = "e91fbeacb357d33d361e16251b8c532e"
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
    response = requests.get(url)

    if not response.ok:
        time.sleep(200)
        get_movie(movielens_id, tmdb_id)
    
    response_json = response.json()
    rating = response_json.get("vote_average", None)

    return str(datetime.now()), movielens_id, tmdb_id, float(rating)

if __name__ == '__main__':
  for ml_id, tmdb_id in get_movies_id():
    uptime, mlid, tmdbid, rating = get_movie(ml_id, tmdb_id)
  spark.sql("INSERT INTO MovieLensRTRatings values ('{}', {}, {}, {})".format(uptime, mlid, tmdbid, rating))


