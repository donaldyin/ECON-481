# Donald Yin
# ECON 481
# Problem Set 1
# 04/02/2024

import numpy as np
from datetime import datetime, date, time, timedelta
from typing import Union

# Exercise 0:
def github() -> str:
    '''
    This function returns the github link to my solutions to this problem set.
    '''
    return "https://github.com/donaldyin/ECON-481/blob/main/ProblemSet1.py"

# Exercise 2
def evens_and_odds(n: int) -> dict:
    '''
    This function takes in an integer and returns a dictionary that has even and odds.
    The dictionary values are the sums of the even natural numbers and odd natural numbers.
    '''
    even_sum = 0
    odd_sum = 0
    total_sums = {"evens": 0, "odds": 0}
    for num in range(n):
        if num % 2 == 0:
            total_sums["evens"] += num
        else:
            total_sums["odds"] += num
    
    return total_sums

# Exercise 3:
# Union is imported at the beginning of the assignment.
def time_diff(date_1: str, date_2: str, out="float") -> Union[str, float]:
    '''
    This function takes in two dates and returns the difference of the dates in days in the specified
    type. If no type is specified, then it defaults to float.
    '''

    first_date = datetime.strptime(date_1, "%Y-%m-%d")
    second_date = datetime.strptime(date_2, "%Y-%m-%d")
    difference = (first_date - second_date).days
    if difference < 0:
        difference = -difference
    if out == "string":
        return f"There are {difference} days between the two dates"
    return difference

# Exercise 4:
def reverse(in_list: list) -> list:
    """
    This function takes in a list and returns a list in the reversed order of elements.
    """
    reversed_list = []
    for i in range(len(in_list)-1, -1, -1):
        reversed_list.append(in_list[i])
    return reversed_list


# Exercise 5: 
def factorial(num): # helper method for prob_k_heads method
    returned_num = 1
    for i in range(num, 0, -1): # backwards for visualization (i.e. 5*4*3*2*1 for 5!)
        returned_num *= i
    return returned_num

def prob_k_heads(n: int, k: int) -> float:
    """
    This function takes in a tw natural values n and k, representing the n amount of coin flips
    and k amount of heads wanted. It returns the probability of getting k heads from n flips.
    """

    probability = (factorial(n)/((factorial(k))*(factorial(n-k))))*(0.5**k)*(0.5**(n-k))

    return probability


