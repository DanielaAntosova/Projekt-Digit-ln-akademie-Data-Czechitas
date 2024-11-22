#Tento Python kód načte data z CSV souboru, získá unikátní žánry a spočítá frekvence slov v názvech filmů pro každý žánr. Nejprve pomocí funkce pro tokenizaci rozdělí názvy na jednotlivá slova, přičemž ignoruje běžná slova (stop words). 
#Nakonec vypočítá nejčastější slova pro každý žánr a uloží výsledek do nového CSV souboru.

import pandas as pd
#Načítá knihovnu pandas, která slouží pro práci s tabulkovými daty, jako jsou CSV soubory.

from collections import Counter
#Importuje třídu Counter, která je užitečná pro počítání výskytů jednotlivých prvků v seznamu.

import re
#Načítá modul pro práci s regulárními výrazy, který slouží k hledání nebo manipulaci s textovými vzory

data = pd.read_csv('Spojeni_rating_basics (1).csv')
#Načte soubor do tabulky DataFrame

def tokenize_title(title):
    #Definuje funkci pro rozdělení textu na jednotlivá slova.
    return re.findall(r'\b\w+\b', title.lower())
    #Pomocí regulárního výrazu najde všechna slova v textu:
    #\b\w+\b: Hledá celá slova.
    #title.lower(): Převede text na malá písmena, aby se ignorovala velikost písmen.
    #Výstup: Funkce vrací seznam slov (například z "My Movie Title" vrátí ['my', 'movie', 'title']).

stop_words = {
'a','about','above',
 'after',
 'again',
 'against',
 'ain',
 'all',
 'am',
 'an',
 'and',
 'any',
 'are',
 'aren',
 "aren't",
 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',
 'con',
 'couldn',
 "couldn't",
 'd',
 'de',
 'del',
 'der',
 'des',
 'did',
 'didn',
 "didn't",
 'die',
 'do',
 'does',
 'doesn',
 "doesn't",
 'doing',
 'don',
 "don't",
 'down',
 'du',
 'during',
 'each',
 'el',
 'en',
 'et',
 'few',
 'for',
 'from',
 'further',
 'had',
 'hadn',
 "hadn't",
 'has',
 'hasn',
 "hasn't",
 'have',
 'haven',
 "haven't",
 'having',
 'he',
 'her',
 'here',
 'hers',
 'herself',
 'him',
 'himself',
 'his',
 'how',
 'i',
 'if',
 'ii',
 'in',
 'into',
 'is',
 'isn',
 "isn't",
 'it',
 "it's",
 'its',
 'itself',
 'just',
 'l',
 'la',
 'le',
 'les',
 'los',
 'll',
 'm',
 'ma',
 'me',
 'mightn',
 "mightn't",
 'more',
 'most',
 'movie',
 'mustn',
 "mustn't",
 'my',
 'myself',
 'needn',
 "needn't",
 'no',
 'nor',
 'not',
 'now',
 'o',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 're',
 's',
 'same',
 'shan',
 "shan't",
 'she',
 "she's",
 'should',
 "should've",
 'shouldn',
 "shouldn't",
 'so',
 'some',
 'such',
 't',
 'than',
 'that',
 "that'll",
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 'these',
 'they',
 'this',
 'those',
 'through',
 'to',
 'too',
 'un',
 'und',
 'under',
 'until',
 'up',
 'v',
 've',
 'very',
 'was',
 'wasn',
 "wasn't",
 'we',
 'were',
 'weren',
 "weren't",
 'what',
 'when',
 'where',
 'which',
 'while',
 'who',
 'whom',
 'why',
 'will',
 'with',
 'won',
 "won't",
 'wouldn',
 "wouldn't",
 'y',
 'you',
 "you'd",
 "you'll",
 "you're",
 "you've",
 'your',
 'yours',
 'yourself',
 'yourselves',
 '2',
 '3',
 'à',
 'f',
 'c',
 'fu',
 'two',
 'one',
 'e',
 'x'
}
#Obsahuje seznam tzv. stop slov – běžných slov, která nemají zvláštní význam


unique_genres = pd.unique(data[['Genre_1', 'Genre_2', 'Genre_3']].values.ravel('K'))
unique_genres = [genre for genre in unique_genres if pd.notna(genre)]
#pd.unique: Extrahuje unikátní hodnoty z vybraných sloupců (Genre_1, Genre_2, Genre_3).
#ravel('K'): Převede tabulku hodnot na jednorozměrné pole (pro snazší získání unikátních hodnot).
#pd.notna(genre): Odstraní hodnoty NaN (prázdné nebo chybějící).
#Výstup: Seznam obsahující všechny unikátní žánry.

genre_word_counts_list = []
#Prázdný seznam, který bude později obsahovat výsledky (žánr, slovo, počet).

for genre in unique_genres:
    genre_data = data[(data['Genre_1'] == genre) | (data['Genre_2'] == genre) | (data['Genre_3'] == genre)]
    words = []
    #Prochází každý žánr v seznamu unikátních žánrů.
    #Filtruje řádky, kde je aktuální žánr přítomen v některém ze sloupců
    #Prázdný seznam, který bude obsahovat všechna relevantní slova pro aktuální žánr.

  
    for title in genre_data['primaryTitle'].dropna():
    #Prochází názvy filmů (primaryTitle) v rámci aktuálního žánru, přičemž ignoruje prázdné hodnoty (dropna).
        tokens = tokenize_title(title)
        #Rozdělí název na jednotlivá slova pomocí funkce
        meaningful_words = [word for word in tokens if word not in stop_words]
        #Filtrovací seznamová komprehense, která odstraní stop slova.
        words.extend(meaningful_words)
        #Přidá zpracovaná slova do seznamu words
    word_counts = Counter(words).most_common(20)
    #Použije Counter, aby spočítal výskyty jednotlivých slov a vybral 20 nejčastějších.
  
    for word, count in word_counts:
        genre_word_counts_list.append([genre, word, count])
        #Přidá aktuální žánr, slovo a jeho počet do seznamu výsledků.

df_genre_words = pd.DataFrame(genre_word_counts_list, columns=['Žánr', 'Slovo', 'Počet'])
#Převádí seznam výsledků na tabulku (DataFrame)
#Pojmenovává sloupce tabulky.

df_genre_words.to_csv('slova_zanry.csv', index=False, encoding='utf-8')
#Uloží tabulku

print(df_genre_words)
#Zobrazí tabulku.
