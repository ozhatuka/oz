import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

def find_most_frequent_year(df, n):
    '''
    :param df: pd.Dataframe
    :param n: positive, integer;  n'th most frequent year
    :return: int; the n'th most frequent year
    :raise: ValueError - if n is not a positive int
    '''
    if isinstance(n, int) == False or n<=0:
        raise ValueError("n must be a strictly positive integer (>0)")
    return (df['Year'].value_counts(sort=True, ascending=False)).keys()[n-1]


def filterby_criteria(df, criteria):
    '''
        The function filters all rows that do not have values
        that are included in the dict criteria
    :param df: pd.dataframe of in format_2
    :param criteria: a dictionary mapping columns to values to keep;
    key � is a column name; values is a values list
    :return: a df without the rows that do not include the specified values
    :raise: ValueError if key is not in dataframe
    '''
    if criteria=={}:
        return
    df_col=(sorted(list(df.columns)))
    for key in criteria.keys():
        if key < df_col[0] or key > df_col[len(df_col) - 1]:
             raise ValueError(key, " is not a column in df")
        for col in df_col:
            if key<col:
                raise ValueError(key, " is not a column in df")
            if key==col:
                break

    keys_in_df= df[list(criteria.keys())].isin(criteria)
    return df[keys_in_df.all(1)]





def find_extremes(df, fun=np.sum, by_item=True, by_value=True, n=5):
    '''
    :param df: pd.DataFrame in format_2; only including importing/exporting rows
    :param by_item: If True group rows by item, otherwise by Area
    :param by_value: If True should find the n most extreme items by value, otherwise by quantity
    :param fun:  a function to be applied, one of: np.prod(),np.std(),np.var(),
    np.sum(), np.min(), np.max(), np.mean(), np.midian()
    :param n: if positive get the least extreme item, otherwise, get the most
    :return: list of the n least/most imported/exported items
    raise: ValueError if n is not an int != 0
    raise: ValueError df contains both import and export values
    raise: ValueError fun is not one of the specified above functions
    '''
    if isinstance(n, int) == False or n==0:
        raise ValueError("Error message: 'n must be an integer'")
    if (df.apply(pd.Series.nunique).Element)!=1:
        raise ValueError("Error message: 'The dataframe must only include Import or Export rows")
    if fun not in [np.prod, np.std, np.var, np.sum, np.min, np.max, np.mean, np.median]:
        raise ValueError("Invalid function! function must be one of np.prod(),np.std(),np.var(), np.sum(), np.min(), np.max(), np.mean(), np.midian()")

    if by_item:
        grpby=df.groupby(by=["Item"],sort=True).apply(fun)
    else:
        grpby=df.groupby(by=["Area"],sort=True).apply(fun)

    if by_value:
        if n>0:
            sorted_group=grpby.sort_values(by=["Price(k,usd)"],ascending=True)[:n]
        else:
            sorted_group=grpby.sort_values(by=["Price(k,usd)"],ascending=False)[:n*-1]
    else:
        if n>0:
            sorted_group=grpby.sort_values(by=["Quantity(tons)"],ascending=True)[:n]
        else:
            sorted_group=grpby.sort_values(by=["Quantity(tons)"],ascending=False)[:n*-1]

    if by_item:
        return(list(sorted_group["Item"].keys()))
    else:
        return(list(sorted_group["Area"].keys()))


def generate_scatter_import_vs_export(df, countries, year, output):
    '''
    The function produces a scatter plot of the total import/export values of the specified countries in the specified year
    :param df: a dataframe in format_2
    :param countries: a list of strings specifying countries
    :param year: int; only rows of the specified year are used
    :param output: a filename (str) to which the scatter plot is to be saved
    :return: None; saves the plot to output.png
    '''
    df_imp = filterby_criteria(df, {"Area": countries, "Year": [year], "Element": ["Import"]})
    df_exp = filterby_criteria(df, {"Area": countries, "Year": [year], "Element": ["Export"]})
    imp_grp = df_imp.groupby(by=['Area'])
    imp_grp = imp_grp['Price(k,usd)'].apply(sum)
    exp_grp = df_exp.groupby(by=['Area'])
    exp_grp = exp_grp['Price(k,usd)'].apply(sum)
    zipped = list(zip(list(imp_grp), list(exp_grp)))
    plt_df = pd.DataFrame(zipped, imp_grp.index, columns=["Export", "Import"])
    ax = plt_df.plot.scatter("Import", "Export", alpha=0.5, logx=True, logy=True)
    for i, txt in enumerate(plt_df.index):
        ax.annotate(txt, (plt_df["Import"].iat[i], plt_df["Export"].iat[i]))
    plt.title("Exports as function of imports")
    plt.savefig(output + ".png")










if __name__ == '__main__':

    LN_SEP = "\n---------------------------------------------"

    df = pd.read_pickle("fixed_df.pickle")
    # PART C
    # C. 1
    year1 = find_most_frequent_year(df, 1)
    year2 = find_most_frequent_year(df, 4)
    print('year1, year2:', year1, year2)

    # PART C
    # C. 2
    df_isr75_export = filterby_criteria(df, {"Area": ["Israel"], "Year": [1975], "Element":["Export"]})
    df_isr13_export = filterby_criteria(df, {"Area": ["Israel"], "Year": [2013], "Element": ["Export"]})



    # PART C
    # C. 3
    most_items = find_extremes(df_isr75_export, by_item=True, by_value=True, n=-5)
    print("most exported items from israel 2013 by value:\n", "\n".join(most_items), LN_SEP)
    most_items = find_extremes(df_isr13_export, by_item=True, by_value=False, n=-5)
    print("most exported items from israel 2013 by quantity:\n", "\n".join(most_items), LN_SEP)

    df_exp = filterby_criteria(df, {"Element": ["Export"], "Year":[2013]})
    df_imp = filterby_criteria(df, {"Element": ["Import"], "Year":[2013]})

    most_exp_countries = find_extremes(df_exp, by_item=False, by_value=True, n=-12)
    most_imp_countries = find_extremes(df_imp, by_item=False, by_value=True, n=-12)
    countries = list(set(most_exp_countries + most_imp_countries))

    print("List of countries that import and export the most by value:\n","\n".join(countries), LN_SEP)
    generate_scatter_import_vs_export(df, countries=countries, year=2013, output='import_vs_export')


