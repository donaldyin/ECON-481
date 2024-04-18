# Donald Yin
# ECON 481
# Problem Set 2
# 04/17/2024

import numpy as np
import scipy as sp
import pandas as pd


# Exercise 0:
def github() -> str:
    '''
    This function returns the github link to my solutions to this problem set.
    '''
    return "https://github.com/donaldyin/ECON-481/blob/main/ProblemSet3.py"


# Exercise 1:
def import_yearly_data(years: list) -> pd.DataFrame:
    """
    This function takes in a list of years and returns a DataFrame containing data for
    greenhouse gas emissions for those years.
    """
    all_dfs = []
    for year in years:
        url = f"https://lukashager.netlify.app/econ-481/data/ghgp_data_{year}.xlsx"
        df = pd.read_excel(url, sheet_name="Direct Emitters", skiprows=3)
        df["year"] = year
        all_dfs.append(df)
    
    return pd.concat(all_dfs)

# print(import_yearly_data([2019, 2020, 2021, 2022]))


# Exercise 2:
def import_parent_companies(years: list) -> pd.DataFrame:
    """
    Takes in a list of years and returns data for parent company data
    for greenhouse gases for those years.
    """
    all_dfs = []
    for year in years:
        url = "https://lukashager.netlify.app/econ-481/data/ghgp_data_parent_company_09_2023.xlsb"
        df = pd.read_excel(url, sheet_name=str(year))
        df["year"] = year
        all_dfs.append(df)
    
    return pd.concat(all_dfs).dropna(how="all")

# print(import_parent_companies([2019, 2020]))


# Exercise 3:
def n_null(df: pd.DataFrame, col: str) -> int:
    """
    Takes in a DataFrame and a column name and returns the number of NaN values in 
    that column.
    """
    return df[col].isna().sum()

# print(n_null(import_parent_companies([2020]), "FRS ID (FACILITY)"))


# Exercise 4:
def clean_data(emissions_data: pd.DataFrame, parent_data: pd.DataFrame) -> pd.DataFrame:
    """
    Takes in emissions dataframe and parent company dataframe,
    and returns a merged DataFrame with specific columns. 
    """
    parent_data.rename(columns={"GHGRP FACILITY ID":"Facility Id"}, inplace=True)
    new_df = pd.merge(emissions_data, parent_data, on=["year", "Facility Id"], how='left')
    subset_df = new_df[["Facility Id", 
                        "year", 
                        "State", 
                        "Industry Type (sectors)", 
                        "Total reported direct emissions", 
                        "PARENT CO. STATE", 
                        "PARENT CO. PERCENT OWNERSHIP"]]
    subset_df.columns = [col.lower() for col in subset_df.columns] 
    return subset_df

test_df = clean_data(import_yearly_data([2019]), import_parent_companies([2019]))
# print(test_df)


# Exercise 5:
def aggregate_emissions(df: pd.DataFrame, group_vars: list) -> pd.DataFrame:
    """
    This takes in a data frame and a list of variable names,
    and returns a data frame that displays summary statistics
    grouped by the input variable names.
    """
    # filter and grab summary statistics
    statistics = df.groupby(group_vars, as_index=True)[
                 ["total reported direct emissions", 
                  "parent co. percent ownership"]].describe()
    
    # filter only summary statistics we need: min, median, mean, max
    final_statistics = statistics.loc[:, 
                                     [("total reported direct emissions", "min"),
                                      ("total reported direct emissions", "50%"),
                                      ("total reported direct emissions", "mean"),
                                      ("total reported direct emissions", "max"),
                                      ("parent co. percent ownership", "min"),
                                      ("parent co. percent ownership", "50%"),
                                      ("parent co. percent ownership", "mean"),
                                      ("parent co. percent ownership", "max")]]
    
    # rename "50%" to median
    final_statistics.rename(columns={("50%"):("median")}, level=1, inplace=True)

    return final_statistics

print(aggregate_emissions(test_df, ["year"]))