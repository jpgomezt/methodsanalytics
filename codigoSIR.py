# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 14:55:06 2021

@author: david
"""
from numpy import ndarray
import pandas as pd
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os 
# pip install xrd

# pip install pandas

# pip install xlsxwriter 

import random

def vaccine_rate(t):
    return 20776

def adjust_rate(contact_rate, day):
    if day > 0:
        return contact_rate
    else:
        return contact_rate

    



def deriv(state, t, N, beta, gamma, alpha):
    S, I, R, V = state
    # Change in S population over time

    vaccinated_today = min(S, alpha * vaccine_rate(t))
    infected_today = min(S, beta * S * I / N)
    recovered_today = min(I, gamma * I)


    dSdt = (-infected_today # Infectados ese día
         -vaccinated_today) # Vacunados ese día
    # Change in I population over time
    dIdt = (infected_today - recovered_today) # Recuperados ese día
    # Change in R population over time
    dRdt = recovered_today # Recuperados ese día

    dVdt = vaccinated_today # Vacunados ese día
    return dSdt, dIdt, dRdt, dVdt

effective_contact_rate = 0.149
recovery_rate = 1/8
vaccine_efficacy = 0.9

# We'll compute this for fun
print("R0 is", effective_contact_rate / recovery_rate)

# What's our start population look like?
# Everyone not infected or recovered is susceptible
total_pop = 50300000
recovered = 0
infected = 86437
vaccinated = 0
susceptible = total_pop - infected - recovered

# A list of days, 0-160
days = range(0, 365*6)

# Use differential equations magic with our population
ret = odeint(deriv,
             [susceptible, infected, recovered, vaccinated],
             days,
             args=(total_pop, effective_contact_rate, recovery_rate, 
                vaccine_efficacy))
S, I, R, V = ret.T

I = list(map(abs, I))
S = list(map(abs, S))

# Build a dataframe because why not
df = pd.DataFrame({
    'suseptible': S,
    'infected': I,
    'recovered': R,
    'vaccinated': V,
    'day': days
})

plt.style.use('ggplot')
df.plot(x='day',
        y=['infected', 'suseptible', 'recovered', 'vaccinated'],
        color=['#bb6424', '#aac6ca', '#cc8ac0', '#ccffcc'],
        kind='area',
        stacked=True)

plt.show()

# If you get the error:
#
#     When stacked is True, each column must be either all
#     positive or negative.infected contains both...
#
# just change stacked=True to stacked=False