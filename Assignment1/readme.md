# Assignment1

## Introduction

This is my personal assignment for **LSGI524** _URBAN AND GEOSPATIAL BIG DATA ANALYTICS_

This Readme gives you a brief introduction to my files structure and understand to corresponding relationship between my codes and the tasks.

So this is my file tree in the .zip file.

    ./
    	code/
    		data_raw/
    		data_cleaned/
    		config/
    			global_vars.py
    		utils/
    			customized_plot.py
    			preprocess.py
    			validate.py
    		0_task1.py
    		1_task2.py
    		2_task3.py
    		3_task4.py
    	reports/
    		assignment1.pdf
    		clsuter_groups.csv

In all these files, the core codes of processing and analyting are in utils/... and scripts name end with task1-4.py are the straight scripts completing the tasks using the functions in utils/...

## Content

This section I will give an brief introduction to the scripts.

| logical level | script name        | function                                                                                               |
| ------------- | ------------------ | ------------------------------------------------------------------------------------------------------ |
| Config        | global_vars.py     | Store global static variables forthe project, such as paths and projection coordinates.                |
| Utils         | Preprocessing.py   | Filtering invalid data, coordinate transformation, and basic geographical calculations.                |
| Utils         | Validate.py        | Re-validating the spatiotemporal validity of the data before conducting further data analysis.         |
| Utils         | Customized_plot.py | Customized plotting the data using different types of chart, for visualization and spatial perception. |
| Assignment    | Task1-4.py         | Completing task1-4 using the function defined from above scripts.                                      |

## Reports

Reports are put in reports/...
Notice: The result of **_station ids in each cluster _** is put in cluster_groups.csv due to the station number is large.

## Notice

Reports can be reproduce by directly executing scripts task1-4.py. But raw_data should be put in corresponding folder before running.

## Others

All the python packages used are written in requirements.txt
QGIS was used for do some mapping when writing report. Figures that generated by QGIS are (Fig.3 Fig.5 Fig.8 Fig.10 )
Fig.11 is generated by Python.
