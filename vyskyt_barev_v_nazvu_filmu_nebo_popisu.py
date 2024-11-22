import pandas as pd
import stanza

#stáhnu si češtinu stanzy
stanza.download('cs')

# inicializuje zpracovatelský kanál pro češtinu, který analyzuje text na věty, slova, slovní druhy, lemmata a syntaktické vztahy
nlp = stanza.Pipeline('cs')

# barvy v češtině, musí být mužský rod
barvy = [
    'černý', 'hnědý', 'šedý', 'červený', 'bílý', 'oranžový', 'žlutý', 'zelený',
    'modrý', 'tyrkysový', 'fialový', 'růžový',
    'béžový', 'zlatý', 'stříbrný', 'khaki', 'purpurový'
]

# Funkce, která vytáhne barvy z textu
def extract_colors(text):
    if not isinstance(text, str): #Funkce zajišťuje, že vstup text je skutečně řetězec (str).
        return {}  # zda je vstup text typu řetězec, a pokud není, vrátí prázdný slovník (slovník protože barva: počet)
    
    doc = nlp(text) #Zpracuje vstupní text pomocí Stanza NLP pipeline a vytvoří objekt doc, který obsahuje informace o větách, slovech, jejich základních tvarech (lemmata) a dalších vlastnostech
    lemmas = [word.lemma for sentence in doc.sentences for word in sentence.words] #Extrahuje lemmata (základní tvary slov) ze všech vět a slov v textu a uloží je do seznamu lemmas.
    color_count = {} #Prázdný slovník, který bude ukládat jednotlivé barvy jako klíče a jejich počet výskytů jako hodnoty
    for lemma in lemmas: #uplně klasické nahazování do slovníku
        if lemma in barvy:
            if lemma in color_count:
                color_count[lemma] += 1
            else:
                color_count[lemma] = 1
    return color_count #vrací počet barev

# Input and output file 
input_file = "CSFD_cleaned_final.csv"
output_file = "CSFD_colors_extracted.csv"

#Jdeme zpracovávat po chunkách
chunksize = 10000  # nastavuje velikost čuníka, který bude zpracovaný za účelem šetření paměti
chunk_list = []   #prázdný seznam, jakási ohrádka pro čuníky nebo chlívek

# Načítání souboru po čuníkách
for chunk in pd.read_csv(input_file, chunksize=chunksize): #načtení čuníka z obrovského chlívku CSV
    chunk['color_counts'] = chunk['plot_text'].apply(extract_colors) #Čuníka krmíme, aby se dozvěděl, kolik barev v sobě má (počítáme barvy ve sloupci plot_text).
    chunk_list.append(chunk) # po zpracování jde čuník do ohrádky za kamarády a čeká tam na ostatní

# Spojení všech zpracovaných částí do jednoho DataFrame, Všechny čuníky spojíme do jednoho velkého stáda DataFrame
result_df = pd.concat(chunk_list)

#uložit dataframe do CSV
result_df.to_csv(output_file, index=False)
