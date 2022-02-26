import argparse
import logging
import pandas as pd


def readfile_raw(filename):
    """
    Read raw file dataframe from file location as string

    Reads csv file as as raw data using pandas package.
    Skips lines with too many columns and gives a warning.

    :param filename: the path the file to read
    :return: pandas.DataFrame from input csv
    """
    file_df = pd.read_csv(filename,
                          names=['time', 'voltage'],
                          on_bad_lines='warn')
    return file_df


def process_raw(file_df):
    """
    Process and log non-numeric or NaN values from dataframe

    Function processes non-numerics or NaN values, warns the
    user with the line number the error was found, removes the
    line returns a processed dataframe.

    :param file_df: pandas.DataFrame from the input csv file
    :return: processed pandas.DataFrame
    """
    file_df = file_df.apply(pd.to_numeric, errors='coerce').astype(float)
    na_lines = file_df.isna().any(axis=1)
    for line, nan in na_lines.iteritems():
        if nan:
            logging.warning("Non-Numeric value in line {0}, "
                            "skipping".format(str(line)))
    processed_df = file_df[~na_lines]
    return processed_df


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", type=str,
                        help="input file name")
    parser.add_argument("-o", "--output", type=str,
                        help="output filename")
    args = parser.parse_args()

    logging.basicConfig(filename="ecg_analysis_run.log",
                        filemode="w", level=logging.INFO)

    if args.input:
        file = args.input
    else:
        file = "test_data/test_data1.csv"
        logging.warning("No input file given, using default "+file)

    if args.output:
        output = args.output
    else:
        output = ''.join(file.split(".")[:-1] + [".json"])

    df = readfile_raw(file)
    df = process_raw(df)
    print(df)
