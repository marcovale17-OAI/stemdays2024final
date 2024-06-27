import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
from utils import generate_wordcloud, logo
from streamlit_navigation_bar import st_navbar


st.set_page_config(initial_sidebar_state="collapsed")


df = pd.read_csv("data/songs_with_prediction.csv")
music_features = [
    "danceability",
    "energy",
    "loudness",
    "speechiness",
    "acousticness",
    "instrumentalness",
    "liveness",
    "valence",
    "tempo"
]

colors = {"pop":"#471ca8", "rock":"#884ab2", "country": "#ff930a", "rb": "#f24b04", "misc": "#d1105a", "rap": "#ff99b6"} #colori da cambiare

def side_menu(selected_page):
    page=st_navbar(["Home + US!", "♪ Artist", "📊 Stats", '🔮️Predictions'], selected=selected_page)
    if page == "Home + US!":
        st.switch_page(page="app.py")
    if page == "♪ Artist":
        st.switch_page(page="pages/♪ artist.py")
    if page == "🔮️Predictions":
        st.switch_page(page="pages/🔮️predictions.py")

def show_metrics():

    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Canzoni", value=len(df), delta_color="off")
    col2.metric(label="Cantanti", value=df["artists"].nunique(), delta_color="off")
    col3.metric(label="Generi musicali", value=df["tag"].nunique(), delta_color="off")
    col4.metric(label="Ultima release", value=df["year"].max(), delta_color="off")


def plot_pie():

    fig = plt.figure()
    plt.pie(
        df["tag"].value_counts(),
        labels=df["tag"].value_counts().index,
        autopct="%1.2f%%",
        colors=[colors[key] for key in df["tag"].value_counts().index]
        )
    plt.title(f"Distribuzione dei generi")
    my_circle = plt.Circle((0, 0), 0.5, color='white')
    p = plt.gcf()
    p.gca().add_artist(my_circle)

    return fig


def plot_music_feature_distribution(feature):

    fig, ax = plt.subplots(figsize=(6, 3))
    feature_per_tag = df.groupby("tag")[feature].mean().sort_values(ascending=True)
    plt.barh(feature_per_tag.index, feature_per_tag, color=[colors[key] for key in feature_per_tag.index])
    plt.title(f"{feature.capitalize()} media per genere musicale")
    plt.xlabel(f"{feature.capitalize()}")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()


    return fig


def worcloud_section():
    genre = st.selectbox("Seleziona un genere", df["tag"].unique())
    wordcloud = generate_wordcloud(df=df, selection=genre, column="tag", title=f"{genre} wordcloud")
    st.pyplot(fig=wordcloud)


def artisti():
    col1, col2 = st.columns(2)
    artists_pop = df.groupby("artists")["popularity"].mean()
    with col1:
        st.image("images/Chris Brown.jpg")
        top_artists = artists_pop.sort_values(ascending=False).head(5).reset_index()
        expansion = st.expander("TOP 5 artisti più ascoltati")
        with expansion:
            for _, row in top_artists.iterrows():
                artist = row["artists"]
                popularity = round(row["popularity"])
                st.write(f"🎤 <b>{artist}</b> (popolarità: {popularity})", unsafe_allow_html=True)

    with col2:
        st.image("images/nu_shooz.jpeg")
        expansion = st.expander("TOP 5 artisti meno ascoltati")
        flop_artists = artists_pop.sort_values(ascending=True).head(5).reset_index()
        with expansion:
            for _, row in flop_artists.iterrows():
                artist = row["artists"]
                popularity = round(row["popularity"])
                st.write(f"🎤 <b>{artist}</b> (popolarità: {popularity})", unsafe_allow_html=True)


def canzoni():
    col1, col2 = st.columns(2)
    with col1:
        st.image("images/as_it_was.jpeg")
        top_songs = df.sort_values("popularity", ascending=False).head(5).reset_index()
        expansion = st.expander("TOP 5 canzoni piu ascoltate")
        with expansion:
            for _, song in top_songs.iterrows():
                track_name = song["track_name"]
                artist = song["artists"]
                year = song["year"]
                popularity = song["popularity"]
                st.write(
                    f"♪ :violet[<b>{track_name}</b>] by <i>{artist}</i> ({year}) - popolarità: <b>{popularity}</b>",
                    unsafe_allow_html=True)

    with col2:
        st.image("images/warewolves.jpeg")
        flop_songs = df.sort_values("popularity", ascending=True).head(5).reset_index()
        expansion = st.expander("TOP 5 canzoni meno ascoltate")
        with expansion:
            for _, song in flop_songs.iterrows():
                track_name = song["track_name"]
                artist = song["artists"]
                year = song["year"]
                popularity = song["popularity"]
                st.write(f"♪ :violet[<b>{track_name}</b>] by <i>{artist}</i> ({year}) - popolarità: <b>{popularity}</b>", unsafe_allow_html=True)

side_menu("📊 Stats")
st.title("Descrizione dei dati")

show_metrics()

st.subheader("Le classifiche più popolari")
artisti()
canzoni()

st.subheader("Generi musicali")
col1, col2 = st.columns([2, 3])
pie = plot_pie()
col1.text("")
col1.pyplot(fig=pie)
feature = col2.selectbox("Seleziona una feature", music_features)
barchart = plot_music_feature_distribution(feature)
col2.pyplot(fig=barchart)

worcloud_section()

col1, col2, col3 = st.columns([1,2,1])
with col2:
    logo()
