# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:30:25 2023

@Author: Kingsley
'''

from config.global_vars import Project_Configs
import pandas as pd
import geopandas as gpd


def read_data(
    bike_data_path: str = Project_Configs.BIKE_DATA_PATH,
    station_data_path: str = Project_Configs.STATION_DATA_PATH,
    encoding: str = Project_Configs.ENCODING,
):
    """Read raw data, both chicago_bike & chicago_station and print out the basic info of them.

    Args:
        bike_data_path (_type_, optional): _raw chicago_bike data_. Defaults to Project_Configs.BIKE_DATA_PATH.
        station_data_path (_type_, optional): _raw chicago_station data_. Defaults to Project_Configs.STATION_DATA_PATH.

    Returns:
        1.raw_bike: dataframe, raw chicago_bike data
        2.raw_station: dataframe, raw chicago_station data
        _type_: _Dataframe_
    """

    raw_bike = pd.read_csv(bike_data_path, encoding=encoding)
    raw_station = pd.read_csv(station_data_path, encoding=encoding)
    print("================RAW BIKE INFO================")
    print(raw_bike.info())

    print("================RAW STATION INFO================")
    print(raw_station.info())

    return raw_bike, raw_station


# NOTE: Task1 a):Data Cleaning for chicago.csv
def clean_raw_bike(raw_bike: pd.DataFrame):
    """clean bicycle data

    # step1: drop useless columns in this dataframe.
    # step2: drop rows that with missing values
    # step3: convert data type into reasonable data type
    # step4: build up a timewindow and filter those out of range

    Args:
        raw_bike (pd.DataFrame): _raw chicago data_

    Returns:
        cleaned_chicago_bike_data
        _type_: _Dataframe_
    """

    # NOTE STEP1:drop useless columns
    bike_column_filtered = raw_bike.drop(
        [
            "usertype", "gender", "birthyear", "from_station_name",
            "to_station_name"
        ],
        axis=1,
    )

    # NOTE STEP2:drop rows with missing values(any)
    bike_missing_filter = bike_column_filtered[~bike_column_filtered.isna().
                                               any(axis=1)]

    # NOTE STEP3:convert datatype
    # ID should be the identity, they should all be integer but not float.
    # datetime is also converted, in order to be compareable in time
    (
        bike_missing_filter["bikeid"],
        bike_missing_filter["trip_id"],
        bike_missing_filter["from_station_id"],
        bike_missing_filter["to_station_id"],
        bike_missing_filter["tripduration"],
        bike_missing_filter["start_time"],
        bike_missing_filter["end_time"],
    ) = (
        bike_missing_filter["bikeid"].astype("int"),
        bike_missing_filter["trip_id"].astype("int"),
        bike_missing_filter["from_station_id"].astype("int"),
        bike_missing_filter["to_station_id"].astype("int"),
        bike_missing_filter["tripduration"].astype("int"),
        pd.to_datetime(
            bike_missing_filter["start_time"],
            format=Project_Configs.DATETIME_FORMAT.value,
        ),
        pd.to_datetime(
            bike_missing_filter["end_time"],
            format=Project_Configs.DATETIME_FORMAT.value,
        ),
    )

    # NOTE STEP4: Filter time window
    WINDOW_START = pd.to_datetime(Project_Configs.TIME_WINDOW_START.value)
    WINDOW_END = pd.to_datetime(Project_Configs.TIME_WINDOW_END.value)

    bike_cleaned = bike_missing_filter[
        (bike_missing_filter["start_time"] >= WINDOW_START)
        & (bike_missing_filter["end_time"] < WINDOW_END)]

    return bike_cleaned.reset_index(drop=True)


def clean_station(raw_station: pd.DataFrame):
    """Clean the raw station data: select useful columns and rename

    Args:
        raw_station (pd.DataFrame): raw station data

    Returns:
        _type_: _cleaned station data_
        _type_: pd.Dataframe
    """

    # NOTE Step1: select useful columns and rename them into easy name
    station_selected = raw_station[[
        "data__stations__lon", "data__stations__lat",
        "data__stations__station_id"
    ]].rename(
        {
            "data__stations__station_id": "station_id",
            "data__stations__lon": "lon",
            "data__stations__lat": "lat",
        },
        axis=1,
    )
    # set station_id into index
    station_cleaned = station_selected.set_index(["station_id"])

    return station_cleaned


def merging_bike_station(cleaned_bike_data: pd.DataFrame,
                         cleaned_station_data: pd.DataFrame):
    """adding station location info into bike data

    Args:
        cleaned_bike_data (pd.DataFrame): _cleaned bike data_
        cleaned_station_data (pd.DataFrame): _cleaned station data_

    Returns:
        bike data that merged start & end location data
        _type_: pd.Dataframe
    """

    # NOTE "inner join" will automatically drop those records not in station.csv
    start_station_merge = pd.merge(
        cleaned_bike_data,
        cleaned_station_data,
        how="inner",
        left_on="from_station_id",
        right_index=True,
    )
    start_plus_end_station_merge = pd.merge(
        start_station_merge,
        cleaned_station_data,
        how="inner",
        left_on="to_station_id",
        right_index=True,
        suffixes=("_from", "_to"),
    )
    merging_data = start_plus_end_station_merge.sort_values(
        "start_time").reset_index(drop=True)
    return merging_data


def cal_distance_in_proj_coord(df: gpd.GeoDataFrame, column_name: str):
    """calculate spatial distance(Euclidean distance) in projected coordinates
    Make Sure that it's not a geographic coordinate

    Args:
        df (gpd.GeoDataFrame): geodataframe for calculating spatial distance
        column_name (str): _description_

    Returns:
        _type_: _description_
    """
    df[column_name] = df.apply(
        lambda x: x["from_point"].distance(x["to_point"]), axis=1)
    return df


def convert_coordinate(cleaned_bike: gpd.GeoDataFrame,
                       origin_epsg: int = None,
                       target_epsg: int = None):
    """generate from point(geometry) and to point(geometry) and transform epsg using station lon&lat.

    Args:
        cleaned_bike (gpd.GeoDataFrame): bike data (merged with station location data)
        origin_epsg (int, optional): origin epsg. Defaults to None.
        target_epsg (int, optional): target epsg. Defaults to None.

    Returns:
        _type_: GeoDataframe with two geometry(from point & to point) per row.
    """
    cleaned_bike["from_point"] = gpd.points_from_xy(
        cleaned_bike["lon_from"],
        cleaned_bike["lat_from"],
        crs=f"epsg:{origin_epsg}").to_crs(f"epsg:{target_epsg}")
    cleaned_bike["to_point"] = gpd.points_from_xy(
        cleaned_bike["lon_to"],
        cleaned_bike["lat_to"],
        crs=f"epsg:{origin_epsg}").to_crs(f"epsg:{target_epsg}")

    bike_with_proj_geom = cleaned_bike.drop(
        ["lon_from", "lat_from", "lon_to", "lat_to"], axis=1)
    return bike_with_proj_geom
