# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:31:07 2023

@Author: Kingsley
'''

from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
from utils.preprocess import clean_station
from config.global_vars import Project_Configs
import geopandas as gpd
from utils.customized_plot import plot_clustering


def pre_for_cluster():
    """prepare station data for cluster
    goals: a cleaned projected station data in geodataframe.

    Returns:
        gpd.GeoDataframe: station with geometry
    """
    station = clean_station(
        pd.read_csv(Project_Configs.STATION_DATA_PATH.value))
    station["geometry"] = gpd.points_from_xy(station["lon"], station["lat"])
    station_geom = gpd.GeoDataFrame(
        station,
        crs="epsg:4326").to_crs(f"epsg:{Project_Configs.PROJECT_CRS.value}")
    return station_geom


def cluster_station(station_geom):
    """core for clustering, eps = 600m, and , min_sample = 3
    (exclude current point)

    Args:
        station_geom (_type_): station for clustering

    Returns:
        gpd.GeoDataframe: gdf with a field "clustering"
    """

    # generate ndarray for dbscan
    points_list = (station_geom["geometry"].apply(
        lambda geom: [geom.x, geom.y]).to_list())
    points_to_cluster = np.array(points_list)

    # clustering
    dbscan = DBSCAN(eps=600, min_samples=3)
    clusters = dbscan.fit_predict(points_to_cluster)

    # return the clustering result to gdf
    station_geom["clusters"] = clusters
    station_geom = gpd.GeoDataFrame(station_geom)
    return clusters, station_geom


def complete_task4_bonus():
    chicago_base = gpd.read_file(Project_Configs.BASE_CHICAGO.value)
    # generate a gdf with spatial location, used for spatial clustering
    station_geom = pre_for_cluster()
    # clustering
    clusters, clustered_station = cluster_station(station_geom)

    # bonus: visualizing clustering
    plot_clustering(clustered_station, clusters, chicago_base)
    # print the information about station id and clustering groups
    print(
        "\n====================number of stations for each cluster====================\n"
    )
    print(clustered_station[clustered_station['clusters'] != -1].groupby(
        "clusters").count()[['lon']].rename({"lon": "station_count"}, axis=1))

    print(
        "\n==================== station_id and its cluster group ====================\n"
    )
    print(clustered_station[clustered_station['clusters'] != -1][[
        'clusters'
    ]].sort_values("clusters"))


if __name__ == "__main__":
    complete_task4_bonus()
