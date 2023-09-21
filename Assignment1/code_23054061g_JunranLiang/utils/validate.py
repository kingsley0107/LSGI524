# -*- coding: utf-8 -*-
'''
Created on Wed 09 20 09:30:37 2023

@Author: Kingsley
'''

from config.global_vars import Project_Configs
import pandas as pd
import geopandas as gpd


def time_window_is_correct(df: pd.DataFrame, date: str = None):
    """check date: if unexpected datetime exist in dataframe, raise error.

    Args:
        df (pd.DataFrame): dataframe to be analysed
        date (str, optional): expected date. Defaults to None.

    Raises:
        Exception: _raise data error in datetime_

    Returns:
        _type_: bool
    """
    # check date
    if date:
        time_window = pd.to_datetime(date,
                                     format=Project_Configs.DATETIME_FORMAT)
        if (len(df[(df["start_time"].dt.date != time_window)
                   | (df["end_time"].dt.date != time_window)]) >= 1):
            raise Exception("Data Error: Time range incorrect!")
    else:
        return True


def crs_is_correct(gdf: gpd.GeoDataFrame, crs: int = None):
    """check crs: if unexpected crs comes, return false.

    Args:
        gdf (gpd.GeoDataFrame): _description_
        crs (int, optional): _description_. Defaults to None.
    """
    if crs:
        return gdf.crs.to_epsg() == crs
