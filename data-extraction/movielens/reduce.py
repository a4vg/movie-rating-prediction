# movieId,rating

import sys

movie_rating_count = {}

def reducer():
    for line in sys.stdin:
        movieid, rating = line.strip().split(",")
        rating = float(rating)
        
        if movieid in movie_rating_count:
            movie_rating_count[movieid][0] += rating
            movie_rating_count[movieid][1] += 1
        else:
            movie_rating_count[movieid] = [rating, 1]
    for movieid, rating in movie_rating_count.items():
        rating_sum, rating_count = rating
        rating_avg = round(rating_sum/rating_count, 1)
        print(f"{movieid},{rating_avg}")

if __name__ == "__main__":
    reducer()
