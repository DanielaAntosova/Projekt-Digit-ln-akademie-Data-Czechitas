#Tento kód načte filmová data, zpracuje texty pomocí lemmatizace, odstraní nevýznamná slova, převede texty na čísla a naučí model, jak rozpoznávat žánry na základě textu. Na závěr uloží nejdůležitější slova pro každý žánr.

import pandas as pd
# Modul pro práci s tabulkovými daty

from sklearn.feature_extraction.text import TfidfVectorizer
# Modul pro převod textu na číselnou reprezentaci pomocí TF-IDF

from sklearn.linear_model import LogisticRegression
# Modul pro klasifikační model logistické regrese

from sklearn.model_selection import train_test_split
# Funkce pro rozdělení dat na trénovací a testovací sadu

from sklearn.metrics import classification_report
# Funkce pro vyhodnocení modelu, vypisuje metriky jako přesnost a recall

import stanza  
# Modul pro zpracování přirozeného jazyka (lemmatizaci a další NLP úlohy)


stanza.download("cs")
# Stáhne jazykový model pro češtinu z knihovny Stanza (nutné jen jednou)

nlp = stanza.Pipeline("cs", processors="tokenize,lemma", use_gpu=False)
# Nastaví pipeline Stanza pro češtinu; používá tokenizaci a lemmatizaci


czech_stopwords = [
    "a", "aby", "ako", "akční", "ale", "anebo", "ani", "ano", "asi", "až", "během",
    "boj", "bude", "by", "byla", "byli", "bylo", "byl", "být", "chce", "chtít", "co",
    "často", "či", "dne", "do", "dokument", "dokonce", "drama", "dva", "film", "filmu",
    "ho", "historický", "horor", "i", "jak", "jako", "je", "jej", "jeho", "její", 
    "jejich", "jen", "jenž", "ještě", "ji", "jí", "jsem", "jsi", "jsme", "jsou", 
    "já", "kam", "ke", "kde", "keď", "která", "které", "kterou", "který", "kdy", 
    "když", "konečně", "komedie", "let", "léta", "mafie", "má", "manžel", "mezi", 
    "mi", "mne", "mnoho", "muset", "mu", "my", "máte", "mě", "na", "nad", "naprosto",
    "například", "náhodou", "náš", "něco", "něj", "někde", "někdo", "několik", "ne", 
    "nebo", "není", "než", "nic", "ní", "no", "nový", "od", "on", "osobní", "ostatní",
    "pak", "pan", "pokud", "pomocí", "po", "pod", "použití", "příběh", "právě", 
    "pro", "proto", "protože", "proč", "před", "přes", "při", "prichádza", "pribeh", 
    "príbeh", "rámec", "režisér", "rok", "romantický", "sa", "sam", "scénář", "se", 
    "sebe", "seriál", "si", "spolu", "století", "stále", "své", "svého", "svět", 
    "svet", "sveta", "svou", "svůj", "svým", "s", "tak", "také", "takový", "tam", 
    "ten", "tento", "televizní", "the", "thriller", "tím", "to", "toho", "tohle", 
    "totiž", "toto", "trochu", "tvář", "ty", "u", "už", "v", "ve", "velmi", "všechen",
    "vo", "vy", "více", "za", "ze", "že"
]
# Seznam českých stopwords (běžná slova, která nechceme analyzovat)


def lemmatize_text(text):
# Funkce pro lemmatizaci textu, bere text a vrátí jeho lemmatizovanou podobu

    doc = nlp(text)
    # Zpracuje text pomocí pipeline Stanza (rozdělí na věty a slova)
    
    lemmas = [word.lemma for sentence in doc.sentences for word in sentence.words]
    # Získá základní tvary všech slov v textu
    
    return " ".join(lemmas)
    # Spojí základní tvary slov zpět do jednoho textu


data = pd.read_csv("nazev_zanry_obsah_CSFD.csv")
# Načte data z CSV souboru a uloží je do proměnné `data` jako tabulku (DataFrame)


genre_columns = ["genres_0", "genres_1", "genres_2", "genres_3", 
                 "genres_4", "genres_5", "genres_6", "genres_7", "genres_8"]
# Definování sloupců s žánry


exploded_data = data.explode(genre_columns).melt(
# Vytvoření nové tabulky, kde každý řádek odpovídá jednomu žánru
# Rozbalí tabulku tak, aby každý řádek odpovídal jen jednomu žánru
    
    id_vars=["plot_text", "plots_others"],
    # Sloupce s textem zůstanou beze změny
    
    value_vars=genre_columns,
    # Rozbalí sloupce s žánry
    
    value_name="genre"
    # Výsledný sloupec s názvem "genre" bude obsahovat jednotlivé žánry
    
).drop(columns="variable").dropna()
# Odstraní nepotřebný sloupec a řádky s prázdnými hodnotami


