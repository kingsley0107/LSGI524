# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:29:51 2023

@Author: Kingsley
'''

# ==========================================Configuration==========================================
from enum import Enum


# NOTE: global params
class Project_Configs(str, Enum):
    """global & static variables for this project.

    Args:
        str (_type_): inheritated from string type
        Enum (_type_): inheritated from enumerate, which is suitable for storing uneditable configs.
    """

    BIKE_DATA_PATH = r"./data_raw/chicago_data.csv"
    STATION_DATA_PATH = r"./data_raw/station.csv"
    PREPROCESSED_BIKE = r"./data_cleaned/chicago_data_cleaned.csv"
    PREPROCESSED_STATION = r"./data_cleaned/station_cleaned.csv"
    BASE_CHICAGO = r"./data_raw/chicago.geojson"
    DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    TIME_WINDOW_START = "2019-07-25 00:00:00"
    TIME_WINDOW_END = "2019-07-26 00:00:00"
    ENCODING = "utf-8"
    PROJECT_CRS = 26916


# ==========================================End of Configuration=============================
