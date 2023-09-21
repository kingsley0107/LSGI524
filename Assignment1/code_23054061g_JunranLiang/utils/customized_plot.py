# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:30:16 2023

@Author: Kingsley
'''

import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import transbigdata as tbd
from config.global_vars import Project_Configs

plt.style.use("seaborn")


def plot_kde(df: pd.DataFrame, topic="distance"):
    """probability distribution plotting

    Args:
        df (pd.DataFrame): df containing data
        topic (str, optional): topic. Defaults to "distance".

    Raises:
        TypeError: _description_
    """
    if topic == "distance":
        column = "trip_distance"
        xlabel = "trip_distance"
        ylabel = "probability density"
        title = "trip_distance probability density"
        step = 2500
    elif topic == "duration":
        column = "tripduration"
        xlabel = "trip_duration"
        ylabel = "probability density"
        title = "trip_duration probability density"
        step = 3000
    else:
        raise TypeError(f"Topic {topic} Not Found.")
    plt.figure(figsize=(10, 6))

    sns.kdeplot(
        data=df[column],
        shade=True,
        color="b",
        label=xlabel,
    )
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.xticks(range(0, round(df[column].max()), step))
    plt.show()


# NOTE Task 3.1 plot line trend
def plot_trend(
    df: pd.DataFrame,
    target_column="start_time",
    x_column="departure_hour",
    y_column="departure_station_counts",
    palette=["#FF6B6B", "#FFD166", "#06D6A0", "#277DA1", "#FEAA40"],
    emphasis_range=[(7, 9), (16, 18)],
):
    """line chart, showing time trend

    Args:
        df (pd.DataFrame): data
        target_column (str, optional): aggregated by which filed. 
        Defaults to "start_time".
        x_column (str, optional): time field. 
        Defaults to "departure_hour".
        y_column (str, optional): data field. 
        Defaults to "departure_station_counts".
        palette (list, optional): color space. 
        Defaults to ["#FF6B6B", "#FFD166", "#06D6A0", "#277DA1", "#FEAA40"].
        emphasis_range (list, optional):emphasis background, used for emphasis
          commuting time in this taks. Defaults to [(7, 9), (16, 18)].
    """

    # extracting hour
    temp_column1 = x_column
    temp_column2 = y_column
    bike_group_by_hour = df.copy()

    bike_group_by_hour[temp_column1] = df[target_column].dt.hour
    bike_time_line_plot = (bike_group_by_hour.groupby([temp_column1]).count()[[
        target_column
    ]].rename({target_column: temp_column2}, axis=1))

    # create figure
    plt.figure(figsize=(10, 6))
    macaron_colors = palette

    # plot
    line_plot = sns.lineplot(
        x=temp_column1,
        y=temp_column2,
        data=bike_time_line_plot,
        color="b",
        markers=True,
        marker="o",
    )

    # some detailed, like axes and backgrounds.
    plt.xticks(range(0, 24, 1))
    if len(emphasis_range) >= 1:
        plt.axvspan(
            emphasis_range[0][0],
            emphasis_range[0][1],
            alpha=0.2,
            color=macaron_colors[0],
            label=
            f"Rush Hour ({emphasis_range[0][0]}:00-{emphasis_range[0][1]}:00)",
        )
        plt.axvspan(
            emphasis_range[1][0],
            emphasis_range[1][1],
            alpha=0.2,
            color=macaron_colors[1],
            label=
            f"Rush Hour ({emphasis_range[1][0]}:00-{emphasis_range[1][1]}:00)",
        )
    for spine in plt.gca().spines.values():
        spine.set_edgecolor("white")
    for line in line_plot.lines:
        line.set_markerfacecolor("w")
        line.set_markeredgecolor("b")
    plt.gca().set_facecolor("white")
    plt.xlabel(temp_column1)
    plt.ylabel(temp_column2)
    plt.legend()
    plt.show()


def plot_departure_spatial_distribution(df_bike: pd.DataFrame,
                                        df_station: pd.DataFrame,
                                        base_df: gpd.GeoDataFrame):
    depature_stations_number = (df_bike.groupby(["from_station_id"]).count()[[
        "trip_id"
    ]].rename({"trip_id": "departure_stations_count"}, axis=1))

    fig, ax = plt.subplots(figsize=(8, 8))
    df_station["geometry"] = gpd.points_from_xy(
        df_station["lon"], df_station["lat"],
        crs="epsg:4326").to_crs(f"epsg:{Project_Configs.PROJECT_CRS.value}")
    station_geom = df_station.drop(["lon", "lat"], axis=1)
    depature_station_gdf = gpd.GeoDataFrame(
        depature_stations_number.merge(station_geom,
                                       left_index=True,
                                       right_index=True))
    base_df.plot(ax=ax, alpha=0.5)
    depature_station_gdf.plot(ax=ax,
                              column="departure_stations_count",
                              cmap="YlOrRd",
                              legend=True)
    plt.axis("off")
    plt.title("Spatial distribution of the number of depature stations")
    plt.show()


def plot_arrival_spatial_distribution(df_bike: pd.DataFrame,
                                      df_station: pd.DataFrame,
                                      base_df: gpd.GeoDataFrame):
    arrival_stations_number = (df_bike.groupby(["to_station_id"]).count()[[
        "trip_id"
    ]].rename({"trip_id": "arrival_stations_count"}, axis=1))
    fig = plt.figure(1, (8, 8))
    ax = plt.subplot(111)
    df_station["geometry"] = gpd.points_from_xy(
        df_station["lon"], df_station["lat"],
        crs="epsg:4326").to_crs(f"epsg:{Project_Configs.PROJECT_CRS.value}")
    station_geom = df_station.drop(["lon", "lat"], axis=1)
    depature_station_gdf = gpd.GeoDataFrame(
        arrival_stations_number.merge(station_geom,
                                      left_index=True,
                                      right_index=True))
    base_df.plot(ax=ax, alpha=0.5)
    depature_station_gdf.plot(ax=ax,
                              column="arrival_stations_count",
                              cmap="YlOrRd",
                              legend=True)
    plt.axis("off")
    plt.title("Spatial distribution of the number of arrival stations")
    plt.show()


def plot_boxplot(df: pd.DataFrame, field: str, xlabel: str, ylabel: str,
                 title: str, **kwargs):
    """simple box plot
    """
    fig = plt.figure(1, (12, 6), dpi=100)
    ax = plt.subplot(111)
    sns.boxplot(df[field], ax=ax, **kwargs)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


def plot_scale_and_north_arrow(vector_boundary, ax, crs="epsg:4326"):
    """copied and customized method.
    reference: transbigdata

    Args:
        vector_boundary (_type_): data boundary, for adjusting scale location.
        ax (_type_): canvas
        crs (str, optional):data coordinate system. Defaults to "epsg:4326".
    """
    from shapely.geometry import Polygon
    import math
    textcolor = 'k'
    textsize = 8
    lon1 = vector_boundary[0]
    lat1 = vector_boundary[1]
    lon2 = vector_boundary[2]
    lat2 = vector_boundary[3]
    accuracy = (int((lon2 - lon1) / 0.0003 / 1000 + 0.5) * 1000)
    a, c = [0., 0.0]
    b = 1 - a
    d = 1 - c
    alon, alat = (b * lon1 + a * lon2) / (a + b), (d * lat1 + c * lat2) / (c +
                                                                           d)
    deltaLon = accuracy * 360 / (2 * math.pi * 6371004 * math.cos(
        (lat1 + lat2) * math.pi / 360))
    scale = gpd.GeoDataFrame(
        {
            'color': [(0, 0, 0), (1, 1, 1), (0, 0, 0), (1, 1, 1)],
            'geometry': [
                Polygon([(alon, alat), (alon + deltaLon, alat),
                         (alon + deltaLon, alat + deltaLon * 0.4),
                         (alon, alat + deltaLon * 0.4)]),
                Polygon([(alon + deltaLon, alat), (alon + 2 * deltaLon, alat),
                         (alon + 2 * deltaLon, alat + deltaLon * 0.4),
                         (alon + deltaLon, alat + deltaLon * 0.4)]),
                Polygon([(alon + 2 * deltaLon, alat),
                         (alon + 4 * deltaLon, alat),
                         (alon + 4 * deltaLon, alat + deltaLon * 0.4),
                         (alon + 2 * deltaLon, alat + deltaLon * 0.4)]),
                Polygon([(alon + 4 * deltaLon, alat),
                         (alon + 8 * deltaLon, alat),
                         (alon + 8 * deltaLon, alat + deltaLon * 0.4),
                         (alon + 4 * deltaLon, alat + deltaLon * 0.4)])
            ]
        },
        crs=crs)
    scale.plot(ax=ax, edgecolor='k', facecolor=scale['color'], lw=0.6)
    ax.text(alon + 1 * deltaLon,
            alat + deltaLon * 0.5,
            str(int(1 * accuracy / 1000)),
            color=textcolor,
            fontsize=textsize,
            ha='center',
            va='bottom')

    ax.text(alon + 2 * deltaLon,
            alat + deltaLon * 0.5,
            str(int(2 * accuracy / 1000)),
            color=textcolor,
            fontsize=textsize,
            ha='center',
            va='bottom')
    ax.text(alon + 4 * deltaLon,
            alat + deltaLon * 0.5,
            str(int(4 * accuracy / 1000)),
            color=textcolor,
            fontsize=textsize,
            ha='center',
            va='bottom')
    ax.text(alon + 8 * deltaLon,
            alat + deltaLon * 0.5,
            str(int(8 * accuracy / 1000)),
            color=textcolor,
            fontsize=textsize,
            ha='center',
            va='bottom')
    ax.text(alon + 8.5 * deltaLon,
            alat + deltaLon * 0.5,
            "KM",
            color=textcolor,
            fontsize=textsize,
            ha='left',
            va='top')
    # add compass
    compasssize = 1
    deltaLon = compasssize * deltaLon
    alon = alon - deltaLon
    compass = gpd.GeoDataFrame(
        {
            'color': [(0, 0, 0), (1, 1, 1)],
            'geometry': [
                Polygon([[alon, alat], [alon, alat + deltaLon],
                         [alon + 1 / 2 * deltaLon, alat - 1 / 2 * deltaLon]]),
                Polygon([[alon, alat], [alon, alat + deltaLon],
                         [alon - 1 / 2 * deltaLon, alat - 1 / 2 * deltaLon]])
            ]
        },
        crs=crs)
    compass.plot(ax=ax,
                 edgecolor=textcolor,
                 facecolor=compass['color'],
                 lw=0.6)
    ax.text(alon,
            alat + deltaLon,
            'N',
            color=textcolor,
            fontsize=textsize,
            ha='center',
            va='bottom')
    return ax


def randomly_color_space(number):
    import matplotlib.colors as mcolors
    import random

    # random generate color space for clusters
    colors = [
        '#{:02x}{:02x}{:02x}'.format(random.randint(0, 255),
                                     random.randint(0, 255),
                                     random.randint(0, 255))
        for _ in range(number)
    ]
    unique_colors = list(set(colors))
    while len(unique_colors) < number:
        unique_colors.append('#{:02x}{:02x}{:02x}'.format(
            random.randint(0, 255), random.randint(0, 255),
            random.randint(0, 255)))
    random.shuffle(unique_colors)
    plattee = unique_colors[:40]
    custom_cmap = mcolors.ListedColormap(plattee)
    return custom_cmap


def plot_clustering(clustering_station, clusters, base_boundary):
    """bonus visualizing clusters results

    Args:
        clustering_station (df.Dataframe): stations with clusters
        clusters (bp.ndarray): clsuters array
        base_boundary (gdf.geodataframe): boundary, used for better visualize the location
    """

    fig, ax = plt.subplots(1, 1, figsize=(4, 8), dpi=300)
    clustering_station = clustering_station.to_crs("epsg:4326")
    base_boundary = base_boundary.to_crs("epsg:4326")
    # extracting plotting boundary
    bounds = base_boundary.dissolve().bounds.values[0]
    bounds[1] = bounds[1] - 0.1
    bounds[3] = bounds[3] + 0.1

    # requesting tiles from openstreetmap as background
    tbd.plot_map(plt, bounds, zoom=11, style=4)
    base_boundary.plot(ax=ax,
                       alpha=0.5,
                       edgecolor="white",
                       facecolor="grey",
                       linewidth=1)

    color_space = randomly_color_space(len(clusters))
    # for each cluster, corresponding a color from color space(randomly generated)
    for cluster in set(clusters):
        if cluster != -1:
            subset = clustering_station[clustering_station['clusters'] ==
                                        cluster]
            subset.plot(ax=ax,
                        color=color_space(cluster),
                        markersize=12,
                        label=f"Cluster {cluster}")

    # for noisy points(not core points or border points in DBSCAN clustering)
    clustering_station[clustering_station["clusters"] == -1].plot(
        ax=ax, color="grey", markersize=8, label="Noisy Points", alpha=0.8)
    ax.legend(title="Legend")

    # plot scale and north arrow
    plot_scale_and_north_arrow(bounds, ax, crs="epsg:4326")
    plt.title("station clustering")
    plt.show()
