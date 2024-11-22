--Co tento kód dělá:
--Seskupení žánrů:
    --Kombinuje tři různé sloupce s žánry (Genre_1, Genre_2, Genre_3) do jednoho seznamu, spolu s rokem, ve kterém byl film vytvořen.
--Počet výskytů žánrů:
    --Počítá, kolikrát se každý žánr objevil v daném roce.
--Celkový počet žánrů v roce:
    --Počítá celkový počet všech žánrů (napříč všemi filmy) pro každý rok.
--Procentuální podíl:
    --Vypočítá, jak velký procentuální podíl má každý žánr na celkovém počtu žánrů v konkrétním roce.
--Řazení:
    --Výstup je seřazen podle roku a následně podle procentuálního podílu v sestupném pořadí (nejpopulárnější žánry jsou na začátku).

--Tato část kombinuje informace o žánrech z více sloupců do jedné tabulky:
WITH combined_genres AS (
    SELECT b."startYear" AS year, b."Genre_1" AS genre
    --rok, kdy byl film vydán a sloupec pro první žánr filmu (mohou být až tři)
    FROM KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    WHERE b."Genre_1" IS NOT NULL AND b."Genre_1" <> '' AND b."startYear" IS NOT NULL
    --Filtruje pouze filmy, které mají definovaný žánr (žádné prázdné nebo NULL hodnoty) a mají uvedený rok (startYear).

    UNION ALL
    --Spojuje data ze tří sloupců (Genre_1, Genre_2, Genre_3) do jedné tabulky.
    --Použití UNION ALL místo UNION zachovává duplicitní řádky.


    SELECT b."startYear" AS year, b."Genre_2" AS genre
    FROM KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    WHERE b."Genre_2" IS NOT NULL AND b."Genre_2" <> '' AND b."startYear" IS NOT NULL

    UNION ALL

    SELECT b."startYear" AS year, b."Genre_3" AS genre
    FROM KEBOOLA_21904.WORKSPACE_88546684."Title_basic_movie_TVmovie_cleaned_genres_years_minutes" AS b
    WHERE b."Genre_3" IS NOT NULL AND b."Genre_3" <> '' AND b."startYear" IS NOT NULL
),
--Tato část počítá, kolikrát se každý žánr objevil v každém roce.
genre_counts AS (
    SELECT 
        year,
        genre,
        COUNT(*) AS genre_count
        --Počet výskytů daného žánru v konkrétním roce.
    FROM 
        combined_genres
    GROUP BY 
        year, genre
        --Seskupuje data podle roku a žánru, aby bylo možné spočítat výskyty pro každou kombinaci.
),
--Tato část počítá celkový počet všech žánrů (všech výskytů) pro každý rok.
 total_genres_per_year AS (
    SELECT 
        year,
        SUM(genre_count) AS total_genres
        --Celkový počet všech žánrů v konkrétním roce
    FROM 
        genre_counts
    GROUP BY 
        year
)
SELECT
--Tato část kombinuje informace o počtu jednotlivých žánrů a celkovém počtu žánrů za rok a vypočítává procentuální podíl jednotlivých žánrů.    
    gc.year,
    gc.genre,
    gc.genre_count,
    tg.total_genres,
    ROUND((gc.genre_count * 100.0 / tg.total_genres), 2) AS percentage
    --Vypočítává procentuální podíl daného žánru vůči všem žánrům v konkrétním roce.
    --Výsledek je zaokrouhlen na dvě desetinná místa.
FROM 
    genre_counts gc
JOIN 
    total_genres_per_year tg ON gc.year = tg.year
    --Spojuje tabulky genre_counts a total_genres_per_year na základě roku.
ORDER BY 
    gc.year, percentage DESC;
    --Výsledek je seřazen podle roku a v rámci roku podle procenta žánrů sestupně.


--Celkový účel kódu
--Dotaz analyzuje popularitu jednotlivých filmových žánrů v průběhu let:

--Kombinuje data o žánrech z několika sloupců.
    --Počítá, kolikrát se každý žánr objevil v konkrétním roce.
    --Počítá celkový počet všech žánrů za rok.
    --Vypočítává procentuální podíl jednotlivých žánrů.
    --Seřadí výsledky podle roku a popularity žánru.
--Výsledná tabulka obsahuje:

    --Rok vydání filmu.
    --Žánr.
    --Počet výskytů žánru.
    --Celkový počet žánrů za rok.
    --Procentuální zastoupení žánru.
--Tento dotaz umožňuje sledovat, jak se popularita jednotlivých žánrů měnila v průběhu let.








