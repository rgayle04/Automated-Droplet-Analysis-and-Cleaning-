# Automated-Droplet-Analysis
Contains files used in order to automate the analysis of water droplets contains files for:

The cleaning of Data by removal of Null/Nan Values: dataSwiffer.py
The calculating of Linear and 3rd degree Polynomial Permeability: autoAnalyze.py
The automatic comparison of files within a set folder for their permeability both 3rd Degree Polynomial and Linear: data_analyzer.py

This acts as a sort of mini version of the Detectron Droplet Detector to be used by the Chemistry Department for comparision between Hough Transform and Detectron2:

These should be used in the following order: 1) dataSwiffer.py 2) autoAnalyze.py 3) data_analyzer.py

dataSwiffer.py -path to csv files -path to output directory/folder
-cleans out the given csv of any odd characters that may show up

autoAnalyze.py -path to csvFiles -path to output directory/folder
-will automatically perform the permeability calcs and and other statistics of the given csv about the water droplets 

data_analyzer.py -path to csvFiles -path to output directory/Folder
-Goes through a directory of files and will take the Permeability of the files and will put it into a summarized csv with the mean Permeability of grouped csvs by name and the standard deviation of the files as well 
