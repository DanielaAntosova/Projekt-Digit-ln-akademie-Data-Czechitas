# Projekt digitální akademie Czechitas

Corn & Coke: Tento projekt je absolventskou analýzou v rámci Digitální akademie Data u Czechitas.

Závěry projektu a vizualizace jsou k dispozici na [blogu](https://medium.com/@d.antosova/corn-coke-aplikace-a-komparativn%C3%AD-anal%C3%BDza-%C4%8Dsfd-a-imdb-b0f0ba2b333f).
 

## 1. Průměrné hodnocení filmů na ČSFD a IMDb za dekádu

[SQL script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/prumerne_hodnoceni_filmu_na_csfd_a_imdb_za_dekadu.sql)

Použité koncepty:

**Common Table Expressions (CTEs)**
Použití WITH pro vytváření dočasných tabulek (UniqueMovies, CSFD_ratings, IMDB_ratings) za účelem zlepšení organizace a čitelnosti komplexního SQL dotazu.

**COALESCE**
Kombinace sloupců z různých tabulek pro zajištění nenulových hodnot v případě chybějících dat.

**FULL OUTER JOIN**
Spojení tabulek (CSFD_ratings a IMDB_ratings), včetně záznamů bez odpovídajících hodnot, což poskytuje kompletní přehled dat.

**FLOOR() a CAST() pro zaokrouhlování do dekád**
Převod hodnot roku na dekády pomocí FLOOR(CAST(year / 10) * 10). Elegantní způsob, jak seskupit data podle desetiletí.

**CASE výrazy pro kategorizaci**
Dynamická kategorizace původu filmu (Czech nebo Foreign) a výpočet průměrného hodnocení podle zadaných podmínek.

## 2. Vývoj vznikajících žánrů IMDb

[SQL script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/vyvoj_vznikajicich_zanru_imdb.sql)

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

## 3. Vývoj vznikajících žánrů ČSFD

[SQL script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/vyvoj_vznikajicich_zanru_csfd.sql)

Použité koncepty:

**UNPIVOT**
Transformuje sloupce (např. genres_0, genres_1, ..., genres_8) na řádky v rámci tabulky.
Syntaxe: UNPIVOT ("genres" FOR "genre_col" IN (...)) převádí hodnoty ze zadaných sloupců do jediného sloupce genres.
Zjednodušuje práci s daty v případě, kdy jsou hodnoty uloženy ve více sloupcích, ale potřebujete je analyzovat jako řádky.

**Filtrování (WHERE podmínka)**
Vyloučení neplatných hodnot (NULL nebo prázdné řetězce) pro zajištění kvality výsledků.

**Agregace s COUNT(DISTINCT)**
Výpočet unikátních filmů v každém roce a žánru pomocí COUNT(DISTINCT "movie_id").

**Výpočet procentuálního zastoupení**
ROUND((gc."genre_count" / yt."total_count") * 100, 2) pro normalizované porovnání žánrů mezi roky.

**Použití více CTE (Common Table Expressions)**
Rozdělení dotazu do kroků:

*unpivoted_data: převod sloupců na řádky.
*filtered_data: filtrování neplatných dat.
*genre_counts: výpočet počtu unikátních filmů podle žánru a roku.
*year_totals: součet všech žánrů za rok.
*final_data: výpočet procentuálního zastoupení žán

Výhoda: Modularita kódu zlepšuje jeho čitelnost, laditelnost a opakovanou použitelnost.

## 4. Výskyt barev v názvu filmů nebo popisu ČSFD

[Python script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/vyskyt_barev_v_nazvu_filmu_nebo_popisu_csfd.py)

Použité koncepty:

**Použití NLP pipeline (Stanza) a práce s lemmaty.**
Zpracování českého textu, rozpoznávání větných struktur a extrakce základních tvarů slov (lemmata).

**Vnořené seznamové komprehense pro rychlou iteraci.**
Konstrukce
```python
[word.lemma for sentence in doc.sentences for word in sentence.words] pro rychlou extrakci základních tvarů slov.
```

**Manipulace se slovníky pro počítání výskytů.**
Efektivní aktualizace počtu výskytů klíčových slov pomocí slovníku.

**Práce s velkými soubory pomocí chunků.**
Použití pd.read_csv s parametrem chunksize umožňuje načítat a zpracovávat velké soubory po menších částech, což šetří paměť.

**Spojování dat (pd.concat) a efektivní ukládání do CSV.**
Načítání velkých datových souborů po částech (chunksize) pro úsporu paměti.

## 5. Výskyt barev v názvu filmů nebo popisu IMDb

[Python script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/vyskyt_barev_v_nazvu_filmu_nebo_popisu_imdb.py)

Použité koncepty:

**Použití Counter pro počítání výskytů**
Počítání výskytů slov v seznamu bez nutnosti manuální iterace.

**Seznamová komprehense**
Seznamová komprehense umožňuje vytvořit nový seznam na základě podmínek a transformací v jednom řádku. Tato konstrukce iteruje přes všechna slova, převádí je na malá písmena a přidává do seznamu pouze ta slova, která odpovídají barvám.

```python
[word.lower() for word in words if word.lower() in color_adjectives]
```

**Slovníková komprehense pro výpočet procent**
Slovníková komprehense je podobná seznamové komprehensi, ale místo seznamu vrací slovník. Zde je navíc použit výpočet procent, zaokrouhlování na desetinné místo a iterace přes položky slovníku color_count.
color_percentages = {color: round((count / total_color_words) * 100, 1) for color, count in color_count.items()}

**Zpracování textových dat**
```python
if isinstance(title, str):
    words = title.split()
```

Zpracování textových dat zahrnuje kontroly typu dat (isinstance), práci s řetězci (split) a jejich převod na malá písmena (lower). Kód také musí rozpoznat a ošetřit případy, kdy je hodnota NaN nebo jiného nečekaného typu.

## 6. Nejčastější slova v názvech nebo popisech filmů pro konkrétní žánr IMDb

[Python script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/nejcastejsi_slova_v_nazvech_nebo_popisech_filmu_pro_konkretni_zanr_imdb.py)

Použité koncepty:

**Tokenizace a čištění textu**
Rozdělení textu názvů filmů na jednotlivá slova, odstranění speciálních znaků a převod na malá písmena.

**Použití modulu re pro regulární výrazy**
```python
re.findall(r'\b\w+\b', title.lower())
```

Vyhledává všechna slova v textu (řetězec rozpoznává jako posloupnosti alfanumerických znaků) a ignoruje speciální znaky.

**Filtrování stop slov**
```python 
meaningful_words = [word for word in tokens if word not in stop_words]
```
 
Odstraňuje běžná a nevýznamná slova (např. "and", "the", "of") ze seznamu slov.

**Filtrování dat podle více podmínek**
```python 
genre_data = data[(data['Genre_1'] == genre) | (data['Genre_2'] == genre) | (data['Genre_3'] == genre)]
```

Vybere jen ty filmy, které mají zadaný žánr v jednom ze tří sloupců.

## 7. Nejčastější slova v názvech nebo popisech filmů pro konkrétní žánr ČSFd

[Python script](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/nejcastejsi_slova_v_nazvech_nebo_popisech_filmu_pro_konkretni_zanr_csfd.py)

Použité koncepty:


**Zpracování přirozeného jazyka (NLP) pomocí lemmatizace**
NLP (zpracování přirozeného jazyka) umožňuje počítačům porozumět psanému i mluvenému textu. Lemmatizace je klíčovou technikou NLP, která převádí slova na jejich základní tvary (např. „běžím" → „běžet"). V tomto projektu byla použita knihovna Stanza, která texty tokenizuje (rozděluje na slova) a následně lemmatizuje. Tento krok sjednocuje různé tvary slov a zvyšuje kvalitu vstupních dat pro další analýzu.

**Prezentace textu pomocí TF-IDF**
TF-IDF (Term Frequency-Inverse Document Frequency) je standardní metoda pro převod textu na číselnou reprezentaci. Váží slova podle jejich četnosti v jednom dokumentu a jejich vzácnosti v celém souboru dokumentů. To pomáhá zvýraznit důležitá slova a potlačit běžná slova, která nemají velký význam pro analýzu. V našem případě byla použita omezená reprezentace na 1000 nejvýznamnějších slov, což optimalizuje výkon modelu.

**Trénink klasifikačního modelu logistické regrese**
Logistická regrese byla zvolena jako model pro přiřazování popisů filmů k předem definovaným žánrům. Texty převedené na číselnou reprezentaci pomocí TF-IDF sloužily jako vstupní data pro trénink modelu. Model se naučil rozpoznávat souvislost mezi klíčovými slovy a jednotlivými žánry, což umožňuje automatickou klasifikaci textových popisů. Logistická regrese je populární, protože je rychlá, snadno pochopitelná a často dostačuje.

**Vyhodnocení a interpretaci modelu pomocí metrik klasifikace.**
Kvalitu modelu byla hodnocena pomocí metrik, jako jsou přesnost (accuracy), citlivost (recall), přesnost předpovědi (precision) a F1 skóre. Tyto metriky ukázaly, jak dobře model předpovídá žánry na základě popisů. Analýza výsledků identifikovala silné i slabé stránky modelu, což pomáhá v dalším zlepšení.

![Vyhodnocení](https://github.com/DanielaAntosova/Projekt-Digitalni-akademie-Data-Czechitas/blob/main/Klasifikace_heatmap.png "Heatmap klasifikace modelu")

Model si vede dobře u kategorií jako Thriller (F1 = 0,50) a Dokumentární (F1 = 0,48) a vykazuje potenciál i u větších kategorií jako Drama (Recall = 0,54). Slabý výkon u málo zastoupených tříd, jako Katastrofický, lze zlepšit rozšířením dat. S vyvážením datasetu a optimalizací modelu může výkon dále růst! 

**Machine Learning (strojové učení)**
Strojové učení v mém kódu výrazně zjednodušilo a zefektivnilo proces klasifikace filmů na základě jejich popisů. Pomocí modelu logistické regrese bylo možné automaticky přiřazovat filmy k jednotlivým žánrům, což šetří čas a eliminuje riziko chyb, které by mohly vzniknout při manuálním třídění. Model také umožnil identifikaci klíčových slov (lemmat), která nejvíce ovlivňují rozhodování modelu o žánru, což poskytuje důležitý vhled do charakteristik jednotlivých kategorií. Díky tomu lze lépe pochopit, jak model pracuje, a analyzovat, která slova jsou pro jednotlivé žánry nejvýznamnější. Navíc model dokáže předpovídat žánry na nových, dosud neznámých datech, což je zásadní pro aplikace, které potřebují zpracovávat dynamické texty. Strojové učení tak umožnilo nejen efektivní klasifikaci, ale i hlubší interpretaci dat a jejich lepší využití.












