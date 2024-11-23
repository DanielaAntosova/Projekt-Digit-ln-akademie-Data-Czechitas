# Importování potřebných modulů
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import stanza  # Pro lemmatizaci

# Načtení českého modelu Stanza
stanza.download("cs")  # Jednorázové stažení českého modelu
nlp = stanza.Pipeline("cs", processors="tokenize,lemma", use_gpu=False)

# Seznam českých stopwords
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

# Funkce pro lemmatizaci textu
def lemmatize_text(text):
    doc = nlp(text)
    lemmas = [word.lemma for sentence in doc.sentences for word in sentence.words]
    return " ".join(lemmas)

# Načtení dat
data = pd.read_csv("nazev_zanry_obsah_CSFD.csv")

# Definování sloupců s žánry
genre_columns = ["genres_0", "genres_1", "genres_2", "genres_3", 
                 "genres_4", "genres_5", "genres_6", "genres_7", "genres_8"]

# Vytvoření nového datasetu, kde každý řádek odpovídá jednomu žánru
exploded_data = data.explode(genre_columns).melt(
    id_vars=["plot_text", "plots_others"],
    value_vars=genre_columns,
    value_name="genre"
).drop(columns="variable").dropna()

# Odebrání prázdných nebo duplicitních žánrů
exploded_data = exploded_data[exploded_data["genre"].str.strip() != ""].drop_duplicates()

# Spojení textových sloupců pro analýzu
exploded_data["text"] = exploded_data["plot_text"].fillna("") + " " + exploded_data["plots_others"].fillna("")

# Lemmatizace textu
exploded_data["lemmatized_text"] = exploded_data["text"].apply(lemmatize_text)

# Filtrace tříd s méně než dvěma výskyty
class_counts = exploded_data["genre"].value_counts()
valid_classes = class_counts[class_counts >= 2].index
filtered_data = exploded_data[exploded_data["genre"].isin(valid_classes)]

# Rozdělení na trénovací a testovací sady
X_train, X_test, y_train, y_test = train_test_split(
    filtered_data["lemmatized_text"], filtered_data["genre"], stratify=filtered_data["genre"], random_state=0
)

# Převod textu na TF-IDF reprezentaci
vectorizer = TfidfVectorizer(max_features=1000, stop_words=czech_stopwords)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# Trénink klasifikačního modelu
model = LogisticRegression(max_iter=1000, random_state=0)
model.fit(X_train_vec, y_train)

# Vyhodnocení modelu
y_pred = model.predict(X_test_vec)
print(classification_report(y_test, y_pred))

# Identifikace nejdůležitějších lemmat pro každý žánr
feature_names = vectorizer.get_feature_names_out()
importance = model.coef_

# Uložení nejdůležitějších lemmat do požadovaného formátu
formatted_data = []
for genre, coef in zip(model.classes_, importance):
    sorted_indices = coef.argsort()[::-1]  # Seřadit podle důležitosti
    for idx in sorted_indices[:20]:  # Top 20
        formatted_data.append({'genre': genre, 'word': feature_names[idx], 'importance': coef[idx]})

# Vytvoření DataFrame
formatted_lemmas_df = pd.DataFrame(formatted_data)

# Uložení do CSV
formatted_lemmas_df.to_csv("important_lemmas_final.csv", index=False)

print("Výsledky byly uloženy do 'important_lemmas_final.csv'.")
