import streamlit as st
import pandas as pd
import textdistance
from streamlit_scripts import find_similarities, textdistance_streamlit_code

import time

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
    slider_button_2 = st.sidebar.slider("Select a Record Limit", max_value=100)
    multiselect_sidebar_1 = st.sidebar.multiselect("Select one or more algorithms", edit_based_algorithms)
    # multiselect_sidebar_2 = st.sidebar.multiselect("Select one or more 'Token based' algorithms", token_based_algorithms)
    # multiselect_sidebar_3 = st.sidebar.multiselect("Select one or more 'Sequence based' algorithms", text_algorithms)
    # multiselect_sidebar_4 = st.sidebar.multiselect("Select one or more 'Compression based' algorithms", text_algorithms)
    # multiselect_sidebar_5 = st.sidebar.multiselect("Select one or more 'Phonetic' algorithms", text_algorithms)
    multiselect_algorithm_methods = list(map(edit_based_algorithms.get, multiselect_sidebar_1))
    new_title = '<p style="font-family:sans-serif; color:Red; font-size: 60px;">textdistance app</p>'
    col1, col2, col3 = st.columns((2, 1, 1))

    col1.markdown(new_title, unsafe_allow_html=True)
    with col2.expander("About this App"):
        st.subheader("Goal")
        st.write("""The purpose of this app is to democratize the use of the [textdistance library](https://pypi.org/project/textdistance/). The script in the background
        takes one or more tabular datasets **(-> DataFrames)**, processes the data based on user specifications in the sidebar and the fields chosen to measure. 
        The *find_similarities()* function found at the bottom of this app to get the """)
        st.subheader("Outcomes")
        st.write("(A) Normalized Similarity of 2 Fields with one or more algorithms from the textdistance library.")
        st.write("(B) A downloadable CSV of the Output")
    with col3.expander("How to use this app"):
        st.subheader("Files")
        st.write("""(A) The files can be excel and/or csv.""")
        st.write("""(B) If your data is not on the first row of the data, make sure to specify the starting row of the data in the expander below their respective file upload component""")
        st.write("""(C) This app uses the first file as a *base*, to match against the selected field from the second file""")
        st.subheader("Parameters")
        st.write("(A) **Similarity Threshold**: this is the normalized similarity between")
        st.write("(B) **Record Limit**: this is the normalized similarity between")
        st.write("(C) **Algorithms**: [This is a list of availble algorithms and all methods](https://pypi.org/project/textdistance/)")


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
        col1, col2, col3, col4 = st.columns((2, 1, 2, 1))

        file_1 = col1.file_uploader(label='Select a file')

        file_2 = col3.file_uploader(label='Select another file')

        col1, col2, col3, col4 = st.columns((3, 1, 3, 1))
        with col1.expander("Customize file #1 upload"):
            st.number_input("Enter in starting row ", 0)
        with col3.expander("Customize file #2 upload"):
            st.number_input("Enter in starting row  ", 0)

        if file_1 is not None and file_2 is not None and multiselect_sidebar_1 is not None:
            first_df = pd.read_excel(file_1, engine='openpyxl')
            second_df = pd.read_excel(file_2, engine='openpyxl')
            # option_1 = col1.multiselect("Multiselect", [*df_1.columns.values, *df_2.columns.values]
            col1, col2, col3, col4 = st.columns((1.5, 2, 1.5, 2))
            option_1 = col1.selectbox("Select header from first file", convert_tuple(first_df.columns.values))
            option_2 = col3.selectbox("Select item from second file", convert_tuple(second_df.columns.values))
            col1, col2, col3 = st.columns((1, 1, 5))
            if col1.button('Refresh Data'):
                if multiselect_sidebar_1:
                    with st.spinner(text='Hold on, trying to match your data...'):
                        df = find_similarities(df_1=first_df, df_2=second_df, match_on=[option_1, option_2], set_similarity_threshold=slider_button_1/100, set_record_limit=slider_button_2, algo_list=multiselect_algorithm_methods)
                            # df = find_similarities(df_1=first_df, df_2=second_df, match_on=[option_1, option_2], set_similarity_threshold=slider_button_1/100, set_record_limit=3, algo_list=multiselect_algorithm_methods)
                        # col1, col2 = st.columns((5, 2))

                        col2.download_button(label="Download Data", data=df.to_csv().encode('utf-8'),
                                             file_name='textdistance_streamlit_output.csv', mime='text/csv')
                        output_result = f'<p style="font-family:sans-serif; color:Red; font-size: 16px;">Similarity Threshold of {slider_button_1} | Record limit of {slider_button_2}</p>'
                        st.markdown(output_result, unsafe_allow_html=True)
                        st.write(df)
                        st.balloons()
                else:
                    st.error("Please select a textdistance algorithm from the sidebar!")





        else:
            st.markdown("***")
            with st.expander("View Source Code"):
                st.code(textdistance_streamlit_code(), language='python')


    # print(dir(st))


if __name__ == "__main__":

    main()

