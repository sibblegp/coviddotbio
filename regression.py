import numpy as np
from scipy.optimize import curve_fit


def func_exp(x, a, b, c):
        c = 0
        return a * np.exp(b * x) + c

def exponential_regression (x_data, y_data):
    popt, pcov = curve_fit(func_exp, x_data, y_data, p0 = (-1, 0.01, 1))
    print(popt)
    return func_exp(x_data, *popt)