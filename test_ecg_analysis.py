import pytest
import numpy as np
import pandas as pd
from testfixtures import LogCapture
from ecg_analysis import readfile_raw, process_raw

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
    assert (series.equals(exp_series))


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


df1 = pd.DataFrame([[1, 2], [1, np.nan]], columns=['time', 'voltage'])
df1_exp = ("root", "ERROR", "Non-Numeric value in line {0}, "
                            "skipping.".format(str(1)))
df2 = pd.DataFrame([[1, 2], [1, 350]], columns=['time', 'voltage'])
df2_exp = ("root", "WARNING", "Voltage exceeded normal range "
                              "in file {0}".format("test"))
df3 = pd.DataFrame([[1, 2], [1, 3]], columns=['time', 'voltage'])
df3_exp = ()

df_data = [
    (df1, df1_exp),
    (df2, df2_exp),
    (df3, df3_exp),
]


@pytest.mark.parametrize("df, log", df_data)
def test_process_raw_log(df, log):
    from ecg_analysis import process_raw
    with LogCapture() as log_c:
        process_raw(df)
    if log:
        log_c.check(log)
    else:
        log_c.check()


df1 = process_raw(readfile_raw("test_data/test_data1_orig.csv"))
df1_exp = pd.Series([[0.254, 1.028, 1.842, 2.631, 3.419,
                    4.208, 5.025, 5.681, 6.675, 7.517,
                    8.328, 9.119, 9.889, 10.731,
                    11.586, 12.406, 13.236, 14.058,
                    14.853, 15.65, 16.439, 17.264,
                    18.131, 18.956, 19.739, 20.536,
                    21.306, 22.092, 22.906, 23.719,
                    24.547, 25.394, 26.2, 26.972]])
df_data = [(df1, df1_exp)]


@pytest.mark.parametrize("df, exp_series", df_data)
def test_detect_beats(df, exp_series):
    from ecg_analysis import detect_beats
    series = detect_beats(df)
    assert (np.allclose(list(series), list(exp_series), atol=0.07))


df1 = process_raw(readfile_raw("test_data/test_data1.csv"))
df1_exp = {
    "duration": 27.775,
    "min": -2.08,
    "max": 2.308,
    "beats": [
        0.286, 1.05, 1.864,
        2.647, 3.447, 4.231, 5.047,
        5.697, 6.697, 7.544, 8.347,
        9.147, 9.914, 10.747, 11.611,
        12.431, 13.264, 14.081, 14.881,
        15.678, 16.464, 17.283, 18.15,
        18.981, 19.764, 20.561, 21.331,
        22.114, 22.931, 23.747, 24.578,
        25.414, 26.228, 26.997],
    "num_beats": 34,
    "mean_hr_bpm": 73.44734473447345
}

df_data = [(df1, df1_exp)]


@pytest.mark.parametrize("df, exp", df_data)
def test_get_metrics(df, exp):
    from ecg_analysis import get_metrics
    metrics = get_metrics(df)
    assert (np.isclose(metrics['duration'], exp['duration']))
    assert (np.isclose(metrics['min'], exp['min']))
    assert (np.isclose(metrics['max'], exp['max']))
    assert (np.isclose(metrics['num_beats'], exp['num_beats'], atol=1))
    assert (np.isclose(metrics['mean_hr_bpm'], exp['mean_hr_bpm'], atol=10))
    assert (np.allclose(metrics['beats'], metrics['beats'], atol=0.001))


df1 = df1_exp
df1_exp = ["""{
    "duration": 27.775,
    "min": -2.08,
    "max": 2.308,
    "beats": [
        0.286,
        1.05,
        1.864,
        2.647,
        3.447,
        4.231,
        5.047,
        5.697,
        6.697,
        7.544,
        8.347,
        9.147,
        9.914,
        10.747,
        11.611,
        12.431,
        13.264,
        14.081,
        14.881,
        15.678,
        16.464,
        17.283,
        18.15,
        18.981,
        19.764,
        20.561,
        21.331,
        22.114,
        22.931,
        23.747,
        24.578,
        25.414,
        26.228,
        26.997
    ],
    "num_beats": 34,
    "mean_hr_bpm": 73.44734473447345
}""", ]

df_data = [(df1, df1_exp)]


@pytest.mark.parametrize("metrics, exp", df_data)
def test_to_json(metrics, exp):
    json_str = exp[0]
    from ecg_analysis import to_json
    assert (to_json("./test_data/unittest.json", metrics) == json_str)


def test_main_blank():
    from ecg_analysis import main
    for i in [1, 2, 3, 4, 5, 6, 7, 10,
              11, 16, 20, 22, 23, 28, 32]:
        main("test_data/test_data" + str(i) + ".csv")
