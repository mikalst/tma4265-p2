import numpy as np
import matplotlib.pyplot as plt

def simulate_poisson(intensity, days):
    events = []
    time = 0
    
    while (time <= days):
        time += np.random.exponential(1/intensity)
        if (time <= days):
            #print("Event at {}".format(time))
            events.append(time)
    
    states = np.zeros((days+1),)
    
    for t in events:
        states[int(np.ceil(t))]+=1
        
    for i, s in enumerate(states[1:]):
        states[i+1] += states[i]
    
    return states, events

def nonhomogeneous_poisson(ll, days):
    
    lmax=max([ll(x) for x in range(days)])
    thrash, events = simulate_poisson(lmax, days)

    # Apply thinning
    print(len(events))
    events = filter(lambda t: ll(t)/lmax >= np.random.uniform(), events)

    states = np.zeros((days+1),)

    for t in events:
        states[int(np.ceil(t))]+=1
                
    for i, s in enumerate(states[1:]):
        states[i+1] += states[i]
                
    return states, events

def average_over_simulate(days, ITERATIONS, intensity=None):
    average = np.zeros((days+1),)
    realizations = []
    for _ in range(ITERATIONS):
        if (isinstance(intensity, int)):
            chain, times = simulate_poisson(intensity, days)
        else:
            chain, times = nonhomogeneous_poisson(intensity, days)
        
        for i, d in enumerate(chain):
            average[i] += d
        
        
        realizations.append(chain)
        
    average/=ITERATIONS
    
    return average, realizations
    

#==============================================================================
# Testing
# r1, *t = average_over_simulate(59, 100, 3)
# #print(r1)
# r2, *t = average_over_simulate(59, 100, lambda t: 2+np.cos(t*np.pi/182.5))
# print(r2)
#     
# plt.plot(range(60), [100*(2+np.cos(t*np.pi/182.5)) for t in range(60)])
# plt.plot(range(60), r1)
# plt.plot(range(60), r2)
#==============================================================================
