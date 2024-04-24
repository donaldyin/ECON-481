# Donald Yin
# ECON 481
# Problem Set 4
# 04/22/2024

import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt


# Exercise 0:
def github() -> str:
    """
    This function returns the github link to my solutions to this problem set.
    """
    return "https://github.com/donaldyin/ECON-481/blob/main/ProblemSet4.py"


# Exercise 1:
def load_data() -> pd.DataFrame:
    """
    Returns a DataFrame containing Tesla stock price history.
    """
    url = "https://lukashager.netlify.app/econ-481/data/TSLA.csv"
    data = pd.read_csv(url)

    return data

# print(load_data())


# Exercise 2:
def plot_close(df: pd.DataFrame, start: str = "2010-06-29", end: str = "2024-04-15") -> None:
    """
    Takes in a dataFrame of Tesla stock price history, a start date, and end date,
    and it plots the closing prices between those two dates.
    """

    df["Date"] = pd.to_datetime(df["Date"])
    start_date = pd.to_datetime(start)
    end_date = pd.to_datetime(end)
    date_range = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    print(date_range)
    plt.plot(
            date_range["Date"],
            date_range["Close"],
            color="black"
        )
    plt.title(f"Closing prices between {start} and {end}")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

# plot_close(load_data())
    

# Exercise 3:
def autoregress(df: pd.DataFrame) -> float:
    """
    Takes in a DataFrame and returns the t-statistic of a random walk hypothesis
    regression on Closing prices.

    """
    df.set_index("Date", inplace=True) # sets the dates as the index
    df.index = pd.to_datetime(df.index) # makes the date indices as a datetime type
    df["D_x"] = df["Close"].diff() # calculates the differences in closing prices (as the y column)
    df.dropna(subset=["D_x"], inplace=True) # drops any NaN rows by looking at the D_x column
    df["D_x_lag"] = df["D_x"].shift(1) # shifts to create a lag column, D_x_t-1
    df.dropna(subset=["D_x_lag"], inplace=True) # drops NaN rows by looking at the D_x_lag column 
    # print(df), used to check if df contains what we want
    X = df["D_x_lag"] 
    y = df["D_x"]
    model = sm.OLS(y, X).fit(cov_type="HC1")
    t_stat = model.tvalues["D_x_lag"]

    return t_stat

# print(autoregress(load_data()))


# Exercise 4:
import pandas as pd
import statsmodels.api as sm

def autoregress_logit(df: pd.DataFrame) -> float:
    """
    Takes in a DataFrame and returns the t-statistic of the probability that there
    is a positive change in closing prices. 
    """
    df.set_index("Date", inplace=True) # sets the dates as the index
    df.index = pd.to_datetime(df.index)
    df["D_x"] = df["Close"].diff() # finds difference in closing prices
    df["y"] = (df["D_x"] > 0).astype(int) # creates a binary outcome where we want y to be positive changes in x
    df["D_x_lag"] = df["D_x"].shift(1) # lags x variable by one day
    df.dropna(subset=["D_x_lag", "y"], inplace=True) # drops NaN values 
    # print(df), used to check if df contains what we want
    X = df["D_x_lag"] 
    y = df["y"]
    logit_model = sm.Logit(y, X).fit()
    t_stat = logit_model.tvalues["D_x_lag"]

    return t_stat

# print(autoregress_logit(load_data()))


# Exercise 5:
def plot_delta(df: pd.DataFrame) -> None:
    """
    Takes in a DataFrame and plots the difference in closing prices for each consecutive date.
    """

    df["Date"] = pd.to_datetime(df["Date"])
    df["D_x"] = df["Close"].diff()
    plt.plot(
            df["Date"],
            df["D_x"],
            color="black"
        )
    plt.title(f"Delta x for each business day")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.show()

# plot_delta(load_data())