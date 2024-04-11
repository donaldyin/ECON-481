# Donald Yin
# ECON 481
# Problem Set 2
# 04/09/2024

import numpy as np
import scipy as sp


# Exercise 0:
def github() -> str:
    '''
    This function returns the github link to my solutions to this problem set.
    '''
    return "https://github.com/donaldyin/ECON-481/blob/main/ProblemSet2.py"


# Exercise 1
def simulate_data(seed: int=481) -> tuple: # simulated data generator
    '''
    Takes in a seed and returns a tuple of 2 arrays where the first array is the simulated
    outpute and the second array is the simulated inputs.
    '''

    np.random.default_rng(seed)

    X = np.random.normal(0, np.sqrt(2), size=(1000, 3)) 
    error = np.random.normal(0, 1, size=1000)

    y = np.dot(X, np.array([3, 2, 6])) + 5 + error

    return (y, X)

results = simulate_data(481)
y_array, X_array = results[0], results[1]


# Exercise 2
def neg_ll(betas: np.array, y: np.array, X: np.array) -> float: # helper function for MLE function
    '''
    Takes in guess parameters beta (including intercept) and data observations X 
    and response variables y, and returns the negative log-likelihood. 
    '''

    beta_0, beta_i = betas[0], betas[1:]
    y_pred = beta_0 + np.dot(X, beta_i)
    nll = -np.sum(-0.5 * np.log(2 * np.pi) - 0.5 * ((y - y_pred)**2))
    return nll 

print(neg_ll(np.array([5,3,2,6]), y_array, X_array)) # test output

def estimate_mle(y: np.array, X: np.array) -> np.array:
    '''
    Returns an estimate of the beta parameters using a maximum likelihood estimate
    based on the inputted data.
    '''

    param_estimate = sp.optimize.minimize(
                        fun=neg_ll, 
                        x0=np.array([10,5,1,4]), 
                        args=(y, X), 
                        method = 'Nelder-Mead' 
                                         )
    return param_estimate.x

print(estimate_mle(y_array, X_array)) #test output


# Exercise 3
def sum_squared_errors(betas: np.array, y: np.array, X: np.array) -> float: # helper function for OLS estimate
    '''
    Takes in beta parameters vector, an observation array X, and response
    variable array y, and returns the sum of squared errors based on the 
    input beta parameters.
    '''

    beta_0, beta_i = betas[0], betas[1:]
    y_pred = np.dot(X, beta_i) + beta_0
    sse = np.sum((y-y_pred)**2)
    return sse

def estimate_ols(y: np.array, X: np.array) -> np.array:
    """
    Some docstrings.
    """
    param_estimate = sp.optimize.minimize(
                        fun=sum_squared_errors, 
                        x0=np.array([10,5,1,4]), 
                        args=(y, X), 
                        method = 'Nelder-Mead' 
                                         )
    return param_estimate.x

print(estimate_ols(y_array, X_array)) # test code
