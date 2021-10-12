import streamlit as st
import pandas as pd
import textdistance

# class StreamlitScripts():
#
#     def __init__(self, name):
#         self.name = name
#         self.tricks = []    # creates a new empty list for each dog
#
#     def add_trick(self, trick):
#         self.tricks.append(trick)
#
#     def test(self):
#         self.
#         return "this is a test"


def find_similarities(df_1: pd.DataFrame, df_2: pd.DataFrame, match_on: list,
    set_record_limit: int,
    set_similarity_threshold: int, # ToDo: keep in case we need
    algo_list: list):
    """
    The purpose of this script is to find the similarity between 2 strings from the textdistance library, using Levenshtein
    distancing and other algorithms.
    :param set_record_limit:
    :param set_similarity_threshold:
    :param demographic_type:
    :returns full_df, threshold_df: full_df shows the the records with the top nth records based on record limit
    threshold_df is filtered from full_df, but cuts off the dataframe depending on Levensthein ratio
    """
    similarity_df = []
    for df_2_index, df_2_row in df_2.iterrows():
        for df_1_index, df_1_row in df_1.iterrows():
            Levenshtein_sim = textdistance.levenshtein.normalized_similarity(df_2_row[match_on[1]], df_1_row[match_on[0]])

            similarity_df.append({
                'df_1_index': df_1_index,
                'df_2_index': df_2_index,
                'df_1_row': df_1_row[match_on[0]],
                'df_2_row': df_2_row[match_on[1]],
                'text_similarity': Levenshtein_sim,
                'test': algo_list[0]
            })
            # for index, item in enumerate(algo_list):
            #     similarity_df[f"{algo_list[index]}"].append(algo_list[item])
            # similarity_df[f"{algo_list[item]}"] = algo_list[index]

    final_df = pd.DataFrame(similarity_df).sort_values(by=['df_1_index', 'text_similarity']).drop_duplicates()
    final_df = final_df[final_df['text_similarity'].astype(float) >= set_similarity_threshold]

    # last_df = pd.DataFrame()
    # unique_df_1_index = final_df['df_1_index'].unique()
    # print(unique_df_1_index)

    # for index, row in enumerate(unique_df_1_index): # Sort by Algorithm
    #     df_loop = final_df[final_df[row]].head(set_record_limit)
    #     last_df.append(df_loop)


    return final_df


