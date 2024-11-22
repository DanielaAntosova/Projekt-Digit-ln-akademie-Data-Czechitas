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

