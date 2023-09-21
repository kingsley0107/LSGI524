# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:30:54 2023

@Author: Kingsley
'''

import pandas as pd
import geopandas as gpd
from utils.preprocess import cal_distance_in_proj_coord
from config.global_vars import Project_Configs


# NOTE Task 2.1
def convert_coordinate(cleaned_bike: pd.DataFrame,
                       origin_epsg: int = None,
                       target_epsg: int = None):
    """generate from point(geometry) and to point(geometry) and transform epsg
      using station lon&lat.

    Args:
        cleaned_bike (pd.DataFrame): bike data (merged with station location data)
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


# NOTE Task 2.2
def bike_trip_statistic(df_bike: pd.DataFrame):
    """statistic bike trip data

    Args:
        df_bike (pd.DataFrame): dataframe to be describe

    Returns:
        statistic_info: two columns(trip_duration&trip_distance),7 records
        (unique indices)
        _type_: dataframe
    """
    bike_with_dis = cal_distance_in_proj_coord(df_bike, "trip_distance")
    # column 'tripduration' is verified by calculating
    #  'end_time' minus 'start_time'.
    #  It's OK to use it directly.
    bike_with_dis["tripduration"] = (
        bike_with_dis["tripduration"].astype("float").astype("int"))
    indices_trip_duration = [
        bike_with_dis["tripduration"].max(),
        bike_with_dis["tripduration"].min(),
        bike_with_dis["tripduration"].median(),
        bike_with_dis["tripduration"].mean(),
        bike_with_dis["tripduration"].quantile(0.25),
        bike_with_dis["tripduration"].quantile(0.75),
        bike_with_dis["tripduration"].std(),
    ]

    indices_trip_distance = [
        bike_with_dis["trip_distance"].max(),
        bike_with_dis["trip_distance"].min(),
        bike_with_dis["trip_distance"].median(),
        bike_with_dis["trip_distance"].mean(),
        bike_with_dis["trip_distance"].quantile(0.25),
        bike_with_dis["trip_distance"].quantile(0.75),
        bike_with_dis["trip_distance"].std(),
    ]

    statistic_info = pd.DataFrame(
        data={
            "trip_duration/s": indices_trip_duration,
            "trip_distance/m": indices_trip_distance,
        },
        index=[
            "Max Value",
            "Min Value",
            "Median",
            "Mean",
            "25% Percentile",
            "75% Percentile",
            "Standard Deviation",
        ],
    ).round(2)
    return statistic_info


def complete_task2():
    cleaned_chicago_data = pd.read_csv(Project_Configs.PREPROCESSED_BIKE.value)
    proj_coord_data = convert_coordinate(cleaned_chicago_data, 4326,
                                         Project_Configs.PROJECT_CRS.value)
    statistic_info = bike_trip_statistic(proj_coord_data)
    print(
        "\n==================================Task 2==================================\n"
    )
    print(f"the statistical infomation of the trips is :\n {statistic_info}\n")


if __name__ == "__main__":
    complete_task2()
