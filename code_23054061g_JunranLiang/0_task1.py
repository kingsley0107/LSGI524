# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:30:47 2023

@Author: Kingsley
'''

import pandas as pd
from utils.validate import time_window_is_correct
from utils.preprocess import clean_raw_bike
from config.global_vars import Project_Configs


# NOTE Task 1.1
def count_valid_trips(cleaned_bike: pd.DataFrame, date: str = None):
    """count valid trips, chech data validity if necessary

    Args:
        cleaned_bike (pd.DataFrame): cleaned bike trips record.
        date (str, optional): timewindow, if not None, check date before,
        counting trips. Defaults to None.

    Returns:
        _type_: the number of valid trips
    """
    # if time windows unmatched, raise exception.
    if date:
        time_window_is_correct(cleaned_bike, date)
    valid_trips_number = len(cleaned_bike["trip_id"].unique())
    return valid_trips_number


# NOTE Task 1.2
def count_used_stations(cleaned_bike: pd.DataFrame):
    """count used stations (unique)

    Args:
        cleaned_bike (pd.DataFrame): cleaned bike trips record with fileds
          <"from_station_id" and "to_station_id">

    Returns:
        _type_: the number of unique stations used in df.
    """
    # set: remove duplicated data
    used_stations_number = len(
        set(cleaned_bike["from_station_id"].tolist())
        | set(cleaned_bike["to_station_id"].tolist()))
    return used_stations_number


# NOTE Task 1.3
def unique_bikes_number(cleaned_bike: pd.DataFrame):
    """count number of unique bike.

    Args:
        cleaned_bike (pd.DataFrame): cleaned bike trips record with fileds
        <"bikeid">

    Returns:
        _type_: number of unique bike
    """
    unique_bikes_number = len(set(cleaned_bike["bikeid"].tolist()))
    return unique_bikes_number


def complete_task1():
    raw_bike = pd.read_csv(Project_Configs.BIKE_DATA_PATH.value)
    cleaned_chicago_data = clean_raw_bike(raw_bike)

    # use this if clean_bike already exist
    # cleaned_chicago_data = pd.read_csv(Project_Configs.PREPROCESSED_BIKE.value)
    print(
        "\n==================================Task 1==================================\n"
    )
    print(f"the number of valid bicycle trips on 25 July 2019 is :\
        {count_valid_trips(cleaned_chicago_data)}\n")
    print(f"the number of bike stations used on 25 July 2019 is:\
              {count_used_stations(cleaned_chicago_data)}\n")
    print(f"the number of unique bikes were used on 25 July 2019 is:\
              {unique_bikes_number(cleaned_chicago_data)}\n")


if __name__ == "__main__":
    complete_task1()
