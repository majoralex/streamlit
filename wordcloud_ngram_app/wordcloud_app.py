"""
The purpose of this app is to allow anyone to create a series of n-grams and the frequency of their appearance within a column of a CSV file. Once data has been uploaded to the app,
the user can select the column to create n-grams and then filter by the count of n-grams in the corpus of text and the n-grams themselves. 

The app will show the word combinations and their counts in descending order with a wordcloud that only uses base text from the n-gram table to the left of it (in other words, the wordcloud is also affected by the filters).


n-gram wiki: https://en.wikipedia.org/wiki/N-gram
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

nltk.download('stopwords')

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
     A script that returns a bigram given a corpus of text (a list of strings), changing the word_combo param will result in changing the number of word combinations for the n-gram.
     The result is a series witha  list of n-grams given the input list of stirngs.

     :param dataframe: a dataframe with at least one Alphabetical column
     :param corpus_text_col: the column of the dataframe to generate the n-gram for
     :word_combo: the # of Words in the Word combination when making the ngram
     :return: a series based on the corpus_text_col of the dataframe
     """
     words = basic_clean(''.join(str(df[corpus_text_col].tolist())))  # apply the basic clean function above
     return pd.Series(nltk.ngrams(words, word_combo)).value_counts().reset_index()
 
def make_wordcloud(list_data: list):
    """
    Remove the N/As from the list provided, construct the WC object and return the WC image
    :param list_data: list of short-medium-large size text snippets
    :returns: a wordcloud object
    """
    cleaned_data = list(filter(lambda item: item is not None, list_data))
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
    return wc.generate_from_text(str(cleaned_data))


@st.experimental_singleton
def n_gram_multiselect_options(df: pd.DataFrame):
    """to make the loading of optioins faster"""
    return df['n_gram_string'][0:50000] #ToDo: consider changing 

def mainz

    st.set_page_config(
     page_title="WorldCloud | n-gram Generator",
     page_icon="⛅",
     layout="wide",
     initial_sidebar_state="expanded",
    #  menu_items={
    #      'Get Help': 'https://www.extremelycoolapp.com/help',
    #      'Report a bug': "https://www.extremelycoolapp.com/bug",
    #      'About': "# This is a header. This is an *extremely* cool app!"
    #  }
    )

    st.title("⛅ WordCloud | ⛓️ n-gram Generator")
    with st.sidebar:
        st.title("Controls and Filters")
        n_gram_size = st.slider("Number of Words in N-Gram", 1, 10, 3)
        file = st.file_uploader("Add a CSV ...")
        if file:
            df = pd.read_csv(file)
            st.subheader("Filter Original Dataset")

            column_to_ngram_options = st.selectbox("Select a Column to turn into a series of n-grams", options=df.columns)


        st.write("🔍 [What is an n-gram?](https://en.wikipedia.org/wiki/N-gram)")
        st.write("📂  [GitHub repo](https://github.com/majoralex/streamlit/)")
        st.write("👨‍💻 [The Code](https://github.com/majoralex/streamlit/tree/main/wordcloud_ngram_app)")



    try:
        if file is not None and column_to_ngram_options is not None:
            with st.spinner('Working on it..'):
                n_gram_df = make_ngram(df=df, corpus_text_col=column_to_ngram_options, word_combo=n_gram_size).rename(columns={'index': 'n_grams', 0: 'count'}, inplace=False).sort_values(by=['count'], ascending=False)
                n_gram_df['n_gram_string'] = [', '.join(map(str, l)) for l in n_gram_df['n_grams']]

                
                # SCORE CARDS & METRICS
                
                col1, col2, col3, col4= st.columns((2,2,2,2))
                col1.metric("Number of Rows from File", value=f"{df.shape[0]:,}")
                col2.metric("Number of n-grams created", value=f"{n_gram_df.shape[0]:,}")
                col3.metric("Avg. Count of N-Grams", value=n_gram_df['count'].mean().round(2))
                col4.metric("Max. Count of N-Grams", value=f"{n_gram_df['count'].max().round(2):,}")

                max_ngram_count = n_gram_df['count'].max()


                corpus_text_list = ['' if pd.isnull(row) else row.lower() for row in df[column_to_ngram_options]].copy()
                # st.write(corpus_text_list)
                col1, col2, col3= st.columns((2,2,10))

                col1.download_button("Download n-gram Table", data=n_gram_df.to_csv().encode('utf-8'), file_name=f"n_grams_data_size-{n_gram_size}.csv")

                n_gram_options = st.multiselect("Select one or more n-grams (Showing top 50k n-grams)", options=n_gram_multiselect_options(n_gram_df))
                n_gram_count_slider_options = st.slider("Select the Count Range (Default showing top 70%)", min_value=1, max_value=int(max_ngram_count), value=((int(max_ngram_count*0.7)) if int(max_ngram_count*0.7) > 1 else 1, int(max_ngram_count)))
                

                if n_gram_options:
                    n_gram_df = n_gram_df.loc[(n_gram_df['n_gram_string'].isin(n_gram_options))]

                if n_gram_count_slider_options:
                    n_gram_df = n_gram_df.loc[((n_gram_df['count'] >= n_gram_count_slider_options[0]) & (n_gram_df['count'] <= n_gram_count_slider_options[1]))]
                filtered_data = []
                for n in n_gram_df['n_grams']:
                    filtered_text = [f for f in corpus_text_list if all(c in f for c in n)]
                    # st.write(text)
                    filtered_data.append(filtered_text)

                wc = make_wordcloud(filtered_data)

                col1, col2 = st.columns((2,6))
                with col1:

                    st._legacy_dataframe(n_gram_df, width=800, height=1000) # there is a bug with normal method, which truncates the table

                with col2:
                    # st.empty()
                    st.image(wc.to_array(), use_column_width=True)
                    
        else: 
            st.subheader("Upload a file to begin!")
            st.success("Please add a **CSV file** in the Sidebar to get started...", icon="🚦")
    except AttributeError:
        st.error('Looks like the column selected in the sidebar is being read as a Number or the data is not in the **First Row** of the file. \n\n     Try selecting a different column in the sidebar or re-formatting your file.', icon="🚨")
    except ValueError:
        st.error('Looks like there is no data from the filters. \n\n     Try selecting adjusting the slider or the selectbox to show results.', icon="🚨")



    
if __name__ == "__main__":

    main()
