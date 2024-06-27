import streamlit as st
from streamlit_carousel import carousel
import pandas as pd
import re
from scipy import stats
from utils import generate_wordcloud
from streamlit_navigation_bar import st_navbar

from utils import logo


df = pd.read_csv("data/songs_with_prediction.csv")

def side_menu(selected_page):
    page=st_navbar(["Home + US!", "♪ Artist", "📊 Stats", '🔮️Predictions'], selected=selected_page)
    if page == "Home + US!":
        st.switch_page(page="pages/app.py")
    if page == "📊 Stats":
        st.switch_page(page="pages/📊 stats.py")
    if page == "🔮️Predictions":
        st.switch_page(page="pages/🔮️predictions.py")


def get_chorus(text):
    chorus_pattern = re.compile(r"\[Chorus\]\n((.*\n)+?)(?=\[|\Z)")
    chorus_match = chorus_pattern.search(text)
    if chorus_match:
        chorus = chorus_match.group(1).strip()
    else: #se il ritornello non viene trovato, vengono ritornati i primi 4 versi della canzoni
        lines = text.strip().split('\n')
        chorus = '\n'.join(lines[:4])

    return chorus


def artist_info(artist):
    genre = df.loc[df["artists"] == artist]["tag"].value_counts().index[0]
    lyrics = df.loc[df["artists"] == artist].sort_values("popularity", ascending=False)["lyrics"].values[0]
    track_name = df.loc[df["artists"] == artist].sort_values("popularity", ascending=False)["track_name"].values[0]

    chorus = get_chorus(lyrics)
    col1, col2 = st.columns([5, 2])

    with col1:
        st.subheader(artist)
        st.write(f"#### Genere musicale: :violet[{genre}]", unsafe_allow_html=True) #genere predominante dell'artista
        st.text(f"{chorus}") #ritornello canzone più popolare pe rl'artista
        st.write(f"<i>({track_name})</i>", unsafe_allow_html=True)

    with col2:
        st.title("")
        try:
            st.image(f"images/{artist}.jpg") #il nome dell'immagine deve essere uguale al nome dell'artista e in formato jpg
        except:
            pass


def word_cloud(artist):
    wordcloud = generate_wordcloud(df=df, selection=artist, column="artists", title=f"{artist} wordcloud")
    st.pyplot(wordcloud)

def primi_grafici(artist) :
    col1, col2 = st.columns(2)

    with col1:
        st.image("images/tophit.jpeg")
        espansione = st.expander("TOP HITS")
        with espansione:
            top_hits = df.loc[df["artists"] == artist].sort_values("popularity", ascending=False)[:3]
            for _, top_hit in top_hits.iterrows():
                st.write(f"♪ {top_hit['track_name']} ({top_hit['year']})", unsafe_allow_html=True)

    #non abbastanza tracce per artista per mostrare i flow
    with col2:
        st.image("images/popularity.jpeg")
        espansione = st.expander("POPOLARITA' MEDIA")
        popularity = round(df.loc[df["artists"] == artist]["popularity"].mean())
        with espansione:
            if popularity >= 80:
                st.metric(label="popularity", value=popularity, delta="very popular", delta_color="normal")
            elif popularity < 80 and popularity >= 60:
                st.metric(label="popularity", value=popularity, delta="popular", delta_color="normal")
            else:
                st.metric(label="popularity", value=popularity, delta="- not popular", delta_color="normal")


def secondi_grafici():
    col1, col2 = st.columns(2)

    with col1:
        st.image("images/danceability.jpeg")
        espansione = st.expander("DANCEABILITY MEDIA")
        danceability = round(df.loc[df["artists"] == artist]["danceability"].mean())
        with espansione:
            if danceability >= 0.8:
                st.metric(label="danceability", value=danceability, delta="very danceable", delta_color="normal")
            elif danceability < 0.8 and danceability >= 0.6:
                st.metric(label="danceability", value=danceability, delta="danceable", delta_color="normal")
            else:
                st.metric(label="danceability", value=danceability, delta="- not danceable", delta_color="normal")


    with col2:
        st.image("images/speechiness.jpg")
        espansione = st.expander("SPEECHINESS MEDIA")
        speechiness = round(df.loc[df["artists"] == artist]["speechiness"].mean(), 2)
        with espansione:
            st.metric(label="speechiness", value=speechiness, delta_color="off")



def disclaimer ():
    st.warning("! Eventuali immagini, grafici e informazioni potrebbero non essere reperibili per tutti gli artisti, avendo a dispsizione un dataset limitato.")

side_menu("♪ Artist")

st.title("Artisti")
artist = st.selectbox(
    "Seleziona l'artista",
    df.groupby("artists")["popularity"].mean().sort_values(ascending=False).index,
    placeholder="Choose an option...",
    help="Seleziona un artista o inizia a scrivere sulla barra per vedere le opzioni", index=0)

artist_info(artist)
disclaimer()
word_cloud(artist)
primi_grafici(artist)
secondi_grafici()

col1, col2, col3 = st.columns([1,2,1])
with col2:
    logo()
