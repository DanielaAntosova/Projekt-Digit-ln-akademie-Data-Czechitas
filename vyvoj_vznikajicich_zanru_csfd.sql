--Tento SQL dotaz analyzuje popularitu filmových žánrů v průběhu let:
--Výstupem je tabulka, která ukazuje, jak populární byly různé žánry v jednotlivých letech, seřazené podle popularity.

--Převádí data žánrů z více sloupců do jednoho.
--Filtrováním odstraní neplatné záznamy.
--Počítá počet unikátních filmů pro každý žánr v konkrétním roce.
--Získává celkový počet žánrů za rok.
--Vypočítává procentuální zastoupení jednotlivých žánrů v rámci celkového počtu filmů za rok.

--Tato část slouží k transformaci dat:
WITH unpivoted_data AS (
    SELECT
        "origin_text_2" AS "year",
        "id" AS "movie_id",
        "genres"
        --Výstupní sloupec, do kterého budou vloženy hodnoty z více žánrových sloupců
    FROM KEBOOLA_21904.WORKSPACE_88546684."CSFD_cleaned_final"
    UNPIVOT ("genres" FOR "genre_col" IN ("genres_0", "genres_1", "genres_2", "genres_3", "genres_4", "genres_5", "genres_6", "genres_7", "genres_8"))
    --Převádí data z více sloupců (genres_0, genres_1, ..., genres_8) do jednoho sloupce genres.
),
filtered_data AS (
    SELECT
        *
    FROM unpivoted_data
    WHERE "genres" IS NOT NULL AND "genres" <> '' -- Vyloučení NULL a prázdných řetězců
    --Filtruje výsledky z předchozího kroku
    --Vyloučí řádky, kde je žánr NULL.
    --Vyloučí řádky, kde je žánr prázdný řetězec.
    --Tímto krokem se odstraní všechny neplatné nebo prázdné záznamy, aby další analýza byla přesná.
),
--Počítá počet unikátních filmů pro každý rok a žánr:
genre_counts AS (
    SELECT
        "year",
        "genres" AS "genre",
        COUNT(DISTINCT "movie_id") AS "genre_count"
        --Počet unikátních filmů (movie_id) v každém roce pro každý žánr.
    FROM filtered_data
    GROUP BY "year", "genres"
    --Seskupí data podle roku (year) a žánru (genres), aby bylo možné vypočítat počet filmů pro každou kombinaci.
),
--Počítá celkový počet všech žánrů v každém roce
year_totals AS (
    SELECT
        "year",
        SUM("genre_count") AS "total_count"
        --Součet všech žánrů (včetně duplicit) za konkrétní rok.
    FROM genre_counts
    GROUP BY "year"
    --Seskupí data podle roku (year), aby byl pro každý rok vypočítán celkový počet žánrů.
),
--Spojuje informace o počtu žánrů s celkovým počtem žánrů za rok a počítá procentuální zastoupení:
final_data AS (
    SELECT
        gc."year",
        gc."genre",
        gc."genre_count",
        --Počet filmů daného žánru v konkrétním roce.
        ROUND((gc."genre_count" / yt."total_count") * 100, 2) AS "percentage"
        --Vypočítá procento zastoupení daného žánru vůči celkovému počtu žánrů za rok.
        --Výsledek je zaokrouhlen na dvě desetinná místa.
    FROM genre_counts gc
    JOIN year_totals yt
    --Spojuje tabulky genre_counts a year_totals na základě sloupce year.
    --Tím zajistí, že každý řádek v genre_counts má přístup k celkovému počtu žánrů (total_count) z year_totals.
    ON gc."year" = yt."year"
)
SELECT *
--hlavní dotaz    
FROM final_data
ORDER BY "year", "percentage" DESC;
--Výsledky jsou seřazeny vzestupně podle roku a sestupně podle procentuálního zastoupení žánrů.

