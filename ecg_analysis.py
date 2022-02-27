import json
import argparse
import logging
import pandas as pd
from ecgdetectors import Detectors


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


def process_raw(file_df, filename="test"):
    """
    Process and log non-numeric or NaN values from dataframe

    Function processes non-numerics or NaN values, warns the
    user with the line number the error was found, removes the
    line returns a processed dataframe.

    :param filename:
    :param file_df: pandas.DataFrame from the input csv file
    :return: processed pandas.DataFrame
    """
    file_df = file_df.apply(pd.to_numeric, errors='coerce')
    file_df = file_df.astype(float)
    na_lines = file_df.isna().any(axis=1)
    for line, nan in na_lines.iteritems():
        if nan:
            logging.error("Non-Numeric value in line {0}, "
                          "skipping.".format(str(line)))
    ex_lines = abs(file_df['voltage']) > 300
    if ex_lines.any():
        logging.warning("Voltage exceeded normal range "
                        "in file {0}".format(filename))
    processed_df = file_df[~na_lines]
    return processed_df


def detect_beats(df):
    """
    Function that detects time of heartbeats

    The function detects the time of heartbeats and returns a
    list of times of the r_peak estimates of the QRS curve
    of the heartbeat using the Hamiltonian Method

    :param df: dataframe with columns time and voltage
    :return: list of times with heartbeat
    """
    unfiltered_ecg = df['voltage']
    freq = 1 / df['time'].diff().median()
    detectors = Detectors(freq)
    r_peaks = detectors.hamilton_detector(unfiltered_ecg)
    times = df['time'][r_peaks]
    return times


def get_metrics(df):
    """
    A function that takes in the ECG data dataframe and
    outputs calculated metrics

    The function calculates and returns the following in a dictionary
    The following data should be calculated and saved as keys in a Python
    dictionary called metrics

    1. duration: time duration of the ECG strip as a numeric value
    2. voltage_extremes: tuple in the form (min, max) where min and max are
    the minimum and maximum lead voltages as found in the raw data file.
    3. num_beats: number of detected beats in the strip, as a numeric value
    4. mean_hr_bpm: estimated average heart rate over the
    length of the strip as a numeric value
    5. attribute beats: list of times when a beat occurred.

    :param df: dataframe with columns time and voltage
    :return: a dict of metrics params
    """
    metrics = dict()
    metrics['duration'] = df.iloc[-1].time - df.iloc[0].time
    metrics['min'] = df['voltage'].min()
    metrics['max'] = df['voltage'].max()
    metrics['beats'] = list(detect_beats(df))
    metrics['num_beats'] = len(metrics['beats'])
    metrics['mean_hr_bpm'] = metrics['num_beats']/(metrics['duration']/60)
    return metrics


def main(filename, output_name=None):
    """
    Driver function for program

    Main driver function for the program that takes in the
    input filename and output filename as parameters and runs the
    program

    :param filename: input filename
    :param output_name: output filename
    :return: json file as output
    """
    if output_name is None:
        output_name = ''.join(filename.split(".")[:-1] + [".json"])
    df = readfile_raw(filename)
    df = process_raw(df, filename)
    metrics = get_metrics(df)
    json_str = json.dumps(metrics, indent=4)
    with open(output_name, 'w+') as fp:
        json.dump(metrics, fp, indent=4)
    return json_str


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
        logging.warning("No input file given, using default {0}".format(file))

    if args.output:
        output = args.output
    else:
        output = ''.join(file.split(".")[:-1] + [".json"])

    main(file, output)
