--Tento dotaz porovnává průměrná hodnocení filmů mezi dvěma databázemi (CSFD a IMDB) v průběhu dekád. Výsledkem je tabulka, která obsahuje:
--Dekádu.
--Průměrné hodnocení českých a zahraničních filmů na ČSFD.
--Průměrné hodnocení filmů na IMDb.
--Pomocí tohoto kódu lze analyzovat trendy hodnocení filmů v čase a porovnat, jak jsou filmy hodnoceny na různých platformách.

--Tato část vytváří dočasnou tabulku zvanou UniqueMovies, která obsahuje unikátní informace o filmech.
WITH UniqueMovies AS (
    SELECT 
        "id",
        --identifikátor filmu
        "origin_text_2",
        --rok vzniku
        "rating",
        --hodnocení filmu
        (FLOOR(CAST("origin_text_2" AS INTEGER) / 10) * 10) AS "decade_start",
        --Vypočítá počáteční rok dekády filmu. Například rok 1995 bude převeden na 1990.
        CASE 
            WHEN "origin_text_0" LIKE '%Česko%' OR "origin_text_0" LIKE '%Čechy%' THEN 'Czech'
            ELSE 'Foreign'
        END AS "movie_origin"
        --Rozděluje filmy podle jejich původu na české a zahraniční. 
    FROM 
        KEBOOLA_21904.WORKSPACE_88546684."CSFD_cleaned_final"
        --Čerpá data z tabulky CSFD_cleaned_final, data jsou získaná webscrapingem a očištěná.
    GROUP BY 
        "id", "origin_text_2", "rating", "origin_text_0"
        --Zajišťuje, že každá kombinace hodnot bude v tabulce unikátní.
),

--Tato část počítá průměrné hodnocení českých a zahraničních filmů pro každou dekádu.
CSFD_ratings AS (
    SELECT 
        "decade_start" AS "decade",
        CASE 
            WHEN "movie_origin" = 'Czech' THEN ROUND(AVG("rating") / 10.0, 1)
        END AS "CSFD_rating_cz",
        CASE 
            WHEN "movie_origin" = 'Foreign' THEN ROUND(AVG("rating") / 10.0, 1)
        END AS "CSFD_rating_other"
        --Pokud je film český, vypočítá průměrné hodnocení dělené deseti a zaokrouhlené na jedno desetinné místo. Pokud je film zahraniční, provede stejný výpočet. 
    FROM 
        UniqueMovies
        --Používá data z předchozí tabulky UniqueMovies.
    GROUP BY 
        "decade_start", "movie_origin"
        --Data jsou seskupena podle dekády a původu filmu.
),
--Tato část počítá průměrná hodnocení filmů z databáze IMDb pro každou dekádu.
IMDB_ratings AS (
    SELECT 
        FLOOR(b."startYear" / 10) * 10 AS "decade",
        --Vypočítá dekádu filmu na základě roku vzniku.
        ROUND(AVG(r."averageRating"), 2) AS "IMDB_rating"
        --Vypočítá průměrné hodnocení filmu a zaokrouhlí na dvě desetinná místa.
    FROM 
        KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
        --Tabulka Title_basic_movie_TVmovie_cleaned_genres_years_minutes obsahuje základní informace o filmech (včetně roku).
    LEFT JOIN 
        KEBOOLA_21904.WORKSPACE_88546684."title_ratings" AS r
        --Tabulka title_ratings obsahuje hodnocení filmů. 
    ON 
        b."tconst" = r."tconst"
        --Spojuje obě tabulky na základě shodného ID filmu (tconst).
    WHERE 
        b."startYear" IS NOT NULL AND r."averageRating" IS NOT NULL
        --Filtruje pouze filmy, které mají uvedený rok vzniku a hodnocení.
    GROUP BY 
        "decade"
        --Seskupuje filmy podle dekády.
)
--Kombinuje data z předchozích částí CSFD_ratings a IMDB_ratings:
SELECT 
    COALESCE(csfd."decade", imdb."decade") AS "decade",
    --Sloučí dekády z obou tabulek. Pokud dekáda existuje pouze v jedné tabulce, použije ji.
    MAX(csfd."CSFD_rating_cz") AS "CSFD_rating_cz",
    --Zobrazí nejvyšší hodnocení pro české a zahraniční filmy v rámci dekády (hodnota je stejná, protože jsou data již seskupena).
    MAX(csfd."CSFD_rating_other") AS "CSFD_rating_other",
    --Zobrazuje průměrné hodnocení z IMDb.
    imdb."IMDB_rating"
FROM 
    CSFD_ratings AS csfd
FULL OUTER JOIN 
    IMDB_ratings AS imdb 
ON 
    csfd."decade" = imdb."decade"
    --Zajistí, že dekády z obou tabulek budou zahrnuty, i pokud existují pouze v jedné z tabulek.
GROUP BY 
    COALESCE(csfd."decade", imdb."decade"), imdb."IMDB_rating"
    --Seskupuje podle dekády a IMDb hodnocení.
ORDER BY 
    "decade";
    --Výsledek je seřazen podle dekády.


