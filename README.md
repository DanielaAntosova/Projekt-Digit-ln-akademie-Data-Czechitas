# Projekt digitální akademie Czechitas
Corn &amp; Coke. Tato analýza je absolventským projektem Digitální akademie Data u Czechitas. 

**První skript je v souboru prumerne_hodnoceni_filmu_na_csfd_a_imdb_za_dekadu.sql**

Použité koncepty:

**Common Table Expressions (CTEs)**
Použití WITH pro vytváření dočasných tabulek (UniqueMovies, CSFD_ratings, IMDB_ratings) pro organizaci a zlepšení čitelnosti komplexního SQL dotazu.

**COALESCE**
Sloučení sloupců z různých tabulek tak, aby se zajistilo, že výsledná hodnota bude vždy nenulová.

**FULL OUTER JOIN**
Kombinace dvou tabulek (CSFD_ratings a IMDB_ratings), včetně případů, kdy jedna z nich nemá odpovídající hodnoty, což zajistí kompletní přehled dat.

**FLOOR() a CAST() pro zaokrouhlování do dekád**
Transformace hodnot roku na dekády pomocí FLOOR(CAST(...) / 10) * 10, což je elegantní způsob seskupení dat podle časových období.

**CASE výrazy pro kategorizaci**
Dynamické klasifikace původu filmu (Czech nebo Foreign) nebo výpočtu průměrného hodnocení na základě specifických podmínek.

**Druhý skript je v souboru vyvoj_vznikajicich_zanru_imdb.sql**

**Common Table Expressions (CTE)**
Použití více CTE (WITH combined_genres, genre_counts, total_genres_per_year) pro rozdělení složitého dotazu na logické části.
To usnadňuje čitelnost a opakované použití dílčích výsledků v hlavním dotazu.

**UNION ALL**
Sloučení dat z několika sloupců (Genre_1, Genre_2, Genre_3) do jedné tabulky, přičemž zachovává duplicitní hodnoty.
To umožňuje efektivně pracovat s více hodnotami žánrů na jednom řádku.

**Agregace s GROUP BY**
Výpočet metrik, jako je počet výskytů žánrů (COUNT(*)) nebo celkový počet všech žánrů za rok (SUM(genre_count)).
GROUP BY umožňuje rozdělit data podle roku a žánru, což je klíčové pro analýzu trendů.

**Relace mezi CTE pomocí JOIN**
Spojení dvou CTE (genre_counts a total_genres_per_year) podle společného klíče (year), aby bylo možné vypočítat procentuální zastoupení žánru v daném roce.
Efektivní použití relací mezi dočasnými výsledky.

**Výpočet odvozených hodnot**
ROUND((gc.genre_count * 100.0 / tg.total_genres), 2):
Pokročilý výpočet procentuálního podílu jednotlivých žánrů v daném roce s zaokrouhlením na dvě desetinná místa.
Kombinace matematických operací a zaokrouhlování ukazuje praktické použití odvozených metrik.

