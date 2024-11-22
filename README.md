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

Použité koncepty:

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

**Třetí skript je v souboru vyvoj_vznikajicich_zanru_csfd.sql**

Použité koncepty:

**UNPIVOT**
Co dělá:
Transformuje sloupce (např. genres_0, genres_1, ..., genres_8) na řádky v rámci tabulky.
Syntaxe: UNPIVOT ("genres" FOR "genre_col" IN (...)) převádí hodnoty ze zadaných sloupců do jediného sloupce genres.
Výhoda:
Zjednodušuje práci s daty v případě, kdy jsou hodnoty uloženy ve více sloupcích, ale potřebujete je analyzovat jako řádky.

**Filtrování (WHERE podmínka)**
Co dělá:
Filtruje záznamy s neplatnými hodnotami (NULL nebo prázdné řetězce).
Výhoda: Zajišťuje, že další analýza pracuje pouze s relevantními daty, což zlepšuje kvalitu výsledků.

**Agregace s COUNT(DISTINCT)**
Co dělá:
COUNT(DISTINCT "movie_id") počítá unikátní filmy v každém roce a žánru.
Výhoda: Agregace umožňuje získat přehled o počtu filmů v každém žánru bez duplicit.

**Výpočet procentuálního zastoupení**
Co dělá:
ROUND((gc."genre_count" / yt."total_count") * 100, 2):
Vypočítává podíl jednotlivých žánrů na celkovém počtu filmů v každém roce.
Výsledek je zaokrouhlen na dvě desetinná místa.
Výhoda: Tento výpočet poskytuje normalizované údaje, které usnadňují srovnání žánrů mezi lety.

**Použití více CTE (Common Table Expressions)**
Co dělá:
Rozděluje dotaz na logické kroky:
unpivoted_data: Převádí sloupce žánrů na řádky.
filtered_data: Filtruje neplatné záznamy.
genre_counts: Počítá počet unikátních filmů v každém roce a žánru.
year_totals: Sčítá celkové počty žánrů za rok.
final_data: Spojuje výsledky a vypočítává procenta.
Výhoda: Modularita kódu zlepšuje jeho čitelnost, laditelnost a opakovanou použitelnost.

**Čtvrtý skript je v souboru vyskyt_barev_v_nazvu_filmu_nebo_popisu_csfd.py**

Použité koncepty:

**Použití NLP pipeline (Stanza) a práce s lemmaty.**
NLP pipeline Stanza zpracovává český text a rozpoznává jeho jazykové struktury, jako jsou věty, slova a základní tvary slov (lemmata).

**Vnořené seznamové komprehense pro rychlou iteraci.**
Konstrukce [word.lemma for sentence in doc.sentences for word in sentence.words] rychle extrahuje základní tvary slov z každé věty a každého slova v textu.

**Manipulace se slovníky pro počítání výskytů.**
Kód efektivně počítá výskyty barev ve slovníku tím, že kontroluje přítomnost klíče a aktualizuje hodnoty nebo přidává nové klíče.

**Práce s velkými soubory pomocí chunků.**
Použití pd.read_csv s parametrem chunksize umožňuje načítat a zpracovávat velké soubory po menších částech, což šetří paměť.

**Spojování dat (pd.concat) a efektivní ukládání do CSV.**
Funkce pd.concat kombinuje všechny zpracované části dat (chunky) do jednoho velkého DataFrame.

**Pátý skript je v souboru vyskyt_barev_v_nazvu_filmu_nebo_popisu_imdb.py**

Použité koncepty:

**Použití Counter pro počítání výskytů**
Counter je speciální datová struktura, která umožňuje snadno počítat výskyty prvků v seznamu. Místo běžného slovníku (dict), kde bychom museli ručně kontrolovat a přičítat hodnoty, Counter to zvládne automaticky.

**Seznamová komprehense**
Seznamová komprehense umožňuje vytvořit nový seznam na základě podmínek a transformací v jednom řádku. Tato konstrukce iteruje přes všechna slova, převádí je na malá písmena a přidává do seznamu pouze ta slova, která odpovídají barvám.
[word.lower() for word in words if word.lower() in color_adjectives]

**Slovníková komprehense pro výpočet procent**
Slovníková komprehense je podobná seznamové komprehensi, ale místo seznamu vrací slovník. Zde je navíc použit výpočet procent, zaokrouhlování na desetinné místo a iterace přes položky slovníku color_count.
color_percentages = {color: round((count / total_color_words) * 100, 1) for color, count in color_count.items()}

**Zpracování textových dat**
if isinstance(title, str):
    words = title.split()
Zpracování textových dat zahrnuje kontroly typu dat (isinstance), práci s řetězci (split) a jejich převod na malá písmena (lower). Kód také musí rozpoznat a ošetřit případy, kdy je hodnota NaN nebo jiného nečekaného typu.














