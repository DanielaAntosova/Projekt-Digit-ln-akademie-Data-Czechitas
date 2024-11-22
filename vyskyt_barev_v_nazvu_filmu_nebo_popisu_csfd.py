import pandas as pd
#Načítá knihovnu pandas, která je užitečná pro práci s tabulkovými daty (např. CSV soubory). 
import stanza
#Načítá knihovnu stanza, což je nástroj pro zpracování přirozeného jazyka (Natural Language Processing, NLP). 
#Umožňuje analyzovat text a rozpoznávat jazykové prvky jako slova, slovní druhy nebo základní tvary slov.

stanza.download('cs')
#Stahuje jazykový model pro češtinu.

nlp = stanza.Pipeline('cs')
# inicializuje zpracovatelský kanál pro češtinu, který analyzuje text na věty, slova, slovní druhy, lemmata a syntaktické vztahy

barvy = [
    'černý', 'hnědý', 'šedý', 'červený', 'bílý', 'oranžový', 'žlutý', 'zelený',
    'modrý', 'tyrkysový', 'fialový', 'růžový',
    'béžový', 'zlatý', 'stříbrný', 'khaki', 'purpurový'
]
# barvy v češtině, musí být mužský rod

def extract_colors(text):
    # Funkce, která vytáhne barvy z textu
    if not isinstance(text, str): 
    #Funkce zajišťuje, že vstup text je skutečně řetězec (str).
        return {}  
        # zda je vstup text typu řetězec, a pokud není, vrátí prázdný slovník (slovník protože barva: počet)
    
    doc = nlp(text) 
    #Zpracuje vstupní text pomocí Stanza NLP pipeline a vytvoří objekt doc, který obsahuje informace o větách, slovech, jejich základních tvarech (lemmata) a dalších vlastnostech
    lemmas = [word.lemma for sentence in doc.sentences for word in sentence.words] 
    #Extrahuje lemmata (základní tvary slov) ze všech vět a slov v textu a uloží je do seznamu lemmas.
    color_count = {} 
    #Prázdný slovník, který bude ukládat jednotlivé barvy jako klíče a jejich počet výskytů jako hodnoty
    for lemma in lemmas: 
    #uplně klasické nahazování do slovníku
        if lemma in barvy:
            if lemma in color_count:
                color_count[lemma] += 1
            else:
                color_count[lemma] = 1
    return color_count 
    #vrací počet barev

input_file = "CSFD_cleaned_final.csv"
output_file = "CSFD_colors_extracted.csv"
# Input and output file 

chunksize = 10000
#Počet řádků, které se zpracují najednou (např. 10 000 řádků). To šetří paměť při práci s velkými soubory.
chunk_list = []   
#Prázdný seznam, který bude sloužit k ukládání zpracovaných částí (chunků) souboru.

for chunk in pd.read_csv(input_file, chunksize=chunksize):
#Načítá soubor po částech (chunky) podle velikosti chunksize.
    
    chunk['color_counts'] = chunk['plot_text'].apply(extract_colors)
    #Aplikuje funkci extract_colors na každý text ve sloupci plot_text.
    
    chunk_list.append(chunk)
    #Přidá zpracovaný chunk do seznamu chunk_list.

result_df = pd.concat(chunk_list)
# Spojení všech zpracovaných částí do jednoho DataFrame. 

result_df.to_csv(output_file, index=False)
# Uloží výsledný DataFrame do souboru CSV bez přidání indexového sloupce
