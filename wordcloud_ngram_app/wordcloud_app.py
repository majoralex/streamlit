""""

 """
import streamlit as st
import pandas as pd
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import os
import re
import unicodedata
import nltk
from tqdm import tqdm

import plotly.graph_objects as go

# import nltk; nltk.download('popular')
nltk.download('omw-1.4')

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 200)
pd.set_option('display.max_rows', None)
 
def basic_clean(text):
     """
     A simple function to clean up the data. All the words that are not designated as a stop word is then lemmatized after
     encoding and basic regex parsing are performed.
     Lemmatization usually refers to the morphological analysis of words, which aims to remove inflectional endings.
     :param text: the text that is to be cleaned
     return: a corpus of text that is cleaned and prepped for the ngram function
     """
     ADDITIONAL_STOPWORDS = ["a", "b"]  # add additional stop words if needed
     wnl = nltk.stem.WordNetLemmatizer()  # instantiate the Lemmatizer from the nltk library
     # get the stop words from nltk and our custom list, add them together
     stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS
     # Perform some cleansing of the data
     text = (unicodedata.normalize('NFKD', text)
             .encode('ascii', 'ignore')
             .decode('utf-8', 'ignore')
             .lower())
     # regex to trim trailing and leading whitespace of the text
     words = re.sub(r'[^\w\s]', '', text).split()
     # Lemmatize the corpus text that was cleaned
     return [wnl.lemmatize(word) for word in words if word not in stopwords]
 
 
 
def make_ngram(df: pd.DataFrame, corpus_text_col: str, word_combo: int):
     """
     A script that returns a bigram given a corpus of text
     changing the '2' in the return statement changes the ngrams (word combinations)
     :param dataframe: a dataframe with column for an indicator and a column for text
     :param corpus_text_col: the column of the dataframe to generate the bigram for
     :word_combo: the # of Words in the Word combination when making the ngram
     :return: a series based on the corpus_text_col of the dataframe
     """
     words = basic_clean(''.join(str(df[corpus_text_col].tolist())))  # apply the basic clean function above
     return pd.Series(nltk.ngrams(words, word_combo)).value_counts().reset_index()
 
def make_wordcloud(df: pd.DataFrame, corpus_text: str):
     """
     Given a string, use the word cloud library to generate a word cloud. It is important to have this filepath
     "CURRENT-DIRECTORY/Ouput/word-clouds/" where ever this Python Script is being stored.
     :param DataFrame: a dataframe with column for an indicator and a column for text
     :param group_by: The column of the dataframe to group the WordClouds e.g Indicator_1
     :param corpus_text_col: The column of the dataframe where the text to be processed exists e.g Trigger_summary
     :return: a WordCloud in a PNG format for each unique item in the group_by parameter
     """
    #  data = df.loc[(~pd.isnull(df[corpus_text])) & (df[corpus_text] != "corpus_text")]
     data = df.loc[(~pd.isnull(df[corpus_text])) ]
     wc = WordCloud(
         width=1500,
         height=800,
         min_font_size=8,
         background_color="white",
         random_state=1,
         collocations=False,
         stopwords=STOPWORDS,
         mask=None,
         contour_width=1,
         contour_color="black",
     )
     # based on the filtered dataframe, create a WordCloud
     return wc.generate_from_text(str(data[corpus_text]))


def mark_plotly_bar_chart(df: pd.DataFrame, x_series: list, y_series: list):
    # fig = go.Figure()
    fig = go.Figure([go.Bar(x=x_series, y=y_series, orientation='h')])
    return fig

def make_aagrid_table(df: pd.DataFrame):
    return AgGrid(df)



def main():

    st.set_page_config(
     page_title="WorldCloud | N-GRAM",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
    )

    st.write("# WordCloud and N-Grams")

    with st.sidebar:
        refresh_button = st.button("Refresh Data")
        n_gram_size = st.slider("Number of Words in N-Gram", 1, 10, 3)
        file = st.file_uploader("Add a CSV ...")
    if file:
        n_gram_df = pd.read_csv(file)

        column_ngram_options = st.selectbox("Select a Column to turn into a series of n-grams", options=n_gram_df.columns)
        n_gram_df = make_ngram(df=n_gram_df, corpus_text_col=column_ngram_options, word_combo=n_gram_size).rename(columns={'index': 'n_grams', 0: 'count'}, inplace=False).sort_values(by=['count'], ascending=False)
        # n_gram_df['n_gram_merged'] = ["; ".join(x) for x in n_gram_df.iloc[:, 0]]
        
        flat_list = list()  
        for sub_list in n_gram_df['n_grams']:
            flat_list += sub_list

        wc = make_wordcloud(df=pd.DataFrame({'data': flat_list}), corpus_text='data')
        col1, col2 = st.columns((2,6))
        with col1:
            st._legacy_dataframe(n_gram_df, width=500, height=1000)

        with col2:
            st.image(wc.to_array(), use_column_width=True)
    else: 
        st.subheader("Upload a file to begin!")


    
if __name__ == "__main__":

    main()
