# movie_id rating runtime country budget

import requests
import csv
import time

def get_movie(movielens_id, tmdb_id, error_csv):
    api_key = "e91fbeacb357d33d361e16251b8c532e"
    url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={api_key}"
    response = requests.get(url)

    if not response.ok:
        with open(error_csv, "a") as f:
            f.write(f"{tmdb_id},{response.status_code}\n")
        return None
    
    response_json = response.json()
    budget = response_json.get("budget", None)
    rating = response_json.get("vote_average", None)
    runtime = response_json.get("runtime", None)
    country = response_json.get("production_countries", None)
    if country: country = country[0]['iso_3166_1'] 
    if not country: country = None
    
    return [movielens_id, tmdb_id, rating, runtime , country, budget ]

def export(movielens_csv, output_csv, error_csv):
    infile = open(movielens_csv, 'r')
    outfile = open(output_csv, "a")

    writer = csv.writer(outfile, delimiter=',')
    writer.writerow(["movie_id","rating","runtime","country","budget"])
    next(infile)
    start_time = time.time()
    for c, line in enumerate(infile):
        ml_id, _, tmdb_id = line.strip().split(",")
        if tmdb_id:
          r = get_movie(int(ml_id), int(tmdb_id), error_csv)
          if r: # not empty
              writer.writerow( r )

          if c % 100 == 0:
              print(c)
              print("--- %s seconds ---" % (time.time() - start_time))
              start_time = time.time()
    
    infile.close()
    outfile.close()

if __name__ == '__main__':
    export("../../raw-data/links.csv", "tmdb_movies.csv","errors.csv")
