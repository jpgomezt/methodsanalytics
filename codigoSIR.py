# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:55:06 2021

@author: david
"""

import pandas as pd
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os 
# pip install xrd

# pip install pandas

# pip install xlsxwriter 


def adjust_rate(contact_rate, day):
    if day > 0:
        return contact_rate
    else:
        return contact_rate

def deriv_adjusted(state, t, N, beta, gamma):
    S, I, R = state
    
    beta = adjust_rate(beta, t)
    # Change in S population over time
    dSdt = -beta * S * I / N
    # Change in I population over time
    dIdt = beta * S * I / N - gamma * I
    # Change in R population over time
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def saveAsExcel(df, fileName):

    if '/' in fileName:

        route = "./" + str(os.path.split(fileName)[1])

    else:

        route = "D:\Documentos\Semestre 2021-1" + fileName + ".xlsx"



    writer = pd.ExcelWriter(route, engine='xlsxwriter') # pylint: disable=abstract-class-instantiated

    df.to_excel(writer, 'Hoja X', index=False)

    writer.save()
    
# The SIR model differential equations.


def deriv(state, t, N, beta, gamma):
    S, I, R = state
    # Change in S population over time
    dSdt = -beta * S * I / N
    # Change in I population over time
    dIdt = beta * S * I / N - gamma * I
    # Change in R population over time
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

effective_contact_rate = 0.5
recovery_rate = 1/4

# We'll compute this for fun
print("R0 is", effective_contact_rate / recovery_rate)

# What's our start population look like?
# Everyone not infected or recovered is susceptible
total_pop = 50300000
recovered = 2240000
infected = 5986
susceptible = total_pop - infected - recovered

# A list of days, 0-160
days = range(0, 160)

# Use differential equations magic with our population
ret = odeint(deriv,
             [susceptible, infected, recovered],
             days,
             args=(total_pop, effective_contact_rate, recovery_rate))
S, I, R = ret.T

# Build a dataframe because why not
df = pd.DataFrame({
    'suseptible': S,
    'infected': I,
    'recovered': R,
    'day': days
})

plt.style.use('ggplot')
df.plot(x='day',
        y=['infected', 'suseptible', 'recovered'],
        color=['#bb6424', '#aac6ca', '#cc8ac0'],
        kind='area',
        stacked=True)

saveAsExcel(df,"analisisVacuna")

# segunda parte

effective_contact_rate = 0.2
recovery_rate = 1/14

# We'll compute this for fun
print("R0 is", effective_contact_rate / recovery_rate)

# What's our start population look like?
# Everyone not infected or recovered is susceptible
total_pop = 1000
recovered = 0
infected = 1
susceptible = total_pop - infected - recovered

# A list of days
days = range(0, 200)

# First do it with our original derivation...
ret = odeint(deriv,
             [susceptible, infected, recovered],
             days,
             args=(total_pop, effective_contact_rate, recovery_rate))
S, I, R = ret.T

# ...then do it again with the adjusted one.
ret = odeint(deriv_adjusted,
             [susceptible, infected, recovered],
             days,
             args=(total_pop, effective_contact_rate, recovery_rate))
S_adj, I_adj, R_adj = ret.T

# Build a dataframe because why not
df = pd.DataFrame({
    'infected': I,
    'infected_lockdown': I_adj,
    'day': days
})

plt.style.use('ggplot')
df.plot(x='day',
        y=['infected', 'infected_lockdown'])





# If you get the error:
#
#     When stacked is True, each column must be either all
#     positive or negative.infected contains both...
#
# just change stacked=True to stacked=False