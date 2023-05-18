import numpy as np

def clean_outliers (variable):
    """
    Remove outliers from a variable of a dataframe using the 1.5 iqr condition.   
    Args:
        variable vector : dataframe
            Input variable.

    Return:
        filtered: dataframe
            Output variable.
    """
    iqr = np.percentile(df_subset[variable], 75) - np.percentile(df_subset[variable], 25)
    max = np.percentile(df_subset[variable], 75) + 1.5 *iqr
    min = np.percentile(df_subset[variable], 25)- 1.5*iqr
    filtered = df_subset[(df_subset[variable] <= max) & (df_subset[variable] >= min)]
    return filtered