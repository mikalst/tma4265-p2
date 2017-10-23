import numpy as np
import matplotlib.pyplot as plt
from heapq import heappush, heappop
from math import factorial

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
    events = [k for k in filter(lambda t: ll(t)/lmax >= np.random.uniform(), events)]
    

    states = np.zeros((days+1),)

    for t in events:
        states[int(np.ceil(t))]+=1
                
    for i, s in enumerate(states[1:]):
        states[i+1] += states[i]
                
    return states, events

def weighted_events(times, mu, sigma):
        
    N = len(times)
    weights = np.random.normal(mu, sigma, N)
    weights = np.exp(weights)
    
    return sum(weights)

def discount_events(times, mu, sigma, alpha):
    
    N = len(times)
    weights = np.exp(np.random.normal(mu, sigma, N))
    discount_factors = [k for k in map(lambda t: -alpha*t, times)]
    
    return np.dot(np.exp(discount_factors), weights)

def average_over_simulate(days, ITERATIONS, limit, intensity=None):
    
    print("N simulations = {}".format(ITERATIONS))
    
    average = np.zeros((days+1),)
    costs = []
    discounts = []
    exceeded = 0
    realizations = []
    
    for _ in range(ITERATIONS):
        if (isinstance(intensity, int)):
            chain, times = simulate_poisson(intensity, days)
        else:
            chain, times = nonhomogeneous_poisson(intensity, days)
        for i, d in enumerate(chain):
            average[i] += d
        costs.append(weighted_events(times, -2.0, 1.0))
        discounts.append(discount_events(times, -2.0, 1.0, 0.001))
        
        if (len(times) > 175):
            exceeded += 1
            
        
        realizations.append((chain, times))
        
    average/=ITERATIONS
    exceeded/=ITERATIONS
    
    discounts.sort()
    top_95 = discounts[int(ITERATIONS*0.95)]
    
    
    
    return average, realizations, np.mean(costs), np.var(costs), np.mean(discounts), np.var(discounts), top_95, exceeded
    
def task_a():
    
    poisson = lambda l, t, n: (l*t)**n/(factorial(n))*np.exp(-l*t)
    prob = 1-sum([poisson(3, 59, k) for k in range(0, 176)])
    print("Probability of recieving more than 175 claims = {}".format(prob))
    
    r1, realizations, cost, S_cost, discount, S_discount, t95, exceeded = average_over_simulate(59, 100, 175, 3)
    
    print("Simulated ratio with more than 175 claims recieved = {}".format(exceeded))
    
    plt.style.use("ggplot")
    plt.plot(range(60), r1, lw = 3.0, color="black", zorder=100)

    for r, t in realizations:
        plt.plot(t, range(1,len(t)+1))
    
    plt.title("$N(t)$,   $\lambda = 3$")
    plt.legend(["Average"])
    plt.xlabel("Days after January 1st 0:00.00")
    plt.ylabel("$N(t)$")
    plt.savefig("task_a.pdf")
    plt.show()

def smart_factorial(l, n):
    while n>0:
        return l/n*smart_factorial(l, n-1)
    return np.exp(-l)

def task_b():
    
    prob = 1-sum([smart_factorial(167.367, k) for k in range(0, 176)])
    print("Probability of recieving more than 175 claims = {}".format(prob))
    
    r1, realizations, cost, S_cost, discount, S_discount, t95, exceeded = average_over_simulate(59, 100, 175,
                                                                      lambda t: 2+np.cos(t*np.pi/182.5))
    
    print("Simulated ratio with more than 175 claims recieved = {}".format(exceeded))
    
    plt.style.use("ggplot")
    plt.plot(range(60), r1, lw = 3.0, color="black", zorder=100)

    for r, t in realizations:
        plt.plot(t, range(1,len(t)+1))
    
    plt.title("$N(t)$,   $\lambda(t) = 2+cos(t\pi/182.5)$")
    plt.legend(["Average"])
    plt.xlabel("Days after January 1st 0:00.00")
    plt.ylabel("$N(t)$")
    plt.plot(range(60), r1)
    plt.savefig("task_b.pdf")
    plt.show()

def task_c():
    r1, realizations, cost, S_cost, discount, S_discount, t95, exceeded = average_over_simulate(59, 1000, 175, 3)
    print("fixed lambda, mean(Z)={}, S_Z = {}".format(
            cost, S_cost))
    r1, realizations, cost, S_cost, discount, S_discount, t95, exceeded = average_over_simulate(59, 1000, 175, lambda t: 2+np.cos(t*np.pi/182.5))
    print("varying lambda, mean(Z)={}, S_Z = {}".format(
            cost, S_cost))

def task_d():
    r1, realizations, cost, S_cost, discount, S_discount, t95, exceeded = average_over_simulate(365, 1000, 175, 3)
    print("fixed lambda, mean(Z)={}, S_Z = {}".format(
            discount, S_discount))
    print("value indicating 95th percentile = {}".format(t95))
    
    r1, realizations, cost, S_cost, discount, S_discount, t95, exceeded = average_over_simulate(365, 1000, 175, lambda t: 2+np.cos(t*np.pi/182.5))
    print("varying lambda, mean(Z)={}, S_Z = {}".format(
            discount, S_discount))
    print("value indicating 95th percentile = {}".format(t95))
    

if __name__ == "__main__":
    #task_a()
    #task_b()
    #task_c()
    task_d()