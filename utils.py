from matplotlib import pyplot as plt
from wordcloud import WordCloud
import streamlit as st
from streamlit_option_menu import option_menu

def generate_wordcloud(df, selection, column, title, max_words=50):

    text = " ".join(df[df[column] == selection]["clean_lyrics"])
    fig = plt.figure(figsize=(8,4))
    wordcloud = WordCloud(
        background_color="rgba(255, 255, 255, 0)",
        mode="RGBA",
        max_words=max_words,
        collocations=False,
        colormap="plasma",
        max_font_size=100

    ).generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.tight_layout()
    return fig


def logo():
    st.image("images/MagicEraser_240620_165341.png")

def on_change(key):
    if key == 1:
        st.switch_page(page="pages/♪ artist.py")
    if key == 2:
        st.switch_page(page="pages/📊 stats.py")
    if key == 3:
        st.switch_page(page="pages/🔮️predictions.py")
    st.write(key)
    st.write(type(key))


#def side_menu()
    # 2. horizontal menu
    ##page = option_menu(
    #    None, ["Home + US!", "Artist", "Stats", 'Predictions'],
    #    icons=['house', 'music-note', "bar-chart", 'gear'], #https://icons.getbootstrap.com/
    #    menu_icon="cast", default_index=selected_page, orientation="horizontal", on_change=on_change, key=selected_page
    #)
    # Use the custom class in a container