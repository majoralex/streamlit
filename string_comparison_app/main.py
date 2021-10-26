import streamlit as st
import pandas as pd
import textdistance
from streamlit_scripts import find_similarities, textdistance_streamlit_code


def convert_tuple(list):
    return (*list, )

def main():

    st.set_page_config(layout="wide")
    radio_options = ['1 Excel or CSV File', '2 Excel and/or CSV Files']
    radio_button_1 = st.sidebar.radio("Select an Option", radio_options)


    dict_algorithms ={'Hamming': 'hamming',
                            'MLIPNS': 'mlipns',
                            'Levenshtein': 'levenshtein',
                            'Damerau-Levenshtein': 'damerau_levenshtein',
                            'Jaro-Winkler': 'jaro_winkler',
                            'Strcmp95': 'strcmp95',
                            'Needleman-Wunsch': 'needleman_wunsch',
                            'Gotoh': 'gotoh',
                            'Smith-Waterman': 'smith_waterman',
                            'Jaccard': 'jaccard',
                            'Sørensen–Dice coefficient': 'sorensen',
                            'Tversky index': 'tversky',
                            'Overlap coefficient': 'overlap',
                            'Tanimoto distance': 'tanimoto',
                            'Cosine similarity': 'cosine',
                            'Monge-Elkan': 'monge_elkan',
                            'Bag distance': 'bag',
                            'longest common subsequence similarity': 'lcsseq',
                            'longest common substring similarity': 'lcsstr',
                            'Ratcliff-Obershelp similarity': 'ratcliff_obershelp',
                            'Arithmetic coding': 'arith_ncd',
                            'RLE': 'rle_ncd',
                            'BWT RLE': 'bwtrle_ncd',
                            'Square Root': 'sqrt_ncd',
                            'Entropy': 'entropy_ncd',
                            'BZ2': 'bz2_ncd',
                            'LZMA': 'lzma_ncd',
                            'ZLib': 'zlib_ncd',
                            'MRA': 'mra',
                            'Editex': 'editex',
                            'Prefix similarity': 'prefix',
                            'Postfix similarity': 'postfix',
                            'Length distance': 'length',
                            'Identity similarity': 'identity',
                            'Matrix similarity': 'matrix'
                        }
    dict_algorithm_methods ={
                            'Normalized Similarity': 'normalized_similarity',
                            'Normalized distance': 'normalized_distance',
                            'Distance': 'distance',
                            'Similarity': 'similarity',
                            'Maximum': 'maximum',
                            }



    slider_button_1 = st.sidebar.slider("Select a Similarity Threshold minimum (0 - 1)")
    slider_button_2 = st.sidebar.slider("Select a Record Limit", min_value=1, max_value=100)
    multiselect_sidebar_1 = st.sidebar.multiselect("Select one or more algorithms", dict_algorithms)
    multiselect_sidebar_2 = st.sidebar.multiselect("Select one or more algorithm methods", dict_algorithm_methods, default=["Normalized Similarity"])

    st.sidebar.markdown("\n\n\n\n***")
    with st.sidebar.expander("Resources"):
        st.write("1. [TextDistance GitHub](https://github.com/life4/textdistance)")
        st.write("2. [String similarity — the basic know your algorithms guide!](https://itnext.io/string-similarity-the-basic-know-your-algorithms-guide-3de3d7346227)")
        st.write("3. [Guide to Fuzzy Matching with Python](http://theautomatic.net/2019/11/13/guide-to-fuzzy-matching-with-python/)")

    multiselect_algorithms = list(map(dict_algorithms.get, multiselect_sidebar_1))
    multiselect_algorith_methods = list(map(dict_algorithm_methods.get, multiselect_sidebar_2))
    new_title = '<p style="font-family:sans-serif; color:Red; font-size: 60px;">TextDistance App</p>'
    col1, col2, col3 = st.columns((2, 1, 1))

    col1.markdown(new_title, unsafe_allow_html=True)
    with col2.expander("About this App"):
        st.subheader("Goal")
        st.write("""The purpose of this app is to democratize the use of the 
        [textdistance library](https://pypi.org/project/textdistance/). The script in the background
        takes one or more datasets in an Excel or CSV format, processes the data based on user specifications in the 
        sidebar and the fields chosen to measure below the file upload components. The *find_similarities()* function at
         the bottom of this app is the logic that this app uses to compare 2 fields. """)
        st.subheader("Outcomes")
        st.write("(A) Access to 30+ algorithms for comparing distance between two or more sequences.")
        st.write("(B) A downloadable CSV of the Output with all of the desired algorithms and algorithm methods from "
                 "the sidebar")
    with col3.expander("How to use this app"):
        st.subheader("Data")
        st.write("""(A) The files can be excel and/or csv.""")
        st.write("""(B) If your data is not on the first row of the data, make sure to specify the starting row of the data in the expander below their respective file upload component""")
        st.write("""(C) This app uses the first file, algorithm, and algorithm method from the inputs as the values
        being search and sorted by in the output. For example, if the first inputs from the sidebar are Levenshtein and Normalized Similarity,
        the record limit and similarity threshold would be based on the top matches from the Levenshtein Normalized similarity.""")
        st.subheader("Parameters")
        st.write("""(A) **Algorithm Method  Threshold**: """)
        st.write("* Distance: calculate distance between sequences.")
        st.write("* Similarity: calculate similarity for sequences.")
        st.write("* Maximum: maximum possible value for distance and similarity. For any sequence: distance + similarity == maximum.")
        st.write("* Normalized Distance: normalized distance between sequences. The return value is a float between 0 and 1, where 0 means equal, and 1 totally different.")
        st.write("* Normalized Similarity: normalized similarity for sequences. The return value is a float between 0 and 1, where 0 means totally different, and 1 equal.")

        st.write("(C) **Algorithms**: [This is a list of availble algorithms and all methods](https://pypi.org/project/textdistance/)")

    if radio_button_1 == radio_options[0]:
        col1, col2, col3, col4 = st.columns((5, 1.5, 2, 1.5))

        xlsx_csv_radio = col1.radio("Select Excel or CSV", ['Excel', 'CSV'])
        with col1.expander("Customize file #1 upload"):
            header_file = st.number_input("Enter in starting row ", 0)
        file = col1.file_uploader(label='Select a file')
        if file is not None and multiselect_sidebar_1 is not None:

            if xlsx_csv_radio == 'Excel':
                one_file_df = pd.read_excel(file, skiprows=int(header_file), engine='openpyxl')
            else:
                pass
            if xlsx_csv_radio == 'CSV':
                one_file_df = pd.read_csv(file, encoding = 'latin-1', engine ='c')
            else:
                pass

            col1, col2, col3, col4 = st.columns((1.5, 2, 1.5, 2))
            option_1 = col1.selectbox("Select header from first file", convert_tuple(one_file_df.columns.values), key=222)
            option_2 = col3.selectbox("Select header from second file", convert_tuple(one_file_df.columns.values))
            col1, col2, col3 = st.columns((1, 1, 5))
            if col1.button('Refresh Data'):
                if multiselect_sidebar_1:
                    with st.spinner(text='Hold on, trying to match your data...'):
                        df = find_similarities(df_1=one_file_df, df_2=one_file_df, match_on=[option_1, option_2],
                                               set_similarity_threshold=slider_button_1 / 100,
                                               set_record_limit=slider_button_2, algo_list=multiselect_algorithms,
                                               algo_method=multiselect_algorith_methods)

                        col2.download_button(label="Download Data", data=df.to_csv().encode('utf-8'),
                                             file_name='textdistance_streamlit_output.csv', mime='text/csv')
                        output_result = f'<p style="font-family:sans-serif; color:Red; font-size: 16px;">Similarity Threshold of {slider_button_1} | Record limit of {slider_button_2} | Length of New Dataset {df.shape[0]}</p>'
                        st.markdown(output_result, unsafe_allow_html=True)
                        st.write(df)
                    st.balloons()
                else:
                    st.error("Please select a textdistance algorithm from the sidebar!")

        st.markdown("***")
        with st.expander("View Source Code"):
            st.code(textdistance_streamlit_code(), language='python')
    elif radio_button_1 == radio_options[1]:
        col1, col2, col3, col4 = st.columns((2, 1.5, 2, 1.5))

        xlsx_csv_radio_1 = col1.radio("Select Excel or CSV", ['Excel', 'CSV'])
        with col1.expander("Customize file #1 upload"):
            header_file_1 = st.number_input("Enter in starting row ", value=0)
        file_1 = col1.file_uploader(label='Select a spreadsheet file')

        xlsx_csv_radio_2 = col3.radio("Select Excel or CSV ", ['Excel', 'CSV'])
        with col3.expander("Customize file #2 upload"):
            header_file_2 = st.number_input("Enter in starting row  ",value=0)
        file_2 = col3.file_uploader(label='Select a second spreadsheet')


        if file_1 is not None and file_2 is not None and multiselect_sidebar_1 is not None:

            if xlsx_csv_radio_1 == 'Excel':
                first_df = pd.read_excel(file_1, skiprows=int(header_file_1), engine='openpyxl')
            else:
                pass
            if xlsx_csv_radio_2 == 'Excel':
                second_df = pd.read_excel(file_2, skiprows=int(header_file_2), engine='openpyxl')
            else:
                pass

            if xlsx_csv_radio_1 == 'CSV':
                first_df = pd.read_csv(file_1, encoding = 'latin-1', engine ='c')
            else:
                pass
            if xlsx_csv_radio_2 == 'CSV':
                second_df = pd.read_csv(file_2, encoding = 'latin-1', engine ='c')
            else:
                pass

            st.markdown("***")

            col1, col2, col3, col4 = st.columns((1.5, 2, 1.5, 2))
            option_1 = col1.selectbox("Select header from first file", convert_tuple(first_df.columns.values), key=111)
            option_2 = col3.selectbox("Select header from second file", convert_tuple(second_df.columns.values), key=110)
            col1, col2, col3 = st.columns((1, 1, 5))
            if col1.button('Refresh Data'):
                if multiselect_sidebar_1:

                    with st.spinner(text='Hold on, trying to match your data...'):
                        df = find_similarities(df_1=first_df, df_2=second_df, match_on=[option_1, option_2], set_similarity_threshold=slider_button_1/100, set_record_limit=slider_button_2, algo_list=multiselect_algorithms, algo_method=multiselect_algorith_methods)

                        col2.download_button(label="Download Data", data=df.to_csv().encode('utf-8'),
                                             file_name='textdistance_streamlit_output.csv', mime='text/csv')
                        output_result = f'<p style="font-family:sans-serif; color:Red; font-size: 16px;">Similarity Threshold of {slider_button_1} | Record limit of {slider_button_2} | Length of New Dataset {df.shape[0]}</p>'
                        st.markdown(output_result, unsafe_allow_html=True)
                        st.write(df)
                        st.markdown("***")
                        with st.expander("View Source Code"):
                            st.code(textdistance_streamlit_code(), language='python')
                        st.balloons()
                else:
                    st.error("Please select a textdistance algorithm from the sidebar!")
        else:
            st.markdown("***")
            with st.expander("View Source Code"):
                st.code(textdistance_streamlit_code(), language='python')

if __name__ == "__main__":

    main()

