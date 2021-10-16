import streamlit as st
import pandas as pd
import textdistance


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
            first_algo = eval(
                f"textdistance.{algo_list[0]}.normalized_similarity(df_2_row[match_on[1]], df_1_row[match_on[0]])")

            similarity_df.append({
                'df_1_index': df_1_index,
                'df_2_index': df_2_index,
                match_on[0]: df_1_row[match_on[0]],
                match_on[1]: df_2_row[match_on[1]],
                f'{algo_list[0]}_score': first_algo,
            })

    final_df = pd.DataFrame(similarity_df).sort_values(by=['df_1_index', f'{algo_list[0]}_score']).drop_duplicates()

    for index, row in final_df.iterrows():
        for algo_index, algo in enumerate(algo_list):
            algo_output = eval(
                f"textdistance.{algo_list[algo_index]}.normalized_similarity(final_df[match_on[0]][{index}], final_df[match_on[1]][{index}])")
            print(f'{algo_list[algo_index]}_score', algo, "Output -> ", algo_output)
            final_df.at[index, f'{algo}_score'] = algo_output

    final_df = final_df[final_df[f'{algo_list[0]}_score'].astype(float) >= set_similarity_threshold]

    return final_df

def textdistance_streamlit_code():
    return """
                import streamlit as st
                import pandas as pd
                import textdistance
                
                
                def find_similarities(df_1: pd.DataFrame, df_2: pd.DataFrame, match_on: list,
                    set_record_limit: int,
                    set_similarity_threshold: int, # ToDo: keep in case we need
                    algo_list: list):
                    \"""
                    The purpose of this script is to find the similarity between 2 strings from the textdistance library, using Levenshtein
                    distancing and other algorithms.
                    :param set_record_limit:
                    :param set_similarity_threshold:
                    :param demographic_type:
                    :returns full_df, threshold_df: full_df shows the the records with the top nth records based on record limit
                    threshold_df is filtered from full_df, but cuts off the dataframe depending on Levensthein ratio
                    \"""
                    similarity_df = []
                    for df_2_index, df_2_row in df_2.iterrows():
                        for df_1_index, df_1_row in df_1.iterrows():
                            first_algo = eval(
                                f"textdistance.{algo_list[0]}.normalized_similarity(df_2_row[match_on[1]], df_1_row[match_on[0]])")
                
                            similarity_df.append({
                                'df_1_index': df_1_index,
                                'df_2_index': df_2_index,
                                match_on[0]: df_1_row[match_on[0]],
                                match_on[1]: df_2_row[match_on[1]],
                                f'{algo_list[0]}_score': first_algo,
                            })
                
                    final_df = pd.DataFrame(similarity_df).sort_values(by=['df_1_index', f'{algo_list[0]}_score']).drop_duplicates()
                
                    for index, row in final_df.iterrows():
                        for algo_index, algo in enumerate(algo_list):
                            algo_output = eval(
                                f"textdistance.{algo_list[algo_index]}.normalized_similarity(final_df[match_on[0]][{index}], final_df[match_on[1]][{index}])")
                            print(f'{algo_list[algo_index]}_score', algo, "Output -> ", algo_output)
                            final_df.at[index, f'{algo}_score'] = algo_output
                
                    final_df = final_df[final_df[f'{algo_list[0]}_score'].astype(float) >= set_similarity_threshold]
                
                    return final_df
                """

