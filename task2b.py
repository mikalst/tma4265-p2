# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
# This file contains our simulation of the birth death process 
# and task 2b

plt.style.use("ggplot")
TITLESIZE = 18
TEXTSIZE = 12.5

HOURS = 7 * 24

def simulate_bd(l, my):
    t = 0
    # previous state
    prev = 0
    alive = 0
    forwarded = 0
    # time[n] = time spent in state n when running for 24 * 7 hours
    time = np.array([ 0.0 ] * 33) 
    
    while True:
        delta_t = np.random.exponential(1 / (l + alive * my))
        t += delta_t
        if t > HOURS:
            time[prev] += HOURS - t + delta_t
            break
        if np.random.rand() <= l / (l + alive * my): 
            # we have a births
            if alive == 32:
                forwarded += 1
            else:
                alive += 1
        elif alive > 0: 
            # we have a death
            alive -= 1
        time[prev] += delta_t
        prev = alive # or forwarded
    
    return time

def main():
    # birthrate
    l = 25
    # deahtrate
    my = 1
    
    # Simulateing the equilibrium distributuion
    res = np.array([0.0] * 33)
    for i in range (100):
       res += simulate_bd(l, my)
       
    res = [ t / (24 * 7 * 100) for t in res ]
    n = [ i for i in range (0, 33) ]
    plt.plot (n, res, 'b')
    plt.plot (n, res, 'o')
    plt.xlabel("$n$", fontsize = TEXTSIZE)
    plt.title( "Ratio of time spent in state $n$ over 100 realizations", fontsize = TITLESIZE )
    plt.xlim(1, 31)
    
    """
    # How many jobs are forwarded on average per hour?
    forwarded = 0
    for i in range (100):
        forwarded += simulate_bd(l, my)
    forwarded /= ( 100 * 24 * 7 )
    print (forwarded)
    """
    return 0

main()
