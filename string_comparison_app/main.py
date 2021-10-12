import streamlit as st
import pandas as pd
import textdistance
from streamlit_scripts import find_similarities

# df = pd.DataFrame()
# data = {
#     'column_1': 'data',
#     'column_2': 'data',
#     'column_3': 'data',
#     'column_4': 'data'
# }
# df = df.append(data, ignore_index=True)
#
# st.write("Hello World")
# st.write(test())

def v_spacer(height, sb=False) -> None:
    for _ in range(height):
        if sb:
            st.sidebar.write('\n')
        else:
            st.write('\n')

def convert_tuple(list):
    return (*list, )

def main():

    st.set_page_config(layout="wide")
    radio_options = ['1 Excel File', '2 Excel File']
    radio_button_1 = st.sidebar.radio("Select an Option", radio_options)
    edit_based_algorithms ={'Hamming': 'hamming',
                            'MLIPNS': 'mlipns',
                            'Levenshtein': 'levenshtein',
                            'Damerau-Levenshtein': 'damerau_levenshtein',
                            'Jaro-Winkler': 'jaro_winkler',
                            'Strcmp95': 'strcmp95',
                            'Needleman-Wunsch': 'needleman_wunsch',
                            'Gotoh': 'gotoh',
                            'Smith-Waterman': 'smith_waterman'
                            }
    # token_based_algorithms = ['Hamming', 'MLIPNS', 'Levenshtein', 'Damerau-Levenshtein','Jaro-Winkler', 'Strcmp95', 'Needleman-Wunsch', 'Gotoh']


    slider_button_1 = st.sidebar.slider("Select a Similarity Threshold")
    slider_button_2 = st.sidebar.slider("Select a Record Limit", max_value=20)
    multiselect_sidebar_1 = st.sidebar.multiselect("Select one or more algorithms", edit_based_algorithms)
    # multiselect_sidebar_2 = st.sidebar.multiselect("Select one or more 'Token based' algorithms", token_based_algorithms)
    # multiselect_sidebar_3 = st.sidebar.multiselect("Select one or more 'Sequence based' algorithms", text_algorithms)
    # multiselect_sidebar_4 = st.sidebar.multiselect("Select one or more 'Compression based' algorithms", text_algorithms)
    # multiselect_sidebar_5 = st.sidebar.multiselect("Select one or more 'Phonetic' algorithms", text_algorithms)
    multiselect_algorithm_methods = list(map(edit_based_algorithms.get, multiselect_sidebar_1))

    if multiselect_sidebar_1 is not None:
        st.write(multiselect_algorithm_methods)

    col1, col2 = st.columns((1, 1))
    if radio_button_1 == radio_options[0]:
        file = col1.file_uploader(label='Select a file')
        st.markdown("***")
        if file is not None and multiselect_sidebar_1 is not None:
            df = pd.read_excel(file, engine='openpyxl')
            col1, col2 = st.columns((1, 1))
            option_1 = col1.selectbox("Select header from first file", convert_tuple(df.columns.values))
            option_2 = col2.selectbox("Select item from second file", convert_tuple(df.columns.values))

            df = find_similarities(df_1=df, df_2=df, match_on=[option_1, option_2], set_similarity_threshold=slider_button_1/100, set_record_limit=3, algo_list=multiselect_algorithm_methods)
            st.write(f"With a Similarity Threshold of {slider_button_1} and a Maximum of {slider_button_2} matches per record in the first file")
            st.write(df)
        else:
            col1.write("")
    elif radio_button_1 == radio_options[1]:

        file_1 = col1.file_uploader(label='Select a file')
        file_2 = col2.file_uploader(label='Select another file')

        if file_1 is not None and file_2 is not None and multiselect_sidebar_1 is not None:

            first_df = pd.read_excel(file_1, engine='openpyxl')
            second_df = pd.read_excel(file_2, engine='openpyxl')
            # option_1 = col1.multiselect("Multiselect", [*df_1.columns.values, *df_2.columns.values]
            option_1 = col1.selectbox("Select header from first file", convert_tuple(first_df.columns.values))
            option_2 = col2.selectbox("Select item from second file", convert_tuple(second_df.columns.values))
            col1, col2 = st.columns((1, 1))
            df = find_similarities(df_1=first_df, df_2=second_df, match_on=[option_1, option_2], set_similarity_threshold=slider_button_1/100, set_record_limit=3, algo_list=multiselect_algorithm_methods)
            col1, col2 = st.columns((5, 2))
            col1.write(f"With a Similarity Threshold of {slider_button_1} and a Maximum of {slider_button_2} matches per record in the first file")



            st.write(df.head(1000))

        else:
            st.markdown("***")


    # print(dir(st))


if __name__ == "__main__":

    main()

