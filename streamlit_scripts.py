import pandas as pd
import textdistance


def find_similarities(df_1: pd.DataFrame, df_2: pd.DataFrame, match_on: list,
                      set_record_limit: int,
                      set_similarity_threshold: int,
                      algo_list: list,
                      algo_method: list) -> pd.DataFrame:
    """
    The purpose of this script is to find the similarity between 2 text columns from a DataFrame using the textdistance
    library.
    :param algo_method: list of algorithm methods
    :param algo_list: list of algorithms functions Not Classes
    :param match_on: a list of the two desired headers to perform matching
    :param df_1: the first DataFrame to match
    :param df_2: the second DataFrame to match against the first
    :param set_record_limit: the number of desired matched for df_1's header, algorithm type, and method
    :param set_similarity_threshold: a number from 0 - 1, this dooes not work with the methods that return results > 1
    :returns final_df_record_limit: a DataFrame with the matched data and their respective scores given their methods
    """
    similarity_df = []
    for df_2_index, df_2_row in df_2.iterrows():
        for df_1_index, df_1_row in df_1.iterrows():
            first_algo = eval(
                f"textdistance.{algo_list[0]}.{algo_method[0]}(df_2_row[match_on[1]], df_1_row[match_on[0]])")
            similarity_df.append({
                f'{match_on[0]}_index': df_1_index,
                f'{match_on[1]}_index': df_2_index,
                match_on[0]: df_1_row[match_on[0]],
                match_on[1]: df_2_row[match_on[1]],
                f'{algo_list[0]}_{algo_method[0]}': first_algo,
            })

    final_df = pd.DataFrame(similarity_df).sort_values(by=[f'{match_on[0]}_index', f'{algo_list[0]}_{algo_method[0]}'],
                                                       ascending=[True, False]).drop_duplicates()

    for index, row in final_df.iterrows():
        for algo_index, algo in enumerate(algo_list):
            for algo_method_index, algo_method_item in enumerate(algo_method):
                algo_output = eval(
                    f"textdistance.{algo_list[algo_index]}.{algo_method[algo_method_index]}(final_df[match_on[0]][{index}], final_df[match_on[1]][{index}])")
                final_df.at[index, f'{algo}_{algo_method_item}'] = algo_output

    final_df = final_df[final_df[f'{algo_list[0]}_{algo_method[0]}'].astype(float) >= set_similarity_threshold]
    grouped_df = final_df.groupby(f'{match_on[0]}_index')
    final_df_record_limit = grouped_df.head(set_record_limit)

    return final_df_record_limit


def textdistance_streamlit_code():
    return """
            def find_similarities(df_1: pd.DataFrame, df_2: pd.DataFrame, match_on: list,
                                  set_record_limit: int,
                                  set_similarity_threshold: int,
                                  algo_list: list,
                                  algo_method: list) -> pd.DataFrame:
                ""\"
                The purpose of this script is to find the similarity between 2 text columns from a DataFrame using the textdistance 
                library.     
                :param algo_method: list of algorithm methods
                :param algo_list: list of algorithms functions Not Classes
                :param match_on: a list of the two desired headers to perform matching
                :param df_1: the first DataFrame to match
                :param df_2: the second DataFrame to match against the first
                :param set_record_limit: the number of desired matched for df_1's header, algorithm type, and method
                :param set_similarity_threshold: a number from 0 - 1, this dooes not work with the methods that return results > 1
                :returns final_df_record_limit: a DataFrame with the matched data and their respective scores given their methods
                
                ""\"
                similarity_df = []
                for df_2_index, df_2_row in df_2.iterrows():
                    for df_1_index, df_1_row in df_1.iterrows():
                        first_algo = eval(
                            f"textdistance.{algo_list[0]}.{algo_method[0]}(df_2_row[match_on[1]], df_1_row[match_on[0]])")
                        similarity_df.append({
                            f'{match_on[0]}_index': df_1_index,
                            f'{match_on[1]}_index': df_2_index,
                            match_on[0]: df_1_row[match_on[0]],
                            match_on[1]: df_2_row[match_on[1]],
                            f'{algo_list[0]}_{algo_method[0]}': first_algo,
                        })
            
                final_df = pd.DataFrame(similarity_df).sort_values(by=[f'{match_on[0]}_index', f'{algo_list[0]}_{algo_method[0]}'],
                                                                   ascending=[True, False]).drop_duplicates()
            
                for index, row in final_df.iterrows():
                    for algo_index, algo in enumerate(algo_list):
                        for algo_method_index, algo_method_item in enumerate(algo_method):
                            algo_output = eval(
                                f"textdistance.{algo_list[algo_index]}.{algo_method[algo_method_index]}(final_df[match_on[0]][{index}], final_df[match_on[1]][{index}])")
                            final_df.at[index, f'{algo}_{algo_method_item}'] = algo_output
            
                final_df = final_df[final_df[f'{algo_list[0]}_{algo_method[0]}'].astype(float) >= set_similarity_threshold]
                grouped_df = final_df.groupby(f'{match_on[0]}_index')
                final_df_record_limit = grouped_df.head(set_record_limit)
            
                return final_df_record_limit
                
                
                
                
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
                """
