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
    col1, col2 = st.columns((1, 1))
    if radio_button_1 == radio_options[0]:
        file = col1.file_uploader(label='Select a file')
        st.markdown("***")
        if file is not None:
            df = pd.read_excel(file, engine='openpyxl')
            col1.multiselect("Multiselect", df.columns.values)
            col1 = st.markdown("***")
            col1.write(df)
        else:
            col1.write("")
    elif radio_button_1 == radio_options[1]:

        file_1 = col1.file_uploader(label='Select a file')
        file_2 = col2.file_uploader(label='Select another file')

        if file_1 is not None and file_2 is not None:

            first_df = pd.read_excel(file_1, engine='openpyxl')
            second_df = pd.read_excel(file_2, engine='openpyxl')
            # option_1 = col1.multiselect("Multiselect", [*df_1.columns.values, *df_2.columns.values]
            option_1 = col1.selectbox("Select header from first file", convert_tuple(first_df.columns.values))
            option_2 = col2.selectbox("Select header from second file", convert_tuple(second_df.columns.values))
            col1, col2 = st.columns((1, 1))
            df = find_similarities(df_1=first_df, df_2=second_df, match_on=[option_1, option_2], set_similarity_threshold=0.7, set_record_limit=3)
            st.write(df)
            # col1.write(df_1)
            # col2.write(df_2)
        else:
            st.markdown("***")


    # print(dir(st))


if __name__ == "__main__":
    main()

