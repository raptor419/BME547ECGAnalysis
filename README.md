# ECG Analysis Assignment
![Work Flow Status](../../actions/workflows/pytest.yml/badge.svg)

This is ECG Raw data analysis program implemented in python3

## Requirements
This program requires a running version of `python3` 
and the following packages

```
pytest
pytest-pycodestyle
pandas
numpy
argparse
coverage
testfixtures
py-ecg-detectors
simplejson
```

## Description
The program calculates the following metrics from raw ECG Data:

1. `duration`: time duration of the ECG strip as a numeric value
2. `voltage_extremes`: tuple in the form (min, max) where min and max are
the minimum and maximum lead voltages as found in the raw data file.
3. `num_beats`: number of detected beats in the strip, as a numeric value
4. `mean_hr_bpm`: estimated average heart rate over the
length of the strip as a numeric value
5. `beats`: list of times when a beat occurred.

The program takes in data as a csv files,
sample inputs are given in [test_data](./test_data) 
Input data must follow specification as described in the
[data readme](./test_data/README.md). 

By default it saves the a json file with the same name as 
the input csv file (also takes ./test_data/test_data.csv as 
default input if no input is given), but this behaviour can be changed
(see extended usage)

The program uses Hamilton QRS Detectors (see citation) implemented in python using the `py-ecg-detectors` package and 
calculates/extrapolates others metrics including the `mean_hr_bpm` using simple mathematics

## Usage

```
git clone https://github.com/raptor419/BME547ECGAnalysis
pip install -r requirements
python ecg_analysis.py
```

## Extended Usage
```
usage: ecg_analysis.py [-h] [-i INPUT] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        input file name
  -o OUTPUT, --output OUTPUT
                        output filename
```

## Citation:

    P. Hamilton, "Open source ECG analysis," Computers in Cardiology, 2002.
    pp. 101-104, doi: 10.1109/CIC.2002.1166717. 
