# Problem

This tool is designed to produce aggregated statistics of **certified** H1b-visa applications based on the data provided by the US Department of Labor and its [Office of Foreign Labor Certification Performance Data](https://www.foreignlaborcert.doleta.gov/performancedata.cfm#dis). Aggregation is done separately by two attributes: **occupations** and **employment states**. At most 10 highest ranking attribute values (i.e., occupations or states) are outputted along with the number of certified applications and the share of this attribute value (in percents rounded to the first decimal place).

The tool accepts as input a CSV (semicolon-delimeted) file named __`h1b_input.csv`__ in the __`input`__ subfolder. After a successful run, the script outputs two text files __`top_10_occupations.txt`__ and __`top_10_states.txt`__ into the __`output`__ subfolder. Filenames could be changed by editing the script file __`run.sh`__.

See [Run](README.md#run) for additional input file structure requirements.

# Approach

The tool consists of a Python 3.x script that uses a standard csv library to read an input dataset. The script initializes two dictionaries (occupations and states) with attribute values and counters as keys and values, respectively. Only certified applications are counted. After reading the entire input file, counts are sorted, tallied up, and percent shares are calculated. The generated output of atmost 10 highest ranking attribute values has the following schema: TOP_<OCCUPATIONS,STATES>;NUMBER_CERTIFIED_APPLICATIONS;PERCENTAGE (for occupations and states, respectively).

The script accepts different naming conventions for the used attributes (fields, variables, features). Please make sure that these attributes exist in your input data (i.e., rename the attributes in the data file if necessary):

__`STATUS`__ or __`CASE_STATUS`__ for application status
__`LCA_CASE_SOC_NAME`__ or __`SOC_NAME`__ for standardized occupation name
__`LCA_CASE_WORKLOC1_STATE`__ or __`WORKSITE_STATE`__ for employment state

Note:
FY2014 data specifies up to two working locations. The current version of the script considers the first location (__`LCA_CASE_WORKLOC1_STATE`__ is state of the first location) as the primary location for the analysis. However, if state of the first location is missing, the state of the second location (__`LCA_CASE_WORKLOC2_STATE`__) is considered, if available.

# Run 

Run __`./run.sh`__ to generate statistics based on the provided input dataset.
You can edit __`run.sh`__ to specify alternative paths and names for the python script, input dataset, top occupations text file, and top states text file.
