WITH combined_genres AS (
    SELECT b."startYear" AS year, b."Genre_1" AS genre
    FROM KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    WHERE b."Genre_1" IS NOT NULL AND b."Genre_1" <> '' AND b."startYear" IS NOT NULL

    UNION ALL

    SELECT b."startYear" AS year, b."Genre_2" AS genre
    FROM KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    WHERE b."Genre_2" IS NOT NULL AND b."Genre_2" <> '' AND b."startYear" IS NOT NULL

    UNION ALL

    SELECT b."startYear" AS year, b."Genre_3" AS genre
    FROM KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    WHERE b."Genre_3" IS NOT NULL AND b."Genre_3" <> '' AND b."startYear" IS NOT NULL
),
genre_counts AS (
    SELECT 
        year,
        genre,
        COUNT(*) AS genre_count
    FROM 
        combined_genres
    GROUP BY 
        year, genre
),
total_genres_per_year AS (
    SELECT 
        year,
        SUM(genre_count) AS total_genres
    FROM 
        genre_counts
    GROUP BY 
        year
)
SELECT 
    gc.year,
    gc.genre,
    gc.genre_count,
    tg.total_genres,
    ROUND((gc.genre_count * 100.0 / tg.total_genres), 2) AS percentage
FROM 
    genre_counts gc
JOIN 
    total_genres_per_year tg ON gc.year = tg.year
ORDER BY 
    gc.year, percentage DESC;