exploded_data = exploded_data[exploded_data["genre"].str.strip() != ""].drop_duplicates()
# Odstraní z tabulky (exploded_data) všechny řádky, kde je žánr prázdný (obsahuje pouze mezery), a také duplicity, aby zůstaly jen jedinečné záznamy.


exploded_data["text"] = exploded_data["plot_text"].fillna("") + " " + exploded_data["plots_others"].fillna("")
# Spojuje texty z různých sloupců do jednoho; prázdné hodnoty nahrazuje prázdným řetězcem


exploded_data["lemmatized_text"] = exploded_data["text"].apply(lemmatize_text)
# Aplikuje funkci lemmatize_text na každý řádek sloupce "text" a výsledky ukládá do nového sloupce "lemmatized_text"


class_counts = exploded_data["genre"].value_counts()
# Spočítá, kolikrát se každý žánr objevuje v tabulce

valid_classes = class_counts[class_counts >= 2].index
# Vybírá pouze ty žánry, které se vyskytují alespoň dvakrát

filtered_data = exploded_data[exploded_data["genre"].isin(valid_classes)]
# Filtruje řádky tabulky podle těchto žánrů


X_train, X_test, y_train, y_test = train_test_split(
# Rozděluje data na trénovací a testovací sady
    
    filtered_data["lemmatized_text"], filtered_data["genre"], stratify=filtered_data["genre"], random_state=0
)
# Texty (vstupy) pro model, Žánry (výstupy) pro model, Zajišťuje, že rozdělení zachová poměr žánrů 
# Nastavuje náhodné rozdělení tak, aby bylo opakovatelné


vectorizer = TfidfVectorizer(max_features=1000, stop_words=czech_stopwords)
# Nastaví převod textu na číselnou reprezentaci (max. 1000 slov, ignoruje stopwords)

X_train_vec = vectorizer.fit_transform(X_train)
# Naučí se z trénovacích dat a převede texty na čísla

X_test_vec = vectorizer.transform(X_test)
# Použije stejné nastavení na testovací data


# Trénink klasifikačního modelu
model = LogisticRegression(max_iter=1000, random_state=0)
# Vytvoří model logistické regrese (max. 1000 iterací pro trénink)

model.fit(X_train_vec, y_train)
# Vytvoří model logistické regrese (max. 1000 iterací pro trénink)


y_pred = model.predict(X_test_vec)
# Podle naučených pravidel předpoví, jaký žánr mají filmy v testovacích datech.

print(classification_report(y_test, y_pred))
# zobrazí podrobný přehled toho, jak dobře model fungoval, včetně přesnosti, úspěšnosti a celkového skóre pro každý žánr 


# Identifikace nejdůležitějších lemmat pro každý žánr
feature_names = vectorizer.get_feature_names_out()
# Získá seznam všech slov (nebo lemmat), která byla použita v TF-IDF reprezentaci textů, a uloží je do proměnné feature_names.

importance = model.coef_
# Logistická regrese vypočítává koeficienty, které říkají, jak moc jsou jednotlivá slova důležitá pro konkrétní žánr. 
# Tyto koeficienty se pak použijí k identifikaci nejvýznamnějších slov pro každý žánr.
# Uloží do proměnné importance váhy (koeficienty) pro každé slovo v TF-IDF reprezentaci, které model vypočítal; 
# Tyto váhy určují, jak moc každé slovo ovlivňuje rozhodnutí modelu pro konkrétní žánr.


# Uložení nejdůležitějších lemmat do požadovaného formátu
formatted_data = []
#Vytváří prázdný seznam formatted_data, kam budou postupně ukládány nejdůležitější slova (lemmata) spolu s jejich žánrem a významností.

for genre, coef in zip(model.classes_, importance):
# Tento řádek prochází žánry a jejich odpovídající váhy (koeficienty) slov, aby pro každý žánr identifikoval důležitost jednotlivých slov.
    
    sorted_indices = coef.argsort()[::-1]  
    # Řadí podle důležitosti
    
    for idx in sorted_indices[:20]:  
    # Vybírá TOP 20
        
        formatted_data.append({'genre': genre, 'word': feature_names[idx], 'importance': coef[idx]})
        # Ukládá všechna důležitá slova spolu s jejich žánrem a významností, aby mohla být později zpracována (uložena do CSV).


formatted_lemmas_df = pd.DataFrame(formatted_data)
# Vytvoření DataFrame


formatted_lemmas_df.to_csv("important_lemmas_final.csv", index=False)
# Uložení do CSV

print("Výsledky byly uloženy do 'important_lemmas_final.csv'.")
# Zobrazí, že došlo k uložení
