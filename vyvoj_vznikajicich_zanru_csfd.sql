WITH unpivoted_data AS (
    SELECT
        "origin_text_2" AS "year",
        "id" AS "movie_id",
        "genres"
    FROM KEBOOLA_21904.WORKSPACE_88546684."CSFD_cleaned_final"
    UNPIVOT ("genres" FOR "genre_col" IN ("genres_0", "genres_1", "genres_2", "genres_3", "genres_4", "genres_5", "genres_6", "genres_7", "genres_8"))
),
filtered_data AS (
    SELECT
        *
    FROM unpivoted_data
    WHERE "genres" IS NOT NULL AND "genres" <> '' -- Vyloučení NULL a prázdných řetězců
),
genre_counts AS (
    SELECT
        "year",
        "genres" AS "genre",
        COUNT(DISTINCT "movie_id") AS "genre_count"
    FROM filtered_data
    GROUP BY "year", "genres"
),
year_totals AS (
    SELECT
        "year",
        SUM("genre_count") AS "total_count"
    FROM genre_counts
    GROUP BY "year"
),
final_data AS (
    SELECT
        gc."year",
        gc."genre",
        gc."genre_count",
        ROUND((gc."genre_count" / yt."total_count") * 100, 2) AS "percentage"
    FROM genre_counts gc
    JOIN year_totals yt
    ON gc."year" = yt."year"
)
SELECT *
FROM final_data
ORDER BY "year", "percentage" DESC;
