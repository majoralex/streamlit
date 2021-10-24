import pandas as pd
import textdistance


def find_similarities(df_1: pd.DataFrame, df_2: pd.DataFrame, match_on: list,
                      set_record_limit: int,
                      set_similarity_threshold: int,
                      algo_list: list,
                      algo_method: list):
    """
    The purpose of this script is to find the similarity between 2 strings from the textdistance library, using Levenshtein
    distancing and other algorithms.
    :param algo_method:
    :param algo_list:
    :param match_on:
    :param df_2:
    :param df_1:
    :param set_record_limit:
    :param set_similarity_threshold:
    :param demographic_type:
    :returns full_df, threshold_df: full_df shows the the records with the top nth records based on record limit
    threshold_df is filtered from full_df, but cuts off the dataframe depending on Levensthein ratio
    """

    similarity_df = []
    final_df = pd.DataFrame
    for df_2_index, df_2_row in df_2.iterrows():
        for df_1_index, df_1_row in df_1.iterrows():
            # first_algo = eval(
            #     f"textdistance.{algo_list[0]}.normalized_similarity(df_2_row[match_on[1]], df_1_row[match_on[0]])")
            similarity_df.append({
                f'{match_on[0]}_index': df_1_index,
                f'{match_on[1]}_index': df_2_index,
                match_on[0]: df_1_row[match_on[0]],
                match_on[1]: df_2_row[match_on[1]],
                f'{algo_list[0]}_score': 3,
            })

    final_df = pd.DataFrame(similarity_df).sort_values(by=[f'{match_on[0]}_index', f'{algo_list[0]}_score'],
                                                       ascending=[True, False]).drop_duplicates()

    for index, row in final_df.iterrows():
        for algo_index, algo in enumerate(algo_list):
            for algo_method_index, algo_method_item in enumerate(algo_method):
                algo_output = eval(
                    f"textdistance.{algo_list[algo_index]}.{algo_method[algo_method_index]}(final_df[match_on[0]][{index}], final_df[match_on[1]][{index}])")
                # print(f'{algo_list[algo_index]}_score', algo, "Output -> ", algo_output)
                final_df.at[index, f'{algo}_{algo_method_item}'] = algo_output

    final_df = final_df[final_df[f'{algo_list[0]}_score'].astype(float) >= set_similarity_threshold]
    grouped_df = final_df.groupby(f'{match_on[0]}_index')
    final_df_record_limit = grouped_df.head(set_record_limit)

    return final_df_record_limit


def textdistance_streamlit_code():
    return """
                def find_similarities(df_1: pd.DataFrame, df_2: pd.DataFrame, match_on: list,
                    set_record_limit: int,
                    set_similarity_threshold: int,
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
                                f'{match_on[0]}_index': df_1_index,
                                f'{match_on[1]}_index': df_2_index,
                                match_on[0]: df_1_row[match_on[0]],
                                match_on[1]: df_2_row[match_on[1]],
                                'levenstethin_test': textdistance.levenshtein.normalized_similarity(df_2_row[match_on[1]], df_1_row[match_on[0]]),
                                f'{algo_list[0]}_score': first_algo,
                            })
                
                    final_df = pd.DataFrame(similarity_df).sort_values(by=[f'{match_on[0]}_index', f'{algo_list[0]}_score'], ascending=[True, False]).drop_duplicates()
                
                    for index, row in final_df.iterrows():
                        for algo_index, algo in enumerate(algo_list):
                            algo_output = eval(
                                f"textdistance.{algo_list[algo_index]}.normalized_similarity(final_df[match_on[0]][{index}], final_df[match_on[1]][{index}])")
                            print(f'{algo_list[algo_index]}_score', algo, "Output -> ", algo_output)
                            final_df.at[index, f'{algo}_score'] = algo_output
                
                    final_df = final_df[final_df[f'{algo_list[0]}_score'].astype(float) >= set_similarity_threshold]
                    grouped_df = final_df.groupby(f'{match_on[0]}_index')
                    final_df_record_limit = grouped_df.head(set_record_limit)
                    return final_df_record_limit
                """
