-- 1. Borrar tt de los ids de imdb
-- 2. Separar primaryProfession y knownForTitles en arrays
CREATE TABLE splitted AS
SELECT primaryname,
        split(primaryprofession, ",") as primaryProfession,
        split(knownfortitles, ",") as knownForTitles
FROM superclean

-- 3. Castear
ALTER TABLE splitted CHANGE knownForTitles titles ARRAY<BIGINT>


-- 7. Crear tabla de actores de imdb
CREATE TABLE moviesactors as
-- 6. Agrupar actores en array
SELECT id, collect_set(primaryname) as actors
FROM (
  -- 5. Join por movielens id y title id in array
  SELECT t1.*, t2.primaryName
  FROM l_imdb AS t1
  JOIN (
      SELECT primaryName,c
      FROM (
        -- 4. Filtrar tabla actores y actrices
        SELECT primaryname, titles, primaryprofession
        FROM splitted
        WHERE array_contains(primaryprofession, "actress")
            OR array_contains(primaryprofession, "actor")
      ) sp LATERAL VIEW explode(titles) ep AS c
  )
  AS t2
  ON (t1.id=t2.c)
) spfiltable
GROUP BY id

-- 8. Importar csv con data de otras fuentes
-- 9. Convertir tomatometer y audience_score en DOUBLE (si se importó como BIGINT)
ALTER TABLE data2 CHANGE tomatometer tomatometer DOUBLE
ALTER TABLE data2 CHANGE audience_score audience_score DOUBLE

CREATE TABlE final AS
-- 8. JOIN con rotten y el resto de data de otras fuentes
SELECT data2.id, data2.year, data2.genre, data2.director, data2.budget, data2.country, data2.runtime,
    -- Normalizar data
    tmdb_rating / max(tmdb_rating) over () * 10 as r1,
    imdb_rating / max(imdb_rating) over () * 10 as r2,
    ml_rating / max(ml_rating) over () * 10 as r3,
    tomatometer / max(tomatometer) over () * 10 as r4,
    audience_score / max(audience_score) over () * 10 as r5,
    actors[0] main_cast_1,
    actors[1] main_cast_2,
    actors[2] main_cast_3
FROM moviesactors
RIGHT JOIN data2 on moviesactors.id = data2.id
