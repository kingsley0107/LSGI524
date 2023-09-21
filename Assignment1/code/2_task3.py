# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:31:00 2023

@Author: Kingsley
'''

from utils.customized_plot import (plot_trend, plot_kde,
                                   plot_departure_spatial_distribution,
                                   plot_arrival_spatial_distribution,
                                   plot_boxplot)
import pandas as pd
from config.global_vars import Project_Configs
from utils.preprocess import (clean_station, cal_distance_in_proj_coord,
                              convert_coordinate)
import geopandas as gpd


def pre_data_for_task_3():
    """prepare data for task 3: visualization
    mainly goals:
    1. calculate trip_distance by merging station data and convert coordinates
    2. loading chicago boundary for better visualization later.

    Returns:
        _type_: bike,station,chicago_boundary
    """
    cleaned_bike = pd.read_csv(Project_Configs.PREPROCESSED_BIKE.value)
    cleaned_bike["start_time"] = pd.to_datetime(cleaned_bike["start_time"])
    cleaned_bike["end_time"] = pd.to_datetime(cleaned_bike["end_time"])
    cleaned_bike = convert_coordinate(cleaned_bike, 4326,
                                      Project_Configs.PROJECT_CRS.value)
    cleaned_bike = cal_distance_in_proj_coord(cleaned_bike, "trip_distance")
    station_data = clean_station(
        pd.read_csv(Project_Configs.STATION_DATA_PATH.value))
    chicago_base = gpd.read_file(Project_Configs.BASE_CHICAGO.value).to_crs(
        f"epsg:{Project_Configs.PROJECT_CRS.value}")

    return cleaned_bike, station_data, chicago_base


def complete_task3():
    """task 3
    step1:plot line chart, showing the number flow by time

    step2:plot the distribution of departure number aggregated by stations,
    including spatial and numerical.

    step3:plot the distribution of arrival number aggregated by stations,
    including spatial and numerical.

    step4: plot probability density for both trip distance and trip duration.

    """
    cleaned_bike, cleaned_station, chicago_base = pre_data_for_task_3()
    # task 3.1
    plot_trend(cleaned_bike,
               target_column="start_time",
               emphasis_range=[(7, 9), (16, 18)])
    # task 3.2.1
    plot_departure_spatial_distribution(cleaned_bike, cleaned_station,
                                        chicago_base)
    # generate departure aggregation
    depature_stations_number = cleaned_bike.groupby([
        'from_station_id'
    ]).count()[['trip_id']].rename({"trip_id": "departure_stations_count"},
                                   axis=1)
    cleaned_station['geometry'] = gpd.points_from_xy(
        cleaned_station['lon'], cleaned_station['lat'],
        crs="epsg:4326").to_crs("epsg:26916")
    station_geom = cleaned_station.drop(['lon', 'lat'], axis=1)
    depature_station_gdf = gpd.GeoDataFrame(
        depature_stations_number.merge(station_geom,
                                       left_index=True,
                                       right_index=True))
    # plot statistic info for departure aggregation
    plot_boxplot(depature_station_gdf,
                 field="departure_stations_count",
                 xlabel="station_departure_count",
                 ylabel="departure_station",
                 title="distribution of station's departure counts")

    # task 3.2.2
    plot_arrival_spatial_distribution(cleaned_bike, cleaned_station,
                                      chicago_base)

    # generate arrival aggregation
    arrival_stations_number = cleaned_bike.groupby(['to_station_id']).count()[[
        'trip_id'
    ]].rename({"trip_id": "arrival_stations_count"}, axis=1)
    cleaned_station['geometry'] = gpd.points_from_xy(
        cleaned_station['lon'], cleaned_station['lat'],
        crs="epsg:4326").to_crs("epsg:26916")
    station_geom = cleaned_station.drop(['lon', 'lat'], axis=1)

    # plot statistic info for arrival aggregation
    arrival_station_gdf = gpd.GeoDataFrame(
        arrival_stations_number.merge(station_geom,
                                      left_index=True,
                                      right_index=True))

    plot_boxplot(arrival_station_gdf,
                 field="arrival_stations_count",
                 xlabel="station_arrival_count",
                 ylabel="arrival_station",
                 title="distribution of station's arrival counts",
                 color="coral")

    # task 3.3
    plot_kde(cleaned_bike, topic="distance")

    # task 3.4
    plot_kde(cleaned_bike, topic="duration")


if __name__ == "__main__":
    complete_task3()
