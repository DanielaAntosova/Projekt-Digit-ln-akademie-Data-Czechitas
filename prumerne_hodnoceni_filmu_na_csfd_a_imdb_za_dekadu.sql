WITH UniqueMovies AS (
--Tato část vytváří dočasnou tabulku zvanou UniqueMovies, která obsahuje unikátní informace o filmech.
    SELECT 
        "id",
        "origin_text_2",
        "rating",
        (FLOOR(CAST("origin_text_2" AS INTEGER) / 10) * 10) AS "decade_start",
        CASE 
            WHEN "origin_text_0" LIKE '%Česko%' OR "origin_text_0" LIKE '%Čechy%' THEN 'Czech'
            ELSE 'Foreign'
        END AS "movie_origin"
    FROM 
        KEBOOLA_21904.WORKSPACE_88546684."CSFD_cleaned_final"
    GROUP BY 
        "id", "origin_text_2", "rating", "origin_text_0"
),

CSFD_ratings AS (
    SELECT 
        "decade_start" AS "decade",
        CASE 
            WHEN "movie_origin" = 'Czech' THEN ROUND(AVG("rating") / 10.0, 1)
        END AS "CSFD_rating_cz",
        CASE 
            WHEN "movie_origin" = 'Foreign' THEN ROUND(AVG("rating") / 10.0, 1)
        END AS "CSFD_rating_other"
    FROM 
        UniqueMovies
    GROUP BY 
        "decade_start", "movie_origin"
),

IMDB_ratings AS (
    SELECT 
        FLOOR(b."startYear" / 10) * 10 AS "decade",
        ROUND(AVG(r."averageRating"), 2) AS "IMDB_rating"
    FROM 
        KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    LEFT JOIN 
        KEBOOLA_21904.WORKSPACE_88546684."title_ratings" AS r 
    ON 
        b."tconst" = r."tconst"
    WHERE 
        b."startYear" IS NOT NULL AND r."averageRating" IS NOT NULL
    GROUP BY 
        "decade"
)

SELECT 
    COALESCE(csfd."decade", imdb."decade") AS "decade",
    MAX(csfd."CSFD_rating_cz") AS "CSFD_rating_cz",
    MAX(csfd."CSFD_rating_other") AS "CSFD_rating_other",
    imdb."IMDB_rating"
FROM 
    CSFD_ratings AS csfd
FULL OUTER JOIN 
    IMDB_ratings AS imdb 
ON 
    csfd."decade" = imdb."decade"
GROUP BY 
    COALESCE(csfd."decade", imdb."decade"), imdb."IMDB_rating"
ORDER BY 
    "decade";

