#Tento kód analyzuje názvy filmů v datasetu, vyhledává barvy v těchto názvech, počítá jejich výskyty, vypočítává procentuální zastoupení jednotlivých barev a ukládá výsledky do nového CSV souboru.


import pandas as pd
#Načítá knihovnu pandas, která slouží pro práci s tabulkovými daty, jako jsou CSV soubory.

from collections import Counter
#Importuje třídu Counter, která je užitečná pro počítání výskytů jednotlivých prvků v seznamu.

data = pd.read_csv('Spojeni_rating_basics (1).csv')
#Načte CSV soubor s názvem 'Spojeni_rating_basics (1).csv' a uloží jej do proměnné data. 

color_adjectives = {'blue', 'green', 'red', 'yellow', 'black', 'white', 'pink', 'purple', 'orange', 'brown', 'gray', 'turquoise', 'gold', 'silver'}
#Množina (set) obsahující barvy, které se budou hledat v názvech (primaryTitle).

all_color_words = []
#Prázdný seznam, který bude obsahovat všechna nalezená barevná přídavná jména z názvů filmů.
for title in data['primaryTitle']:
#Iteruje přes každý název (primaryTitle) v datasetu.
    if isinstance(title, str):
    #Kontroluje, zda je hodnota názvu textová (např. ne prázdná nebo číslo).
        words = title.split() 
        #Rozděluje název na jednotlivá slova podle mezer.
        all_color_words.extend([word.lower() for word in words if word.lower() in color_adjectives])
        #Seznamová komprehense, která:
            #Převede slova na malá písmena (word.lower()).
            #Vybere jen ta slova, která jsou v množině color_adjectives.
        #all_color_words.extend: Přidá nalezená barevná slova do seznamu all_color_words.

color_count = Counter(all_color_words)
#Spočítá, kolikrát se každé barevné slovo vyskytlo v seznamu all_color_words.
#color_count: Slovník, kde klíčem je barva a hodnotou její počet výskytů.

total_color_words = sum(color_count.values())
#Sečte všechny výskyty barev, aby získal celkový počet nalezených barevných slov.

if total_color_words > 0:
    color_percentages = {color: round((count / total_color_words) * 100, 1) for color, count in color_count.items()}
else:
    color_percentages = {}
#Kontroluje, zda byly nalezeny nějaké barevné výskyty.
#Vypočítá procento pro každou barvu, výsledek zaokrouhlí na jedno desetinné místo.
#Pokud nebyly nalezeny žádné barvy, vytvoří prázdný slovník.

color_percentages_df = pd.DataFrame(list(color_percentages.items()), columns=['Color', 'Percentage'])
#Vytvoří tabulku (DataFrame) ze slovníku color_percentages. Určí názvy sloupců v nové tabulce.

color_percentages_df.sort_values(by='Percentage', ascending=False, inplace=True)
#Seřadí tabulku podle sloupce Percentage od největšího k nejmenšímu.
#inplace=True: Provádí změny přímo na původní tabulce, místo vytváření nové kopie.

color_percentages_df.to_csv('movies_colors.csv', index=False)
#Uloží tabulku jako CSV soubor

print(color_percentages_df)
#Zobrazí výslednou tabulku barev a jejich procentuální zastoupení v názvech filmů.
