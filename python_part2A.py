import pandas as pd
import numpy as np


def get_total_rows(df):
    '''
    :param df: pd.Dataframe in format_1
    :return: int
    '''
    totalRows=df.shape[0]
    return (totalRows)


def get_sorted_columns(df):
    '''
    :param df: pd.Dataframe in format_1
    :return: list
    '''
    sortedCol=sorted(df.columns)
    return sortedCol


def count_unique_values(df):
    '''
    :param df: pd.Dataframe in format_1
    :return: pd.Series
    '''
    #sr=pd.Series(df.columns).value_counts()
    sr=df.apply(pd.Series.nunique)
    return sr


def get_index_as_list(df, column_index):
    '''
    :param df: pd.Dataframe in format_1
    :param column_index: boolean, if True returns the column index, otherwise, the row index
    :return:
    '''
    if (column_index):
        return list(df.columns)
    else:
        return list(range(len(df.columns)))


def find_min_year(df):
    '''
    computes the smallest year value in df
    :param df: pd.Dataframe in format_1
    :return: np.int64
    '''
    return df.agg({'Year':'min'})[0]


def apply_fun_over_numric_columns(df, columns, fun):

    '''
    applies function fun over the columns of df
    :param df:  df: pd.Dataframe in format_1
    :param columns: list of columns that fun should be applied over
    :param fun: a numpy function from the following list:
        np.prod, np.std ,np.var , np.sum , np.min, np.max, np.mean , np.median
    :return: a pd.Series: its index is columns; its values if the result of applying fun over the selected columns;
    '''
    for col in columns:
        if col not in df.columns:
            raise ValueError("value is not in columns of Dataframe")
        elif np.issubdtype(df[str(col)].dtype, np.number)==False:
            raise ValueError("non-numeric column")
    if fun not in [np.prod, np.std, np.var, np.sum, np.min, np.max, np.mean, np.median]:
        raise ValueError("Invalid function! function must be one of np.prod, np.std, np.var, np.sum, np.min,np.max, np.mean, np.median")

    sr = df[columns].apply(fun)
    return sr



# def apply_fun_over_numric_columns(df, columns, fun):
#
#     '''
#
#     :param df:  df: pd.Dataframe in format_1
#     :param columns: list of columns that fun should be applied over
#     :param fun: a numpy function from the following list:
#         np.prod, np.std ,np.var , np.sum , np.min, np.max, np.mean , np.median
#     :return: a pd.Series: its index is columns; its values is the result of applying fun over the selected columns;
#     '''
#     pass
def reshapeDataFrame(df,str):
    df_quantity=df[df["Element"].str.contains(str+" Quantity")]
    df_quantity = df_quantity.drop(labels=["Element"], axis=1)
    df_value=df[df["Element"].str.contains(str+" Value")]
    df_value=df_value.drop(labels=["Element"],axis=1)
    df_merged=pd.merge(df_quantity,df_value,on=["Area","Item","Year"])
    df_merged=df_merged.rename(columns={"Value_x":"Quantity(tons)","Value_y":"Price(k,usd)"})
    df_merged=df_merged.drop(axis=1,labels={"Unit_x","Unit_y"})
    df_merged["Element"]=str

    return df_merged







def reshape(df):
    '''
    The function joins rows that share ('area', 'item', 'year')
    if they are of export type or of import type, see desc. in pdf.
    Rows that only have a single export / import values are removed;
    :param df: pd.Dataframe of format_1
    :return: a pd.Dataframe of format_2
    '''
    df_imp=reshapeDataFrame(df,"Import")
    df_exp=reshapeDataFrame(df,"Export")
    return pd.concat([df_imp,df_exp])



def validate(df):

    assert(df.shape == (5128759, 6))
    assert(pd.Series(df.columns == pd.Index(['Area', 'Item', 'Year', 'Quantity(tons)', 'Price(k,usd)', 'Element'],
                                      dtype='object')).all())


if __name__ == '__main__':

    # PART A
    df = pd.read_pickle('data.pickle') ## 'data_projected.pickle'

    # A. 1
    total_rows = get_total_rows(df)
    # A. 2
    columns_sorted = get_sorted_columns(df)
    # A. 3
    columns_sums_ = count_unique_values(df)
    # A. 4
    res1 = get_index_as_list(df, True)
    res2 = get_index_as_list(df, False)

    # A. 5
    year = find_min_year(df)
    # A. 6
    columns = ["Value", "Year"]
    year_value_means = apply_fun_over_numric_columns(df, columns, np.mean)
    columns = ["Year"]
    max_val = apply_fun_over_numric_columns(df, columns, np.max)

    # PART B
    df_r = reshape(df)
    validate(df_r)
    pd.to_pickle(df_r, "fixed_df.pickle")
