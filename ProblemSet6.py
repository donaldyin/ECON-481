# Donald Yin
# ECON 481
# Problem Set 6
# 05/11/2024

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import pandas as pd


# Exercise 0:
def github() -> str:
    """
    This function returns the github link to my solutions to this problem set.
    """
    return "https://github.com/donaldyin/ECON-481/blob/main/ProblemSet6.py"


path = '/Users/donaldyin/ECON-481/auctions.db'

class DataBase:
    def __init__(self, loc: str, db_type: str = "sqlite") -> None:
        """Initialize the class and connect to the database"""
        self.loc = loc
        self.db_type = db_type
        self.engine = create_engine(f'{self.db_type}:///{self.loc}')
    def query(self, q: str) -> pd.DataFrame:
        """Run a query against the database and return a DataFrame"""
        with Session(self.engine) as session:
            df = pd.read_sql(q, session.bind)
        return(df)

auctions = DataBase(path)
# q = 'select * from bids'
# print(auctions.query(q))


# Exercise 1:
def std() -> str:
    """
    Returns a string SQL query that outputs a table with columns itemID and std.
    std is calculated as the standard deviation of all bids for each unique itemID.
    """
    q = """
        WITH a AS (
            SELECT 
                itemId,
                AVG(bidAmount) AS averageBidAmount,
                COUNT(bidAmount) AS count
            FROM 
                bids
            GROUP BY 
                itemId
            HAVING
                COUNT(bidAmount) > 1
        ),
        c AS(
            SELECT
                b.itemID,
                SQRT(SUM((b.bidAmount - a.averageBidAmount) * (b.bidAmount - a.averageBidAmount)) 
                    OVER (PARTITION BY b.itemId)/(a.count - 1)) AS std
            FROM 
                bids AS b
            INNER JOIN 
                a
            ON 
                b.itemID=a.itemID
        )
        SELECT
            DISTINCT itemID,
            std
        FROM
            c
        """

    return q

# q = std()
# print(auctions.query(q))


# Exercise 2:
def bidder_spend_frac() -> str:
    """
    Returns a string SQL query that outputs a table with columns bidderName, total_spend,
    total_bids, and spend_frac. total_spend is the sum of winning bids, total_bids is the 
    sum of their highest bids, and spend_frac is the ratio of total_spend to total_bids.
    """
    q = """
        WITH highest_bids AS (
            SELECT 
                bidderName, 
                itemId, 
                MAX(bidAmount) AS highestBid
            FROM bids
            GROUP BY 
                bidderName, 
                itemId
        ),
        total_bids AS (
            SELECT 
                bidderName, 
                SUM(highestBid) AS total_bids
            FROM highest_bids
            GROUP BY bidderName
        ),
        winning_bids AS (
            SELECT 
                b.bidderName, b.bidAmount
            FROM bids AS b
            JOIN items AS i 
                ON b.itemId = i.itemId
            WHERE b.bidAmount = i.currentPrice
        ),
        total_spend AS (
            SELECT 
                bidderName, 
                SUM(bidAmount) AS total_spend
            FROM winning_bids
            GROUP BY bidderName
        )
        SELECT 
            tb.bidderName,
            COALESCE(ts.total_spend, 0) AS total_spend,
            tb.total_bids,
            COALESCE(ts.total_spend, 0) / tb.total_bids AS spend_frac
        FROM total_bids tb
        LEFT JOIN total_spend ts 
            ON tb.bidderName = ts.bidderName;
        """
    return q

# q = bidder_spend_frac()
# print(auctions.query(q))


# Exercise 3:
def min_increment_freq() -> str:
    """
    Returns a string SQL query that outputs a table with column freq that is the fraction of
    bids that are exactly the minimum bid increment above the previous bid.
    """
    q = """
        WITH previous_bids AS (
            SELECT
                b1.itemId,
                b1.bidderName,
                b1.bidAmount AS currentBid,
                MAX(b2.bidAmount) AS previousBid,
                i.bidIncrement
            FROM bids AS b1
            LEFT JOIN bids AS b2
                ON b1.itemId = b2.itemId AND b1.bidAmount > b2.bidAmount
            JOIN items AS i
                ON b1.itemId = i.itemId
            WHERE i.isBuyNowUsed = 0
            GROUP BY 
                b1.itemId, 
                b1.bidderName, 
                b1.bidAmount
        ),
        min_increment_bids AS (
            SELECT
                *,
                CASE WHEN (currentBid - previousBid = bidIncrement) THEN 1 ELSE 0 END AS is_min_increment
            FROM previous_bids
        )
        SELECT
            1.0 * SUM(is_min_increment) / COUNT(*) AS freq
        FROM min_increment_bids
        WHERE previousBid IS NOT NULL;
        """
    return q

# q = min_increment_freq()
# print(auctions.query(q))


# Exercise 4: 
def win_perc_by_timestamp() -> str:
    """
    Returns a string SQL query that outputs a table with columns timestamp_bin
    and win_perc. timestamp_bin represents the normalized timestamp for each bid,
    classifying the time within each bin. win_perc represents the frequency that a
    bid is won within that timestamp bin.
    """
    q = """
        WITH auction_lengths AS (
            SELECT
                itemId,
                startTime,
                endTime,
                julianday(endTime) - julianday(startTime) AS length
            FROM items
        ),
        normalized_bids AS (
            SELECT
                b.itemId,
                b.bidderName,
                b.bidAmount,
                b.bidTime,
                a.startTime,
                a.endTime,
                (julianday(a.endTime) - julianday(b.bidTime)) / a.length AS time_norm
            FROM bids AS b
            INNER JOIN auction_lengths AS a 
                ON b.itemId = a.itemId
        ),
        binned_bids AS (
            SELECT
                itemId,
                bidderName,
                bidAmount,
                CASE
                    WHEN time_norm <= 0.1 THEN 1
                    WHEN time_norm <= 0.2 THEN 2
                    WHEN time_norm <= 0.3 THEN 3
                    WHEN time_norm <= 0.4 THEN 4
                    WHEN time_norm <= 0.5 THEN 5
                    WHEN time_norm <= 0.6 THEN 6
                    WHEN time_norm <= 0.7 THEN 7
                    WHEN time_norm <= 0.8 THEN 8
                    WHEN time_norm <= 0.9 THEN 9
                    ELSE 10
                END AS timestamp_bin
            FROM normalized_bids
        ),
        winning_bids AS (
            SELECT
                i.itemId,
                i.currentPrice,
                b.bidderName,
                b.bidAmount
            FROM items AS i
            JOIN bids AS b 
                ON i.itemId = b.itemId
            WHERE i.currentPrice = b.bidAmount
        ),
        binned_winning_bids AS (
            SELECT
                wb.itemId,
                wb.bidderName,
                wb.bidAmount,
                bb.timestamp_bin
            FROM winning_bids AS wb
            JOIN binned_bids bb 
                ON wb.itemId = bb.itemId AND wb.bidderName = bb.bidderName AND wb.bidAmount = bb.bidAmount
        )
        SELECT
            bb.timestamp_bin,
            COUNT(bwb.bidAmount) * 1.0 / COUNT(bb.bidAmount) AS win_perc
        FROM binned_bids AS bb
        LEFT JOIN binned_winning_bids AS bwb 
            ON bb.itemId = bwb.itemId AND bb.bidderName = bwb.bidderName AND bb.bidAmount = bwb.bidAmount
        GROUP BY bb.timestamp_bin
        ORDER BY bb.timestamp_bin;
        """
    return q

# q = win_perc_by_timestamp()
# print(auctions.query(q))