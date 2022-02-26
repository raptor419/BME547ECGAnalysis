import pytest
import numpy as np
import pandas as pd

df1 = pd.DataFrame([[1.0, 1.0],
                    [1.0, np.nan]],
                   columns=['time', 'voltage'])
df1_exp = pd.Series([False, True])
df2 = pd.DataFrame([[1.0, 1.0],
                    [1.0, np.nan]],
                   columns=['time', 'voltage'])
df2_exp = pd.Series([False, True])
df3 = pd.DataFrame([[1.0, 1.0],
                    [1.0, np.nan]],
                   columns=['time', 'voltage'])
df3_exp = pd.Series([False, True])

df_data = [
    (df1, df1_exp),
    (df2, df2_exp),
    (df3, df3_exp),
]


@pytest.mark.parametrize("df, exp_series", df_data)
def test_df_is_na(df, exp_series):
    series = df.isna().any(axis=1)
    assert(series.equals(exp_series))


df1 = pd.DataFrame([[1.0, 2.0], [1.0, "2.9"]], columns=['time', 'voltage'])
df1_exp = pd.DataFrame([[1.0, 2.0], [1.0, 2.9]], columns=['time', 'voltage'])
df2 = pd.DataFrame([[1, 2], [1, 'String']], columns=['time', 'voltage'])
df2_exp = pd.DataFrame([[1.0, 2.0], [1.0, np.nan]],
                       columns=['time', 'voltage'])
df3 = pd.DataFrame([[1, 2], [1, 'NaN']], columns=['time', 'voltage'])
df3_exp = pd.DataFrame([[1.0, 2.0], [1.0, np.nan]],
                       columns=['time', 'voltage'])
df_data = [
    (df1, df1_exp),
    (df2, df2_exp),
    (df3, df3_exp),
]


@pytest.mark.parametrize("input_df, expected_df", df_data)
def test_pd_as_type(input_df, expected_df):
    processed_df = input_df.apply(pd.to_numeric, errors='coerce')
    processed_df = processed_df.astype(float)
    assert (processed_df.equals(expected_df))


df1 = pd.DataFrame([[1, 2], [1, 2]], columns=['time', 'voltage'])
df1_exp = pd.DataFrame([[1.0, 2.0], [1.0, 2.0]], columns=['time', 'voltage'])
df2 = pd.DataFrame([[1, 2], [1, 'String']], columns=['time', 'voltage'])
df2_exp = pd.DataFrame([[1.0, 2.0]], columns=['time', 'voltage'])
df3 = pd.DataFrame([[1, 2], [1, np.nan]], columns=['time', 'voltage'])
df3_exp = pd.DataFrame([[1.0, 2.0]], columns=['time', 'voltage'])


df_data = [
    (df1, df1_exp),
    (df2, df2_exp),
    (df3, df3_exp),
]


@pytest.mark.parametrize("file_df, expected_df", df_data)
def test_process_raw(file_df, expected_df):
    from ecg_analysis import process_raw
    processed_df = process_raw(file_df)
    print(processed_df, expected_df)
    assert (processed_df.equals(expected_df))
